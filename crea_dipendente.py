#!/usr/bin/env python3
"""
Script per creare un utente dipendente di esempio
"""

from app import app, db, User
from werkzeug.security import generate_password_hash

def crea_dipendente():
    with app.app_context():
        # Verifica se il dipendente esiste già
        dipendente = User.query.filter_by(username='dipendente').first()
        if not dipendente:
            dipendente = User(
                username='dipendente',
                password_hash=generate_password_hash('dipendente123'),
                is_admin=False,
                nome_completo='Mario Rossi'
            )
            db.session.add(dipendente)
            db.session.commit()
            print("✅ Utente dipendente creato con successo!")
            print("   Username: dipendente")
            print("   Password: dipendente123")
            print("   Nome: Mario Rossi")
            print("   Ruolo: Dipendente")
        else:
            print("⚠️  L'utente dipendente esiste già")
            print("   Username: dipendente")
            print("   Password: dipendente123")

if __name__ == '__main__':
    crea_dipendente() 