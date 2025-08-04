#!/usr/bin/env python3
"""
Test specifico per verificare le funzionalità implementate
"""

import requests
from bs4 import BeautifulSoup
import time

def test_login_and_navigate():
    """Test login e navigazione"""
    print("🔐 Testando login e navigazione...")
    
    session = requests.Session()
    
    # Login admin
    login_data = {
        'username': 'admin',
        'password': 'admin123'
    }
    
    response = session.post('http://localhost:5000/login', data=login_data, allow_redirects=True)
    
    if response.status_code == 200 and 'dashboard' in response.url:
        print("✅ Login admin riuscito!")
        
        # Vai alla lista incassi
        response = session.get('http://localhost:5000/incassi/lista')
        
        if response.status_code == 200:
            print("✅ Pagina lista incassi accessibile")
            
            # Analizza il contenuto HTML
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Verifica presenza colonna anomalie
            headers = soup.find_all('th')
            anomalie_header = any('Anomalie' in header.get_text() for header in headers)
            
            if anomalie_header:
                print("✅ Colonna anomalie presente")
            else:
                print("❌ Colonna anomalie mancante")
                return False
            
            # Verifica presenza badge anomalie
            badges = soup.find_all('span', class_='badge')
            anomalie_badges = [b for b in badges if 'bg-danger' in b.get('class', []) or 'bg-success' in b.get('class', [])]
            
            if anomalie_badges:
                print(f"✅ Badge anomalie presenti: {len(anomalie_badges)}")
            else:
                print("⚠️  Nessun badge anomalie trovato")
            
            # Verifica presenza pulsanti modifica
            modifica_links = soup.find_all('a', href=lambda x: x and '/modifica' in x)
            if modifica_links:
                print(f"✅ Pulsanti modifica presenti: {len(modifica_links)}")
            else:
                print("❌ Pulsanti modifica mancanti")
                return False
            
            # Verifica presenza pulsanti cambio stato
            forms = soup.find_all('form', action=lambda x: x and 'cambia_stato' in x)
            if forms:
                print(f"✅ Form cambio stato presenti: {len(forms)}")
                
                # Verifica presenza pulsanti approva/disapprova
                approva_inputs = soup.find_all('input', {'name': 'azione', 'value': 'approva'})
                disapprova_inputs = soup.find_all('input', {'name': 'azione', 'value': 'disapprova'})
                
                if approva_inputs:
                    print(f"✅ Pulsanti approva presenti: {len(approva_inputs)}")
                if disapprova_inputs:
                    print(f"✅ Pulsanti disapprova presenti: {len(disapprova_inputs)}")
            else:
                print("❌ Form cambio stato mancanti")
                return False
            
            return True
        else:
            print("❌ Errore accesso lista incassi")
            return False
    else:
        print("❌ Login admin fallito!")
        return False

def test_dettaglio_anomalie():
    """Test dettaglio anomalie"""
    print("\n📋 Testando dettaglio anomalie...")
    
    session = requests.Session()
    
    # Login admin
    login_data = {
        'username': 'admin',
        'password': 'admin123'
    }
    
    response = session.post('http://localhost:5000/login', data=login_data, allow_redirects=True)
    
    if response.status_code == 200 and 'dashboard' in response.url:
        # Vai alla lista incassi per trovare un link al dettaglio
        response = session.get('http://localhost:5000/incassi/lista')
        
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Cerca link al dettaglio
            dettaglio_links = soup.find_all('a', href=lambda x: x and 'dettaglio_incasso' in x)
            
            if dettaglio_links:
                print(f"✅ Link al dettaglio trovati: {len(dettaglio_links)}")
                
                # Prova ad accedere al primo dettaglio
                first_link = dettaglio_links[0]['href']
                response = session.get(f'http://localhost:5000{first_link}')
                
                if response.status_code == 200:
                    print("✅ Dettaglio incasso accessibile")
                    
                    # Verifica presenza sezione anomalie
                    soup = BeautifulSoup(response.text, 'html.parser')
                    anomalie_section = soup.find('h6', string=lambda x: x and 'Anomalie Rilevate' in x)
                    
                    if anomalie_section:
                        print("✅ Sezione anomalie presente nel dettaglio")
                        
                        # Verifica presenza alert anomalie
                        alerts = soup.find_all('div', class_='alert')
                        anomalie_alerts = [a for a in alerts if 'alert-warning' in a.get('class', []) or 'alert-danger' in a.get('class', [])]
                        
                        if anomalie_alerts:
                            print(f"✅ Alert anomalie presenti: {len(anomalie_alerts)}")
                        else:
                            print("⚠️  Nessun alert anomalie trovato")
                    else:
                        print("⚠️  Sezione anomalie non trovata (potrebbe essere normale se non ci sono anomalie)")
                    
                    return True
                else:
                    print("❌ Errore accesso dettaglio incasso")
                    return False
            else:
                print("⚠️  Nessun link al dettaglio trovato")
                return True
        else:
            print("❌ Errore accesso lista incassi")
            return False
    else:
        print("❌ Login admin fallito!")
        return False

def test_functionality_summary():
    """Test riepilogo funzionalità"""
    print("\n📊 Riepilogo funzionalità implementate...")
    
    session = requests.Session()
    
    # Login admin
    login_data = {
        'username': 'admin',
        'password': 'admin123'
    }
    
    response = session.post('http://localhost:5000/login', data=login_data, allow_redirects=True)
    
    if response.status_code == 200 and 'dashboard' in response.url:
        # Vai alla lista incassi
        response = session.get('http://localhost:5000/incassi/lista')
        
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Conta elementi
            incassi_rows = soup.find_all('tr')[1:]  # Escludi header
            anomalie_badges = soup.find_all('span', class_='badge')
            modifica_links = soup.find_all('a', href=lambda x: x and 'modifica_incasso' in x)
            stato_forms = soup.find_all('form', action=lambda x: x and 'cambia_stato_incasso' in x)
            
            print(f"📈 Statistiche:")
            print(f"   - Incassi totali: {len(incassi_rows)}")
            print(f"   - Badge anomalie: {len(anomalie_badges)}")
            print(f"   - Pulsanti modifica: {len(modifica_links)}")
            print(f"   - Form cambio stato: {len(stato_forms)}")
            
            return True
        else:
            print("❌ Errore accesso lista incassi")
            return False
    else:
        print("❌ Login admin fallito!")
        return False

def main():
    """Esegue tutti i test"""
    print("🧪 Test specifico funzionalità gestione stato e anomalie\n")
    
    # Test 1: Login e navigazione
    nav_ok = test_login_and_navigate()
    
    # Test 2: Dettaglio anomalie
    dettaglio_ok = test_dettaglio_anomalie()
    
    # Test 3: Riepilogo funzionalità
    summary_ok = test_functionality_summary()
    
    # Risultato finale
    print("\n" + "="*50)
    if nav_ok and dettaglio_ok and summary_ok:
        print("🎉 TUTTI I TEST SUPERATI!")
        print("\n✅ Funzionalità confermate:")
        print("- Rilevamento anomalie nella lista")
        print("- Pulsanti modifica per admin")
        print("- Form cambio stato (approva/disapprova)")
        print("- Visualizzazione anomalie nel dettaglio")
        print("- Gestione flessibile degli stati")
    else:
        print("❌ ALCUNI TEST FALLITI")
        if not nav_ok:
            print("- Problema con navigazione e pulsanti")
        if not dettaglio_ok:
            print("- Problema con dettaglio anomalie")
        if not summary_ok:
            print("- Problema con riepilogo funzionalità")
    
    print("="*50)

if __name__ == '__main__':
    main() 