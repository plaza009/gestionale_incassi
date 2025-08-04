#!/usr/bin/env python3
"""
Script di debug per ispezionare l'HTML della pagina lista movimenti cassaforte
"""

import requests
from bs4 import BeautifulSoup
import sys

def debug_html_monete():
    """Debug dell'HTML della pagina lista movimenti cassaforte"""
    base_url = "http://localhost:5000"
    
    print("🔍 Debug HTML pagina lista movimenti cassaforte")
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
    
    # Accesso alla lista movimenti
    response = session.get(f"{base_url}/cassaforte/lista")
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Cerca elementi con "Saldo Monete Attuale"
        saldo_elements = soup.find_all(string=lambda text: text and 'Saldo Monete Attuale' in text)
        print(f"Trovati {len(saldo_elements)} elementi con 'Saldo Monete Attuale'")
        
        # Cerca elementi con "€" e numeri
        euro_elements = soup.find_all(string=lambda text: text and '€' in text and any(c.isdigit() for c in text))
        print(f"Trovati {len(euro_elements)} elementi con '€' e numeri:")
        for i, elem in enumerate(euro_elements):
            print(f"  {i+1}: '{elem.strip()}'")
        
        # Cerca elementi con "Livello Minimo" o "OK"
        livello_elements = soup.find_all(string=lambda text: text and ('Livello Minimo' in text or 'OK' in text))
        print(f"Trovati {len(livello_elements)} elementi con 'Livello Minimo' o 'OK':")
        for i, elem in enumerate(livello_elements):
            print(f"  {i+1}: '{elem.strip()}'")
        
        # Cerca pulsanti con "Approva"
        pulsanti_approva = soup.find_all('button', string=lambda text: text and 'Approva' in text)
        print(f"Trovati {len(pulsanti_approva)} pulsanti con 'Approva'")
        
        # Cerca form con "approva"
        form_approva = soup.find_all('form', action=lambda action: action and 'approva' in action)
        print(f"Trovati {len(form_approva)} form con 'approva'")
        
        # Salva l'HTML per ispezione
        with open('lista_movimenti_cassaforte_debug.html', 'w', encoding='utf-8') as f:
            f.write(response.text)
        print("💾 HTML salvato in 'lista_movimenti_cassaforte_debug.html'")
        
    else:
        print(f"❌ Errore nell'accesso alla lista movimenti: {response.status_code}")

if __name__ == "__main__":
    debug_html_monete() 