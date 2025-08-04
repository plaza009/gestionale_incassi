#!/usr/bin/env python3
"""
Script per verificare che il database sia stato pulito correttamente
"""
from app import app, db, User, Incasso, Cassaforte
from datetime import date

with app.app_context():
    # Conta tutti i dati
    incassi_totali = Incasso.query.count()
    movimenti_totali = Cassaforte.query.count()
    utenti_totali = User.query.count()
    
    print("🧹 Verifica database pulito")
    print("=" * 40)
    print(f"📈 Incassi: {incassi_totali}")
    print(f"💰 Movimenti cassaforte: {movimenti_totali}")
    print(f"👥 Utenti: {utenti_totali}")
    
    # Verifica utenti presenti
    print("\n👥 Utenti nel sistema:")
    print("-" * 20)
    for utente in User.query.all():
        ruolo = "Admin" if utente.is_admin else "Dipendente"
        print(f"   👤 {utente.username} ({utente.nome_completo}) - {ruolo}")
    
    # Verifica che non ci siano dati di test
    if incassi_totali == 0 and movimenti_totali == 0:
        print("\n✅ Database completamente pulito!")
        print("🚀 Pronto per i dati reali!")
    else:
        print("\n⚠️  Attenzione: Ci sono ancora dati nel database")
        if incassi_totali > 0:
            print(f"   📈 {incassi_totali} incassi ancora presenti")
        if movimenti_totali > 0:
            print(f"   💰 {movimenti_totali} movimenti cassaforte ancora presenti")
    
    # Verifica che gli utenti admin e dipendente siano presenti
    admin = User.query.filter_by(username='admin').first()
    dipendente = User.query.filter_by(username='dipendente').first()
    
    if admin and dipendente:
        print("\n✅ Utenti di base configurati correttamente")
        print("   👤 admin (Amministratore)")
        print("   👤 dipendente (Dipendente)")
    else:
        print("\n❌ Errore: Utenti di base mancanti")
        if not admin:
            print("   ❌ Admin mancante")
        if not dipendente:
            print("   ❌ Dipendente mancante")
    
    print("\n🎯 Sistema pronto per l'uso!")
    print("💡 Puoi ora iniziare a inserire i tuoi dati reali") 