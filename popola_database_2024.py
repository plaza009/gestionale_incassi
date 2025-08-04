#!/usr/bin/env python3
"""
Script per popolare il database con dati fittizzi ma realistici per tutto il 2024
"""
import sys
import os
from datetime import datetime, date, timedelta
import random
from decimal import Decimal

# Aggiungi il percorso del progetto al path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app import app, db, User, Incasso, Cassaforte

def genera_dati_realistici():
    """Genera dati fittizzi ma realistici per il 2024"""
    
    # Assicurati che l'app sia nel contesto corretto
    with app.app_context():
        
        # Verifica che esistano gli utenti
        admin = User.query.filter_by(username='admin').first()
        dipendente = User.query.filter_by(username='dipendente').first()
        
        if not admin or not dipendente:
            print("❌ Errore: Utenti admin e dipendente non trovati nel database")
            print("Assicurati di aver eseguito la creazione degli utenti")
            return False
        
        print("🎯 Inizio popolamento database 2024...")
        print("=" * 50)
        
        # Parametri per dati realistici
        mesi_stagionali = {
            1: {'fatturato_basso': True, 'nome': 'Gennaio'},
            2: {'fatturato_basso': True, 'nome': 'Febbraio'},
            3: {'fatturato_basso': False, 'nome': 'Marzo'},
            4: {'fatturato_basso': False, 'nome': 'Aprile'},
            5: {'fatturato_basso': False, 'nome': 'Maggio'},
            6: {'fatturato_basso': False, 'nome': 'Giugno'},
            7: {'fatturato_basso': True, 'nome': 'Luglio'},
            8: {'fatturato_basso': True, 'nome': 'Agosto'},
            9: {'fatturato_basso': False, 'nome': 'Settembre'},
            10: {'fatturato_basso': False, 'nome': 'Ottobre'},
            11: {'fatturato_basso': False, 'nome': 'Novembre'},
            12: {'fatturato_basso': False, 'nome': 'Dicembre'}
        }
        
        # Giorni della settimana con fatturato diverso
        giorni_settimana = {
            0: {'nome': 'Lunedì', 'fatturato_basso': True},
            1: {'nome': 'Martedì', 'fatturato_basso': False},
            2: {'nome': 'Mercoledì', 'fatturato_basso': False},
            3: {'nome': 'Giovedì', 'fatturato_basso': False},
            4: {'nome': 'Venerdì', 'fatturato_basso': True},
            5: {'nome': 'Sabato', 'fatturato_basso': True},
            6: {'nome': 'Domenica', 'fatturato_basso': True}
        }
        
        # Motivi prelievo realistici
        motivi_prelievo = [
            "Pagamento fornitori",
            "Spese straordinarie",
            "Manutenzione locale",
            "Acquisto materiali",
            "Spese pulizia",
            "Pagamento utenze",
            "Spese marketing",
            "Riparazioni urgenti"
        ]
        
        # Note realistiche per incassi
        note_incassi = [
            "Giornata normale",
            "Evento speciale",
            "Promozione attiva",
            "Giornata festiva",
            "Cliente importante",
            "Giornata tranquilla",
            "Molti clienti",
            "Pochi clienti"
        ]
        
        # Note realistiche per cassaforte
        note_cassaforte = [
            "Controllo giornaliero",
            "Rifornimento cassa",
            "Prelievo per spese",
            "Deposito in banca",
            "Controllo sicurezza",
            "Movimento straordinario",
            "Rifornimento monete",
            "Prelievo urgente"
        ]
        
        # Contatori
        incassi_creati = 0
        movimenti_creati = 0
        prelievi_creati = 0
        
        # Genera dati per ogni giorno del 2024
        data_inizio = date(2024, 1, 1)
        data_fine = date(2024, 12, 31)
        data_corrente = data_inizio
        
        while data_corrente <= data_fine:
            
            # Determina il mese e il giorno della settimana
            mese = data_corrente.month
            giorno_settimana = data_corrente.weekday()
            
            # Determina se è un giorno lavorativo (escludi domeniche e alcuni sabati)
            is_lavorativo = giorno_settimana != 6 and not (giorno_settimana == 5 and random.random() < 0.3)
            
            if is_lavorativo:
                
                # Genera 1-3 incassi al giorno (più probabile nei weekend)
                num_incassi = random.randint(1, 3) if giorno_settimana in [4, 5] else random.randint(1, 2)
                
                for _ in range(num_incassi):
                    
                    # Determina l'operatore (più probabile dipendente)
                    operatore = dipendente if random.random() < 0.8 else admin
                    
                    # Calcola fatturato base in base a stagionalità e giorno
                    base_fatturato = 800 if mesi_stagionali[mese]['fatturato_basso'] else 1200
                    base_fatturato = base_fatturato * 0.7 if giorni_settimana[giorno_settimana]['fatturato_basso'] else base_fatturato
                    
                    # Aggiungi variabilità
                    fatturato_pos = base_fatturato * random.uniform(0.6, 1.4)
                    fatturato_cash = base_fatturato * random.uniform(0.3, 0.8)
                    
                    # Arrotonda a 2 decimali
                    incasso_pos = round(fatturato_pos, 2)
                    cash_totale = round(fatturato_cash + random.uniform(50, 200), 2)
                    fondo_cassa = round(random.uniform(50, 150), 2)
                    
                    # Calcola cash effettivo
                    cash_effettivo = cash_totale - fondo_cassa
                    
                    # Determina se c'è un prelievo (20% di probabilità)
                    has_prelievo = random.random() < 0.2
                    prelievo_importo = 0
                    prelievo_motivo = None
                    
                    if has_prelievo:
                        prelievo_importo = round(random.uniform(50, min(cash_effettivo * 0.3, 300)), 2)
                        prelievo_motivo = random.choice(motivi_prelievo)
                        prelievi_creati += 1
                    
                    # Calcola cash scontrinato e non scontrinato
                    cash_scontrinato = round(cash_effettivo * random.uniform(0.6, 0.9), 2)
                    cash_non_scontrinato = round(cash_effettivo - cash_scontrinato, 2)
                    
                    # Determina approvazione (più probabile per admin, meno per dipendente)
                    approvato = random.random() < 0.9 if operatore == admin else random.random() < 0.3
                    
                    # Crea l'incasso
                    incasso = Incasso(
                        data=data_corrente,
                        operatore_id=operatore.id,
                        fondo_cassa_iniziale=fondo_cassa,
                        incasso_pos=incasso_pos,
                        cash_totale_cassa=cash_totale,
                        cash_scontrinato=cash_scontrinato,
                        cash_non_scontrinato=cash_non_scontrinato,
                        prelievo_importo=prelievo_importo,
                        prelievo_motivo=prelievo_motivo,
                        note=random.choice(note_incassi),
                        approvato=approvato
                    )
                    
                    db.session.add(incasso)
                    incassi_creati += 1
                
                # Genera 1-2 movimenti cassaforte al giorno
                num_movimenti = random.randint(1, 2)
                
                for _ in range(num_movimenti):
                    
                    # Determina tipo movimento (più probabile entrata)
                    tipo_movimento = 'entrata' if random.random() < 0.7 else 'uscita'
                    
                    # Calcola importo realistico
                    if tipo_movimento == 'entrata':
                        importo = round(random.uniform(100, 500), 2)
                    else:
                        importo = round(random.uniform(50, 300), 2)
                    
                    # Determina operatore
                    operatore_mov = dipendente if random.random() < 0.8 else admin
                    
                    # Crea il movimento
                    movimento = Cassaforte(
                        data=data_corrente,
                        operatore_id=operatore_mov.id,
                        tipo_movimento=tipo_movimento,
                        importo=importo,
                        descrizione=random.choice(note_cassaforte)
                    )
                    
                    db.session.add(movimento)
                    movimenti_creati += 1
            
            # Passa al giorno successivo
            data_corrente += timedelta(days=1)
            
            # Mostra progresso ogni 30 giorni
            if (data_corrente - data_inizio).days % 30 == 0:
                print(f"📅 Processati {(data_corrente - data_inizio).days} giorni...")
        
        # Commit delle modifiche
        try:
            db.session.commit()
            print("✅ Commit al database completato con successo")
        except Exception as e:
            print(f"❌ Errore durante il commit: {e}")
            db.session.rollback()
            return False
        
        # Statistiche finali
        print("\n📊 Statistiche popolamento database 2024:")
        print("=" * 50)
        print(f"📈 Incassi creati: {incassi_creati}")
        print(f"💰 Movimenti cassaforte creati: {movimenti_creati}")
        print(f"💸 Prelievi creati: {prelievi_creati}")
        print(f"📅 Periodo: 01/01/2024 - 31/12/2024")
        print(f"👥 Operatori utilizzati: admin, dipendente")
        
        # Verifica dati inseriti
        incassi_totali = Incasso.query.filter(
            Incasso.data >= date(2024, 1, 1),
            Incasso.data <= date(2024, 12, 31)
        ).count()
        
        movimenti_totali = Cassaforte.query.filter(
            Cassaforte.data >= date(2024, 1, 1),
            Cassaforte.data <= date(2024, 12, 31)
        ).count()
        
        print(f"\n✅ Verifica finale:")
        print(f"   📈 Incassi nel database: {incassi_totali}")
        print(f"   💰 Movimenti nel database: {movimenti_totali}")
        
        if incassi_totali == incassi_creati and movimenti_totali == movimenti_creati:
            print("🎉 Popolamento database completato con successo!")
            return True
        else:
            print("⚠️  Discrepanza nei dati inseriti")
            return False

if __name__ == "__main__":
    try:
        success = genera_dati_realistici()
        if success:
            print("\n🚀 Database pronto per i test!")
            print("💡 Ricorda di pulire i dati prima del deployment in produzione")
            sys.exit(0)
        else:
            print("\n❌ Errore durante il popolamento del database")
            sys.exit(1)
    except Exception as e:
        print(f"❌ Errore durante l'esecuzione: {e}")
        sys.exit(1) 