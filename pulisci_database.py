#!/usr/bin/env python3
"""
Script per pulire il database rimuovendo tutti i dati di test
"""
import sys
import os
from datetime import date

# Aggiungi il percorso del progetto al path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app import app, db, User, Incasso, Cassaforte

def pulisci_database():
    """Pulisce il database rimuovendo tutti i dati di test"""
    
    # Assicurati che l'app sia nel contesto corretto
    with app.app_context():
        
        print("🧹 Inizio pulizia database...")
        print("=" * 50)
        
        # Conta i dati prima della pulizia
        incassi_prima = Incasso.query.count()
        movimenti_prima = Cassaforte.query.count()
        utenti_prima = User.query.count()
        
        print(f"📊 Dati presenti prima della pulizia:")
        print(f"   📈 Incassi: {incassi_prima}")
        print(f"   💰 Movimenti cassaforte: {movimenti_prima}")
        print(f"   👥 Utenti: {utenti_prima}")
        
        # Rimuovi tutti gli incassi
        incassi_rimossi = Incasso.query.delete()
        print(f"🗑️  Rimossi {incassi_rimossi} incassi")
        
        # Rimuovi tutti i movimenti cassaforte
        movimenti_rimossi = Cassaforte.query.delete()
        print(f"🗑️  Rimossi {movimenti_rimossi} movimenti cassaforte")
        
        # Mantieni solo gli utenti admin e dipendente
        utenti_da_mantenere = ['admin', 'dipendente']
        utenti_rimossi = 0
        
        for utente in User.query.all():
            if utente.username not in utenti_da_mantenere:
                db.session.delete(utente)
                utenti_rimossi += 1
        
        print(f"🗑️  Rimossi {utenti_rimossi} utenti di test")
        
        # Commit delle modifiche
        try:
            db.session.commit()
            print("✅ Commit al database completato con successo")
        except Exception as e:
            print(f"❌ Errore durante il commit: {e}")
            db.session.rollback()
            return False
        
        # Verifica dati dopo la pulizia
        incassi_dopo = Incasso.query.count()
        movimenti_dopo = Cassaforte.query.count()
        utenti_dopo = User.query.count()
        
        print(f"\n📊 Dati presenti dopo la pulizia:")
        print(f"   📈 Incassi: {incassi_dopo}")
        print(f"   💰 Movimenti cassaforte: {movimenti_dopo}")
        print(f"   👥 Utenti: {utenti_dopo}")
        
        # Verifica che gli utenti admin e dipendente siano ancora presenti
        admin = User.query.filter_by(username='admin').first()
        dipendente = User.query.filter_by(username='dipendente').first()
        
        if admin and dipendente:
            print("✅ Utenti admin e dipendente mantenuti")
        else:
            print("❌ Errore: Utenti admin o dipendente mancanti")
            return False
        
        # Verifica che il database sia pulito
        if incassi_dopo == 0 and movimenti_dopo == 0:
            print("\n🎉 Database pulito con successo!")
            print("🚀 Pronto per i dati reali!")
            return True
        else:
            print("\n⚠️  Errore: Alcuni dati sono ancora presenti")
            return False

if __name__ == "__main__":
    try:
        success = pulisci_database()
        if success:
            print("\n✅ Database pulito e pronto per i dati reali!")
            print("💡 Ora puoi iniziare a inserire i tuoi dati reali")
            sys.exit(0)
        else:
            print("\n❌ Errore durante la pulizia del database")
            sys.exit(1)
    except Exception as e:
        print(f"❌ Errore durante l'esecuzione: {e}")
        sys.exit(1) 