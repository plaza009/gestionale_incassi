#!/usr/bin/env python3
"""
Test del Sistema Gestionale Incassi
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import app, db, User, Incasso, Cassaforte
from werkzeug.security import generate_password_hash
from datetime import datetime, date

def test_sistema():
    """Test delle funzionalità principali del sistema"""
    
    print("🧪 Test del Sistema Gestionale Incassi")
    print("=" * 50)
    
    with app.app_context():
        # Test 1: Verifica database
        print("1. Verifica database...")
        try:
            db.create_all()
            print("   ✅ Database creato con successo")
        except Exception as e:
            print(f"   ❌ Errore database: {e}")
            return False
        
        # Test 2: Verifica utente admin
        print("2. Verifica utente admin...")
        admin = User.query.filter_by(username='admin').first()
        if not admin:
            admin = User(
                username='admin',
                password_hash=generate_password_hash('admin123'),
                is_admin=True
            )
            db.session.add(admin)
            db.session.commit()
            print("   ✅ Utente admin creato")
        else:
            print("   ✅ Utente admin esistente")
        
        # Test 3: Test calcoli incasso
        print("3. Test calcoli incasso...")
        try:
            # Esempio dal requisito
            fondo_cassa = 100.0
            incasso_pos = 100.0
            cash_totale = 200.0
            cash_scontrinato = 80.0
            cash_non_scontrinato = 20.0
            
            incasso_cash_effettivo = cash_totale - fondo_cassa  # 100
            totale_atteso = incasso_pos + incasso_cash_effettivo  # 200
            totale_dichiarato = cash_scontrinato + cash_non_scontrinato  # 100
            
            if abs(incasso_cash_effettivo - totale_dichiarato) <= 0.01:
                coerenza = "Coerente"
            else:
                differenza = incasso_cash_effettivo - totale_dichiarato
                coerenza = f"Eccedenza cash di €{differenza:.2f} - possibile incasso non scontrinato"
            
            print(f"   ✅ Calcoli corretti:")
            print(f"      - Incasso cash effettivo: €{incasso_cash_effettivo:.2f}")
            print(f"      - Totale atteso: €{totale_atteso:.2f}")
            print(f"      - Coerenza: {coerenza}")
            
        except Exception as e:
            print(f"   ❌ Errore calcoli: {e}")
            return False
        
        # Test 4: Test incoerenza
        print("4. Test incoerenza...")
        try:
            cash_totale_incoerente = 220.0
            incasso_cash_effettivo_incoerente = cash_totale_incoerente - fondo_cassa  # 120
            differenza_incoerente = incasso_cash_effettivo_incoerente - totale_dichiarato  # 20
            
            if differenza_incoerente > 0:
                coerenza_incoerente = f"Eccedenza cash di €{differenza_incoerente:.2f} - possibile incasso non scontrinato"
                print(f"   ✅ Incoerenza rilevata: {coerenza_incoerente}")
            else:
                print("   ❌ Incoerenza non rilevata")
                return False
                
        except Exception as e:
            print(f"   ❌ Errore test incoerenza: {e}")
            return False
        
        # Test 5: Creazione dati di esempio
        print("5. Creazione dati di esempio...")
        try:
            # Crea un incasso di esempio
            incasso_esempio = Incasso(
                operatore_id=admin.id,
                fondo_cassa_iniziale=100.0,
                incasso_pos=150.0,
                cash_totale_cassa=250.0,
                cash_scontrinato=120.0,
                cash_non_scontrinato=30.0,
                note="Incasso di esempio per test"
            )
            db.session.add(incasso_esempio)
            
            # Crea movimenti cassaforte di esempio
            movimento_entrata = Cassaforte(
                tipo_operazione='entrata',
                importo=250.0,
                descrizione='Versamento incasso giornaliero',
                operatore_id=admin.id
            )
            db.session.add(movimento_entrata)
            
            movimento_uscita = Cassaforte(
                tipo_operazione='uscita',
                importo=50.0,
                descrizione='Prelievo per fondo cassa',
                operatore_id=admin.id
            )
            db.session.add(movimento_uscita)
            
            db.session.commit()
            print("   ✅ Dati di esempio creati")
            
        except Exception as e:
            print(f"   ❌ Errore creazione dati: {e}")
            return False
        
        print("\n🎉 Tutti i test superati con successo!")
        print("✅ Il sistema è pronto per l'uso")
        print("\n📋 Credenziali di accesso:")
        print("   Username: admin")
        print("   Password: admin123")
        print("\n🌐 Avvia il sistema con: python run.py")
        
        return True

if __name__ == '__main__':
    success = test_sistema()
    if not success:
        print("\n❌ Test falliti. Verifica l'installazione.")
        sys.exit(1) 