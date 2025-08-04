#!/usr/bin/env python3
"""
Script di debug per ispezionare l'HTML della pagina dettaglio
"""

import requests
from bs4 import BeautifulSoup
import sys

def debug_html_prelievo():
    """Debug dell'HTML della pagina dettaglio"""
    base_url = "http://localhost:5000"
    
    print("🔍 Debug HTML pagina dettaglio")
    print("=" * 50)
    
    # Login come admin
    session = requests.Session()
    login_data = {
        'username': 'admin',
        'password': 'admin123'
    }
    
    response = session.post(f"{base_url}/login", data=login_data, allow_redirects=True)
    if response.status_code != 200:
        print("❌ Errore nel login")
        return
    
    print("✅ Login riuscito")
    
    # Testa diversi incassi
    for incasso_id in range(1, 5):
        print(f"\n--- Incasso {incasso_id} ---")
        response = session.get(f"{base_url}/incassi/{incasso_id}")
        
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Cerca tutti gli h6
            h6_elements = soup.find_all('h6')
            print(f"Trovati {len(h6_elements)} elementi h6:")
            for i, h6 in enumerate(h6_elements):
                print(f"  {i+1}: '{h6.get_text(strip=True)}'")
            
            # Cerca elementi con "Prelievo"
            prelievo_elements = soup.find_all(string=lambda text: text and 'Prelievo' in text)
            print(f"\nTrovati {len(prelievo_elements)} elementi con 'Prelievo':")
            for i, elem in enumerate(prelievo_elements):
                print(f"  {i+1}: '{elem.strip()}'")
            
            # Cerca elementi con "Importo"
            importo_elements = soup.find_all(string=lambda text: text and 'Importo' in text)
            print(f"\nTrovati {len(importo_elements)} elementi con 'Importo':")
            for i, elem in enumerate(importo_elements):
                print(f"  {i+1}: '{elem.strip()}'")
            
            # Cerca elementi con "Motivo"
            motivo_elements = soup.find_all(string=lambda text: text and 'Motivo' in text)
            print(f"\nTrovati {len(motivo_elements)} elementi con 'Motivo':")
            for i, elem in enumerate(motivo_elements):
                print(f"  {i+1}: '{elem.strip()}'")
        else:
            print(f"❌ Errore nell'accesso all'incasso {incasso_id}")

if __name__ == "__main__":
    debug_html_prelievo() 