#!/usr/bin/env python3
"""
Script per inizializzare il database su Render
Esegui questo script una volta dopo il deployment per creare le tabelle
"""
from app import app, db, User
from werkzeug.security import generate_password_hash

def init_database():
    """Inizializza il database con tabelle e utenti di base"""
    
    print("🔧 Inizializzazione Database")
    print("=" * 40)
    
    with app.app_context():
        try:
            # Crea tutte le tabelle
            db.create_all()
            print("✅ Tabelle create con successo")
            
            # Crea utente admin se non esiste
            admin = User.query.filter_by(username='admin').first()
            if not admin:
                admin = User(
                    username='admin',
                    password_hash=generate_password_hash('admin123'),
                    is_admin=True,
                    nome_completo='Amministratore Sistema'
                )
                db.session.add(admin)
                db.session.commit()
                print("✅ Utente admin creato: username='admin', password='admin123'")
            else:
                print("ℹ️  Utente admin già esistente")
            
            # Crea utente dipendente se non esiste
            dipendente = User.query.filter_by(username='dipendente').first()
            if not dipendente:
                dipendente = User(
                    username='dipendente',
                    password_hash=generate_password_hash('dipendente123'),
                    is_admin=False,
                    nome_completo='Dipendente Sistema'
                )
                db.session.add(dipendente)
                db.session.commit()
                print("✅ Utente dipendente creato: username='dipendente', password='dipendente123'")
            else:
                print("ℹ️  Utente dipendente già esistente")
            
            print("\n🎉 Database inizializzato con successo!")
            print("Puoi ora accedere con:")
            print("  - Admin: admin / admin123")
            print("  - Dipendente: dipendente / dipendente123")
            
        except Exception as e:
            print(f"❌ Errore durante l'inizializzazione: {e}")
            return False
    
    return True

if __name__ == "__main__":
    init_database() 