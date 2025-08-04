# Gestionale Incassi

Sistema completo per la gestione e il controllo degli incassi giornalieri con funzionalità di cassaforte integrata.

## 🎯 Caratteristiche Principali

### Sezione 1: Controllo Incassi Giornalieri

#### Funzionalità per Operatori:
- **Inserimento dati incassi**: Fondo cassa iniziale, incasso POS, cash totale in cassa
- **Dettagli opzionali**: Distinzione tra cash scontrinato e non scontrinato
- **Calcoli automatici**: Sistema calcola automaticamente incasso cash effettivo e totale atteso
- **Controllo coerenza**: Verifica automatica delle discrepanze con alert

#### Funzionalità per Amministratori:
- **Approvazione incassi**: Sistema di approvazione per ogni incasso registrato
- **Report giornalieri**: Visualizzazione completa dei totali e calcoli
- **Controllo accessi**: Login protetto con gestione ruoli

### Sezione 2: Gestione Cassaforte

- **Movimenti entrata/uscita**: Registrazione completa dei flussi contabili
- **Storia movimenti**: Tracciamento completo di tutti i movimenti
- **Grafici dinamici**: Visualizzazione dell'andamento del saldo nel tempo
- **Statistiche**: Totali entrate, uscite e saldo attuale
- **Monitoraggio Monete**: Controllo separato di monete e banconote con indicatori di livello minimo
- **Visualizzazione 3 Saldi**: Totale in cassaforte, monete in cassa, importo cash
- **Campo Nota**: Possibilità per i dipendenti di aggiungere note ai movimenti

### Sezione 3: Grafico Incassi (Solo Admin)

- **Andamento giornaliero**: Visualizzazione degli ultimi 30 giorni di incassi
- **Dati aggregati**: POS, Cash e Totale per ogni giorno
- **Statistiche in tempo reale**: Totali calcolati automaticamente
- **Interfaccia interattiva**: Grafico responsive con Chart.js

## 🚀 Installazione

### Prerequisiti
- Python 3.8 o superiore
- pip (gestore pacchetti Python)

### Installazione Locale

1. **Clona o scarica il progetto**
   ```bash
   cd "gestionale incassi"
   ```

2. **Installa le dipendenze**
   ```bash
   pip install -r requirements.txt
   ```

3. **Inizializza il database**
   ```bash
   python init_db.py
   ```

4. **Avvia l'applicazione**
   ```bash
   python app.py
   ```

5. **Accedi al sistema**
   - Apri il browser e vai a `http://localhost:5000`
   - Username: `admin`
   - Password: `admin123`
   - Username: `dipendente`
   - Password: `dipendente123`

### Deploy Online

Per mettere l'applicazione online, consulta la guida completa in [`DEPLOY.md`](DEPLOY.md).

**Opzioni consigliate:**
- **Render** (gratuito) - [render.com](https://render.com)
- **Railway** (gratuito) - [railway.app](https://railway.app)
- **PythonAnywhere** (gratuito) - [pythonanywhere.com](https://pythonanywhere.com)

## 📊 Come Funziona

### Logica di Calcolo degli Incassi

Il sistema implementa la logica esatta descritta nei requisiti:

1. **Incasso Cash Effettivo** = Cash Totale in Cassa - Fondo Cassa Iniziale
2. **Totale Incasso Atteso** = Incasso POS + Incasso Cash Effettivo
3. **Verifica Coerenza** = Confronto tra cash effettivo e cash dichiarato (scontrinato + non scontrinato)

### Esempio Pratico

**Input:**
- Fondo cassa iniziale: €100
- Incasso POS: €100
- Cash totale in cassa: €200
- Cash scontrinato: €80
- Cash non scontrinato: €20

**Calcoli automatici:**
- Incasso cash effettivo: €200 - €100 = €100
- Totale atteso: €100 + €100 = €200
- Coerenza: €100 (effettivo) vs €100 (dichiarato) = ✅ Coerente

**Variante con incoerenza:**
- Cash totale in cassa: €220
- Incasso cash effettivo: €220 - €100 = €120
- Se cash dichiarato = €100 → Alert: "Eccedenza cash di €20 - possibile incasso non scontrinato"

## 👥 Ruoli e Permessi

### Dipendente
- Registrare nuovi incassi (in attesa di approvazione)
- Visualizzare i propri incassi
- Registrare movimenti cassaforte (in attesa di approvazione)
- Visualizzare storia cassaforte
- Controllare anomalie e coerenza dei dati
- Specificare importi in monete e banconote nei movimenti cassaforte

### Amministratore
- **Controllo totale**: Visualizzazione di tutti i dati del sistema
- **Sistema di approvazione**: Approvazione di incassi e movimenti cassaforte
- **Grafico incassi**: Visualizzazione dell'andamento giornaliero degli incassi
- **Report e statistiche**: Accesso completo a tutti i report
- **Gestione utenti**: Creazione, modifica ed eliminazione di utenti del sistema
- **Monitoraggio monete**: Controllo saldo monete con indicatori di livello minimo (€50)
- **Eliminazione dati**: Possibilità di eliminare incassi e movimenti specifici

### Flusso di Lavoro
1. **Dipendente** inserisce i dati → Sistema verifica coerenza
2. **Dipendente** controlla anomalie e invia dati
3. **Amministratore** riceve notifica e controlla i dati
4. **Amministratore** approva o richiede modifiche
5. **Sistema** traccia tutto il processo di approvazione

## 🎨 Interfaccia Utente

### Design Moderno e Mobile-Friendly
- **Bootstrap 5**: Interfaccia responsive e moderna
- **Mobile-first**: Design ottimizzato per dispositivi mobili
- **Font Awesome**: Icone intuitive per tutte le funzioni
- **Sidebar navigazione**: Menu laterale per accesso rapido
- **Dashboard interattiva**: Statistiche in tempo reale
- **Touch-friendly**: Pulsanti e controlli ottimizzati per touch

### Funzionalità Mobile
- **Sidebar mobile**: Menu hamburger su dispositivi mobili
- **Header responsive**: Barra superiore con info utente
- **Tabelle adattive**: Colonne che si nascondono su schermi piccoli
- **Form ottimizzati**: Input e pulsanti touch-friendly
- **Animazioni fluide**: Transizioni smooth per migliore UX

### Funzionalità Avanzate
- **Calcoli in tempo reale**: Aggiornamento automatico durante l'inserimento dati
- **Validazione form**: Controlli automatici sui dati inseriti
- **Grafici dinamici**: Visualizzazione andamento cassaforte con Chart.js
- **Alert intelligenti**: Notifiche per incoerenze e stati

## 📈 Report e Statistiche

### Report Giornaliero (Solo Admin)
- Numero incassi registrati
- Totale incasso POS
- Totale incasso cash
- Totale giornaliero
- Movimenti cassaforte
- Saldo cassaforte

### Statistiche Cassaforte
- Totale entrate
- Totale uscite
- Saldo attuale
- Grafico andamento nel tempo

### Monitoraggio Monete
- **Saldo monete attuale**: Calcolo automatico basato sui movimenti approvati
- **Indicatori di livello**: Badge rosso quando sotto €50, verde quando OK
- **Separazione monete/banconote**: Tracciamento separato per tipo di valuta
- **Validazione automatica**: Controllo che monete + banconote = importo totale
- **Scenari complessi**: Gestione di prelievi/versamenti misti con controllo saldo

### Gestione Eliminazione (Solo Admin)
- **Eliminazione incassi**: Possibilità di eliminare incassi specifici con conferma
- **Eliminazione movimenti**: Possibilità di eliminare movimenti cassaforte specifici
- **Sicurezza**: Solo admin può eliminare, con conferme JavaScript
- **Tracciabilità**: Messaggi dettagliati per ogni eliminazione
- **Controllo accessi**: Dipendenti non vedono pulsanti eliminazione

### Nuove Funzionalità Cassaforte
- **Visualizzazione 3 Saldi Distinti**: Totale in cassaforte (cash+monete), monete in cassa, importo cash
- **Campo Nota per Dipendenti**: Possibilità di aggiungere note dettagliate ai movimenti
- **Colonna Nota nella Tabella**: Visualizzazione badge per movimenti con note
- **Layout Migliorato**: 3 indicatori colorati per facile identificazione
- **Tracciabilità Migliorata**: Note per motivazioni e dettagli dei movimenti

## 🔒 Sicurezza

- **Autenticazione**: Sistema di login con password hashate
- **Gestione sessioni**: Controllo accessi per ogni pagina
- **Validazione dati**: Controlli sui valori inseriti
- **Tracciamento**: Log di tutte le operazioni con timestamp

## 🛠️ Personalizzazione

### Aggiungere Nuovi Utenti
```python
# Nel file app.py, aggiungere:
nuovo_utente = User(
    username='operatore1',
    password_hash=generate_password_hash('password123'),
    is_admin=False
)
db.session.add(nuovo_utente)
db.session.commit()
```

### Modificare Calcoli
Le funzioni di calcolo sono in `app.py`:
- `calcola_incasso_cash_effettivo()`
- `calcola_totale_incasso_atteso()`
- `verifica_coerenza()`

## 👥 Gestione Utenti

### Funzionalità Disponibili
- **Lista Utenti**: Visualizzazione di tutti gli utenti del sistema
- **Creazione Utenti**: Aggiunta di nuovi utenti con ruoli specifici
- **Modifica Utenti**: Aggiornamento di nome completo, password e ruolo
- **Eliminazione Utenti**: Rimozione sicura di utenti (con controlli)

### Sicurezza
- **Username immutabile**: Non può essere modificato dopo la creazione
- **Password hashate**: Tutte le password sono crittografate
- **Controlli eliminazione**: Impedisce l'eliminazione di utenti con dati associati
- **Auto-protezione**: Impedisce l'eliminazione del proprio account

### Accesso
- **Solo Amministratori**: Tutte le funzioni di gestione utenti sono riservate agli admin
- **Navigazione**: Menu "Gestione Utenti" nella sidebar (solo per admin)
- **Dashboard**: Pulsante "Gestione Utenti" nella sezione amministratore

## 📱 Compatibilità

### Browser Desktop
- **Chrome**: Versione 90+
- **Firefox**: Versione 88+
- **Safari**: Versione 14+
- **Edge**: Versione 90+

### Dispositivi Mobili
- **iPhone**: iOS 12+ (Safari, Chrome)
- **Android**: Chrome, Firefox, Samsung Internet
- **iPad**: Safari, Chrome
- **Android Tablet**: Chrome, Firefox

### Responsive Design
- **Smartphone**: 320px - 480px
- **Tablet**: 481px - 768px
- **Desktop**: 769px+
- **Dispositivi**: Desktop, tablet, smartphone
- **Sistema**: Windows, macOS, Linux

## 🆘 Supporto

### Problemi Comuni

1. **Errore "Module not found"**
   - Verifica di aver installato tutte le dipendenze: `pip install -r requirements.txt`

2. **Database non trovato**
   - Il database SQLite viene creato automaticamente al primo avvio

3. **Porta 5000 occupata**
   - Cambia la porta in `app.py`: `app.run(debug=True, port=5001)`

### Log e Debug
- Attiva il debug mode per vedere errori dettagliati
- I log vengono mostrati nella console durante l'esecuzione

## 📄 Licenza

Sistema sviluppato per uso interno. Tutti i diritti riservati.

---

**Sistema Gestionale Incassi** - Controllo completo degli incassi giornalieri con gestione cassaforte integrata. 