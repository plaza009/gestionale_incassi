#!/usr/bin/env python3
"""
Test script per verificare l'inserimento di un movimento di entrata
"""
import requests
from bs4 import BeautifulSoup
import sys
import time

def test_movimento_entrata():
    """Testa l'inserimento di un movimento di entrata"""
    base_url = "http://localhost:5000"
    print("🧪 Test movimento entrata")
    print("=" * 50)
    
    # Test 1: Login admin
    session = requests.Session()
    login_data = {'username': 'admin', 'password': 'admin123'}
    response = session.post(f"{base_url}/login", data=login_data, allow_redirects=True)
    if response.status_code != 200 or "Dashboard" not in response.text:
        print("❌ Errore nel login admin")
        return False
    print("✅ Login admin riuscito")
    
    # Test 2: Inserisci movimento di entrata
    movimento_data = {
        'data_movimento': '2025-08-03',
        'tipo_movimento': 'entrata',
        'importo': '100.00',
        'monete_importo': '20.00',
        'banconote_importo': '80.00',
        'descrizione': 'Test movimento entrata - €100 (€20 monete + €80 banconote)'
    }
    
    print(f"📝 Invio dati movimento: {movimento_data}")
    
    response = session.post(f"{base_url}/cassaforte/nuovo", data=movimento_data, allow_redirects=True)
    print(f"📊 Status code: {response.status_code}")
    print(f"📊 URL finale: {response.url}")
    
    # Verifica che il movimento sia stato inserito controllando la lista
    if "Movimento cassaforte registrato con successo" in response.text:
        print("✅ Movimento di entrata inserito con successo")
    else:
        print("❌ Errore nell'inserimento del movimento")
        return False
    
    # Test 3: Verifica nella lista movimenti
    response = session.get(f"{base_url}/cassaforte/lista")
    if response.status_code != 200:
        print("❌ Errore nell'accesso alla lista movimenti")
        return False
    
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Cerca il movimento appena inserito
    movimento_trovato = False
    for row in soup.find_all('tr'):
        cells = row.find_all('td')
        if len(cells) >= 3:
            # Verifica se è il movimento di test
            importo_cell = cells[2].get_text().strip()
            if '€100.00' in importo_cell:
                tipo_cell = cells[1].get_text().strip()
                if 'Entrata' in tipo_cell:
                    movimento_trovato = True
                    print("✅ Movimento di entrata trovato nella lista")
                    break
    
    if not movimento_trovato:
        print("❌ Movimento di entrata non trovato nella lista")
        return False
    
    # Test 4: Verifica nella dashboard
    response = session.get(f"{base_url}/dashboard")
    if response.status_code != 200:
        print("❌ Errore nell'accesso alla dashboard")
        return False
    
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Cerca il movimento nella dashboard
    dashboard_movimento = False
    for row in soup.find_all('tr'):
        cells = row.find_all('td')
        if len(cells) >= 2:
            importo_cell = cells[1].get_text().strip()
            if '€100.00' in importo_cell:
                tipo_cell = cells[0].get_text().strip()
                if 'Entrata' in tipo_cell:
                    dashboard_movimento = True
                    print("✅ Movimento di entrata trovato nella dashboard")
                    break
    
    if not dashboard_movimento:
        print("❌ Movimento di entrata non trovato nella dashboard")
        return False
    
    print("\n🎉 Test movimento entrata completato con successo!")
    print("\n📋 Verifiche effettuate:")
    print("  ✅ Movimento di entrata inserito correttamente")
    print("  ✅ Tipo 'Entrata' visualizzato correttamente nella lista")
    print("  ✅ Tipo 'Entrata' visualizzato correttamente nella dashboard")
    print("  ✅ Importo €100.00 visualizzato correttamente")
    return True

if __name__ == "__main__":
    try:
        success = test_movimento_entrata()
        if success:
            sys.exit(0)
        else:
            sys.exit(1)
    except Exception as e:
        print(f"❌ Errore durante il test: {e}")
        sys.exit(1) 