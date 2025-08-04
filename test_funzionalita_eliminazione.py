#!/usr/bin/env python3
"""
Test script per verificare la funzionalità di eliminazione
"""

import requests
from bs4 import BeautifulSoup
import sys
import time

def test_funzionalita_eliminazione():
    """Testa la funzionalità di eliminazione per admin"""
    base_url = "http://localhost:5000"
    
    print("🧪 Test funzionalità eliminazione")
    print("=" * 50)
    
    # Test 1: Login come admin
    print("\n1. Login come admin...")
    session = requests.Session()
    
    login_data = {
        'username': 'admin',
        'password': 'admin123'
    }
    
    response = session.post(f"{base_url}/login", data=login_data, allow_redirects=True)
    if response.status_code != 200:
        print("❌ Errore nel login admin")
        return False
    
    # Verifica che il login sia andato a buon fine
    if "Dashboard" not in response.text:
        print("❌ Login admin fallito")
        return False
    
    print("✅ Login admin riuscito")
    
    # Test 2: Verifica presenza pulsanti eliminazione nella lista incassi
    print("\n2. Verifica pulsanti eliminazione nella lista incassi...")
    response = session.get(f"{base_url}/incassi/lista")
    if response.status_code != 200:
        print("❌ Errore nell'accesso alla lista incassi")
        return False
    
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Verifica presenza pulsanti eliminazione
    pulsanti_elimina = soup.find_all('button', string=lambda text: text and 'Elimina' in text)
    form_elimina = soup.find_all('form', action=lambda action: action and 'elimina' in action)
    
    if not pulsanti_elimina and not form_elimina:
        print("❌ Pulsanti eliminazione non trovati nella lista incassi")
        return False
    
    print("✅ Pulsanti eliminazione presenti nella lista incassi")
    
    # Test 3: Verifica presenza pulsanti eliminazione nella lista movimenti cassaforte
    print("\n3. Verifica pulsanti eliminazione nella lista movimenti cassaforte...")
    response = session.get(f"{base_url}/cassaforte/lista")
    if response.status_code != 200:
        print("❌ Errore nell'accesso alla lista movimenti cassaforte")
        return False
    
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Verifica presenza pulsanti eliminazione
    pulsanti_elimina_cassaforte = soup.find_all('button', string=lambda text: text and 'Elimina' in text)
    form_elimina_cassaforte = soup.find_all('form', action=lambda action: action and 'elimina' in action)
    
    if not pulsanti_elimina_cassaforte and not form_elimina_cassaforte:
        print("❌ Pulsanti eliminazione non trovati nella lista movimenti cassaforte")
        return False
    
    print("✅ Pulsanti eliminazione presenti nella lista movimenti cassaforte")
    
    # Test 4: Verifica pulsante eliminazione nella pagina dettaglio incasso
    print("\n4. Verifica pulsante eliminazione nella pagina dettaglio...")
    response = session.get(f"{base_url}/incassi/1")
    if response.status_code != 200:
        print("❌ Errore nell'accesso al dettaglio incasso")
        return False
    
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Verifica presenza pulsante eliminazione
    pulsante_elimina_dettaglio = soup.find('button', string=lambda text: text and 'Elimina' in text)
    form_elimina_dettaglio = soup.find_all('form', action=lambda action: action and 'elimina' in action)
    
    if not pulsante_elimina_dettaglio and not form_elimina_dettaglio:
        print("❌ Pulsante eliminazione non trovato nella pagina dettaglio")
        return False
    
    print("✅ Pulsante eliminazione presente nella pagina dettaglio")
    
    # Test 5: Verifica che i dipendenti NON vedano i pulsanti eliminazione
    print("\n5. Verifica che i dipendenti non vedano i pulsanti eliminazione...")
    session = requests.Session()
    
    login_data_dipendente = {
        'username': 'dipendente',
        'password': 'dipendente123'
    }
    
    response = session.post(f"{base_url}/login", data=login_data_dipendente, allow_redirects=True)
    if response.status_code != 200:
        print("❌ Errore nel login dipendente")
        return False
    
    if "Dashboard" not in response.text:
        print("❌ Login dipendente fallito")
        return False
    
    print("✅ Login dipendente riuscito")
    
    # Verifica che i dipendenti non vedano pulsanti eliminazione
    response = session.get(f"{base_url}/incassi/lista")
    if response.status_code != 200:
        print("❌ Errore nell'accesso alla lista incassi come dipendente")
        return False
    
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Verifica assenza pulsanti eliminazione per dipendenti
    pulsanti_elimina_dipendente = soup.find_all('button', string=lambda text: text and 'Elimina' in text)
    form_elimina_dipendente = soup.find_all('form', action=lambda action: action and 'elimina' in action)
    
    if pulsanti_elimina_dipendente or form_elimina_dipendente:
        print("❌ Pulsanti eliminazione trovati per dipendenti (dovrebbero essere nascosti)")
        return False
    
    print("✅ Pulsanti eliminazione correttamente nascosti per dipendenti")
    
    print("\n🎉 Tutti i test di eliminazione completati con successo!")
    return True

if __name__ == "__main__":
    try:
        success = test_funzionalita_eliminazione()
        if success:
            print("\n✅ Test funzionalità eliminazione: SUCCESSO")
            sys.exit(0)
        else:
            print("\n❌ Test funzionalità eliminazione: FALLITO")
            sys.exit(1)
    except Exception as e:
        print(f"\n❌ Errore durante il test: {e}")
        sys.exit(1) 