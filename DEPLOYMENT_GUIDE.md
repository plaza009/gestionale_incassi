# Guida Deployment Online - Gestionale Incassi

## 🛠️ Tecnologie Utilizzate

### Backend
- **Python 3.8+** - Linguaggio principale
- **Flask 2.2.5** - Framework web
- **Flask-SQLAlchemy 3.0.3** - ORM per database
- **Flask-Login 0.6.2** - Gestione autenticazione
- **Werkzeug 2.2.3** - Utilità web
- **Gunicorn 21.2.0** - Server WSGI per produzione

### Database
- **SQLite** - Database locale (sviluppo)
- **PostgreSQL** - Database produzione (psycopg2-binary 2.9.7)

### Frontend
- **HTML5/CSS3** - Struttura e stili
- **Bootstrap 5** - Framework CSS responsive
- **JavaScript** - Interattività client-side
- **Chart.js** - Grafici interattivi
- **Font Awesome** - Icone

### Dipendenze Python
```
Flask==2.2.5
Flask-SQLAlchemy==3.0.3
Flask-Login==0.6.2
Flask-WTF==1.1.1
WTForms==3.0.1
python-dotenv==1.0.0
Werkzeug==2.2.3
gunicorn==21.2.0
psycopg2-binary==2.9.7
```

## 🚀 Caratteristiche Hosting Richieste

### Requisiti Minimi
- **Python 3.8+** supportato
- **PostgreSQL** database
- **SSL/HTTPS** supportato
- **Domini personalizzati** supportati
- **Backup automatici** disponibili

### Requisiti Raccomandati
- **512MB RAM** minimo
- **1GB storage** minimo
- **Supporto variabili d'ambiente**
- **Logs accessibili**
- **Monitoring** disponibile

## 🎯 Piattaforme Hosting Consigliate

### 1. **Render** (RACCOMANDATO - Più Veloce)
**Vantaggi:**
- ✅ Setup automatico da GitHub
- ✅ PostgreSQL incluso
- ✅ SSL gratuito
- ✅ Deploy automatico
- ✅ Piano gratuito disponibile

**Procedura:**
1. Push su GitHub
2. Connessione a Render
3. Deploy automatico

### 2. **Railway**
**Vantaggi:**
- ✅ Molto semplice
- ✅ PostgreSQL incluso
- ✅ Deploy veloce
- ✅ Buona performance

### 3. **PythonAnywhere**
**Vantaggi:**
- ✅ Specializzato Python
- ✅ Controllo completo
- ✅ Database incluso
- ✅ Domini personalizzati

### 4. **Heroku**
**Vantaggi:**
- ✅ Molto stabile
- ✅ PostgreSQL incluso
- ✅ Add-ons disponibili
- ✅ Buona documentazione

## ⚡ Procedura Più Veloce: Render

### Passo 1: Preparazione Repository
```bash
# Assicurati che tutti i file siano committati
git add .
git commit -m "Preparazione per deployment"
git push origin main
```

### Passo 2: Setup Render
1. Vai su [render.com](https://render.com)
2. Crea account gratuito
3. Clicca "New Web Service"
4. Connetti il tuo repository GitHub
5. Configura il servizio:
   - **Name**: `gestionale-incassi`
   - **Environment**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn app:app`

### Passo 3: Configurazione Database
1. Crea nuovo "PostgreSQL" su Render
2. Copia la URL del database
3. Aggiungi come variabile d'ambiente:
   - **Key**: `DATABASE_URL`
   - **Value**: `postgresql://user:pass@host:port/db`

### Passo 4: Variabili d'Ambiente
Aggiungi queste variabili su Render:
```
DATABASE_URL=postgresql://...
SECRET_KEY=your-secret-key-here
FLASK_ENV=production
```

### Passo 5: Deploy
1. Clicca "Create Web Service"
2. Aspetta il deploy automatico (2-5 minuti)
3. Il sito sarà disponibile su `https://your-app.onrender.com`

## 🔧 File di Configurazione Necessari

### Procfile (già presente)
```
web: gunicorn app:app
```

### runtime.txt (già presente)
```
python-3.9.18
```

### wsgi.py (già presente)
```python
from app import app

if __name__ == "__main__":
    app.run()
```

## 📋 Checklist Pre-Deployment

### ✅ Preparazione Codice
- [ ] Tutti i file committati su GitHub
- [ ] `requirements.txt` aggiornato
- [ ] `Procfile` presente
- [ ] `runtime.txt` presente
- [ ] `wsgi.py` presente
- [ ] Database pulito (dati di test rimossi)

### ✅ Configurazione Database
- [ ] Database PostgreSQL configurato
- [ ] URL database copiata
- [ ] Variabile `DATABASE_URL` impostata

### ✅ Variabili d'Ambiente
- [ ] `SECRET_KEY` generata
- [ ] `FLASK_ENV=production`
- [ ] `DATABASE_URL` configurata

### ✅ Test Locali
- [ ] App funziona localmente
- [ ] Login admin/dipendente funziona
- [ ] Tutte le funzionalità testate

## 🚀 Deploy Veloce (5 minuti)

### 1. Push su GitHub
```bash
git add .
git commit -m "Ready for deployment"
git push origin main
```

### 2. Setup Render
1. Vai su render.com
2. "New Web Service" → GitHub
3. Seleziona repository
4. Configura:
   - **Name**: `gestionale-incassi`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn app:app`

### 3. Database
1. "New PostgreSQL"
2. Copia DATABASE_URL
3. Aggiungi come variabile d'ambiente

### 4. Deploy
1. "Create Web Service"
2. Aspetta 2-5 minuti
3. ✅ Sito online!

## 🔐 Sicurezza Post-Deployment

### Cambia Credenziali
1. Accedi come admin
2. Vai su "Gestione Utenti"
3. Modifica password admin e dipendente
4. Rimuovi utenti di test se presenti

### Backup Database
- Configura backup automatici su Render
- Mantieni backup locali regolari

### Monitoraggio
- Controlla logs su Render
- Monitora performance
- Verifica uptime

## 💡 Alternative Veloce

### Railway (3 minuti)
1. Vai su railway.app
2. "New Project" → GitHub
3. Seleziona repository
4. Deploy automatico

### PythonAnywhere (5 minuti)
1. Account su pythonanywhere.com
2. "Web" → "Add a new web app"
3. Upload da GitHub
4. Configura database

## 🎯 Raccomandazione Finale

**Render** è la scelta migliore per:
- ⚡ Deploy più veloce (2-5 minuti)
- 🆓 Piano gratuito generoso
- 🗄️ PostgreSQL incluso
- 🔒 SSL automatico
- 📱 Interfaccia semplice

Il tuo sistema sarà online in meno di 10 minuti! 🚀 