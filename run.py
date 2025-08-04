#!/usr/bin/env python3
"""
Avvio del Sistema Gestionale Incassi
"""

import sys
import os

# Aggiungi la directory corrente al path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import app

if __name__ == '__main__':
    print("🚀 Avvio Sistema Gestionale Incassi...")
    print("📊 Sistema di controllo incassi giornalieri")
    print("🔐 Credenziali di default:")
    print("   Username: admin")
    print("   Password: admin123")
    print("🌐 Apri il browser su: http://localhost:5000")
    print("⏹️  Premi Ctrl+C per fermare il server")
    print("-" * 50)
    
    try:
        app.run(debug=True, host='0.0.0.0', port=5000)
    except KeyboardInterrupt:
        print("\n👋 Sistema fermato dall'utente")
    except Exception as e:
        print(f"❌ Errore durante l'avvio: {e}")
        print("💡 Verifica che la porta 5000 sia libera") 