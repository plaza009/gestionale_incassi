#!/usr/bin/env python3
"""
Script per inizializzare il database con la nuova struttura
"""

import os
from app import app, db, User
from werkzeug.security import generate_password_hash

def inizializza_database():
    with app.app_context():
        # Elimina il database esistente se presente
        db_path = 'gestionale_incassi.db'
        if os.path.exists(db_path):
            os.remove(db_path)
            print(f"🗑️  Database esistente eliminato: {db_path}")
        
        # Forza la ricreazione delle tabelle
        db.drop_all()
        db.create_all()
        print("✅ Tabelle create con successo")
        
        # Crea utente admin
        admin = User(
            username='admin',
            password_hash=generate_password_hash('admin123'),
            is_admin=True,
            nome_completo='Amministratore Sistema'
        )
        db.session.add(admin)
        
        # Crea utente dipendente
        dipendente = User(
            username='dipendente',
            password_hash=generate_password_hash('dipendente123'),
            is_admin=False,
            nome_completo='Mario Rossi'
        )
        db.session.add(dipendente)
        
        db.session.commit()
        
        print("✅ Utenti creati con successo!")
        print("\n📋 Credenziali di accesso:")
        print("   👑 Amministratore:")
        print("      Username: admin")
        print("      Password: admin123")
        print("      Ruolo: Amministratore")
        print("\n   👤 Dipendente:")
        print("      Username: dipendente")
        print("      Password: dipendente123")
        print("      Ruolo: Dipendente")
        print("\n🚀 Il sistema è pronto per l'uso!")

if __name__ == '__main__':
    inizializza_database() 