#!/usr/bin/env python3
"""
Script per creare incassi di test con anomalie
"""

from app import app, db, Incasso, User
from werkzeug.security import generate_password_hash
from datetime import datetime, date
import random

def crea_incassi_test():
    """Crea incassi di test con varie anomalie"""
    
    with app.app_context():
        # Assicurati che esistano gli utenti
        admin = User.query.filter_by(username='admin').first()
        if not admin:
            admin = User(
                username='admin',
                password_hash=generate_password_hash('admin123'),
                is_admin=True,
                nome_completo='Amministratore Sistema',
                created_at=datetime.utcnow()
            )
            db.session.add(admin)
        
        dipendente = User.query.filter_by(username='dipendente').first()
        if not dipendente:
            dipendente = User(
                username='dipendente',
                password_hash=generate_password_hash('dipendente123'),
                is_admin=False,
                nome_completo='Dipendente Test',
                created_at=datetime.utcnow()
            )
            db.session.add(dipendente)
        
        db.session.commit()
        
        # Elimina incassi esistenti per evitare duplicati
        Incasso.query.delete()
        
        # Incasso 1: Normale (nessuna anomalia)
        incasso1 = Incasso(
            operatore_id=dipendente.id,
            data=date.today(),
            fondo_cassa_iniziale=100.0,
            incasso_pos=150.0,
            cash_totale_cassa=250.0,
            cash_scontrinato=140.0,
            cash_non_scontrinato=10.0,
            note='Incasso normale - nessuna anomalia',
            approvato=False
        )
        db.session.add(incasso1)
        
        # Incasso 2: Discrepanza cash
        incasso2 = Incasso(
            operatore_id=dipendente.id,
            data=date.today(),
            fondo_cassa_iniziale=100.0,
            incasso_pos=200.0,
            cash_totale_cassa=300.0,
            cash_scontrinato=180.0,
            cash_non_scontrinato=10.0,
            note='Incasso con discrepanza cash (dovrebbe essere 190 dichiarato)',
            approvato=False
        )
        db.session.add(incasso2)
        
        # Incasso 3: Fondo cassa negativo
        incasso3 = Incasso(
            operatore_id=dipendente.id,
            data=date.today(),
            fondo_cassa_iniziale=-50.0,
            incasso_pos=100.0,
            cash_totale_cassa=50.0,
            cash_scontrinato=0.0,
            cash_non_scontrinato=0.0,
            note='Incasso con fondo cassa negativo',
            approvato=True,
            approvato_da=admin.id,
            approvato_il=datetime.utcnow()
        )
        db.session.add(incasso3)
        
        # Incasso 4: POS zero
        incasso4 = Incasso(
            operatore_id=dipendente.id,
            data=date.today(),
            incasso_pos=0.0,
            fondo_cassa_iniziale=100.0,
            cash_totale_cassa=100.0,
            cash_scontrinato=0.0,
            cash_non_scontrinato=0.0,
            note='Incasso con POS zero',
            approvato=False
        )
        db.session.add(incasso4)
        
        # Incasso 5: Cash totale negativo
        incasso5 = Incasso(
            operatore_id=dipendente.id,
            data=date.today(),
            fondo_cassa_iniziale=100.0,
            incasso_pos=50.0,
            cash_totale_cassa=-20.0,
            cash_scontrinato=0.0,
            cash_non_scontrinato=0.0,
            note='Incasso con cash totale negativo',
            approvato=False
        )
        db.session.add(incasso5)
        
        # Incasso 6: Multipla anomalie
        incasso6 = Incasso(
            operatore_id=dipendente.id,
            data=date.today(),
            fondo_cassa_iniziale=-100.0,
            incasso_pos=-50.0,
            cash_totale_cassa=-150.0,
            cash_scontrinato=0.0,
            cash_non_scontrinato=0.0,
            note='Incasso con multiple anomalie (tutti valori negativi)',
            approvato=False
        )
        db.session.add(incasso6)
        
        db.session.commit()
        
        print("✅ Incassi di test creati con successo!")
        print("\n📋 Incassi creati:")
        print("1. Incasso normale (nessuna anomalia)")
        print("2. Incasso con discrepanza cash")
        print("3. Incasso con fondo cassa negativo (approvato)")
        print("4. Incasso con POS zero")
        print("5. Incasso con cash totale negativo")
        print("6. Incasso con multiple anomalie")
        print("\n🔍 Ora puoi testare le funzionalità di rilevamento anomalie!")

if __name__ == '__main__':
    crea_incassi_test() 