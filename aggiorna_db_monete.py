#!/usr/bin/env python3
"""
Script per aggiornare il database con i nuovi campi per il monitoraggio delle monete
"""

from app import app, db, User, Cassaforte
from datetime import datetime, date
from werkzeug.security import generate_password_hash

def aggiorna_database_monete():
    """Aggiorna il database con i nuovi campi per le monete"""
    with app.app_context():
        print("🔄 Aggiornamento database con campi monete...")
        
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
        
        # Crea alcuni movimenti cassaforte di test con monete
        movimenti_test = [
            {
                'data': date(2024, 1, 15),
                'operatore_id': 2,  # dipendente
                'tipo_movimento': 'entrata',
                'importo': 500.0,
                'monete_importo': 100.0,
                'banconote_importo': 400.0,
                'descrizione': 'Versamento incassi giornalieri',
                'approvato': True,
                'approvato_da': 'admin',
                'approvato_il': datetime.now()
            },
            {
                'data': date(2024, 1, 16),
                'operatore_id': 2,  # dipendente
                'tipo_movimento': 'uscita',
                'importo': 200.0,
                'monete_importo': 50.0,
                'banconote_importo': 150.0,
                'descrizione': 'Prelievo per fondo cassa',
                'approvato': True,
                'approvato_da': 'admin',
                'approvato_il': datetime.now()
            },
            {
                'data': date(2024, 1, 17),
                'operatore_id': 2,  # dipendente
                'tipo_movimento': 'entrata',
                'importo': 300.0,
                'monete_importo': 0.0,
                'banconote_importo': 300.0,
                'descrizione': 'Versamento solo banconote',
                'approvato': True,
                'approvato_da': 'admin',
                'approvato_il': datetime.now()
            },
            {
                'data': date(2024, 1, 18),
                'operatore_id': 2,  # dipendente
                'tipo_movimento': 'uscita',
                'importo': 150.0,
                'monete_importo': 100.0,
                'banconote_importo': 50.0,
                'descrizione': 'Prelievo con più monete che banconote',
                'approvato': False,
                'approvato_da': None,
                'approvato_il': None
            },
            {
                'data': date(2024, 1, 19),
                'operatore_id': 2,  # dipendente
                'tipo_movimento': 'entrata',
                'importo': 80.0,
                'monete_importo': 80.0,
                'banconote_importo': 0.0,
                'descrizione': 'Versamento solo monete',
                'approvato': True,
                'approvato_da': 'admin',
                'approvato_il': datetime.now()
            }
        ]
        
        for movimento_data in movimenti_test:
            movimento = Cassaforte(**movimento_data)
            db.session.add(movimento)
        
        db.session.commit()
        print("✅ Movimenti cassaforte di test con monete creati")
        
        # Calcola e mostra il saldo delle monete
        saldo_monete = 0.0
        for movimento in Cassaforte.query.filter_by(approvato=True).all():
            if movimento.tipo_movimento == 'entrata':
                saldo_monete += movimento.monete_importo
            else:  # uscita
                saldo_monete -= movimento.monete_importo
        
        print(f"💰 Saldo monete attuale: €{saldo_monete:.2f}")
        if saldo_monete < 50:
            print("⚠️  ATTENZIONE: Livello monete sotto il minimo (€50)")
        else:
            print("✅ Livello monete OK")
        
        print("\n🎉 Database aggiornato con successo!")
        print("Nuovi campi aggiunti:")
        print("- monete_importo: Importo in monete")
        print("- banconote_importo: Importo in banconote")
        print("- tipo_movimento: Tipo di movimento (entrata/uscita)")
        print("\nMovimenti di test creati con vari scenari di monete")

if __name__ == "__main__":
    aggiorna_database_monete() 