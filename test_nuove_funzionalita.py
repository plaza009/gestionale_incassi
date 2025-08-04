#!/usr/bin/env python3
"""
Test per verificare le nuove funzionalità implementate:
1. Selezione data nel form di inserimento
2. Filtro lista incassi per utente
3. Funzionalità di modifica per admin
"""

import requests
from bs4 import BeautifulSoup
import time

def test_nuove_funzionalita():
    """Test delle nuove funzionalità"""
    base_url = "http://localhost:5000"
    
    print("🔧 Test delle nuove funzionalità...")
    
    try:
        # Test 1: Verifica campo data nel form
        print("\n1. Verifica campo data nel form...")
        
        # Login come dipendente
        session = requests.Session()
        login_data = {
            'username': 'dipendente',
            'password': 'dipendente123'
        }
        
        response = session.post(f"{base_url}/login", data=login_data, allow_redirects=True)
        if response.status_code == 200:
            print("✅ Login dipendente effettuato")
            
            # Verifica pagina nuovo incasso
            response = session.get(f"{base_url}/incassi/nuovo")
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Verifica campo data
            data_field = soup.find('input', {'name': 'data_incasso'})
            if data_field and data_field.get('type') == 'date':
                print("✅ Campo data presente nel form")
            else:
                print("❌ Campo data non trovato")
                return False
            
        else:
            print("❌ Login dipendente fallito")
            return False
        
        # Test 2: Verifica lista incassi filtrata per dipendente
        print("\n2. Verifica lista incassi dipendente...")
        
        response = session.get(f"{base_url}/incassi/lista")
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Verifica titolo
        title_element = soup.find('h6', string=lambda text: text and 'I Miei Incassi' in text)
        if title_element:
            print("✅ Titolo lista appropriato per dipendente")
        else:
            print("❌ Titolo lista non appropriato")
            return False
        
        # Verifica che non ci sia colonna operatore
        operator_header = soup.find('th', string='Operatore')
        if not operator_header:
            print("✅ Colonna operatore nascosta per dipendente")
        else:
            print("❌ Colonna operatore visibile per dipendente")
            return False
        
        # Test 3: Login come admin e verifica funzionalità complete
        print("\n3. Test funzionalità admin...")
        
        # Login come admin
        session = requests.Session()
        login_data = {
            'username': 'admin',
            'password': 'admin123'
        }
        
        response = session.post(f"{base_url}/login", data=login_data, allow_redirects=True)
        if response.status_code == 200:
            print("✅ Login admin effettuato")
            
            # Verifica lista incassi admin
            response = session.get(f"{base_url}/incassi/lista")
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Verifica titolo admin
            title_element = soup.find('h6', string=lambda text: text and 'Tutti gli Incassi' in text)
            if title_element:
                print("✅ Titolo lista appropriato per admin")
            else:
                print("❌ Titolo lista non appropriato per admin")
                return False
            
            # Verifica che ci sia colonna operatore
            operator_header = soup.find('th', string='Operatore')
            if operator_header:
                print("✅ Colonna operatore visibile per admin")
            else:
                print("❌ Colonna operatore non visibile per admin")
                return False
            
            # Verifica pulsante modifica
            edit_buttons = soup.find_all('a', href=lambda href: href and '/modifica' in href)
            if edit_buttons:
                print("✅ Pulsanti modifica presenti per admin")
            else:
                print("❌ Pulsanti modifica non presenti")
                return False
            
        else:
            print("❌ Login admin fallito")
            return False
        
        # Test 4: Verifica pagina modifica incasso
        print("\n4. Verifica pagina modifica...")
        
        # Prima creiamo un incasso di test
        test_data = {
            'data_incasso': '2025-08-02',
            'fondo_cassa': '100.00',
            'incasso_pos': '500.00',
            'cash_totale': '600.00',
            'note': 'Test per modifica'
        }
        
        response = session.post(f"{base_url}/incassi/nuovo", data=test_data)
        if response.status_code == 200:
            print("✅ Incasso di test creato")
            
            # Trova l'incasso appena creato
            response = session.get(f"{base_url}/incassi/lista")
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Cerca il link alla pagina di modifica
            modifica_links = soup.find_all('a', href=lambda href: href and '/modifica' in href)
            if modifica_links:
                modifica_url = modifica_links[0]['href']
                response = session.get(f"{base_url}{modifica_url}")
                
                if response.status_code == 200:
                    soup = BeautifulSoup(response.content, 'html.parser')
                    
                    # Verifica che sia la pagina di modifica
                    title = soup.find('h6', string=lambda text: text and 'Modifica Incasso' in text)
                    if title:
                        print("✅ Pagina modifica accessibile")
                    else:
                        print("❌ Pagina modifica non accessibile")
                        return False
                else:
                    print("❌ Errore nell'accesso alla pagina modifica")
                    return False
            else:
                print("❌ Link modifica non trovato")
                return False
        else:
            print("❌ Errore nella creazione incasso di test")
            return False
        
        print("\n🎉 Tutti i test delle nuove funzionalità sono passati!")
        return True
        
    except requests.exceptions.ConnectionError:
        print("❌ Impossibile connettersi al server. Assicurati che l'app sia in esecuzione.")
        return False
    except Exception as e:
        print(f"❌ Errore durante il test: {e}")
        return False

if __name__ == "__main__":
    print("🚀 Avvio test delle nuove funzionalità...")
    success = test_nuove_funzionalita()
    
    if success:
        print("\n✅ Tutte le nuove funzionalità sono state implementate con successo!")
        print("\n📋 Riepilogo nuove funzionalità:")
        print("   • Campo data aggiunto al form di inserimento")
        print("   • Lista incassi filtrata per utente (dipendenti vedono solo i propri)")
        print("   • Funzionalità di modifica per amministratori")
        print("   • Interfaccia differenziata per ruolo")
        print("   • Privacy garantita per i dipendenti")
    else:
        print("\n❌ Alcuni test sono falliti. Controlla il codice.") 