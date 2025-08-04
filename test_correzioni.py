#!/usr/bin/env python3
"""
Test per verificare le correzioni apportate:
1. Rimozione del "6 b" dal template base.html
2. Funzionamento del form con campi obbligatori per dipendenti
"""

import requests
from bs4 import BeautifulSoup
import time

def test_correzioni():
    """Test delle correzioni apportate"""
    base_url = "http://localhost:5000"
    
    print("🔧 Test delle correzioni apportate...")
    
    try:
        # Test 1: Verifica che non ci sia più "6 b" nella pagina
        print("\n1. Verifica rimozione '6 b'...")
        response = requests.get(f"{base_url}/login")
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Verifica che il DOCTYPE sia corretto
        if soup.find('html') and not response.text.startswith('6 b'):
            print("✅ '6 b' rimosso correttamente")
        else:
            print("❌ '6 b' ancora presente")
            return False
        
        # Test 2: Login come dipendente e verifica form
        print("\n2. Test form dipendente...")
        
        # Login come dipendente
        session = requests.Session()
        login_data = {
            'username': 'dipendente',
            'password': 'dipendente123'
        }
        
        # Prima ottieni la pagina di login per eventuali token CSRF
        response = session.get(f"{base_url}/login")
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Cerca token CSRF se presente
        csrf_token = soup.find('input', {'name': 'csrf_token'})
        if csrf_token:
            login_data['csrf_token'] = csrf_token.get('value')
        
        response = session.post(f"{base_url}/login", data=login_data, allow_redirects=True)
        
        # Verifica se il login è riuscito controllando se siamo nella dashboard
        if "dashboard" in response.url or "Nuovo Incasso" in response.text:
            print("✅ Login dipendente effettuato")
            
            # Verifica pagina nuovo incasso
            response = session.get(f"{base_url}/incassi/nuovo")
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Debug: stampa tutti gli input per vedere cosa c'è
            print("🔍 Debug - Tutti gli input trovati:")
            all_inputs = soup.find_all('input')
            for inp in all_inputs:
                print(f"   - name: {inp.get('name')}, required: {inp.get('required')}")
            
            # Verifica campi obbligatori
            fondo_cassa = soup.find('input', {'name': 'fondo_cassa'})
            incasso_pos = soup.find('input', {'name': 'incasso_pos'})
            cash_totale = soup.find('input', {'name': 'cash_totale'})
            
            print(f"\n🔍 Debug - Campi obbligatori:")
            print(f"   - fondo_cassa: {fondo_cassa is not None}, required: {fondo_cassa.get('required') if fondo_cassa else 'N/A'}")
            print(f"   - incasso_pos: {incasso_pos is not None}, required: {incasso_pos.get('required') if incasso_pos else 'N/A'}")
            print(f"   - cash_totale: {cash_totale is not None}, required: {cash_totale.get('required') if cash_totale else 'N/A'}")
            
            if (fondo_cassa and fondo_cassa.get('required') and
                incasso_pos and incasso_pos.get('required') and
                cash_totale and cash_totale.get('required')):
                print("✅ Campi obbligatori configurati correttamente")
            else:
                print("❌ Campi obbligatori non configurati")
                return False
            
            # Verifica che i campi admin non siano visibili
            cash_scontrinato = soup.find('input', {'name': 'cash_scontrinato'})
            cash_non_scontrinato = soup.find('input', {'name': 'cash_non_scontrinato'})
            
            if not cash_scontrinato and not cash_non_scontrinato:
                print("✅ Campi admin nascosti per dipendenti")
            else:
                print("❌ Campi admin visibili per dipendenti")
                return False
            
            # Verifica messaggio informativo
            info_alert = soup.find('div', class_='alert-info')
            if info_alert and "Informazioni per Dipendenti" in info_alert.text:
                print("✅ Messaggio informativo presente")
            else:
                print("❌ Messaggio informativo mancante")
                return False
            
        else:
            print("❌ Login dipendente fallito")
            print(f"URL finale: {response.url}")
            print(f"Contenuto pagina: {response.text[:200]}...")
            return False
        
        # Test 3: Login come admin e verifica form
        print("\n3. Test form amministratore...")
        
        # Login come admin
        session = requests.Session()
        login_data = {
            'username': 'admin',
            'password': 'admin123'
        }
        
        # Prima ottieni la pagina di login per eventuali token CSRF
        response = session.get(f"{base_url}/login")
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Cerca token CSRF se presente
        csrf_token = soup.find('input', {'name': 'csrf_token'})
        if csrf_token:
            login_data['csrf_token'] = csrf_token.get('value')
        
        response = session.post(f"{base_url}/login", data=login_data, allow_redirects=True)
        
        if "dashboard" in response.url or "Nuovo Incasso" in response.text:
            print("✅ Login admin effettuato")
            
            # Verifica pagina nuovo incasso
            response = session.get(f"{base_url}/incassi/nuovo")
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Verifica che i campi admin siano visibili
            cash_scontrinato = soup.find('input', {'name': 'cash_scontrinato'})
            cash_non_scontrinato = soup.find('input', {'name': 'cash_non_scontrinato'})
            
            if cash_scontrinato and cash_non_scontrinato:
                print("✅ Campi admin visibili per amministratori")
            else:
                print("❌ Campi admin non visibili per amministratori")
                return False
            
            # Verifica etichetta sezione admin
            admin_section = soup.find('h6', string=lambda text: text and 'Amministratore' in text)
            if admin_section:
                print("✅ Sezione amministratore etichettata correttamente")
            else:
                print("❌ Sezione amministratore non etichettata")
                return False
            
        else:
            print("❌ Login admin fallito")
            return False
        
        print("\n🎉 Tutti i test delle correzioni sono passati!")
        return True
        
    except requests.exceptions.ConnectionError:
        print("❌ Impossibile connettersi al server. Assicurati che l'app sia in esecuzione.")
        return False
    except Exception as e:
        print(f"❌ Errore durante il test: {e}")
        return False

if __name__ == "__main__":
    print("🚀 Avvio test delle correzioni...")
    success = test_correzioni()
    
    if success:
        print("\n✅ Tutte le correzioni sono state applicate con successo!")
        print("\n📋 Riepilogo correzioni:")
        print("   • Rimosso '6 b' dal template base.html")
        print("   • Campi 'incassi pos', 'cash in cassa' e 'fondo cassa' obbligatori per tutti")
        print("   • Campi 'cash scontrinato' e 'cash non scontrinato' visibili solo agli admin")
        print("   • Messaggio informativo per dipendenti")
        print("   • Etichette appropriate per amministratori")
    else:
        print("\n❌ Alcuni test sono falliti. Controlla il codice.") 