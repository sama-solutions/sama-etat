#!/usr/bin/env python3
"""
Script pour mettre à jour le module SAMA SYNDICAT
"""

import xmlrpc.client
import sys

def update_sama_syndicat():
    """Mettre à jour le module SAMA SYNDICAT"""
    
    # Configuration
    url = 'http://localhost:8070'
    db = 'sama_syndicat_final_1756812346'
    username = 'admin'
    password = 'admin'
    
    try:
        # Connexion à Odoo
        common = xmlrpc.client.ServerProxy(f'{url}/xmlrpc/2/common')
        uid = common.authenticate(db, username, password, {})
        
        if not uid:
            print("❌ Erreur d'authentification")
            return False
            
        print(f"✅ Connecté à Odoo (UID: {uid})")
        
        # Accès aux modèles
        models = xmlrpc.client.ServerProxy(f'{url}/xmlrpc/2/object')
        
        # Trouver le module
        module_ids = models.execute_kw(db, uid, password,
            'ir.module.module', 'search',
            [[('name', '=', 'sama_syndicat')]])
            
        if not module_ids:
            print("❌ Module sama_syndicat non trouvé")
            return False
            
        # Obtenir l'état du module
        module_info = models.execute_kw(db, uid, password,
            'ir.module.module', 'read',
            [module_ids], {'fields': ['name', 'state']})
            
        print(f"📦 Module trouvé: {module_info[0]['name']} - État: {module_info[0]['state']}")
        
        # Mettre à jour le module
        print("🔄 Mise à jour du module...")
        models.execute_kw(db, uid, password,
            'ir.module.module', 'button_immediate_upgrade',
            [module_ids])
            
        print("✅ Module mis à jour avec succès!")
        print("🔄 Les contrôleurs devraient maintenant être rechargés")
        return True
        
    except Exception as e:
        print(f"❌ Erreur: {e}")
        return False

if __name__ == "__main__":
    success = update_sama_syndicat()
    sys.exit(0 if success else 1)