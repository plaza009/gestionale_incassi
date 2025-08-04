#!/usr/bin/env python3
"""
Test per verificare che l'applicazione sia pronta per il deploy
"""

import requests
import time
import subprocess
import sys
import os

def test_local_app():
    """Testa l'applicazione locale"""
    print("🧪 Testando l'applicazione locale...")
    
    # Avvia l'applicazione in background
    try:
        process = subprocess.Popen([sys.executable, 'app.py'], 
                                 stdout=subprocess.PIPE, 
                                 stderr=subprocess.PIPE)
        
        # Aspetta che l'app si avvii
        time.sleep(3)
        
        # Testa la connessione
        response = requests.get('http://localhost:5000', timeout=5)
        
        if response.status_code == 200:
            print("✅ Applicazione locale funzionante!")
            return True
        else:
            print(f"❌ Errore: Status code {response.status_code}")
            return False
            
    except requests.exceptions.ConnectionError:
        print("❌ Impossibile connettersi all'applicazione")
        return False
    except Exception as e:
        print(f"❌ Errore: {e}")
        return False
    finally:
        # Termina il processo
        if 'process' in locals():
            process.terminate()
            process.wait()

def check_files():
    """Verifica che tutti i file necessari per il deploy siano presenti"""
    print("\n📁 Verificando file per il deploy...")
    
    required_files = [
        'app.py',
        'requirements.txt',
        'Procfile',
        'runtime.txt',
        'wsgi.py',
        'init_db.py',
        '.gitignore'
    ]
    
    missing_files = []
    for file in required_files:
        if os.path.exists(file):
            print(f"✅ {file}")
        else:
            print(f"❌ {file} - MANCANTE")
            missing_files.append(file)
    
    if missing_files:
        print(f"\n⚠️  File mancanti: {', '.join(missing_files)}")
        return False
    else:
        print("\n✅ Tutti i file necessari sono presenti!")
        return True

def check_requirements():
    """Verifica che requirements.txt contenga tutte le dipendenze necessarie"""
    print("\n📦 Verificando dipendenze...")
    
    required_packages = [
        'Flask',
        'Flask-SQLAlchemy',
        'Flask-Login',
        'gunicorn',
        'psycopg2-binary'
    ]
    
    try:
        with open('requirements.txt', 'r') as f:
            content = f.read()
            
        missing_packages = []
        for package in required_packages:
            if package in content:
                print(f"✅ {package}")
            else:
                print(f"❌ {package} - MANCANTE")
                missing_packages.append(package)
        
        if missing_packages:
            print(f"\n⚠️  Pacchetti mancanti: {', '.join(missing_packages)}")
            return False
        else:
            print("\n✅ Tutte le dipendenze sono presenti!")
            return True
            
    except FileNotFoundError:
        print("❌ File requirements.txt non trovato!")
        return False

def main():
    """Esegue tutti i test"""
    print("🚀 Test di preparazione per il deploy\n")
    
    # Test 1: Verifica file
    files_ok = check_files()
    
    # Test 2: Verifica dipendenze
    deps_ok = check_requirements()
    
    # Test 3: Test applicazione locale
    app_ok = test_local_app()
    
    # Risultato finale
    print("\n" + "="*50)
    if files_ok and deps_ok and app_ok:
        print("🎉 TUTTO PRONTO PER IL DEPLOY!")
        print("\n📋 Prossimi passi:")
        print("1. Carica il progetto su GitHub")
        print("2. Scegli una piattaforma di hosting (Render consigliato)")
        print("3. Segui la guida in DEPLOY.md")
        print("4. Configura le variabili d'ambiente")
        print("5. Esegui python init_db.py sul server")
    else:
        print("❌ CI SONO PROBLEMI DA RISOLVERE")
        if not files_ok:
            print("- Mancano alcuni file necessari")
        if not deps_ok:
            print("- Mancano alcune dipendenze")
        if not app_ok:
            print("- L'applicazione non si avvia correttamente")
    
    print("="*50)

if __name__ == '__main__':
    main() 