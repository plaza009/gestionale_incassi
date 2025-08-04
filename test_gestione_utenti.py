#!/usr/bin/env python3
"""
Script per testare le funzionalità di gestione utenti
"""
import requests
from bs4 import BeautifulSoup
import re

def test_gestione_utenti():
    base_url = "http://localhost:5000"
    
    print("🧪 Test Gestione Utenti")
    print("=" * 50)
    
    # 1. Login come admin
    print("\n1. Login come amministratore...")
    session = requests.Session()
    
    # Ottieni la pagina di login
    response = session.get(f"{base_url}/login")
    if response.status_code != 200:
        print("❌ Errore: Impossibile accedere alla pagina di login")
        return
    
    # Login
    login_data = {
        'username': 'admin',
        'password': 'admin123'
    }
    response = session.post(f"{base_url}/login", data=login_data)
    
    if response.status_code != 200 or 'dashboard' not in response.url:
        print("❌ Errore: Login fallito")
        return
    
    print("✅ Login amministratore completato")
    
    # 2. Test accesso alla lista utenti
    print("\n2. Test accesso alla lista utenti...")
    response = session.get(f"{base_url}/utenti/lista")
    
    if response.status_code != 200:
        print("❌ Errore: Impossibile accedere alla lista utenti")
        return
    
    soup = BeautifulSoup(response.text, 'html.parser')
    title = soup.find('title')
    if title and 'Gestione Utenti' in title.text:
        print("✅ Lista utenti accessibile")
    else:
        print("❌ Errore: Pagina lista utenti non corretta")
        return
    
    # 3. Test accesso al form nuovo utente
    print("\n3. Test accesso al form nuovo utente...")
    response = session.get(f"{base_url}/utenti/nuovo")
    
    if response.status_code != 200:
        print("❌ Errore: Impossibile accedere al form nuovo utente")
        return
    
    soup = BeautifulSoup(response.text, 'html.parser')
    title = soup.find('title')
    if title and 'Nuovo Utente' in title.text:
        print("✅ Form nuovo utente accessibile")
    else:
        print("❌ Errore: Pagina nuovo utente non corretta")
        return
    
    # 4. Test creazione nuovo utente
    print("\n4. Test creazione nuovo utente...")
    nuovo_utente_data = {
        'username': 'test_user',
        'nome_completo': 'Utente Test',
        'password': 'test123',
        'password_confirm': 'test123',
        'is_admin': 'on'
    }
    
    response = session.post(f"{base_url}/utenti/nuovo", data=nuovo_utente_data)
    
    if response.status_code == 200:
        # Verifica se c'è un messaggio di successo
        soup = BeautifulSoup(response.text, 'html.parser')
        success_messages = soup.find_all('div', class_='alert-success')
        if success_messages:
            print("✅ Nuovo utente creato con successo")
        else:
            print("⚠️  Utente potrebbe essere già esistente o errore nella creazione")
    else:
        print("❌ Errore nella creazione del nuovo utente")
    
    # 5. Test accesso alla lista utenti dopo creazione
    print("\n5. Verifica lista utenti aggiornata...")
    response = session.get(f"{base_url}/utenti/lista")
    
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        # Cerca il nuovo utente nella tabella
        table = soup.find('table')
        if table and 'test_user' in table.text:
            print("✅ Nuovo utente visibile nella lista")
        else:
            print("⚠️  Nuovo utente non trovato nella lista")
    
    # 6. Test logout
    print("\n6. Test logout...")
    response = session.get(f"{base_url}/logout")
    
    if response.status_code == 200:
        print("✅ Logout completato")
    else:
        print("❌ Errore nel logout")
    
    print("\n" + "=" * 50)
    print("✅ Test gestione utenti completato!")
    print("\n📋 Funzionalità testate:")
    print("   - Login amministratore")
    print("   - Accesso lista utenti")
    print("   - Accesso form nuovo utente")
    print("   - Creazione nuovo utente")
    print("   - Verifica lista aggiornata")
    print("   - Logout")
    
    print("\n🎯 Prossimi passi:")
    print("   1. Accedi al sistema come admin")
    print("   2. Vai su 'Gestione Utenti' nella sidebar")
    print("   3. Crea un nuovo utente dipendente")
    print("   4. Testa il login con il nuovo utente")
    print("   5. Verifica i permessi del dipendente")

if __name__ == '__main__':
    test_gestione_utenti() 