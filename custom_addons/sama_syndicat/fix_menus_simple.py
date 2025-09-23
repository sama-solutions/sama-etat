#!/usr/bin/env python3
"""
Script simple pour corriger les menus des dashboards
À exécuter quand Odoo est déjà démarré
"""

import xmlrpc.client
import sys

def fix_menus_simple():
    """Corriger les menus de manière simple"""
    
    print("🔧 CORRECTION SIMPLE DES MENUS")
    print("=" * 35)
    
    # Configuration
    url = 'http://localhost:8070'
    db = 'sama_syndicat_final_1756812346'
    username = 'admin'
    password = 'admin'
    
    try:
        # Connexion
        common = xmlrpc.client.ServerProxy(f'{url}/xmlrpc/2/common')
        uid = common.authenticate(db, username, password, {})
        
        if not uid:
            print("❌ Erreur d'authentification")
            print("💡 Vérifiez que Odoo est démarré et accessible")
            return False
        
        print(f"✅ Connecté à Odoo (UID: {uid})")
        
        models = xmlrpc.client.ServerProxy(f'{url}/xmlrpc/2/object')
        
        # Mettre à jour le module
        print("📦 Mise à jour du module...")
        try:
            module_ids = models.execute_kw(db, uid, password,
                'ir.module.module', 'search',
                [[('name', '=', 'sama_syndicat')]])
            
            if module_ids:
                models.execute_kw(db, uid, password,
                    'ir.module.module', 'button_immediate_upgrade',
                    [module_ids])
                print("✅ Module sama_syndicat mis à jour")
            else:
                print("⚠️ Module sama_syndicat non trouvé")
        except Exception as e:
            print(f"⚠️ Erreur lors de la mise à jour: {e}")
        
        # Vérifier les menus
        print("🔍 Vérification des menus...")
        
        # Chercher le menu de test
        test_menus = models.execute_kw(db, uid, password,
            'ir.ui.menu', 'search_read',
            [[('name', 'like', 'Test Dashboard')]],
            {'fields': ['name', 'id']})
        
        if test_menus:
            print(f"✅ Menu de test trouvé: {test_menus[0]['name']} (ID: {test_menus[0]['id']})")
        else:
            print("⚠️ Menu de test non trouvé")
        
        # Chercher tous les menus Syndicat
        syndicat_menus = models.execute_kw(db, uid, password,
            'ir.ui.menu', 'search_read',
            [[('name', 'like', 'Syndicat')]],
            {'fields': ['name', 'id', 'parent_id']})
        
        print(f"📂 Menus Syndicat trouvés: {len(syndicat_menus)}")
        for menu in syndicat_menus:
            parent_name = "Racine"
            if menu['parent_id']:
                parent_name = f"Parent ID: {menu['parent_id'][0]}"
            print(f"  - {menu['name']} (ID: {menu['id']}) - {parent_name}")
        
        # Vider le cache
        print("🔄 Vidage du cache...")
        try:
            models.execute_kw(db, uid, password,
                'ir.ui.menu', 'clear_caches', [])
            print("✅ Cache vidé")
        except:
            print("⚠️ Impossible de vider le cache")
        
        print("\n🎯 INSTRUCTIONS")
        print("=" * 15)
        print("1. Rechargez la page web (F5)")
        print("2. Allez dans le menu Syndicat")
        print("3. Cherchez '🧪 Test Dashboards'")
        print("4. Si absent, redémarrez Odoo complètement")
        
        return True
        
    except ConnectionError:
        print("❌ Impossible de se connecter à Odoo")
        print("💡 Vérifiez que Odoo est démarré sur le port 8070")
        print("🚀 Utilisez: python3 quick_start.py")
        return False
    except Exception as e:
        print(f"❌ Erreur: {e}")
        return False

if __name__ == "__main__":
    success = fix_menus_simple()
    sys.exit(0 if success else 1)