#!/usr/bin/env python3
"""
Script per verificare che tutti i file necessari per il deployment siano presenti
"""
import os
import sys

def verifica_file_deployment():
    """Verifica che tutti i file fondamentali per il deployment siano presenti"""
    
    print("🔍 Verifica File Deployment")
    print("=" * 50)
    
    # Lista dei file fondamentali
    file_fondamentali = [
        'app.py',
        'requirements.txt',
        'Procfile',
        'runtime.txt',
        'wsgi.py'
    ]
    
    # Lista delle cartelle fondamentali
    cartelle_fondamentali = [
        'templates',
        'static'
    ]
    
    # Lista dei file statici
    file_statici = [
        'static/style.css',
        'static/script.js'
    ]
    
    # Contatori
    file_presenti = 0
    file_mancanti = 0
    cartelle_presenti = 0
    cartelle_mancanti = 0
    
    print("\n📁 Verifica File Fondamentali:")
    print("-" * 30)
    
    # Verifica file fondamentali
    for file in file_fondamentali:
        if os.path.exists(file):
            print(f"✅ {file}")
            file_presenti += 1
        else:
            print(f"❌ {file} - MANCANTE")
            file_mancanti += 1
    
    print(f"\n📁 Verifica Cartelle Fondamentali:")
    print("-" * 30)
    
    # Verifica cartelle fondamentali
    for cartella in cartelle_fondamentali:
        if os.path.exists(cartella) and os.path.isdir(cartella):
            print(f"✅ {cartella}/")
            cartelle_presenti += 1
        else:
            print(f"❌ {cartella}/ - MANCANTE")
            cartelle_mancanti += 1
    
    print(f"\n📁 Verifica File Statici:")
    print("-" * 30)
    
    # Verifica file statici
    for file in file_statici:
        if os.path.exists(file):
            print(f"✅ {file}")
            file_presenti += 1
        else:
            print(f"❌ {file} - MANCANTE")
            file_mancanti += 1
    
    # Verifica contenuto requirements.txt
    print(f"\n📋 Verifica Requirements.txt:")
    print("-" * 30)
    
    if os.path.exists('requirements.txt'):
        try:
            with open('requirements.txt', 'r') as f:
                content = f.read()
                if 'Flask' in content and 'gunicorn' in content:
                    print("✅ requirements.txt - Contenuto corretto")
                    file_presenti += 1
                else:
                    print("⚠️  requirements.txt - Contenuto incompleto")
                    file_mancanti += 1
        except Exception as e:
            print(f"❌ Errore lettura requirements.txt: {e}")
            file_mancanti += 1
    else:
        print("❌ requirements.txt - MANCANTE")
        file_mancanti += 1
    
    # Verifica contenuto Procfile
    print(f"\n📋 Verifica Procfile:")
    print("-" * 30)
    
    if os.path.exists('Procfile'):
        try:
            with open('Procfile', 'r') as f:
                content = f.read()
                if 'gunicorn' in content:
                    print("✅ Procfile - Contenuto corretto")
                    file_presenti += 1
                else:
                    print("⚠️  Procfile - Contenuto errato")
                    file_mancanti += 1
        except Exception as e:
            print(f"❌ Errore lettura Procfile: {e}")
            file_mancanti += 1
    else:
        print("❌ Procfile - MANCANTE")
        file_mancanti += 1
    
    # Verifica contenuto runtime.txt
    print(f"\n📋 Verifica Runtime.txt:")
    print("-" * 30)
    
    if os.path.exists('runtime.txt'):
        try:
            with open('runtime.txt', 'r') as f:
                content = f.read().strip()
                if 'python' in content:
                    print(f"✅ runtime.txt - Versione Python: {content}")
                    file_presenti += 1
                else:
                    print("⚠️  runtime.txt - Contenuto errato")
                    file_mancanti += 1
        except Exception as e:
            print(f"❌ Errore lettura runtime.txt: {e}")
            file_mancanti += 1
    else:
        print("❌ runtime.txt - MANCANTE")
        file_mancanti += 1
    
    # Verifica contenuto wsgi.py
    print(f"\n📋 Verifica Wsgi.py:")
    print("-" * 30)
    
    if os.path.exists('wsgi.py'):
        try:
            with open('wsgi.py', 'r') as f:
                content = f.read()
                if 'from app import app' in content:
                    print("✅ wsgi.py - Contenuto corretto")
                    file_presenti += 1
                else:
                    print("⚠️  wsgi.py - Contenuto errato")
                    file_mancanti += 1
        except Exception as e:
            print(f"❌ Errore lettura wsgi.py: {e}")
            file_mancanti += 1
    else:
        print("❌ wsgi.py - MANCANTE")
        file_mancanti += 1
    
    # Verifica template principali
    print(f"\n📋 Verifica Template Principali:")
    print("-" * 30)
    
    template_principali = [
        'templates/base.html',
        'templates/login.html',
        'templates/dashboard.html',
        'templates/nuovo_incasso.html',
        'templates/lista_incassi.html'
    ]
    
    for template in template_principali:
        if os.path.exists(template):
            print(f"✅ {template}")
            file_presenti += 1
        else:
            print(f"❌ {template} - MANCANTE")
            file_mancanti += 1
    
    # Riepilogo finale
    print(f"\n📊 Riepilogo Finale:")
    print("=" * 50)
    print(f"✅ File presenti: {file_presenti}")
    print(f"❌ File mancanti: {file_mancanti}")
    print(f"✅ Cartelle presenti: {cartelle_presenti}")
    print(f"❌ Cartelle mancanti: {cartelle_mancanti}")
    
    totale_file = file_presenti + file_mancanti
    totale_cartelle = cartelle_presenti + cartelle_mancanti
    
    if file_mancanti == 0 and cartelle_mancanti == 0:
        print(f"\n🎉 TUTTI I FILE SONO PRESENTI!")
        print("🚀 Il progetto è pronto per il deployment!")
        return True
    else:
        print(f"\n⚠️  ATTENZIONE: Mancano {file_mancanti} file e {cartelle_mancanti} cartelle")
        print("🔧 Risolvi i problemi prima del deployment")
        return False

if __name__ == "__main__":
    try:
        success = verifica_file_deployment()
        if success:
            print("\n✅ Deployment Ready!")
            sys.exit(0)
        else:
            print("\n❌ Deployment non pronto")
            sys.exit(1)
    except Exception as e:
        print(f"❌ Errore durante la verifica: {e}")
        sys.exit(1) 