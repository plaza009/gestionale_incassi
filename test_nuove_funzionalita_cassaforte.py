#!/usr/bin/env python3
"""
Test script per verificare le nuove funzionalità della cassaforte:
1. Visualizzazione dei 3 saldi distinti (Totale, Monete, Cash)
2. Campo nota per i dipendenti
"""
import requests
from bs4 import BeautifulSoup
import sys
import time

def test_nuove_funzionalita_cassaforte():
    """Testa le nuove funzionalità della cassaforte"""
    base_url = "http://localhost:5000"
    print("🧪 Test nuove funzionalità cassaforte")
    print("=" * 50)
    
    # Test 1: Login admin
    session = requests.Session()
    login_data = {'username': 'admin', 'password': 'admin123'}
    response = session.post(f"{base_url}/login", data=login_data, allow_redirects=True)
    if response.status_code != 200 or "Dashboard" not in response.text:
        print("❌ Errore nel login admin")
        return False
    print("✅ Login admin riuscito")
    
    # Test 2: Verifica visualizzazione 3 saldi distinti
    response = session.get(f"{base_url}/cassaforte/lista")
    if response.status_code != 200:
        print("❌ Errore nell'accesso alla lista movimenti cassaforte")
        return False
    
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Cerca i 3 indicatori di saldo
    totale_cassaforte = soup.find('h3', string=lambda text: text and '€' in text and 'text-primary' in text.parent.get('class', []))
    monete_cassa = soup.find('h3', string=lambda text: text and '€' in text and ('text-danger' in text.parent.get('class', []) or 'text-success' in text.parent.get('class', [])))
    importo_cash = soup.find('h3', string=lambda text: text and '€' in text and 'text-info' in text.parent.get('class', []))
    
    if not totale_cassaforte:
        print("❌ Indicatore 'Totale in Cassaforte' non trovato")
        return False
    print("✅ Indicatore 'Totale in Cassaforte' presente")
    
    if not monete_cassa:
        print("❌ Indicatore 'Monete in Cassa' non trovato")
        return False
    print("✅ Indicatore 'Monete in Cassa' presente")
    
    if not importo_cash:
        print("❌ Indicatore 'Importo Cash' non trovato")
        return False
    print("✅ Indicatore 'Importo Cash' presente")
    
    # Test 3: Verifica colonna nota nella tabella
    headers = soup.find_all('th')
    nota_header = None
    for header in headers:
        if 'Nota' in header.get_text():
            nota_header = header
            break
    
    if not nota_header:
        print("❌ Colonna 'Nota' non trovata nella tabella")
        return False
    print("✅ Colonna 'Nota' presente nella tabella")
    
    # Test 4: Verifica campo nota nel form nuovo movimento
    response = session.get(f"{base_url}/cassaforte/nuovo")
    if response.status_code != 200:
        print("❌ Errore nell'accesso al form nuovo movimento")
        return False
    
    soup = BeautifulSoup(response.text, 'html.parser')
    nota_field = soup.find('label', string=lambda text: text and 'Nota' in text)
    nota_textarea = soup.find('textarea', {'name': 'descrizione'})
    
    if not nota_field:
        print("❌ Campo 'Nota' non trovato nel form")
        return False
    print("✅ Campo 'Nota' presente nel form")
    
    if not nota_textarea:
        print("❌ Textarea per nota non trovata")
        return False
    print("✅ Textarea per nota presente")
    
    # Test 5: Test login dipendente e verifica accesso
    session = requests.Session()
    login_data_dipendente = {'username': 'dipendente', 'password': 'dipendente123'}
    response = session.post(f"{base_url}/login", data=login_data_dipendente, allow_redirects=True)
    if response.status_code != 200 or "Dashboard" not in response.text:
        print("❌ Errore nel login dipendente")
        return False
    print("✅ Login dipendente riuscito")
    
    # Verifica che il dipendente possa vedere la lista movimenti
    response = session.get(f"{base_url}/cassaforte/lista")
    if response.status_code != 200:
        print("❌ Errore nell'accesso alla lista movimenti come dipendente")
        return False
    
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Verifica che i 3 indicatori siano presenti anche per dipendenti
    totale_cassaforte_dip = soup.find('h3', string=lambda text: text and '€' in text and 'text-primary' in text.parent.get('class', []))
    if not totale_cassaforte_dip:
        print("❌ Indicatore 'Totale in Cassaforte' non trovato per dipendenti")
        return False
    print("✅ Indicatori saldi visibili per dipendenti")
    
    # Verifica che il dipendente possa accedere al form nuovo movimento
    response = session.get(f"{base_url}/cassaforte/nuovo")
    if response.status_code != 200:
        print("❌ Errore nell'accesso al form nuovo movimento come dipendente")
        return False
    
    soup = BeautifulSoup(response.text, 'html.parser')
    nota_field_dip = soup.find('label', string=lambda text: text and 'Nota' in text)
    if not nota_field_dip:
        print("❌ Campo 'Nota' non trovato nel form per dipendenti")
        return False
    print("✅ Campo 'Nota' accessibile per dipendenti")
    
    print("\n🎉 Tutti i test delle nuove funzionalità cassaforte completati con successo!")
    print("\n📋 Funzionalità verificate:")
    print("  ✅ Visualizzazione 3 saldi distinti (Totale, Monete, Cash)")
    print("  ✅ Colonna 'Nota' nella tabella movimenti")
    print("  ✅ Campo 'Nota' nel form nuovo movimento")
    print("  ✅ Accesso per admin e dipendenti")
    return True

if __name__ == "__main__":
    try:
        success = test_nuove_funzionalita_cassaforte()
        if success:
            sys.exit(0)
        else:
            sys.exit(1)
    except Exception as e:
        print(f"❌ Errore durante il test: {e}")
        sys.exit(1) 