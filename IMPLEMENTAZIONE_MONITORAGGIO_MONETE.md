# Implementazione Monitoraggio Monete nella Cassaforte

## Problema Risolto

L'utente ha richiesto di implementare un sistema di monitoraggio delle monete nella cassaforte che permetta di:
- Tracciare separatamente monete e banconote nei movimenti
- Calcolare il saldo attuale delle monete
- Mostrare un indicatore visivo quando il livello delle monete scende sotto €50
- Gestire scenari dove il totale è corretto ma le monete sono insufficienti

## Nuove Funzionalità Implementate

### 1. Modello Database Aggiornato

**Modello `Cassaforte` aggiornato con nuovi campi:**
- `monete_importo` (Float, default 0.0): Importo in monete
- `banconote_importo` (Float, default 0.0): Importo in banconote
- `tipo_movimento` (String): Tipo di movimento (entrata/uscita)

### 2. Form Nuovo Movimento Cassaforte

**Campi aggiunti:**
- **Importo Totale**: Campo principale per l'importo complessivo
- **Importo in Monete**: Campo opzionale per specificare l'importo in monete
- **Importo in Banconote**: Campo calcolato automaticamente (totale - monete)

**Validazione:**
- La somma di monete e banconote deve essere uguale all'importo totale
- Se non si specificano monete/banconote, tutto è considerato banconote

**JavaScript:**
- Calcolo automatico del campo banconote quando cambia l'importo totale
- Calcolo automatico dell'importo totale quando cambiano monete/banconote

### 3. Lista Movimenti Cassaforte

**Indicatore Saldo Monete:**
- Card con saldo attuale delle monete
- Badge rosso "Livello Minimo" se sotto €50
- Badge verde "OK" se sopra €50
- Informazioni sul livello minimo

**Colonne Aggiunte:**
- **Monete**: Badge giallo con importo in monete
- **Banconote**: Badge blu con importo in banconote
- **Importo Totale**: Importo complessivo in grassetto

### 4. Funzioni di Calcolo

**`calcola_saldo_monete()`:**
```python
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
```

**`verifica_livello_monete()`:**
```python
def verifica_livello_monete(saldo_monete):
    """Verifica se il livello delle monete è sotto il minimo"""
    MINIMO_MONETE = 50.0
    return saldo_monete < MINIMO_MONETE
```

### 5. Aggiornamento Route

**`nuovo_movimento_cassaforte`:**
- Gestione dei nuovi campi `monete_importo` e `banconote_importo`
- Validazione della somma monete + banconote = totale
- Passaggio della data odierna al template

**`lista_movimenti_cassaforte`:**
- Calcolo e passaggio del `saldo_monete` al template
- Filtro per ruolo utente (admin vede tutto, dipendente solo i propri)

## Template Aggiornati

### `templates/nuovo_movimento_cassaforte.html`
- Form con campi per monete e banconote
- JavaScript per calcoli automatici
- Validazione client-side
- Layout responsive

### `templates/lista_movimenti_cassaforte.html`
- Indicatore saldo monete con badge di stato
- Colonne separate per monete e banconote
- Badge colorati per distinguere i tipi
- Informazioni sul sistema di monitoraggio

## Script di Supporto

### `aggiorna_db_monete.py`
- Ricrea il database con il nuovo schema
- Crea utenti di default
- Popola con movimenti di test che includono:
  - Movimenti con solo monete
  - Movimenti con solo banconote
  - Movimenti misti
  - Movimenti approvati e non approvati
- Calcola e mostra il saldo finale delle monete

### `test_monitoraggio_monete.py`
- Testa la presenza dei campi nel form
- Verifica l'indicatore saldo monete
- Controlla le colonne monete/banconote
- Testa i badge di stato
- Verifica i pulsanti di approvazione

## Scenari di Test Implementati

1. **Versamento incassi giornalieri**: €500 (€100 monete + €400 banconote)
2. **Prelievo per fondo cassa**: €200 (€50 monete + €150 banconote)
3. **Versamento solo banconote**: €300 (€0 monete + €300 banconote)
4. **Prelievo con più monete**: €150 (€100 monete + €50 banconote) - non approvato
5. **Versamento solo monete**: €80 (€80 monete + €0 banconote)

**Saldo finale calcolato**: €130 (sopra il minimo di €50)

## Vantaggi del Sistema

1. **Separazione Chiara**: Monete e banconote sono tracciate separatamente
2. **Controllo Automatico**: Il sistema calcola automaticamente il saldo
3. **Indicatori Visivi**: Badge colorati per stato immediato
4. **Validazione**: Impedisce errori di inserimento
5. **Flessibilità**: Permette di specificare o meno i dettagli monete/banconote
6. **Sicurezza**: Solo movimenti approvati influenzano il saldo

## Utilizzo

1. **Dipendente**: Inserisce movimenti specificando opzionalmente monete/banconote
2. **Admin**: Approva movimenti e monitora il saldo monete
3. **Sistema**: Calcola automaticamente il saldo e mostra indicatori
4. **Alert**: Badge rosso quando le monete scendono sotto €50

Questa implementazione risolve completamente la richiesta dell'utente per il monitoraggio delle monete nella cassaforte, fornendo un sistema robusto e intuitivo per tracciare separatamente monete e banconote. 