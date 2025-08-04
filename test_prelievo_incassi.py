#!/usr/bin/env python3
"""
Test script per verificare la funzionalità prelievo negli incassi
"""

import requests
from bs4 import BeautifulSoup
import sys
import time

def test_prelievo_incassi():
    """Testa la funzionalità prelievo negli incassi"""
    base_url = "http://localhost:5000"
    
    print("🧪 Test funzionalità prelievo incassi")
    print("=" * 50)
    
    # Test 1: Login come dipendente
    print("\n1. Login come dipendente...")
    session = requests.Session()
    
    login_data = {
        'username': 'dipendente',
        'password': 'dipendente123'
    }
    
    response = session.post(f"{base_url}/login", data=login_data, allow_redirects=True)
    if response.status_code != 200:
        print("❌ Errore nel login dipendente")
        return False
    
    # Verifica che il login sia andato a buon fine
    if "Dashboard" not in response.text:
        print("❌ Login dipendente fallito")
        return False
    
    print("✅ Login dipendente riuscito")
    
    # Test 2: Accesso al form nuovo incasso
    print("\n2. Accesso al form nuovo incasso...")
    response = session.get(f"{base_url}/incassi/nuovo")
    if response.status_code != 200:
        print("❌ Errore nell'accesso al form nuovo incasso")
        return False
    
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Verifica presenza campi prelievo
    campo_prelievo_importo = soup.find('input', {'name': 'prelievo_importo'})
    campo_prelievo_motivo_select = soup.find('select', {'id': 'prelievo_motivo_select'})
    campo_prelievo_motivo = soup.find('input', {'name': 'prelievo_motivo'})
    
    if not campo_prelievo_importo:
        print("❌ Campo prelievo importo non trovato")
        return False
    
    if not campo_prelievo_motivo_select:
        print("❌ Campo prelievo motivo select non trovato")
        return False
    
    if not campo_prelievo_motivo:
        print("❌ Campo prelievo motivo input non trovato")
        return False
    
    print("✅ Campi prelievo presenti nel form")
    
    # Verifica opzioni del select
    opzioni_select = campo_prelievo_motivo_select.find_all('option')
    opzioni_valori = [opt.get('value') for opt in opzioni_select]
    
    opzioni_attese = ['', 'fuori busta', 'fornitore', 'custom']
    for opzione in opzioni_attese:
        if opzione not in opzioni_valori:
            print(f"❌ Opzione '{opzione}' mancante nel select")
            return False
    
    print("✅ Opzioni select corrette")
    
    # Test 3: Verifica lista incassi con prelievi
    print("\n3. Verifica lista incassi con prelievi...")
    response = session.get(f"{base_url}/incassi/lista")
    if response.status_code != 200:
        print("❌ Errore nell'accesso alla lista incassi")
        return False
    
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Verifica presenza colonna prelievo
    headers = soup.find_all('th')
    header_prelievo = None
    for header in headers:
        if 'Prelievo' in header.text:
            header_prelievo = header
            break
    
    if not header_prelievo:
        print("❌ Colonna prelievo non trovata nella lista")
        return False
    
    print("✅ Colonna prelievo presente nella lista")
    
    # Verifica presenza badge prelievo
    badges_prelievo = soup.find_all('span', class_='badge bg-info')
    if not badges_prelievo:
        print("❌ Badge prelievo non trovati")
        return False
    
    print(f"✅ Trovati {len(badges_prelievo)} badge prelievo")
    
    # Test 4: Login come admin e verifica dettaglio
    print("\n4. Test accesso admin e dettaglio prelievo...")
    session = requests.Session()
    
    login_data_admin = {
        'username': 'admin',
        'password': 'admin123'
    }
    
    response = session.post(f"{base_url}/login", data=login_data_admin, allow_redirects=True)
    if response.status_code != 200:
        print("❌ Errore nel login admin")
        return False
    
    if "Dashboard" not in response.text:
        print("❌ Login admin fallito")
        return False
    
    print("✅ Login admin riuscito")
    
    # Accesso al dettaglio di un incasso con prelievo
    # Prova diversi ID per trovare un incasso con prelievo
    incasso_con_prelievo_trovato = False
    for incasso_id in range(1, 5):  # Prova incassi da 1 a 4
        response = session.get(f"{base_url}/incassi/{incasso_id}")
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Verifica presenza sezione prelievo
            h6_elements = soup.find_all('h6')
            sezione_prelievo = None
            for h6 in h6_elements:
                if 'Informazioni Prelievo' in h6.get_text():
                    sezione_prelievo = h6
                    break
            
            if sezione_prelievo:
                print(f"✅ Sezione informazioni prelievo trovata nell'incasso {incasso_id}")
                incasso_con_prelievo_trovato = True
                
                # Verifica presenza importo e motivo
                importo_prelievo = soup.find(string=lambda text: text and 'Importo Prelievo:' in text)
                motivo_prelievo = soup.find(string=lambda text: text and 'Motivo:' in text)
                
                if not importo_prelievo:
                    print("❌ Importo prelievo non trovato")
                    return False
                
                if not motivo_prelievo:
                    print("❌ Motivo prelievo non trovato")
                    return False
                
                print("✅ Importo e motivo prelievo presenti")
                break
    
    if not incasso_con_prelievo_trovato:
        print("❌ Nessun incasso con prelievo trovato")
        return False
    
    # Test 5: Verifica form modifica con prelievo
    print("\n5. Test form modifica con prelievo...")
    response = session.get(f"{base_url}/incassi/1/modifica")
    if response.status_code != 200:
        print("❌ Errore nell'accesso al form modifica")
        return False
    
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Verifica presenza campi prelievo nel form modifica
    campo_prelievo_importo_mod = soup.find('input', {'name': 'prelievo_importo'})
    campo_prelievo_motivo_select_mod = soup.find('select', {'id': 'prelievo_motivo_select'})
    campo_prelievo_motivo_mod = soup.find('input', {'name': 'prelievo_motivo'})
    
    if not campo_prelievo_importo_mod:
        print("❌ Campo prelievo importo non trovato nel form modifica")
        return False
    
    if not campo_prelievo_motivo_select_mod:
        print("❌ Campo prelievo motivo select non trovato nel form modifica")
        return False
    
    if not campo_prelievo_motivo_mod:
        print("❌ Campo prelievo motivo input non trovato nel form modifica")
        return False
    
    print("✅ Campi prelievo presenti nel form modifica")
    
    print("\n🎉 Tutti i test di prelievo completati con successo!")
    return True

if __name__ == "__main__":
    try:
        success = test_prelievo_incassi()
        if success:
            print("\n✅ Test prelievo incassi: SUCCESSO")
            sys.exit(0)
        else:
            print("\n❌ Test prelievo incassi: FALLITO")
            sys.exit(1)
    except Exception as e:
        print(f"\n❌ Errore durante il test: {e}")
        sys.exit(1) 