from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, date, timedelta
import os
from dotenv import load_dotenv
from functools import wraps

load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'chiave-segreta-di-sviluppo')

# Configurazione database per deploy
DATABASE_URL = os.getenv('DATABASE_URL', 'sqlite:///gestionale_incassi.db')
if DATABASE_URL.startswith('postgres://'):
    DATABASE_URL = DATABASE_URL.replace('postgres://', 'postgresql://', 1)
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URL
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# Decorator per controllare i permessi admin
def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or not current_user.is_admin:
            flash('Accesso negato. Richiesti permessi di amministratore.', 'error')
            return redirect(url_for('dashboard'))
        return f(*args, **kwargs)
    return decorated_function

# Modelli del database
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(120), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)
    nome_completo = db.Column(db.String(100), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Incasso(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.Date, nullable=False, default=date.today)
    operatore_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    fondo_cassa_iniziale = db.Column(db.Float, nullable=False)
    incasso_pos = db.Column(db.Float, nullable=False)
    cash_totale_cassa = db.Column(db.Float, nullable=False)
    cash_scontrinato = db.Column(db.Float, default=0)  # Mantenuto per compatibilità
    cash_non_scontrinato = db.Column(db.Float, default=0)  # Mantenuto per compatibilità
    chiusura_fiscale = db.Column(db.Float, default=0)  # Nuovo campo per chiusura fiscale
    prelievo_importo = db.Column(db.Float, default=0)
    prelievo_motivo = db.Column(db.String(100), default='')
    note = db.Column(db.Text)
    approvato = db.Column(db.Boolean, default=False)
    approvato_da = db.Column(db.Integer, db.ForeignKey('user.id'))
    approvato_il = db.Column(db.DateTime)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    operatore = db.relationship('User', foreign_keys=[operatore_id])
    approvatore = db.relationship('User', foreign_keys=[approvato_da])

class Cassaforte(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.Date, nullable=False)
    operatore_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    tipo_movimento = db.Column(db.String(20), nullable=False)  # 'entrata' o 'uscita'
    importo = db.Column(db.Float, nullable=False)
    monete_importo = db.Column(db.Float, default=0.0)  # Importo in monete
    banconote_importo = db.Column(db.Float, default=0.0)  # Importo in banconote
    descrizione = db.Column(db.Text)
    approvato = db.Column(db.Boolean, default=False)
    approvato_da = db.Column(db.String(50))
    approvato_il = db.Column(db.DateTime)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    operatore = db.relationship('User', backref='movimenti_cassaforte')

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Funzioni di utilità per i calcoli
def calcola_incasso_cash_effettivo(fondo_cassa, cash_totale):
    return cash_totale - fondo_cassa

def calcola_totale_incasso_atteso(incasso_pos, incasso_cash_effettivo, prelievo_importo=0):
    """Calcola il totale incasso atteso considerando i prelievi"""
    totale_base = incasso_pos + incasso_cash_effettivo
    return totale_base - prelievo_importo

def verifica_coerenza_chiusura_fiscale(incasso_pos, cash_totale, chiusura_fiscale, fondo_cassa, prelievo_importo=0):
    """Nuova logica di verifica coerenza basata sulla chiusura fiscale"""
    # Calcolo: Incasso POS + Cash Totale - Chiusura Fiscale - Fondo Cassa - Prelievo
    cash_effettivo = cash_totale - fondo_cassa
    totale_atteso = incasso_pos + cash_effettivo
    totale_verificato = chiusura_fiscale + fondo_cassa + prelievo_importo
    
    differenza = totale_atteso - totale_verificato
    
    if abs(differenza) > 0.01:  # Tolleranza di 1 centesimo
        if differenza > 0:
            return f"Importo non scontrinato: €{differenza:.2f}"
        else:
            return f"Discrepanza: €{abs(differenza):.2f} - verificare conteggio"
    return "Coerente"

def verifica_coerenza(incasso_cash_effettivo, cash_scontrinato, cash_non_scontrinato):
    """Funzione legacy mantenuta per compatibilità"""
    totale_dichiarato = cash_scontrinato + cash_non_scontrinato
    differenza = incasso_cash_effettivo - totale_dichiarato
    
    if abs(differenza) > 0.01:  # Tolleranza di 1 centesimo
        if differenza > 0:
            return f"Eccedenza cash di €{differenza:.2f} - possibile incasso non scontrinato"
        else:
            return f"Deficit cash di €{abs(differenza):.2f} - verificare conteggio"
    return "Coerente"

def calcola_anomalie_incasso(incasso):
    """Calcola tutte le anomalie per un incasso"""
    anomalie = []
    
    # Calcola cash effettivo
    incasso_cash_effettivo = calcola_incasso_cash_effettivo(incasso.fondo_cassa_iniziale, incasso.cash_totale_cassa)
    
    # Verifica coerenza con chiusura fiscale (nuova logica)
    if hasattr(incasso, 'chiusura_fiscale') and incasso.chiusura_fiscale > 0:
        totale_atteso = incasso.incasso_pos + incasso_cash_effettivo
        totale_verificato = incasso.chiusura_fiscale + incasso.fondo_cassa_iniziale + incasso.prelievo_importo
        differenza = totale_atteso - totale_verificato
        
        if abs(differenza) > 0.01:
            anomalie.append({
                'tipo': 'discrepanza_chiusura_fiscale',
                'severita': 'warning',
                'messaggio': f'Discrepanza chiusura fiscale: €{differenza:.2f}',
                'dettagli': f'Atteso: €{totale_atteso:.2f}, Verificato: €{totale_verificato:.2f}'
            })
    
    # Verifica coerenza cash legacy (mantenuto per compatibilità)
    totale_dichiarato = incasso.cash_scontrinato + incasso.cash_non_scontrinato
    if totale_dichiarato > 0:
        differenza = abs(incasso_cash_effettivo - totale_dichiarato)
        if differenza > 0.01:
            anomalie.append({
                'tipo': 'discrepanza_cash_legacy',
                'severita': 'info',
                'messaggio': f'Discrepanza cash legacy: €{differenza:.2f}',
                'dettagli': f'Cash effettivo: €{incasso_cash_effettivo:.2f}, Dichiarato: €{totale_dichiarato:.2f}'
            })
    
    # Verifica valori negativi
    if incasso.fondo_cassa_iniziale < 0:
        anomalie.append({
            'tipo': 'fondo_negativo',
            'severita': 'danger',
            'messaggio': 'Fondo cassa negativo',
            'dettagli': f'Valore: €{incasso.fondo_cassa_iniziale:.2f}'
        })
    
    if incasso.incasso_pos < 0:
        anomalie.append({
            'tipo': 'pos_negativo',
            'severita': 'danger',
            'messaggio': 'Incasso POS negativo',
            'dettagli': f'Valore: €{incasso.incasso_pos:.2f}'
        })
    
    if incasso.cash_totale_cassa < 0:
        anomalie.append({
            'tipo': 'cash_negativo',
            'severita': 'danger',
            'messaggio': 'Cash totale negativo',
            'dettagli': f'Valore: €{incasso.cash_totale_cassa:.2f}'
        })
    
    # Verifica valori zero sospetti
    if incasso.incasso_pos == 0:
        anomalie.append({
            'tipo': 'pos_zero',
            'severita': 'info',
            'messaggio': 'Incasso POS zero',
            'dettagli': 'Verificare se corretto'
        })
    
    if incasso_cash_effettivo == 0:
        anomalie.append({
            'tipo': 'cash_zero',
            'severita': 'info',
            'messaggio': 'Cash effettivo zero',
            'dettagli': 'Verificare se corretto'
        })
    
    return anomalie

# Route principali
@app.route('/')
def index():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        
        if user and check_password_hash(user.password_hash, password):
            login_user(user)
            return redirect(url_for('dashboard'))
        else:
            flash('Username o password non validi', 'error')
    
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/dashboard')
@login_required
def dashboard():
    oggi = date.today()
    
    # Filtri per ruolo utente
    if current_user.is_admin:
        incassi_oggi = Incasso.query.filter_by(data=oggi).all()
    else:
        # I dipendenti vedono solo i propri incassi non approvati di oggi
        incassi_oggi = Incasso.query.filter_by(
            data=oggi, 
            operatore_id=current_user.id, 
            approvato=False
        ).all()
    
    cassaforte_oggi = Cassaforte.query.filter_by(data=oggi).all()
    
    return render_template('dashboard.html', 
                         incassi_oggi=incassi_oggi,
                         cassaforte_oggi=cassaforte_oggi)

# Gestione incassi
@app.route('/incassi/nuovo', methods=['GET', 'POST'])
@login_required
def nuovo_incasso():
    if request.method == 'POST':
        try:
            # Gestione data
            data_incasso_str = request.form.get('data_incasso', date.today().isoformat())
            data_incasso = datetime.strptime(data_incasso_str, '%Y-%m-%d').date()
            
            fondo_cassa = float(request.form['fondo_cassa'])
            incasso_pos = float(request.form['incasso_pos'])
            cash_totale = float(request.form['cash_totale'])
            cash_scontrinato = float(request.form.get('cash_scontrinato', 0))
            cash_non_scontrinato = float(request.form.get('cash_non_scontrinato', 0))
            chiusura_fiscale = float(request.form.get('chiusura_fiscale', 0))
            prelievo_importo = float(request.form.get('prelievo_importo', 0))
            prelievo_motivo = request.form.get('prelievo_motivo', '')
            note = request.form.get('note', '')
            
            # Calcoli automatici
            incasso_cash_effettivo = calcola_incasso_cash_effettivo(fondo_cassa, cash_totale)
            totale_atteso = calcola_totale_incasso_atteso(incasso_pos, incasso_cash_effettivo, prelievo_importo)
            
            # Usa la nuova logica di coerenza se chiusura_fiscale è fornita
            if chiusura_fiscale > 0:
                coerenza = verifica_coerenza_chiusura_fiscale(incasso_pos, cash_totale, chiusura_fiscale, fondo_cassa, prelievo_importo)
            else:
                coerenza = verifica_coerenza(incasso_cash_effettivo, cash_scontrinato, cash_non_scontrinato)
            
            incasso = Incasso(
                operatore_id=current_user.id,
                data=data_incasso,
                fondo_cassa_iniziale=fondo_cassa,
                incasso_pos=incasso_pos,
                cash_totale_cassa=cash_totale,
                cash_scontrinato=cash_scontrinato,
                cash_non_scontrinato=cash_non_scontrinato,
                chiusura_fiscale=chiusura_fiscale,
                prelievo_importo=prelievo_importo,
                prelievo_motivo=prelievo_motivo,
                note=note
            )
            
            db.session.add(incasso)
            db.session.commit()
            
            flash(f'Incasso registrato con successo. {coerenza}', 'success')
            return redirect(url_for('dashboard'))
            
        except ValueError:
            flash('Errore nei dati inseriti. Verificare i valori numerici.', 'error')
    
    return render_template('nuovo_incasso.html', today=date.today().isoformat())

def raggruppa_incassi_per_mese(incassi):
    """Raggruppa gli incassi per mese/anno"""
    gruppi = {}
    for incasso in incassi:
        chiave = incasso.data.strftime('%Y-%m')
        if chiave not in gruppi:
            gruppi[chiave] = []
        gruppi[chiave].append(incasso)
    return gruppi

@app.route('/incassi/lista')
@login_required
def lista_incassi():
    # Parametri di ricerca
    data_ricerca = request.args.get('data_ricerca', '')
    operatore_ricerca = request.args.get('operatore_ricerca', '')
    
    # Query base
    query = Incasso.query
    
    # Filtri per ruolo utente
    if not current_user.is_admin:
        # I dipendenti vedono solo i propri incassi non approvati
        query = query.filter_by(operatore_id=current_user.id, approvato=False)
    
    # Applica filtri di ricerca
    if data_ricerca:
        try:
            data_ricerca_obj = datetime.strptime(data_ricerca, '%Y-%m-%d').date()
            query = query.filter(Incasso.data == data_ricerca_obj)
        except ValueError:
            # Se la data non è valida, ignora il filtro
            pass
    
    if operatore_ricerca and current_user.is_admin:
        # Cerca per nome utente o nome completo
        query = query.join(User, Incasso.operatore_id == User.id).filter(
            db.or_(
                User.username.ilike(f'%{operatore_ricerca}%'),
                User.nome_completo.ilike(f'%{operatore_ricerca}%')
            )
        )
    
    # Ordina per data decrescente
    incassi = query.order_by(Incasso.data.desc()).all()
    
    # Raggruppa per mese
    incassi_raggruppati = raggruppa_incassi_per_mese(incassi)
    
    # Ottieni lista utenti per il filtro (solo per admin)
    utenti = []
    if current_user.is_admin:
        utenti = User.query.order_by(User.nome_completo).all()
    
    return render_template('lista_incassi.html', 
                         incassi_raggruppati=incassi_raggruppati,
                         data_ricerca=data_ricerca,
                         operatore_ricerca=operatore_ricerca,
                         utenti=utenti)

@app.route('/incassi/grafico')
@login_required
@admin_required
def grafico_incassi():
    # Ottieni gli ultimi 30 giorni di dati
    data_inizio = date.today() - timedelta(days=30)
    incassi = Incasso.query.filter(Incasso.data >= data_inizio).order_by(Incasso.data).all()
    
    # Raggruppa per data
    dati_grafico = {}
    for incasso in incassi:
        data_str = incasso.data.strftime('%Y-%m-%d')
        if data_str not in dati_grafico:
            dati_grafico[data_str] = {
                'pos': 0,
                'cash': 0,
                'totale': 0,
                'count': 0
            }
        
        incasso_cash_effettivo = calcola_incasso_cash_effettivo(incasso.fondo_cassa_iniziale, incasso.cash_totale_cassa)
        totale = calcola_totale_incasso_atteso(incasso.incasso_pos, incasso_cash_effettivo, incasso.prelievo_importo)
        
        dati_grafico[data_str]['pos'] += incasso.incasso_pos
        dati_grafico[data_str]['cash'] += incasso_cash_effettivo
        dati_grafico[data_str]['totale'] += totale
        dati_grafico[data_str]['count'] += 1
    
    return render_template('grafico_incassi.html', dati_grafico=dati_grafico)

@app.route('/incassi/<int:id>')
@login_required
def dettaglio_incasso(id):
    incasso = Incasso.query.get_or_404(id)
    
    # Controllo accesso: admin può vedere tutto, dipendenti solo i propri non approvati
    if not current_user.is_admin:
        if incasso.operatore_id != current_user.id or incasso.approvato:
            flash('Non hai i permessi per visualizzare questo incasso.', 'error')
            return redirect(url_for('lista_incassi'))
    
    # Calcoli per il dettaglio
    incasso_cash_effettivo = calcola_incasso_cash_effettivo(incasso.fondo_cassa_iniziale, incasso.cash_totale_cassa)
    totale_atteso = calcola_totale_incasso_atteso(incasso.incasso_pos, incasso_cash_effettivo, incasso.prelievo_importo)
    coerenza = verifica_coerenza(incasso_cash_effettivo, incasso.cash_scontrinato, incasso.cash_non_scontrinato)
    
    # Calcola anomalie
    anomalie = calcola_anomalie_incasso(incasso)
    
    return render_template('dettaglio_incasso.html', 
                         incasso=incasso,
                         incasso_cash_effettivo=incasso_cash_effettivo,
                         totale_atteso=totale_atteso,
                         coerenza=coerenza,
                         anomalie=anomalie)

@app.route('/incassi/<int:id>/modifica', methods=['GET', 'POST'])
@login_required
def modifica_incasso(id):
    incasso = Incasso.query.get_or_404(id)
    
    # Controllo accesso: admin può modificare tutto, dipendenti solo i propri non approvati
    if not current_user.is_admin:
        if incasso.operatore_id != current_user.id or incasso.approvato:
            flash('Non hai i permessi per modificare questo incasso.', 'error')
            return redirect(url_for('lista_incassi'))
    
    if request.method == 'POST':
        try:
            # Gestione data
            data_incasso_str = request.form.get('data_incasso', incasso.data.isoformat())
            data_incasso = datetime.strptime(data_incasso_str, '%Y-%m-%d').date()
            
            incasso.data = data_incasso
            incasso.fondo_cassa_iniziale = float(request.form['fondo_cassa'])
            incasso.incasso_pos = float(request.form['incasso_pos'])
            incasso.cash_totale_cassa = float(request.form['cash_totale'])
            incasso.cash_scontrinato = float(request.form.get('cash_scontrinato', 0))
            incasso.cash_non_scontrinato = float(request.form.get('cash_non_scontrinato', 0))
            incasso.chiusura_fiscale = float(request.form.get('chiusura_fiscale', 0))
            incasso.prelievo_importo = float(request.form.get('prelievo_importo', 0))
            incasso.prelievo_motivo = request.form.get('prelievo_motivo', '')
            incasso.note = request.form.get('note', '')
            
            # Se l'incasso era approvato, lo riporta in attesa di approvazione
            if incasso.approvato:
                incasso.approvato = False
                incasso.approvato_da = None
                incasso.approvato_il = None
                flash('Incasso modificato e riportato in attesa di approvazione.', 'warning')
            else:
                flash('Incasso modificato con successo.', 'success')
            
            db.session.commit()
            return redirect(url_for('dettaglio_incasso', id=incasso.id))
            
        except ValueError:
            flash('Errore nei dati inseriti. Verificare i valori numerici.', 'error')
    
    return render_template('modifica_incasso.html', incasso=incasso)

@app.route('/incassi/<int:id>/approva', methods=['POST'])
@login_required
@admin_required
def approva_incasso(id):
    incasso = Incasso.query.get_or_404(id)
    incasso.approvato = True
    incasso.approvato_da = current_user.id
    incasso.approvato_il = datetime.utcnow()
    
    db.session.commit()
    flash('Incasso approvato con successo.', 'success')
    return redirect(url_for('lista_incassi'))

@app.route('/incassi/<int:id>/cambia_stato', methods=['POST'])
@login_required
@admin_required
def cambia_stato_incasso(id):
    incasso = Incasso.query.get_or_404(id)
    nuova_azione = request.form.get('azione')
    
    if nuova_azione == 'approva':
        incasso.approvato = True
        incasso.approvato_da = current_user.id
        incasso.approvato_il = datetime.utcnow()
        flash('Incasso approvato con successo.', 'success')
    elif nuova_azione == 'disapprova':
        incasso.approvato = False
        incasso.approvato_da = None
        incasso.approvato_il = None
        flash('Incasso riportato in attesa di approvazione.', 'warning')
    else:
        flash('Azione non valida.', 'error')
        return redirect(url_for('lista_incassi'))
    
    db.session.commit()
    return redirect(url_for('lista_incassi'))

@app.route('/incassi/<int:id>/elimina', methods=['POST'])
@login_required
@admin_required
def elimina_incasso(id):
    incasso = Incasso.query.get_or_404(id)
    
    # Salva informazioni per il messaggio
    data_incasso = incasso.data
    importo_incasso = incasso.incasso_pos + (incasso.cash_totale_cassa - incasso.fondo_cassa_iniziale)
    
    db.session.delete(incasso)
    db.session.commit()
    
    flash(f'Incasso del {data_incasso.strftime("%d/%m/%Y")} (€{importo_incasso:.2f}) eliminato con successo', 'success')
    return redirect(url_for('lista_incassi'))

# Gestione cassaforte
@app.route('/cassaforte/nuovo', methods=['GET', 'POST'])
@login_required
def nuovo_movimento_cassaforte():
    if request.method == 'POST':
        data_movimento = datetime.strptime(request.form['data_movimento'], '%Y-%m-%d').date()
        tipo_movimento = request.form['tipo_movimento']
        importo = float(request.form['importo'])
        monete_importo = float(request.form.get('monete_importo', 0))
        banconote_importo = float(request.form.get('banconote_importo', 0))
        descrizione = request.form['descrizione']
        
        # Validazione: la somma di monete e banconote deve essere uguale all'importo totale
        if abs((monete_importo + banconote_importo) - importo) > 0.01:
            flash('La somma di monete e banconote deve essere uguale all\'importo totale', 'error')
            return redirect(url_for('nuovo_movimento_cassaforte'))
        
        movimento = Cassaforte(
            data=data_movimento,
            operatore_id=current_user.id,
            tipo_movimento=tipo_movimento,
            importo=importo,
            monete_importo=monete_importo,
            banconote_importo=banconote_importo,
            descrizione=descrizione
        )
        
        db.session.add(movimento)
        db.session.commit()
        
        flash('Movimento cassaforte registrato con successo', 'success')
        return redirect(url_for('lista_movimenti_cassaforte'))
    
    today = date.today()
    return render_template('nuovo_movimento_cassaforte.html', today=today)

@app.route('/cassaforte/lista')
@login_required
def lista_movimenti_cassaforte():
    if current_user.is_admin:
        movimenti = Cassaforte.query.order_by(Cassaforte.data.desc()).all()
    else:
        movimenti = Cassaforte.query.filter_by(operatore_id=current_user.id).order_by(Cassaforte.data.desc()).all()
    
    # Calcola i saldi della cassaforte
    saldo_monete = calcola_saldo_monete()
    saldo_banconote = calcola_saldo_banconote()
    totale_cassaforte = calcola_totale_cassaforte()
    
    return render_template('lista_movimenti_cassaforte.html', 
                         movimenti=movimenti, 
                         saldo_monete=saldo_monete,
                         saldo_banconote=saldo_banconote,
                         totale_cassaforte=totale_cassaforte)

def calcola_saldo_monete():
    """Calcola il saldo attuale delle monete nella cassaforte"""
    movimenti = Cassaforte.query.filter_by(approvato=True).all()
    
    saldo = 0.0
    for movimento in movimenti:
        if movimento.tipo_movimento == 'entrata':
            saldo += movimento.monete_importo
        else:  # uscita
            saldo -= movimento.monete_importo
    
    return saldo

def calcola_saldo_banconote():
    """Calcola il saldo attuale delle banconote nella cassaforte"""
    movimenti = Cassaforte.query.filter_by(approvato=True).all()
    
    saldo = 0.0
    for movimento in movimenti:
        if movimento.tipo_movimento == 'entrata':
            saldo += movimento.banconote_importo
        else:  # uscita
            saldo -= movimento.banconote_importo
    
    return saldo

def calcola_totale_cassaforte():
    """Calcola il totale cash+monete nella cassaforte"""
    saldo_monete = calcola_saldo_monete()
    saldo_banconote = calcola_saldo_banconote()
    return saldo_monete + saldo_banconote

def verifica_livello_monete(saldo_monete):
    """Verifica se il livello delle monete è sotto il minimo"""
    MINIMO_MONETE = 50.0
    return saldo_monete < MINIMO_MONETE

@app.route('/cassaforte/<int:id>/approva', methods=['POST'])
@login_required
@admin_required
def approva_movimento_cassaforte(id):
    movimento = Cassaforte.query.get_or_404(id)
    movimento.approvato = True
    movimento.approvato_da = current_user.id
    movimento.approvato_il = datetime.utcnow()
    
    db.session.commit()
    flash('Movimento cassaforte approvato con successo.', 'success')
    return redirect(url_for('lista_movimenti_cassaforte'))

@app.route('/cassaforte/<int:id>/elimina', methods=['POST'])
@login_required
@admin_required
def elimina_movimento_cassaforte(id):
    movimento = Cassaforte.query.get_or_404(id)
    
    # Salva informazioni per il messaggio
    data_movimento = movimento.data
    importo_movimento = movimento.importo
    tipo_movimento = movimento.tipo_movimento
    
    db.session.delete(movimento)
    db.session.commit()
    
    flash(f'Movimento {tipo_movimento} del {data_movimento.strftime("%d/%m/%Y")} (€{importo_movimento:.2f}) eliminato con successo', 'success')
    return redirect(url_for('lista_movimenti_cassaforte'))

# API per report
@app.route('/api/report/giornaliero/<data>')
@login_required
@admin_required
def report_giornaliero(data):
    
    try:
        data_report = datetime.strptime(data, '%Y-%m-%d').date()
    except ValueError:
        return jsonify({'error': 'Formato data non valido'}), 400
    
    incassi = Incasso.query.filter_by(data=data_report).all()
    movimenti_cassaforte = Cassaforte.query.filter_by(data=data_report).all()
    
    totale_pos = sum(i.incasso_pos for i in incassi)
    totale_cash = sum(calcola_incasso_cash_effettivo(i.fondo_cassa_iniziale, i.cash_totale_cassa) for i in incassi)
    totale_cassaforte = sum(m.importo if m.tipo_movimento == 'entrata' else -m.importo for m in movimenti_cassaforte)
    
    return jsonify({
        'data': data,
        'incassi': len(incassi),
        'totale_pos': totale_pos,
        'totale_cash': totale_cash,
        'totale_giornaliero': totale_pos + totale_cash,
        'movimenti_cassaforte': len(movimenti_cassaforte),
        'saldo_cassaforte': totale_cassaforte
    })

# Gestione utenti (solo admin)
@app.route('/utenti/lista')
@login_required
@admin_required
def lista_utenti():
    utenti = User.query.order_by(User.created_at.desc()).all()
    return render_template('lista_utenti.html', utenti=utenti)

@app.route('/utenti/nuovo', methods=['GET', 'POST'])
@login_required
@admin_required
def nuovo_utente():
    if request.method == 'POST':
        try:
            username = request.form['username']
            password = request.form['password']
            password_confirm = request.form.get('password_confirm', '')
            nome_completo = request.form['nome_completo']
            is_admin = 'is_admin' in request.form
            
            # Verifica se l'username esiste già
            if User.query.filter_by(username=username).first():
                flash('Username già esistente. Scegliere un altro username.', 'error')
                return render_template('nuovo_utente.html')
            
            # Verifica che le password coincidano
            if password != password_confirm:
                flash('Le password non coincidono.', 'error')
                return render_template('nuovo_utente.html')
            
            nuovo_utente = User(
                username=username,
                password_hash=generate_password_hash(password),
                nome_completo=nome_completo,
                is_admin=is_admin
            )
            
            db.session.add(nuovo_utente)
            db.session.commit()
            
            flash(f'Utente "{username}" creato con successo.', 'success')
            return redirect(url_for('lista_utenti'))
            
        except Exception as e:
            flash(f'Errore durante la creazione dell\'utente: {str(e)}', 'error')
    
    return render_template('nuovo_utente.html')

@app.route('/utenti/<int:id>/modifica', methods=['GET', 'POST'])
@login_required
@admin_required
def modifica_utente(id):
    utente = User.query.get_or_404(id)
    
    if request.method == 'POST':
        try:
            utente.nome_completo = request.form['nome_completo']
            utente.is_admin = 'is_admin' in request.form
            
            # Se è stata fornita una nuova password, aggiornala
            nuova_password = request.form.get('password')
            password_confirm = request.form.get('password_confirm', '')
            
            if nuova_password:
                # Verifica che le password coincidano
                if nuova_password != password_confirm:
                    flash('Le password non coincidono.', 'error')
                    return render_template('modifica_utente.html', utente=utente)
                
                utente.password_hash = generate_password_hash(nuova_password)
            
            db.session.commit()
            flash(f'Utente "{utente.username}" modificato con successo.', 'success')
            return redirect(url_for('lista_utenti'))
            
        except Exception as e:
            flash(f'Errore durante la modifica dell\'utente: {str(e)}', 'error')
    
    return render_template('modifica_utente.html', utente=utente)

@app.route('/utenti/<int:id>/elimina', methods=['POST'])
@login_required
@admin_required
def elimina_utente(id):
    utente = User.query.get_or_404(id)
    
    # Impedisci l'eliminazione dell'utente corrente
    if utente.id == current_user.id:
        flash('Non puoi eliminare il tuo stesso account.', 'error')
        return redirect(url_for('lista_utenti'))
    
    # Verifica se l'utente ha dati associati
    incassi_utente = Incasso.query.filter_by(operatore_id=utente.id).count()
    movimenti_utente = Cassaforte.query.filter_by(operatore_id=utente.id).count()
    
    if incassi_utente > 0 or movimenti_utente > 0:
        flash(f'Impossibile eliminare l\'utente "{utente.username}". Ha {incassi_utente} incassi e {movimenti_utente} movimenti cassaforte associati.', 'error')
        return redirect(url_for('lista_utenti'))
    
    try:
        username = utente.username
        db.session.delete(utente)
        db.session.commit()
        flash(f'Utente "{username}" eliminato con successo.', 'success')
    except Exception as e:
        flash(f'Errore durante l\'eliminazione dell\'utente: {str(e)}', 'error')
    
    return redirect(url_for('lista_utenti'))

# Gestione prelievi per admin
@app.route('/prelievi/lista')
@login_required
@admin_required
def lista_prelievi():
    # Parametri di ricerca
    data_inizio = request.args.get('data_inizio', '')
    data_fine = request.args.get('data_fine', '')
    operatore_ricerca = request.args.get('operatore_ricerca', '')
    
    # Query base - solo incassi con prelievi
    query = Incasso.query.filter(Incasso.prelievo_importo > 0)
    
    # Applica filtri di ricerca
    if data_inizio:
        try:
            data_inizio_obj = datetime.strptime(data_inizio, '%Y-%m-%d').date()
            query = query.filter(Incasso.data >= data_inizio_obj)
        except ValueError:
            pass
    
    if data_fine:
        try:
            data_fine_obj = datetime.strptime(data_fine, '%Y-%m-%d').date()
            query = query.filter(Incasso.data <= data_fine_obj)
        except ValueError:
            pass
    
    if operatore_ricerca:
        query = query.join(User, Incasso.operatore_id == User.id).filter(
            db.or_(
                User.username.ilike(f'%{operatore_ricerca}%'),
                User.nome_completo.ilike(f'%{operatore_ricerca}%')
            )
        )
    
    # Ordina per data decrescente
    prelievi = query.order_by(Incasso.data.desc()).all()
    
    # Calcola totali
    totale_prelievi = sum(p.prelievo_importo for p in prelievi)
    totale_incassi = sum(p.incasso_pos + (p.cash_totale_cassa - p.fondo_cassa_iniziale) for p in prelievi)
    percentuale_prelievi = (totale_prelievi / totale_incassi * 100) if totale_incassi > 0 else 0
    
    # Raggruppa per mese
    prelievi_raggruppati = {}
    for prelievo in prelievi:
        chiave = prelievo.data.strftime('%Y-%m')
        if chiave not in prelievi_raggruppati:
            prelievi_raggruppati[chiave] = {
                'prelievi': [],
                'totale_prelievi': 0,
                'totale_incassi': 0
            }
        prelievi_raggruppati[chiave]['prelievi'].append(prelievo)
        prelievi_raggruppati[chiave]['totale_prelievi'] += prelievo.prelievo_importo
        prelievi_raggruppati[chiave]['totale_incassi'] += prelievo.incasso_pos + (prelievo.cash_totale_cassa - prelievo.fondo_cassa_iniziale)
    
    # Ottieni lista utenti per il filtro
    utenti = User.query.order_by(User.nome_completo).all()
    
    return render_template('lista_prelievi.html',
                         prelievi_raggruppati=prelievi_raggruppati,
                         data_inizio=data_inizio,
                         data_fine=data_fine,
                         operatore_ricerca=operatore_ricerca,
                         utenti=utenti,
                         totale_prelievi=totale_prelievi,
                         totale_incassi=totale_incassi,
                         percentuale_prelievi=percentuale_prelievi)

# Inizializzazione database e utenti
with app.app_context():
    db.create_all()
    print("✔️ Tabelle create")
    
    # Crea utente admin se non esiste
    admin = User.query.filter_by(username='admin').first()
    if not admin:
        admin = User(
            username='admin',
            password_hash=generate_password_hash('admin123'),
            is_admin=True,
            nome_completo='Amministratore Sistema'
        )
        db.session.add(admin)
        db.session.commit()
        print("Utente admin creato: username='admin', password='admin123'")
    
    # Crea utente dipendente se non esiste
    dipendente = User.query.filter_by(username='dipendente').first()
    if not dipendente:
        dipendente = User(
            username='dipendente',
            password_hash=generate_password_hash('dipendente123'),
            is_admin=False,
            nome_completo='Dipendente Sistema'
        )
        db.session.add(dipendente)
        db.session.commit()
        print("Utente dipendente creato: username='dipendente', password='dipendente123'")

if __name__ == '__main__':
    app.run(debug=True)
