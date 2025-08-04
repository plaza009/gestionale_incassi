#!/usr/bin/env python3
"""
Script per popolare il database con dati di test per settembre 2025
"""

from app import app, db, User, Incasso, Cassaforte
from datetime import datetime, date, timedelta
from werkzeug.security import generate_password_hash
import random

def popola_database_settembre():
    """Popola il database con dati di test per settembre 2025"""
    with app.app_context():
        print("🔄 Popolamento database con dati settembre 2025...")
        
        # Ricrea tutte le tabelle
        db.drop_all()
        db.create_all()
        
        print("✅ Tabelle ricreate con successo")
        
        # Crea utenti di default
        admin = User(
            username='admin',
            password_hash=generate_password_hash('admin123'),
            nome_completo='Amministratore',
            is_admin=True
        )
        
        dipendente = User(
            username='dipendente',
            password_hash=generate_password_hash('dipendente123'),
            nome_completo='Dipendente Test',
            is_admin=False
        )
        
        db.session.add(admin)
        db.session.add(dipendente)
        db.session.commit()
        
        print("✅ Utenti di default creati")
        
        # Genera dati per settembre 2025 (1-30 settembre)
        settembre_2025 = []
        for giorno in range(1, 31):
            data = date(2025, 9, giorno)
            settembre_2025.append(data)
        
        # Incassi di test per settembre 2025
        incassi_settembre = []
        
        for i, data in enumerate(settembre_2025):
            # Varia gli importi per simulare giorni diversi
            base_pos = 800 + random.randint(-200, 300)  # 600-1100
            base_cash = 400 + random.randint(-100, 200)  # 300-600
            base_fondo = 100
            
            # Simula weekend con più affluenza
            if data.weekday() >= 5:  # Sabato e domenica
                base_pos += 200
                base_cash += 100
            
            # Simula giorni speciali (es. 15 settembre)
            if data.day == 15:
                base_pos += 300
                base_cash += 150
            
            incasso = {
                'data': data,
                'operatore_id': 2,  # dipendente
                'fondo_cassa_iniziale': base_fondo,
                'incasso_pos': base_pos,
                'cash_totale_cassa': base_fondo + base_pos + base_cash,
                'cash_scontrinato': base_cash * 0.8,  # 80% scontrinato
                'cash_non_scontrinato': base_cash * 0.2,  # 20% non scontrinato
                'prelievo_importo': random.choice([0, 20, 30, 50]) if random.random() < 0.3 else 0,
                'prelievo_motivo': random.choice(['fuori busta', 'fornitore', 'spese straordinarie']) if random.random() < 0.3 else '',
                'note': f'Incasso giornaliero {data.strftime("%d/%m/%Y")}',
                'approvato': True,
                'approvato_da': 'admin',
                'approvato_il': datetime.now()
            }
            
            incassi_settembre.append(incasso)
        
        # Crea gli incassi
        for incasso_data in incassi_settembre:
            incasso = Incasso(**incasso_data)
            db.session.add(incasso)
        
        print("✅ Incassi settembre 2025 creati")
        
        # Movimenti cassaforte per settembre 2025
        movimenti_settembre = []
        
        # Movimenti di apertura (1 settembre)
        movimenti_settembre.append({
            'data': date(2025, 9, 1),
            'operatore_id': 2,
            'tipo_movimento': 'entrata',
            'importo': 2000.0,
            'monete_importo': 300.0,
            'banconote_importo': 1700.0,
            'descrizione': 'Apertura cassaforte settembre 2025',
            'approvato': True,
            'approvato_da': 'admin',
            'approvato_il': datetime.now()
        })
        
        # Movimenti settimanali
        for settimana in range(1, 5):  # 4 settimane
            # Prelievo fondo cassa settimanale
            movimenti_settembre.append({
                'data': date(2025, 9, 1 + (settimana - 1) * 7),
                'operatore_id': 2,
                'tipo_movimento': 'uscita',
                'importo': 500.0,
                'monete_importo': 100.0,
                'banconote_importo': 400.0,
                'descrizione': f'Prelievo fondo cassa settimana {settimana}',
                'approvato': True,
                'approvato_da': 'admin',
                'approvato_il': datetime.now()
            })
            
            # Versamento incassi settimanali
            movimenti_settembre.append({
                'data': date(2025, 9, 5 + (settimana - 1) * 7),
                'operatore_id': 2,
                'tipo_movimento': 'entrata',
                'importo': 3000.0 + random.randint(-500, 500),
                'monete_importo': 400.0 + random.randint(-100, 100),
                'banconote_importo': 2600.0 + random.randint(-400, 400),
                'descrizione': f'Versamento incassi settimana {settimana}',
                'approvato': True,
                'approvato_da': 'admin',
                'approvato_il': datetime.now()
            })
        
        # Movimenti extra
        movimenti_settembre.extend([
            {
                'data': date(2025, 9, 10),
                'operatore_id': 2,
                'tipo_movimento': 'uscita',
                'importo': 150.0,
                'monete_importo': 50.0,
                'banconote_importo': 100.0,
                'descrizione': 'Prelievo per spese straordinarie',
                'approvato': True,
                'approvato_da': 'admin',
                'approvato_il': datetime.now()
            },
            {
                'data': date(2025, 9, 20),
                'operatore_id': 2,
                'tipo_movimento': 'entrata',
                'importo': 800.0,
                'monete_importo': 200.0,
                'banconote_importo': 600.0,
                'descrizione': 'Versamento extra',
                'approvato': True,
                'approvato_da': 'admin',
                'approvato_il': datetime.now()
            },
            {
                'data': date(2025, 9, 25),
                'operatore_id': 2,
                'tipo_movimento': 'uscita',
                'importo': 300.0,
                'monete_importo': 100.0,
                'banconote_importo': 200.0,
                'descrizione': 'Prelievo per fornitore',
                'approvato': False,
                'approvato_da': None,
                'approvato_il': None
            }
        ])
        
        # Crea i movimenti
        for movimento_data in movimenti_settembre:
            movimento = Cassaforte(**movimento_data)
            db.session.add(movimento)
        
        db.session.commit()
        print("✅ Movimenti cassaforte settembre 2025 creati")
        
        # Calcola statistiche
        incassi_totali = len(incassi_settembre)
        movimenti_totali = len(movimenti_settembre)
        
        # Calcola saldo monete
        saldo_monete = 0.0
        for movimento in Cassaforte.query.filter_by(approvato=True).all():
            if movimento.tipo_movimento == 'entrata':
                saldo_monete += movimento.monete_importo
            else:  # uscita
                saldo_monete -= movimento.monete_importo
        
        print(f"\n📊 Statistiche settembre 2025:")
        print(f"  • Incassi creati: {incassi_totali}")
        print(f"  • Movimenti cassaforte: {movimenti_totali}")
        print(f"  • Saldo monete attuale: €{saldo_monete:.2f}")
        
        if saldo_monete < 50:
            print("  ⚠️  ATTENZIONE: Livello monete sotto il minimo (€50)")
        else:
            print("  ✅ Livello monete OK")
        
        print("\n🎉 Database popolato con successo!")
        print("Dati di test per settembre 2025 creati")
        print("Pronto per il testing del sistema")

if __name__ == "__main__":
    popola_database_settembre() 