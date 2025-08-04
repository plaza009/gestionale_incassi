#!/usr/bin/env python3
"""
Test script per verificare la funzionalità di ricerca nella lista incassi
"""

import requests
from bs4 import BeautifulSoup
import sys
import time

def test_ricerca_incassi():
    """Testa la funzionalità di ricerca nella lista incassi"""
    base_url = "http://localhost:5000"
    
    print("🧪 Test funzionalità ricerca incassi")
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
    
    # Test 2: Accesso alla lista incassi
    print("\n2. Accesso alla lista incassi...")
    response = session.get(f"{base_url}/incassi/lista")
    if response.status_code != 200:
        print("❌ Errore nell'accesso alla lista incassi")
        return False
    
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Verifica presenza form di ricerca
    form_ricerca = soup.find('form', {'action': '/incassi/lista'})
    if not form_ricerca:
        print("❌ Form di ricerca non trovato")
        return False
    
    print("✅ Form di ricerca presente")
    
    # Verifica presenza campi di ricerca
    campo_data = soup.find('input', {'name': 'data_ricerca'})
    campo_operatore = soup.find('input', {'name': 'operatore_ricerca'})
    
    if not campo_data:
        print("❌ Campo ricerca data non trovato")
        return False
    
    if not campo_operatore:
        print("❌ Campo ricerca operatore non trovato")
        return False
    
    print("✅ Campi di ricerca presenti")
    
    # Test 3: Ricerca per data
    print("\n3. Test ricerca per data...")
    data_test = "2024-01-15"  # Data di esempio
    response = session.get(f"{base_url}/incassi/lista?data_ricerca={data_test}")
    
    if response.status_code != 200:
        print("❌ Errore nella ricerca per data")
        return False
    
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Verifica che il campo data contenga il valore di ricerca
    campo_data_risultato = soup.find('input', {'name': 'data_ricerca'})
    if not campo_data_risultato or campo_data_risultato.get('value') != data_test:
        print("❌ Valore ricerca data non mantenuto")
        return False
    
    print("✅ Ricerca per data funziona")
    
    # Test 4: Ricerca per operatore
    print("\n4. Test ricerca per operatore...")
    operatore_test = "dipendente"
    response = session.get(f"{base_url}/incassi/lista?operatore_ricerca={operatore_test}")
    
    if response.status_code != 200:
        print("❌ Errore nella ricerca per operatore")
        return False
    
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Verifica che il campo operatore contenga il valore di ricerca
    campo_operatore_risultato = soup.find('input', {'name': 'operatore_ricerca'})
    if not campo_operatore_risultato or campo_operatore_risultato.get('value') != operatore_test:
        print("❌ Valore ricerca operatore non mantenuto")
        return False
    
    print("✅ Ricerca per operatore funziona")
    
    # Test 5: Pulsante "Pulisci"
    print("\n5. Test pulsante 'Pulisci'...")
    response = session.get(f"{base_url}/incassi/lista")
    
    if response.status_code != 200:
        print("❌ Errore nell'accesso alla lista senza filtri")
        return False
    
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Verifica che i campi siano vuoti
    campo_data_pulito = soup.find('input', {'name': 'data_ricerca'})
    campo_operatore_pulito = soup.find('input', {'name': 'operatore_ricerca'})
    
    if campo_data_pulito and campo_data_pulito.get('value'):
        print("❌ Campo data non pulito")
        return False
    
    if campo_operatore_pulito and campo_operatore_pulito.get('value'):
        print("❌ Campo operatore non pulito")
        return False
    
    print("✅ Pulsante 'Pulisci' funziona")
    
    # Test 6: Verifica raggruppamento per mese
    print("\n6. Test raggruppamento per mese...")
    
    # Cerca sezioni per mese
    sezioni_mese = soup.find_all('h5', class_='text-primary')
    if not sezioni_mese:
        print("❌ Sezioni per mese non trovate")
        return False
    
    print(f"✅ Trovate {len(sezioni_mese)} sezioni per mese")
    
    # Test 7: Login come dipendente e verifica limitazioni
    print("\n7. Test accesso dipendente...")
    session = requests.Session()
    
    login_data_dipendente = {
        'username': 'dipendente',
        'password': 'dipendente123'
    }
    
    response = session.post(f"{base_url}/login", data=login_data_dipendente, allow_redirects=True)
    if response.status_code != 200:
        print("❌ Errore nel login dipendente")
        return False
    
    # Verifica che il login sia andato a buon fine
    if "Dashboard" not in response.text:
        print("❌ Login dipendente fallito")
        return False
    
    print("✅ Login dipendente riuscito")
    
    # Accesso alla lista incassi come dipendente
    response = session.get(f"{base_url}/incassi/lista")
    if response.status_code != 200:
        print("❌ Errore nell'accesso alla lista incassi come dipendente")
        return False
    
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Verifica che il campo operatore NON sia presente per i dipendenti
    campo_operatore_dipendente = soup.find('input', {'name': 'operatore_ricerca'})
    if campo_operatore_dipendente:
        print("❌ Campo ricerca operatore presente per dipendenti (dovrebbe essere nascosto)")
        return False
    
    print("✅ Campo ricerca operatore correttamente nascosto per dipendenti")
    
    print("\n🎉 Tutti i test di ricerca completati con successo!")
    return True

if __name__ == "__main__":
    try:
        success = test_ricerca_incassi()
        if success:
            print("\n✅ Test ricerca incassi: SUCCESSO")
            sys.exit(0)
        else:
            print("\n❌ Test ricerca incassi: FALLITO")
            sys.exit(1)
    except Exception as e:
        print(f"\n❌ Errore durante il test: {e}")
        sys.exit(1) 