# Guida al Deploy - Gestionale Incassi

## Preparazione del Progetto

Il progetto è già configurato per il deploy. I file necessari sono:

- `app.py` - Applicazione Flask principale
- `requirements.txt` - Dipendenze Python
- `Procfile` - Configurazione per hosting
- `runtime.txt` - Versione Python
- `wsgi.py` - Entry point per WSGI
- `.gitignore` - File da escludere

## Opzioni di Hosting

### 1. Render (Raccomandato)

**Vantaggi:**
- Gratuito per progetti personali
- Deploy automatico da GitHub
- Database PostgreSQL incluso
- SSL automatico

**Passi:**
1. Vai su [render.com](https://render.com)
2. Crea un account gratuito
3. Clicca "New Web Service"
4. Connetti il tuo repository GitHub
5. Configura:
   - **Name**: gestionale-incassi
   - **Environment**: Python 3
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn app:app`
6. Clicca "Create Web Service"

### 2. Railway

**Vantaggi:**
- Gratuito per progetti piccoli
- Deploy automatico
- Database incluso

**Passi:**
1. Vai su [railway.app](https://railway.app)
2. Crea un account
3. Clicca "New Project"
4. Seleziona "Deploy from GitHub repo"
5. Seleziona il tuo repository
6. Railway rileverà automaticamente che è un'app Python

### 3. PythonAnywhere

**Vantaggi:**
- Specializzato in Python
- Database SQLite incluso
- Controllo completo

**Passi:**
1. Vai su [pythonanywhere.com](https://pythonanywhere.com)
2. Crea un account gratuito
3. Vai su "Web" tab
4. Clicca "Add a new web app"
5. Seleziona "Flask"
6. Carica i file del progetto
7. Installa le dipendenze: `pip install -r requirements.txt`

## Configurazione del Database

### Per Render/Railway (PostgreSQL):
```python
# In app.py, modifica la configurazione del database
import os
DATABASE_URL = os.environ.get('DATABASE_URL', 'sqlite:///gestionale.db')
if DATABASE_URL.startswith('postgres://'):
    DATABASE_URL = DATABASE_URL.replace('postgres://', 'postgresql://', 1)
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URL
```

### Per PythonAnywhere (SQLite):
Il database SQLite funzionerà direttamente.

## Variabili d'Ambiente

Configura queste variabili nel tuo hosting:

- `SECRET_KEY`: Chiave segreta per Flask
- `FLASK_ENV`: production
- `DATABASE_URL`: URL del database (se usi PostgreSQL)

## Test del Deploy

Dopo il deploy, testa:

1. **Login Admin**: admin/admin123
2. **Login Dipendente**: dipendente/dipendente123
3. **Funzionalità principali**:
   - Inserimento incassi
   - Gestione cassaforte
   - Grafici (solo admin)
   - Gestione utenti (solo admin)

## Troubleshooting

### Errori Comuni:

1. **ModuleNotFoundError**: Verifica che `requirements.txt` contenga tutte le dipendenze
2. **Database Error**: Controlla la configurazione del database
3. **500 Error**: Controlla i log dell'hosting per dettagli

### Log di Debug:

Aggiungi questo codice in `app.py` per debug:
```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

## Costi Stimati

- **Render**: Gratuito (fino a 750 ore/mese)
- **Railway**: Gratuito (fino a $5/mese)
- **PythonAnywhere**: Gratuito (account base)
- **Heroku**: $7/mese (Basic Dyno)

## Raccomandazione Finale

Per iniziare, usa **Render** perché:
- È gratuito
- Ha un'interfaccia semplice
- Include database PostgreSQL
- Ha SSL automatico
- Deploy automatico da GitHub 