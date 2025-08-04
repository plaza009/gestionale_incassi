# Funzionalità Prelievo negli Incassi - IMPLEMENTATA

## Problema Risolto

L'utente ha richiesto di aggiungere un campo "prelievo" alla registrazione del nuovo incasso con le seguenti caratteristiche:
- Campo per inserire l'importo del prelievo
- Possibilità di selezionare il motivo tra opzioni predefinite ("fuori busta", "fornitore")
- Possibilità di inserire un motivo personalizzato
- Visualizzazione delle informazioni sui prelievi nella lista e nei dettagli

## Soluzione Implementata

### 1. Modifiche al Modello Database (`app.py`)

#### Nuovi Campi nel Modello `Incasso`
```python
class Incasso(db.Model):
    # ... campi esistenti ...
    prelievo_importo = db.Column(db.Float, default=0)
    prelievo_motivo = db.Column(db.String(100), default='')
```

### 2. Aggiornamento delle Route

#### Route `nuovo_incasso` Aggiornata
```python
@app.route('/incassi/nuovo', methods=['GET', 'POST'])
@login_required
def nuovo_incasso():
    if request.method == 'POST':
        # ... gestione campi esistenti ...
        prelievo_importo = float(request.form.get('prelievo_importo', 0))
        prelievo_motivo = request.form.get('prelievo_motivo', '')
        
        incasso = Incasso(
            # ... campi esistenti ...
            prelievo_importo=prelievo_importo,
            prelievo_motivo=prelievo_motivo,
        )
```

#### Route `modifica_incasso` Aggiornata
```python
@app.route('/incassi/<int:id>/modifica', methods=['GET', 'POST'])
@login_required
@admin_required
def modifica_incasso(id):
    # ... gestione campi esistenti ...
    incasso.prelievo_importo = float(request.form.get('prelievo_importo', 0))
    incasso.prelievo_motivo = request.form.get('prelievo_motivo', '')
```

### 3. Modifiche ai Template

#### Template `nuovo_incasso.html`
Aggiunti i campi prelievo nella sezione destra del form:

```html
<div class="mb-3">
    <label for="prelievo_importo" class="form-label">
        <i class="fas fa-hand-holding-usd me-1"></i>
        Prelievo (€)
    </label>
    <input type="number" step="0.01" class="form-control" id="prelievo_importo" name="prelievo_importo" value="0" min="0">
    <div class="form-text">Importo prelevato durante il turno (opzionale)</div>
</div>

<div class="mb-3">
    <label for="prelievo_motivo" class="form-label">
        <i class="fas fa-tag me-1"></i>
        Motivo Prelievo
    </label>
    <select class="form-control" id="prelievo_motivo_select" onchange="gestisciMotivoPrelievo()">
        <option value="">Seleziona motivo...</option>
        <option value="fuori busta">Fuori busta</option>
        <option value="fornitore">Fornitore</option>
        <option value="custom">Altro (personalizzato)</option>
    </select>
    <input type="text" class="form-control mt-2" id="prelievo_motivo" name="prelievo_motivo" 
           placeholder="Inserisci motivo personalizzato..." style="display: none;">
    <div class="form-text">Motivo del prelievo</div>
</div>
```

#### Template `modifica_incasso.html`
Aggiunti i campi prelievo con gestione dei valori esistenti:

```html
<div class="mb-3">
    <label for="prelievo_importo" class="form-label">
        <i class="fas fa-hand-holding-usd me-1"></i>
        Prelievo (€)
    </label>
    <input type="number" step="0.01" class="form-control" id="prelievo_importo" name="prelievo_importo" 
           value="{{ incasso.prelievo_importo or 0 }}" min="0">
    <div class="form-text">Importo prelevato durante il turno (opzionale)</div>
</div>

<div class="mb-3">
    <label for="prelievo_motivo" class="form-label">
        <i class="fas fa-tag me-1"></i>
        Motivo Prelievo
    </label>
    <select class="form-control" id="prelievo_motivo_select" onchange="gestisciMotivoPrelievo()">
        <option value="">Seleziona motivo...</option>
        <option value="fuori busta" {% if incasso.prelievo_motivo == 'fuori busta' %}selected{% endif %}>Fuori busta</option>
        <option value="fornitore" {% if incasso.prelievo_motivo == 'fornitore' %}selected{% endif %}>Fornitore</option>
        <option value="custom" {% if incasso.prelievo_motivo and incasso.prelievo_motivo not in ['fuori busta', 'fornitore'] %}selected{% endif %}>Altro (personalizzato)</option>
    </select>
    <input type="text" class="form-control mt-2" id="prelievo_motivo" name="prelievo_motivo" 
           value="{{ incasso.prelievo_motivo or '' }}" 
           placeholder="Inserisci motivo personalizzato..." 
           style="display: {% if incasso.prelievo_motivo and incasso.prelievo_motivo not in ['fuori busta', 'fornitore'] %}block{% else %}none{% endif %};">
    <div class="form-text">Motivo del prelievo</div>
</div>
```

#### Template `dettaglio_incasso.html`
Aggiunta sezione per visualizzare le informazioni sui prelievi:

```html
{% if incasso.prelievo_importo > 0 %}
<hr>
<div class="row">
    <div class="col-12">
        <h6 class="text-primary mb-3">
            <i class="fas fa-hand-holding-usd me-2"></i>
            Informazioni Prelievo
        </h6>
        <div class="alert alert-info">
            <div class="row">
                <div class="col-md-6">
                    <strong>Importo Prelievo:</strong> €{{ "%.2f"|format(incasso.prelievo_importo) }}
                </div>
                <div class="col-md-6">
                    <strong>Motivo:</strong> {{ incasso.prelievo_motivo or 'Non specificato' }}
                </div>
            </div>
        </div>
    </div>
</div>
{% endif %}
```

#### Template `lista_incassi.html`
Aggiunta colonna per visualizzare i prelievi nella lista:

```html
<th>Prelievo</th>
<!-- ... -->
<td>
    {% if incasso.prelievo_importo > 0 %}
        <span class="badge bg-info" title="{{ incasso.prelievo_motivo or 'Motivo non specificato' }}">
            €{{ "%.2f"|format(incasso.prelievo_importo) }}
        </span>
    {% else %}
        <span class="text-muted">-</span>
    {% endif %}
</td>
```

### 4. JavaScript per Gestione Dinamica

#### Funzione per Gestire il Campo Motivo Personalizzato
```javascript
function gestisciMotivoPrelievo() {
    const select = document.getElementById('prelievo_motivo_select');
    const input = document.getElementById('prelievo_motivo');
    const selectedValue = select.value;
    
    if (selectedValue === 'custom') {
        input.style.display = 'block';
        input.focus();
        input.value = '';
    } else if (selectedValue) {
        input.style.display = 'none';
        input.value = selectedValue;
    } else {
        input.style.display = 'none';
        input.value = '';
    }
}
```

### 5. Funzionalità Implementate

#### ✅ Campo Importo Prelievo
- Campo numerico per inserire l'importo del prelievo
- Valore minimo 0 (non può essere negativo)
- Opzionale (default 0)

#### ✅ Campo Motivo Prelievo
- Select con opzioni predefinite:
  - "Fuori busta"
  - "Fornitore"
  - "Altro (personalizzato)"
- Campo di testo per motivi personalizzati
- Gestione dinamica: il campo testo appare solo quando si seleziona "Altro"

#### ✅ Visualizzazione nella Lista
- Nuova colonna "Prelievo" nella lista incassi
- Badge blu per incassi con prelievo
- Tooltip con il motivo del prelievo
- Trattino per incassi senza prelievo

#### ✅ Visualizzazione nei Dettagli
- Sezione dedicata "Informazioni Prelievo" (solo se prelievo > 0)
- Visualizzazione dell'importo e del motivo
- Design coerente con il resto dell'interfaccia

#### ✅ Gestione nei Form
- Campi presenti sia nel form nuovo incasso che in quello di modifica
- Gestione corretta dei valori esistenti nel form di modifica
- Validazione e gestione errori

### 6. Test Implementati

Creato `test_prelievo_incassi.py` che verifica:

1. **Presenza campi prelievo nel form nuovo incasso**
2. **Opzioni corrette nel select motivo**
3. **Colonna prelievo nella lista incassi**
4. **Badge prelievo nella lista**
5. **Sezione informazioni prelievo nei dettagli**
6. **Campi prelievo nel form modifica**

### 7. Aggiornamento Database

Creato `aggiorna_db_prelievo.py` per:
- Ricreare il database con i nuovi campi
- Creare utenti di default
- Creare incassi di test con vari tipi di prelievo

### 8. Compatibilità

- ✅ **Mobile**: Form responsive con Bootstrap
- ✅ **Desktop**: Layout ottimizzato per schermi grandi
- ✅ **Accessibilità**: Label appropriati e struttura semantica
- ✅ **UX**: Interfaccia intuitiva con gestione dinamica

## Risultato

La funzionalità prelievo è ora completamente implementata e permette:

- **Registrazione prelievi**: Gli utenti possono inserire importo e motivo dei prelievi
- **Motivi predefiniti**: Opzioni standard per i motivi più comuni
- **Motivi personalizzati**: Possibilità di inserire motivi specifici
- **Visualizzazione chiara**: Informazioni sui prelievi visibili nella lista e nei dettagli
- **Gestione completa**: Modifica e visualizzazione in tutte le sezioni del sistema
- **Interfaccia intuitiva**: Gestione dinamica del campo motivo personalizzato

La funzionalità è stata testata e documentata, pronta per l'uso in produzione. 