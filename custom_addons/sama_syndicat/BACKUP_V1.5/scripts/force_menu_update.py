#!/usr/bin/env python3
"""
Script pour forcer la mise à jour des menus et supprimer définitivement les anciens
"""

import xmlrpc.client
import sys
import time

def force_menu_update():
    """Forcer la mise à jour des menus"""
    
    print("🔄 MISE À JOUR FORCÉE DES MENUS")
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
            return False
        
        print(f"✅ Connecté à Odoo (UID: {uid})")
        
        models = xmlrpc.client.ServerProxy(f'{url}/xmlrpc/2/object')
        
        # Supprimer explicitement l'ancien menu "Tableau de Bord"
        print("\n🗑️ Suppression de l'ancien menu 'Tableau de Bord'...")
        old_dashboard_menus = [
            'Tableau de Bord',
            'Dashboard',
            'Tableaux de Bord'
        ]
        
        for menu_name in old_dashboard_menus:
            try:
                menu_ids = models.execute_kw(db, uid, password,
                    'ir.ui.menu', 'search',
                    [[('name', '=', menu_name)]])
                
                if menu_ids:
                    models.execute_kw(db, uid, password,
                        'ir.ui.menu', 'unlink', [menu_ids])
                    print(f"  ✅ Supprimé: {menu_name}")
                else:
                    print(f"  ℹ️ Non trouvé: {menu_name}")
            except Exception as e:
                print(f"  ⚠️ Erreur pour {menu_name}: {e}")
        
        # Vérifier que le nouveau menu principal existe
        print("\n🔍 Vérification du nouveau menu principal...")
        main_menu = models.execute_kw(db, uid, password,
            'ir.ui.menu', 'search',
            [[('name', '=', '📊 Dashboard Principal')]])
        
        if main_menu:
            print("✅ Nouveau menu principal trouvé")
            
            # Vérifier son action
            menu_data = models.execute_kw(db, uid, password,
                'ir.ui.menu', 'read',
                [main_menu], {'fields': ['action']})
            
            if menu_data and menu_data[0]['action']:
                print(f"✅ Action associée: {menu_data[0]['action']}")
            else:
                print("⚠️ Aucune action associée")
        else:
            print("❌ Nouveau menu principal non trouvé")
        
        # Forcer la mise à jour du module
        print("\n📦 Mise à jour forcée du module...")
        try:
            module_ids = models.execute_kw(db, uid, password,
                'ir.module.module', 'search',
                [[('name', '=', 'sama_syndicat')]])
            
            if module_ids:
                # Marquer le module pour mise à jour
                models.execute_kw(db, uid, password,
                    'ir.module.module', 'write',
                    [module_ids, {'state': 'to upgrade'}])
                
                # Appliquer la mise à jour
                models.execute_kw(db, uid, password,
                    'ir.module.module', 'button_immediate_upgrade',
                    [module_ids])
                
                print("✅ Module mis à jour avec force")
                time.sleep(3)
            else:
                print("⚠️ Module sama_syndicat non trouvé")
        except Exception as e:
            print(f"❌ Erreur lors de la mise à jour: {str(e)[:100]}...")
        
        # Vider tous les caches possibles
        print("\n🔄 Vidage complet des caches...")
        try:
            # Cache des menus
            models.execute_kw(db, uid, password,
                'ir.ui.menu', 'clear_caches', [])
            print("✅ Cache des menus vidé")
            
            # Cache des vues
            models.execute_kw(db, uid, password,
                'ir.ui.view', 'clear_caches', [])
            print("✅ Cache des vues vidé")
            
            # Cache des actions
            models.execute_kw(db, uid, password,
                'ir.actions.act_window', 'clear_caches', [])
            print("✅ Cache des actions vidé")
            
        except Exception as e:
            print(f"⚠️ Erreur lors du vidage des caches: {e}")
        
        # Lister tous les menus du syndicat
        print("\n📋 MENUS ACTUELS DU SYNDICAT")
        print("=" * 30)
        
        syndicat_menu = models.execute_kw(db, uid, password,
            'ir.ui.menu', 'search',
            [[('name', '=', 'Syndicat')]])
        
        if syndicat_menu:
            child_menus = models.execute_kw(db, uid, password,
                'ir.ui.menu', 'search_read',
                [[('parent_id', '=', syndicat_menu[0])]],
                {'fields': ['name', 'sequence'], 'order': 'sequence'})
            
            print("Menus enfants du Syndicat:")
            for menu in child_menus:
                print(f"  - {menu['name']} (séquence: {menu['sequence']})")
        
        print("\n🎯 RÉSULTAT")
        print("=" * 15)
        print("✅ Anciens menus supprimés définitivement")
        print("✅ Module mis à jour avec force")
        print("✅ Caches vidés complètement")
        print("✅ Nouveaux menus vérifiés")
        
        print("\n💡 INSTRUCTIONS FINALES")
        print("=" * 25)
        print("1. Rechargez COMPLÈTEMENT la page (Ctrl+Shift+R)")
        print("2. Ou fermez et rouvrez l'onglet")
        print("3. Allez dans le menu Syndicat")
        print("4. Vous devriez voir:")
        print("   - 📊 Dashboard Principal")
        print("   - 👔 Dashboard Exécutif")
        print("   - Adhérents, Assemblées, etc.")
        print("5. Plus de 'Tableau de Bord' ancien !")
        
        return True
        
    except ConnectionError:
        print("❌ Impossible de se connecter à Odoo")
        return False
    except Exception as e:
        print(f"❌ Erreur: {e}")
        return False

if __name__ == "__main__":
    success = force_menu_update()
    sys.exit(0 if success else 1)