#!/usr/bin/env python3
"""
Test manuale per verificare le funzionalità implementate
"""

import requests
from bs4 import BeautifulSoup

def test_manual_verification():
    """Test manuale delle funzionalità"""
    print("🔍 Test manuale delle funzionalità...")
    
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
            
            # Salva il contenuto HTML per analisi
            with open('lista_incassi_debug.html', 'w', encoding='utf-8') as f:
                f.write(response.text)
            print("📄 Contenuto HTML salvato in 'lista_incassi_debug.html'")
            
            # Analizza il contenuto HTML
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Cerca tutti i link
            all_links = soup.find_all('a')
            print(f"🔗 Link totali trovati: {len(all_links)}")
            
            # Cerca link di modifica
            modifica_links = [link for link in all_links if '/modifica' in link.get('href', '')]
            print(f"✏️  Link modifica trovati: {len(modifica_links)}")
            
            # Cerca form
            all_forms = soup.find_all('form')
            print(f"📝 Form totali trovati: {len(all_forms)}")
            
            # Cerca form cambio stato
            stato_forms = [form for form in all_forms if 'cambia_stato' in form.get('action', '')]
            print(f"🔄 Form cambio stato trovati: {len(stato_forms)}")
            
            # Cerca input nascosti
            hidden_inputs = soup.find_all('input', type='hidden')
            print(f"👻 Input nascosti trovati: {len(hidden_inputs)}")
            
            # Cerca pulsanti
            all_buttons = soup.find_all('button')
            print(f"🔘 Pulsanti totali trovati: {len(all_buttons)}")
            
            # Cerca badge
            all_badges = soup.find_all('span', class_='badge')
            print(f"🏷️  Badge totali trovati: {len(all_badges)}")
            
            # Verifica presenza anomalie
            anomalie_badges = [b for b in all_badges if 'bg-danger' in b.get('class', []) or 'bg-success' in b.get('class', [])]
            print(f"⚠️  Badge anomalie trovati: {len(anomalie_badges)}")
            
            # Stampa dettagli dei form trovati
            for i, form in enumerate(stato_forms):
                print(f"  Form {i+1}: {form.get('action', 'N/A')}")
                inputs = form.find_all('input')
                for inp in inputs:
                    print(f"    Input: {inp.get('name', 'N/A')} = {inp.get('value', 'N/A')}")
            
            return True
        else:
            print("❌ Errore accesso lista incassi")
            return False
    else:
        print("❌ Login admin fallito!")
        return False

def main():
    """Esegue il test manuale"""
    print("🧪 Test manuale funzionalità gestione stato e anomalie\n")
    
    success = test_manual_verification()
    
    print("\n" + "="*50)
    if success:
        print("✅ Test manuale completato!")
        print("📄 Controlla il file 'lista_incassi_debug.html' per vedere il contenuto")
        print("🔍 Verifica manualmente nel browser: http://localhost:5000/incassi/lista")
    else:
        print("❌ Test manuale fallito!")
    
    print("="*50)

if __name__ == '__main__':
    main() 