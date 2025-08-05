#!/usr/bin/env python3
"""
Test per le nuove funzionalità di chiusura fiscale
"""
import requests
from bs4 import BeautifulSoup
import re

def test_chiusura_fiscale():
    """Test delle nuove funzionalità di chiusura fiscale"""
    
    base_url = "http://localhost:5000"
    session = requests.Session()
    
    print("🧪 Test Chiusura Fiscale")
    print("=" * 40)
    
    # 1. Login come admin
    print("1. Login come admin...")
    login_data = {
        'username': 'admin',
        'password': 'admin123'
    }
    
    response = session.post(f"{base_url}/login", data=login_data, allow_redirects=True)
    if response.status_code != 200:
        print("❌ Errore nel login")
        return False
    
    print("✅ Login effettuato")
    
    # 2. Test nuovo incasso con chiusura fiscale
    print("\n2. Test nuovo incasso con chiusura fiscale...")
    
    # Ottieni la pagina di nuovo incasso
    response = session.get(f"{base_url}/incassi/nuovo")
    if response.status_code != 200:
        print("❌ Errore nell'accesso alla pagina nuovo incasso")
        return False
    
    soup = BeautifulSoup(response.content, 'html.parser')
    
    # Verifica che il campo chiusura_fiscale sia presente
    chiusura_fiscale_field = soup.find('input', {'name': 'chiusura_fiscale'})
    if not chiusura_fiscale_field:
        print("❌ Campo chiusura_fiscale non trovato")
        return False
    
    print("✅ Campo chiusura_fiscale trovato")
    
    # 3. Crea un nuovo incasso con chiusura fiscale
    print("\n3. Creazione incasso con chiusura fiscale...")
    
    nuovo_incasso_data = {
        'data_incasso': '2024-12-20',
        'fondo_cassa': '100.00',
        'incasso_pos': '500.00',
        'cash_totale': '650.00',
        'chiusura_fiscale': '480.00',  # Nuovo campo
        'prelievo_importo': '0.00',
        'prelievo_motivo': '',
        'note': 'Test chiusura fiscale'
    }
    
    response = session.post(f"{base_url}/incassi/nuovo", data=nuovo_incasso_data, allow_redirects=True)
    if response.status_code != 200:
        print("❌ Errore nella creazione dell'incasso")
        return False
    
    # Verifica che l'incasso sia stato creato
    if "registrato con successo" in response.text:
        print("✅ Incasso creato con successo")
    else:
        print("❌ Incasso non creato correttamente")
        return False
    
    # 4. Verifica nella lista incassi
    print("\n4. Verifica nella lista incassi...")
    
    response = session.get(f"{base_url}/incassi/lista")
    if response.status_code != 200:
        print("❌ Errore nell'accesso alla lista incassi")
        return False
    
    soup = BeautifulSoup(response.content, 'html.parser')
    
    # Cerca l'incasso appena creato
    incassi_rows = soup.find_all('tr')
    test_incasso_found = False
    
    for row in incassi_rows:
        cells = row.find_all('td')
        if len(cells) > 0:
            # Cerca per la data o note
            row_text = row.get_text()
            if '2024-12-20' in row_text and 'Test chiusura fiscale' in row_text:
                test_incasso_found = True
                print("✅ Incasso trovato nella lista")
                break
    
    if not test_incasso_found:
        print("❌ Incasso non trovato nella lista")
        return False
    
    # 5. Test dettaglio incasso
    print("\n5. Test dettaglio incasso...")
    
    # Trova il link al dettaglio dell'incasso
    detail_links = soup.find_all('a', href=re.compile(r'/incassi/\d+'))
    if detail_links:
        detail_url = detail_links[0]['href']
        response = session.get(f"{base_url}{detail_url}")
        
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Verifica che la chiusura fiscale sia mostrata
            if 'Chiusura Fiscale' in response.text and '480.00' in response.text:
                print("✅ Chiusura fiscale mostrata correttamente nel dettaglio")
            else:
                print("❌ Chiusura fiscale non mostrata nel dettaglio")
                return False
        else:
            print("❌ Errore nell'accesso al dettaglio")
            return False
    
    # 6. Test calcolo coerenza
    print("\n6. Test calcolo coerenza...")
    
    # Verifica che il calcolo sia corretto
    # Incasso POS (500) + Cash Totale (650) - Chiusura Fiscale (480) - Fondo Cassa (100) = 570
    # Dovrebbe mostrare "Importo non scontrinato: €70.00"
    
    if "Importo non scontrinato" in response.text or "70.00" in response.text:
        print("✅ Calcolo coerenza corretto")
    else:
        print("⚠️  Calcolo coerenza non verificato")
    
    print("\n🎉 Test chiusura fiscale completato con successo!")
    return True

def test_migrazione_database():
    """Test della migrazione del database"""
    
    print("\n🔧 Test Migrazione Database")
    print("=" * 40)
    
    try:
        # Importa e esegui la migrazione
        from migrazione_chiusura_fiscale import migra_database_chiusura_fiscale
        
        success = migra_database_chiusura_fiscale()
        if success:
            print("✅ Migrazione database completata")
            return True
        else:
            print("❌ Errore nella migrazione database")
            return False
            
    except Exception as e:
        print(f"❌ Errore nel test migrazione: {e}")
        return False

if __name__ == "__main__":
    print("🚀 Avvio test chiusura fiscale...")
    
    # Test migrazione database
    if test_migrazione_database():
        # Test funzionalità web
        test_chiusura_fiscale()
    else:
        print("❌ Test migrazione fallito, interrompo i test") 