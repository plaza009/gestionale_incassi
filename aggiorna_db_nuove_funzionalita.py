#!/usr/bin/env python3
"""
Script per aggiornare il database con le nuove funzionalità della cassaforte:
1. Visualizzazione dei 3 saldi distinti
2. Campo nota per i dipendenti
"""
from app import app, db, User, Cassaforte
from datetime import datetime, date
from werkzeug.security import generate_password_hash

def aggiorna_database_nuove_funzionalita():
    """Aggiorna il database con le nuove funzionalità"""
    with app.app_context():
        print("🔄 Aggiornamento database con nuove funzionalità cassaforte...")
        
        # Ricrea le tabelle per assicurarsi che tutti i campi siano presenti
        db.drop_all()
        db.create_all()
        print("✅ Tabelle ricreate con successo")
        
        # Crea utenti di default
        admin = User(username='admin', password_hash=generate_password_hash('admin123'), 
                    nome_completo='Amministratore', is_admin=True)
        dipendente = User(username='dipendente', password_hash=generate_password_hash('dipendente123'), 
                         nome_completo='Dipendente Test', is_admin=False)
        db.session.add(admin)
        db.session.add(dipendente)
        db.session.commit()
        print("✅ Utenti di default creati")
        
        # Crea movimenti cassaforte di test con note
        movimenti_test = [
            {
                'data': date(2024, 1, 15), 'operatore_id': 2, 'tipo_movimento': 'entrata',
                'importo': 500.0, 'monete_importo': 100.0, 'banconote_importo': 400.0,
                'descrizione': 'Versamento incassi giornalieri - Note: Controllo serale completato',
                'approvato': True, 'approvato_da': 'admin', 'approvato_il': datetime.now()
            },
            {
                'data': date(2024, 1, 16), 'operatore_id': 2, 'tipo_movimento': 'uscita',
                'importo': 200.0, 'monete_importo': 50.0, 'banconote_importo': 150.0,
                'descrizione': 'Prelievo per fondo cassa - Note: Necessario per apertura mattina',
                'approvato': True, 'approvato_da': 'admin', 'approvato_il': datetime.now()
            },
            {
                'data': date(2024, 1, 17), 'operatore_id': 2, 'tipo_movimento': 'entrata',
                'importo': 300.0, 'monete_importo': 0.0, 'banconote_importo': 300.0,
                'descrizione': 'Versamento solo banconote - Note: Giornata con poco resto',
                'approvato': True, 'approvato_da': 'admin', 'approvato_il': datetime.now()
            },
            {
                'data': date(2024, 1, 18), 'operatore_id': 2, 'tipo_movimento': 'uscita',
                'importo': 150.0, 'monete_importo': 100.0, 'banconote_importo': 50.0,
                'descrizione': 'Prelievo con più monete che banconote - Note: Scorte monete esaurite',
                'approvato': False, 'approvato_da': None, 'approvato_il': None
            },
            {
                'data': date(2024, 1, 19), 'operatore_id': 2, 'tipo_movimento': 'entrata',
                'importo': 80.0, 'monete_importo': 80.0, 'banconote_importo': 0.0,
                'descrizione': 'Versamento solo monete - Note: Raccolta monete da distributori',
                'approvato': True, 'approvato_da': 'admin', 'approvato_il': datetime.now()
            },
            {
                'data': date(2024, 1, 20), 'operatore_id': 2, 'tipo_movimento': 'entrata',
                'importo': 1200.0, 'monete_importo': 200.0, 'banconote_importo': 1000.0,
                'descrizione': 'Versamento incassi weekend - Note: Sabato sera molto affollato',
                'approvato': True, 'approvato_da': 'admin', 'approvato_il': datetime.now()
            },
            {
                'data': date(2024, 1, 21), 'operatore_id': 2, 'tipo_movimento': 'uscita',
                'importo': 300.0, 'monete_importo': 0.0, 'banconote_importo': 300.0,
                'descrizione': 'Prelievo per spese straordinarie - Note: Acquisto materiale pulizia',
                'approvato': True, 'approvato_da': 'admin', 'approvato_il': datetime.now()
            }
        ]
        
        for movimento_data in movimenti_test:
            movimento = Cassaforte(**movimento_data)
            db.session.add(movimento)
        
        db.session.commit()
        print("✅ Movimenti cassaforte di test con note creati")
        
        # Calcola i saldi per verificare le nuove funzionalità
        saldo_monete = 0.0
        saldo_banconote = 0.0
        
        for movimento in Cassaforte.query.filter_by(approvato=True).all():
            if movimento.tipo_movimento == 'entrata':
                saldo_monete += movimento.monete_importo
                saldo_banconote += movimento.banconote_importo
            else:
                saldo_monete -= movimento.monete_importo
                saldo_banconote -= movimento.banconote_importo
        
        totale_cassaforte = saldo_monete + saldo_banconote
        
        print(f"\n💰 Saldi cassaforte:")
        print(f"  • Totale in cassaforte: €{totale_cassaforte:.2f}")
        print(f"  • Monete in cassa: €{saldo_monete:.2f}")
        print(f"  • Importo cash: €{saldo_banconote:.2f}")
        
        if saldo_monete < 50:
            print("  ⚠️  ATTENZIONE: Livello monete sotto il minimo (€50)")
        else:
            print("  ✅ Livello monete OK")
        
        # Conta movimenti con note
        movimenti_con_note = Cassaforte.query.filter(Cassaforte.descrizione.isnot(None)).count()
        print(f"\n📝 Movimenti con note: {movimenti_con_note}/{len(movimenti_test)}")
        
        print("\n🎉 Database aggiornato con successo!")
        print("Nuove funzionalità implementate:")
        print("- Visualizzazione 3 saldi distinti (Totale, Monete, Cash)")
        print("- Campo nota per i dipendenti")
        print("- Colonna nota nella tabella movimenti")
        print("- Dati di test con note esemplificative")

if __name__ == "__main__":
    aggiorna_database_nuove_funzionalita() 