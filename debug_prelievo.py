#!/usr/bin/env python3
"""
Script di debug per verificare i dati prelievo nel database
"""

from app import app, db, Incasso

def debug_prelievo():
    """Debug dei dati prelievo nel database"""
    with app.app_context():
        print("🔍 Debug dati prelievo nel database")
        print("=" * 50)
        
        # Ottieni tutti gli incassi
        incassi = Incasso.query.all()
        
        print(f"Trovati {len(incassi)} incassi nel database")
        print()
        
        for i, incasso in enumerate(incassi, 1):
            print(f"Incasso {i} (ID: {incasso.id}):")
            print(f"  Data: {incasso.data}")
            print(f"  Prelievo importo: {incasso.prelievo_importo} (tipo: {type(incasso.prelievo_importo)})")
            print(f"  Prelievo motivo: '{incasso.prelievo_motivo}' (tipo: {type(incasso.prelievo_motivo)})")
            print(f"  Prelievo importo > 0: {incasso.prelievo_importo > 0}")
            print()

if __name__ == "__main__":
    debug_prelievo() 