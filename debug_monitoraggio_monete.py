#!/usr/bin/env python3
"""
Script di debug per verificare i dati del monitoraggio monete
"""

from app import app, db, Cassaforte

def debug_monitoraggio_monete():
    """Debug dei dati del monitoraggio monete"""
    with app.app_context():
        print("🔍 Debug monitoraggio monete")
        print("=" * 50)
        
        # Ottieni tutti i movimenti cassaforte
        movimenti = Cassaforte.query.all()
        
        print(f"Trovati {len(movimenti)} movimenti nel database")
        print()
        
        for i, movimento in enumerate(movimenti, 1):
            print(f"Movimento {i} (ID: {movimento.id}):")
            print(f"  Data: {movimento.data}")
            print(f"  Tipo: {movimento.tipo_movimento}")
            print(f"  Importo totale: €{movimento.importo}")
            print(f"  Monete: €{movimento.monete_importo}")
            print(f"  Banconote: €{movimento.banconote_importo}")
            print(f"  Approvato: {movimento.approvato}")
            print(f"  Approvato da: {movimento.approvato_da}")
            print()
        
        # Calcola saldo monete
        saldo_monete = 0.0
        movimenti_approvati = Cassaforte.query.filter_by(approvato=True).all()
        
        for movimento in movimenti_approvati:
            if movimento.tipo_movimento == 'entrata':
                saldo_monete += movimento.monete_importo
            else:  # uscita
                saldo_monete -= movimento.monete_importo
        
        print(f"💰 Saldo monete (solo approvati): €{saldo_monete:.2f}")
        
        # Conta movimenti non approvati
        movimenti_non_approvati = Cassaforte.query.filter_by(approvato=False).all()
        print(f"📋 Movimenti non approvati: {len(movimenti_non_approvati)}")
        
        if movimenti_non_approvati:
            print("Movimenti non approvati:")
            for movimento in movimenti_non_approvati:
                print(f"  - ID {movimento.id}: {movimento.descrizione}")

if __name__ == "__main__":
    debug_monitoraggio_monete() 