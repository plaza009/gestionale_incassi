#!/usr/bin/env python3
"""
Script per inizializzare il database in produzione
"""

from app import app, db, User
from werkzeug.security import generate_password_hash
from datetime import datetime

def init_database():
    with app.app_context():
        # Crea tutte le tabelle
        db.create_all()
        
        # Controlla se esiste già un admin
        admin = User.query.filter_by(username='admin').first()
        if not admin:
            # Crea l'utente admin
            admin = User(
                username='admin',
                password_hash=generate_password_hash('admin123'),
                is_admin=True,
                nome_completo='Amministratore Sistema',
                created_at=datetime.utcnow()
            )
            db.session.add(admin)
            
            # Crea un utente dipendente di esempio
            dipendente = User(
                username='dipendente',
                password_hash=generate_password_hash('dipendente123'),
                is_admin=False,
                nome_completo='Dipendente Esempio',
                created_at=datetime.utcnow()
            )
            db.session.add(dipendente)
            
            db.session.commit()
            print("Database inizializzato con successo!")
            print("Utenti creati:")
            print("- Admin: admin/admin123")
            print("- Dipendente: dipendente/dipendente123")
        else:
            print("Database già inizializzato!")

if __name__ == '__main__':
    init_database() 