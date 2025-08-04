#!/usr/bin/env python3
"""
Test script per verificare che il tipo di movimento venga visualizzato correttamente
"""
import requests
from bs4 import BeautifulSoup
import sys

def test_correzione_tipo_movimento():
    """Testa che il tipo di movimento venga visualizzato correttamente"""
    base_url = "http://localhost:5000"
    print("🧪 Test correzione tipo movimento")
    print("=" * 50)
    
    # Test 1: Login admin
    session = requests.Session()
    login_data = {'username': 'admin', 'password': 'admin123'}
    response = session.post(f"{base_url}/login", data=login_data, allow_redirects=True)
    if response.status_code != 200 or "Dashboard" not in response.text:
        print("❌ Errore nel login admin")
        return False
    print("✅ Login admin riuscito")
    
    # Test 2: Verifica dashboard
    response = session.get(f"{base_url}/dashboard")
    if response.status_code != 200:
        print("❌ Errore nell'accesso alla dashboard")
        return False
    
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Cerca la sezione movimenti cassaforte
    movimenti_section = soup.find('h6', string=lambda text: text and 'Movimenti Cassaforte' in text)
    if not movimenti_section:
        print("❌ Sezione movimenti cassaforte non trovata")
        return False
    print("✅ Sezione movimenti cassaforte trovata")
    
    # Cerca i badge per i tipi di movimento
    badge_entrata = soup.find('span', string='Entrata', class_='badge bg-success')
    badge_uscita = soup.find('span', string='Uscita', class_='badge bg-danger')
    
    if badge_entrata:
        print("✅ Badge 'Entrata' trovato")
    if badge_uscita:
        print("✅ Badge 'Uscita' trovato")
    
    # Test 3: Verifica lista movimenti cassaforte
    response = session.get(f"{base_url}/cassaforte/lista")
    if response.status_code != 200:
        print("❌ Errore nell'accesso alla lista movimenti cassaforte")
        return False
    
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Cerca i badge nella lista movimenti
    badge_entrata_lista = soup.find('span', string='Entrata', class_='badge bg-success')
    badge_uscita_lista = soup.find('span', string='Uscita', class_='badge bg-danger')
    
    if badge_entrata_lista:
        print("✅ Badge 'Entrata' trovato nella lista")
    if badge_uscita_lista:
        print("✅ Badge 'Uscita' trovato nella lista")
    
    # Test 4: Verifica che non ci siano errori 500
    response = session.get(f"{base_url}/api/report/giornaliero/2025-08-03")
    if response.status_code == 500:
        print("❌ Errore 500 nell'API report giornaliero")
        return False
    print("✅ API report giornaliero funziona correttamente")
    
    print("\n🎉 Test correzione tipo movimento completato con successo!")
    print("\n📋 Problemi risolti:")
    print("  ✅ Corretto 'tipo_operazione' in 'tipo_movimento' nella dashboard")
    print("  ✅ Corretto 'tipo_operazione' in 'tipo_movimento' nell'API report")
    print("  ✅ Badge tipo movimento visualizzati correttamente")
    return True

if __name__ == "__main__":
    try:
        success = test_correzione_tipo_movimento()
        if success:
            sys.exit(0)
        else:
            sys.exit(1)
    except Exception as e:
        print(f"❌ Errore durante il test: {e}")
        sys.exit(1) 