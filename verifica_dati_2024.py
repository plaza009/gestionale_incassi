#!/usr/bin/env python3
"""
Script per verificare i dati inseriti nel database
"""
from app import app, db, Incasso, Cassaforte
from datetime import date

with app.app_context():
    # Conta incassi 2024
    incassi_2024 = Incasso.query.filter(
        Incasso.data >= date(2024, 1, 1),
        Incasso.data <= date(2024, 12, 31)
    ).count()
    
    # Conta movimenti 2024
    movimenti_2024 = Cassaforte.query.filter(
        Cassaforte.data >= date(2024, 1, 1),
        Cassaforte.data <= date(2024, 12, 31)
    ).count()
    
    # Conta prelievi 2024
    prelievi_2024 = Incasso.query.filter(
        Incasso.data >= date(2024, 1, 1),
        Incasso.data <= date(2024, 12, 31),
        Incasso.prelievo_importo > 0
    ).count()
    
    print("📊 Verifica dati database 2024:")
    print("=" * 40)
    print(f"📈 Incassi totali: {incassi_2024}")
    print(f"💰 Movimenti cassaforte: {movimenti_2024}")
    print(f"💸 Prelievi: {prelievi_2024}")
    
    # Verifica alcuni dati di esempio
    print("\n📋 Esempi di dati inseriti:")
    print("-" * 30)
    
    # Primi 3 incassi
    primi_incassi = Incasso.query.filter(
        Incasso.data >= date(2024, 1, 1)
    ).order_by(Incasso.data).limit(3).all()
    
    for incasso in primi_incassi:
        print(f"📅 {incasso.data.strftime('%d/%m/%Y')} - €{incasso.incasso_pos:.2f} POS + €{incasso.cash_totale_cassa - incasso.fondo_cassa_iniziale:.2f} Cash")
        if incasso.prelievo_importo > 0:
            print(f"   💸 Prelievo: €{incasso.prelievo_importo:.2f} - {incasso.prelievo_motivo}")
    
    # Primi 3 movimenti
    primi_movimenti = Cassaforte.query.filter(
        Cassaforte.data >= date(2024, 1, 1)
    ).order_by(Cassaforte.data).limit(3).all()
    
    for movimento in primi_movimenti:
        print(f"📅 {movimento.data.strftime('%d/%m/%Y')} - {movimento.tipo_movimento.title()}: €{movimento.importo:.2f}")
    
    print("\n✅ Database popolato con successo!")
    print("🚀 Il sistema è pronto per i test!") 