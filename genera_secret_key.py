#!/usr/bin/env python3
"""
Script per generare una SECRET_KEY sicura per il deployment
"""
import secrets
import string

def genera_secret_key():
    """Genera una SECRET_KEY sicura per Flask"""
    
    # Genera una stringa sicura di 32 caratteri
    alphabet = string.ascii_letters + string.digits + "!@#$%^&*"
    secret_key = ''.join(secrets.choice(alphabet) for i in range(32))
    
    print("🔐 Generazione SECRET_KEY per deployment")
    print("=" * 50)
    print(f"🔑 SECRET_KEY generata:")
    print(f"   {secret_key}")
    print()
    print("📋 Copia questa chiave e usala come variabile d'ambiente:")
    print(f"   SECRET_KEY={secret_key}")
    print()
    print("💡 Aggiungi questa variabile su Render/Railway/PythonAnywhere")
    print("   nella sezione 'Environment Variables'")
    
    return secret_key

if __name__ == "__main__":
    genera_secret_key() 