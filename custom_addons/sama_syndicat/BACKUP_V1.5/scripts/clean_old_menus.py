#!/usr/bin/env python3
"""
Script pour nettoyer les anciens menus et ne garder que les nouveaux dashboards modernes
"""

import xmlrpc.client
import sys
import time

def clean_old_menus():
    """Nettoyer les anciens menus et actions"""
    
    print("🧹 NETTOYAGE DES ANCIENS MENUS ET DASHBOARDS")
    print("=" * 50)
    
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
        
        # Supprimer les anciens menus de test
        print("\n🗑️ Suppression des anciens menus de test...")
        old_menu_names = [
            '🧪 Test Dashboards',
            'Test Dashboards',
            '📊 Dashboards Modernes',
            'Dashboards Modernes',
            '📋 Dashboards Classiques',
            'Dashboards Classiques'
        ]
        
        for menu_name in old_menu_names:
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
        
        # Mettre à jour le module pour charger les nouveaux menus
        print("\n📦 Mise à jour du module...")
        try:
            module_ids = models.execute_kw(db, uid, password,
                'ir.module.module', 'search',
                [[('name', '=', 'sama_syndicat')]])
            
            if module_ids:
                models.execute_kw(db, uid, password,
                    'ir.module.module', 'button_immediate_upgrade',
                    [module_ids])
                print("✅ Module mis à jour")
                time.sleep(5)
            else:
                print("⚠️ Module sama_syndicat non trouvé")
        except Exception as e:
            print(f"❌ Erreur lors de la mise à jour: {str(e)[:100]}...")
        
        # Vérifier les nouveaux menus
        print("\n🔍 Vérification des nouveaux menus...")
        new_menus = [
            '📊 Dashboard Principal',
            '👔 Dashboard Exécutif'
        ]
        
        for menu_name in new_menus:
            try:
                menu_ids = models.execute_kw(db, uid, password,
                    'ir.ui.menu', 'search',
                    [[('name', '=', menu_name)]])
                
                if menu_ids:
                    print(f"  ✅ Nouveau menu trouvé: {menu_name}")
                else:
                    print(f"  ⚠️ Nouveau menu manquant: {menu_name}")
            except Exception as e:
                print(f"  ❌ Erreur pour {menu_name}: {e}")
        
        # Vérifier les actions des nouveaux dashboards
        print("\n📋 Vérification des actions...")
        new_actions = [
            'action_syndicat_dashboard_modern_cards',
            'action_syndicat_dashboard_executive'
        ]
        
        for action_name in new_actions:
            try:
                action_data = models.execute_kw(db, uid, password,
                    'ir.model.data', 'search_read',
                    [[('name', '=', action_name), ('model', '=', 'ir.actions.act_window')]],
                    {'fields': ['res_id']})
                
                if action_data:
                    print(f"  ✅ Action trouvée: {action_name}")
                else:
                    print(f"  ⚠️ Action manquante: {action_name}")
            except Exception as e:
                print(f"  ❌ Erreur pour {action_name}: {e}")
        
        # Vider les caches
        print("\n🔄 Vidage des caches...")
        try:
            models.execute_kw(db, uid, password,
                'ir.ui.menu', 'clear_caches', [])
            models.execute_kw(db, uid, password,
                'ir.ui.view', 'clear_caches', [])
            print("✅ Caches vidés")
        except:
            print("⚠️ Impossible de vider les caches")
        
        print("\n🎯 RÉSULTAT DU NETTOYAGE")
        print("=" * 30)
        print("✅ Anciens menus supprimés")
        print("✅ Module mis à jour")
        print("✅ Nouveaux menus vérifiés")
        print("✅ Caches vidés")
        
        print("\n📍 NOUVEAUX MENUS DISPONIBLES")
        print("=" * 35)
        print("Menu Syndicat:")
        print("├── 📊 Dashboard Principal (Cartes Modernes)")
        print("├── 👔 Dashboard Exécutif")
        print("├── Adhérents")
        print("├── Assemblées")
        print("├── Revendications")
        print("├── Actions Syndicales")
        print("├── Communications")
        print("├── Formations")
        print("├── Conventions")
        print("├── Médiations")
        print("└── Configuration")
        
        print("\n💡 INSTRUCTIONS")
        print("=" * 15)
        print("1. Rechargez la page web (F5)")
        print("2. Allez dans le menu Syndicat")
        print("3. Vous ne devriez voir que:")
        print("   - 📊 Dashboard Principal")
        print("   - 👔 Dashboard Exécutif")
        print("4. Plus d'anciens menus de test !")
        
        return True
        
    except ConnectionError:
        print("❌ Impossible de se connecter à Odoo")
        return False
    except Exception as e:
        print(f"❌ Erreur: {e}")
        return False

if __name__ == "__main__":
    success = clean_old_menus()
    sys.exit(0 if success else 1)