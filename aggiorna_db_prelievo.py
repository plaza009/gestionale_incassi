#!/usr/bin/env python3
"""
Script per aggiornare il database con i nuovi campi prelievo
"""

from app import app, db, User, Incasso
from datetime import datetime, date
from werkzeug.security import generate_password_hash

def aggiorna_database():
    """Aggiorna il database con i nuovi campi prelievo"""
    with app.app_context():
        print("🔄 Aggiornamento database con campi prelievo...")
        
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
        
        # Crea alcuni incassi di test con prelievi
        incassi_test = [
            {
                'data': date(2024, 1, 15),
                'operatore_id': 2,  # dipendente
                'fondo_cassa_iniziale': 100.0,
                'incasso_pos': 150.0,
                'cash_totale_cassa': 250.0,
                'cash_scontrinato': 50.0,
                'cash_non_scontrinato': 0.0,
                'prelievo_importo': 20.0,
                'prelievo_motivo': 'fuori busta',
                'note': 'Test con prelievo fuori busta'
            },
            {
                'data': date(2024, 1, 16),
                'operatore_id': 2,  # dipendente
                'fondo_cassa_iniziale': 100.0,
                'incasso_pos': 200.0,
                'cash_totale_cassa': 300.0,
                'cash_scontrinato': 100.0,
                'cash_non_scontrinato': 0.0,
                'prelievo_importo': 50.0,
                'prelievo_motivo': 'fornitore',
                'note': 'Test con prelievo fornitore'
            },
            {
                'data': date(2024, 1, 17),
                'operatore_id': 2,  # dipendente
                'fondo_cassa_iniziale': 100.0,
                'incasso_pos': 180.0,
                'cash_totale_cassa': 280.0,
                'cash_scontrinato': 80.0,
                'cash_non_scontrinato': 0.0,
                'prelievo_importo': 30.0,
                'prelievo_motivo': 'spese straordinarie',
                'note': 'Test con prelievo personalizzato'
            },
            {
                'data': date(2024, 1, 18),
                'operatore_id': 2,  # dipendente
                'fondo_cassa_iniziale': 100.0,
                'incasso_pos': 120.0,
                'cash_totale_cassa': 220.0,
                'cash_scontrinato': 120.0,
                'cash_non_scontrinato': 0.0,
                'prelievo_importo': 0.0,
                'prelievo_motivo': '',
                'note': 'Test senza prelievo'
            }
        ]
        
        for incasso_data in incassi_test:
            incasso = Incasso(**incasso_data)
            db.session.add(incasso)
        
        db.session.commit()
        print("✅ Incassi di test con prelievi creati")
        
        print("\n🎉 Database aggiornato con successo!")
        print("Nuovi campi aggiunti:")
        print("- prelievo_importo: Importo del prelievo")
        print("- prelievo_motivo: Motivo del prelievo")
        print("\nIncassi di test creati con vari tipi di prelievo")

if __name__ == "__main__":
    aggiorna_database() 