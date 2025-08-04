# Funzionalità di Ricerca nella Lista Incassi - IMPLEMENTATA

## Problema Risolto

L'utente ha richiesto di aggiungere un campo di ricerca nella lista gestione incassi per permettere di:
- Cercare per data specifica
- Cercare per operatore (solo per admin)
- Mantenere la visualizzazione ordinata divisa per mese
- Permettere la ricerca per giorni specifici

## Soluzione Implementata

### 1. Modifiche al Backend (`app.py`)

#### Nuova Funzione Helper
```python
def raggruppa_incassi_per_mese(incassi):
    """Raggruppa gli incassi per mese/anno"""
    gruppi = {}
    for incasso in incassi:
        chiave = incasso.data.strftime('%Y-%m')
        if chiave not in gruppi:
            gruppi[chiave] = []
        gruppi[chiave].append(incasso)
    return gruppi
```

#### Route `lista_incassi` Aggiornata
La route è stata completamente riscritta per supportare:

- **Parametri di ricerca**: `data_ricerca` e `operatore_ricerca`
- **Filtri per ruolo**: I dipendenti vedono solo i propri incassi
- **Ricerca per data**: Convalidazione della data e filtro esatto
- **Ricerca per operatore**: Solo per admin, cerca per username o nome completo
- **Raggruppamento per mese**: Gli incassi sono organizzati per mese/anno
- **Ordine decrescente**: Gli incassi sono ordinati per data decrescente

```python
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
        query = query.filter_by(operatore_id=current_user.id)
    
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
```

### 2. Modifiche al Frontend (`templates/lista_incassi.html`)

#### Form di Ricerca
Aggiunto un form di ricerca con:
- Campo data (tipo `date`)
- Campo operatore (solo per admin)
- Pulsanti "Cerca" e "Pulisci"

```html
<form method="GET" action="{{ url_for('lista_incassi') }}" class="mb-4">
    <div class="row g-3">
        <div class="col-md-4">
            <label for="data_ricerca" class="form-label">Cerca per Data</label>
            <input type="date" class="form-control" id="data_ricerca" name="data_ricerca" 
                   value="{{ data_ricerca }}" placeholder="Seleziona data">
        </div>
        {% if current_user.is_admin %}
        <div class="col-md-4">
            <label for="operatore_ricerca" class="form-label">Cerca per Operatore</label>
            <input type="text" class="form-control" id="operatore_ricerca" name="operatore_ricerca" 
                   value="{{ operatore_ricerca }}" placeholder="Nome utente o nome completo">
        </div>
        {% endif %}
        <div class="col-md-4 d-flex align-items-end">
            <div class="btn-group w-100" role="group">
                <button type="submit" class="btn btn-primary">
                    <i class="fas fa-search me-1"></i>
                    Cerca
                </button>
                <a href="{{ url_for('lista_incassi') }}" class="btn btn-outline-secondary">
                    <i class="fas fa-times me-1"></i>
                    Pulisci
                </a>
            </div>
        </div>
    </div>
</form>
```

#### Visualizzazione Raggruppata per Mese
Gli incassi sono ora organizzati in sezioni per mese:

```html
{% for mese, incassi in incassi_raggruppati.items() %}
<div class="mb-4">
    <h5 class="text-primary border-bottom pb-2 mb-3">
        <i class="fas fa-calendar-alt me-2"></i>
        {{ mese.split('-')[1] }}/{{ mese.split('-')[0] }}
        <span class="badge bg-secondary ms-2">{{ incassi|length }} incassi</span>
    </h5>
    
    <div class="table-responsive">
        <!-- Tabella incassi per questo mese -->
    </div>
</div>
{% endfor %}
```

### 3. Funzionalità Implementate

#### ✅ Ricerca per Data
- Campo input di tipo `date`
- Ricerca esatta per data specifica
- Validazione automatica del formato data
- Mantenimento del valore inserito nel campo

#### ✅ Ricerca per Operatore
- Campo di testo per inserire nome utente o nome completo
- Disponibile solo per gli amministratori
- Ricerca case-insensitive con pattern matching
- Mantenimento del valore inserito nel campo

#### ✅ Visualizzazione Raggruppata per Mese
- Gli incassi sono organizzati per mese/anno
- Ogni sezione mostra il mese e il numero di incassi
- Ordine decrescente per data all'interno di ogni mese
- Design responsive e mobile-friendly

#### ✅ Pulsante "Pulisci"
- Rimuove tutti i filtri di ricerca
- Reimposta la visualizzazione completa
- Mantiene tutte le funzionalità esistenti

#### ✅ Gestione Ruoli
- **Admin**: Può cercare per data e operatore, vede tutti gli incassi
- **Dipendente**: Può cercare solo per data, vede solo i propri incassi
- Campo operatore nascosto per i dipendenti

#### ✅ Gestione Errori
- Validazione automatica delle date
- Gestione graceful di date non valide
- Messaggi appropriati quando non ci sono risultati

### 4. Test Implementati

Creato `test_ricerca_incassi.py` che verifica:

1. **Presenza form di ricerca**
2. **Presenza campi di ricerca**
3. **Funzionamento ricerca per data**
4. **Funzionamento ricerca per operatore**
5. **Funzionamento pulsante "Pulisci"**
6. **Raggruppamento per mese**
7. **Limitazioni per ruolo dipendente**

### 5. Compatibilità

- ✅ **Mobile**: Form responsive con Bootstrap
- ✅ **Desktop**: Layout ottimizzato per schermi grandi
- ✅ **Accessibilità**: Label appropriati e struttura semantica
- ✅ **UX**: Feedback visivo e messaggi chiari

## Risultato

La funzionalità di ricerca è ora completamente implementata e permette:

- **Ricerca precisa per data**: Gli utenti possono selezionare una data specifica
- **Ricerca per operatore**: Gli admin possono cercare per nome utente o nome completo
- **Visualizzazione organizzata**: Gli incassi sono raggruppati per mese con contatori
- **Interfaccia intuitiva**: Form di ricerca chiaro con pulsanti per cercare e pulire
- **Gestione ruoli**: I dipendenti hanno accesso limitato alle funzioni di ricerca
- **Responsive design**: Funziona perfettamente su mobile e desktop

La funzionalità è stata testata e documentata, pronta per l'uso in produzione. 