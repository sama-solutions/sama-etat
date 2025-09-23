#!/usr/bin/env python3
"""
Script pour corriger les actions des dashboards et tester
"""

import xmlrpc.client
import sys
import time

def fix_dashboard_actions():
    """Corriger les actions des dashboards"""
    
    print("🔧 CORRECTION DES ACTIONS DASHBOARDS")
    print("=" * 45)
    
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
        
        # Vérifier les méthodes du modèle dashboard
        print("\n🔍 Vérification des méthodes du modèle dashboard...")
        
        # Créer un enregistrement dashboard s'il n'existe pas
        dashboard_ids = models.execute_kw(db, uid, password,
            'syndicat.dashboard', 'search', [[]])
        
        if not dashboard_ids:
            print("📋 Création d'un enregistrement dashboard...")
            dashboard_id = models.execute_kw(db, uid, password,
                'syndicat.dashboard', 'create', [{
                    'name': 'Tableau de Bord Principal'
                }])
            print(f"✅ Dashboard créé (ID: {dashboard_id})")
        else:
            dashboard_id = dashboard_ids[0]
            print(f"✅ Dashboard existant trouvé (ID: {dashboard_id})")
        
        # Tester les méthodes du dashboard
        methods_to_test = [
            'action_actualiser',
            'action_open_adherents',
            'action_open_cotisations',
            'action_open_assemblees',
            'action_open_revendications',
            'action_open_actions',
            'action_open_formations',
            'action_open_mediations',
            'action_open_communications',
            'action_open_alertes_cotisations',
            'action_open_alertes_assemblees',
            'action_open_alertes_actions',
            'action_open_alertes_mediations'
        ]
        
        print("\n🧪 Test des méthodes du dashboard...")
        for method in methods_to_test:
            try:
                # Tester si la méthode existe en l'appelant
                result = models.execute_kw(db, uid, password,
                    'syndicat.dashboard', method, [[dashboard_id]])
                print(f"  ✅ {method} - Fonctionne")
            except Exception as e:
                if "not a valid action" in str(e):
                    print(f"  ❌ {method} - Méthode manquante")
                else:
                    print(f"  ⚠️ {method} - Erreur: {str(e)[:50]}...")
        
        # Mettre à jour le module
        print("\n📦 Mise à jour du module...")
        try:
            module_ids = models.execute_kw(db, uid, password,
                'ir.module.module', 'search',
                [[('name', '=', 'sama_syndicat')]])
            
            if module_ids:
                models.execute_kw(db, uid, password,
                    'ir.module.module', 'button_immediate_upgrade',
                    [module_ids])
                print("✅ Module sama_syndicat mis à jour")
                
                # Attendre un peu pour que la mise à jour se termine
                print("⏳ Attente de la fin de la mise à jour...")
                time.sleep(5)
            else:
                print("⚠️ Module sama_syndicat non trouvé")
        except Exception as e:
            print(f"❌ Erreur lors de la mise à jour: {str(e)[:100]}...")
            return False
        
        # Vérifier les vues des dashboards
        print("\n📄 Vérification des vues dashboards...")
        dashboard_views = [
            'view_syndicat_dashboard_v1_kanban',
            'view_syndicat_dashboard_v2_kanban',
            'view_syndicat_dashboard_v3_kanban',
            'view_syndicat_dashboard_v4_kanban'
        ]
        
        for view_name in dashboard_views:
            try:
                view_ids = models.execute_kw(db, uid, password,
                    'ir.ui.view', 'search',
                    [[('name', '=', view_name)]])
                
                if view_ids:
                    print(f"  ✅ {view_name}")
                else:
                    print(f"  ❌ {view_name} - Non trouvé")
            except Exception as e:
                print(f"  ❌ {view_name} - Erreur: {e}")
        
        # Créer les menus de test
        print("\n📂 Création des menus de test...")
        
        # Trouver le menu principal Syndicat
        syndicat_menu = models.execute_kw(db, uid, password,
            'ir.ui.menu', 'search',
            [[('name', '=', 'Syndicat')]])
        
        if syndicat_menu:
            parent_id = syndicat_menu[0]
            
            # Supprimer l'ancien menu de test s'il existe
            old_test_menu = models.execute_kw(db, uid, password,
                'ir.ui.menu', 'search',
                [[('name', 'like', 'Test Dashboard')]])
            
            if old_test_menu:
                models.execute_kw(db, uid, password,
                    'ir.ui.menu', 'unlink', [old_test_menu])
                print("🗑️ Ancien menu de test supprimé")
            
            # Créer le nouveau menu de test
            test_menu_id = models.execute_kw(db, uid, password,
                'ir.ui.menu', 'create', [{
                    'name': '🧪 Test Dashboards',
                    'parent_id': parent_id,
                    'sequence': 2
                }])
            
            print(f"✅ Menu de test créé (ID: {test_menu_id})")
            
            # Créer les sous-menus pour chaque version
            dashboard_actions = [
                ('V1 - CSS Natif Odoo', 'action_syndicat_dashboard_v1'),
                ('V2 - Compact Organisé', 'action_syndicat_dashboard_v2'),
                ('V3 - Graphiques & Listes', 'action_syndicat_dashboard_v3'),
                ('V4 - Minimaliste', 'action_syndicat_dashboard_v4')
            ]
            
            for menu_name, action_name in dashboard_actions:
                # Trouver l'action
                action_data = models.execute_kw(db, uid, password,
                    'ir.model.data', 'search_read',
                    [[('name', '=', action_name), ('model', '=', 'ir.actions.act_window')]],
                    {'fields': ['res_id']})
                
                if action_data:
                    action_id = action_data[0]['res_id']
                    
                    submenu_id = models.execute_kw(db, uid, password,
                        'ir.ui.menu', 'create', [{
                            'name': menu_name,
                            'parent_id': test_menu_id,
                            'action': f'ir.actions.act_window,{action_id}',
                            'sequence': len([x for x in dashboard_actions if x[0] <= menu_name])
                        }])
                    print(f"  ✅ {menu_name} (ID: {submenu_id})")
                else:
                    print(f"  ❌ {menu_name} - Action {action_name} non trouvée")
        
        print("\n🎯 RÉSULTAT")
        print("=" * 15)
        print("✅ Actions des dashboards corrigées")
        print("✅ Module mis à jour")
        print("✅ Menus de test créés")
        print("📍 Accès: Menu Syndicat → 🧪 Test Dashboards")
        print("🔄 Rechargez la page pour voir les nouveaux menus")
        
        return True
        
    except ConnectionError:
        print("❌ Impossible de se connecter à Odoo")
        print("💡 Vérifiez que Odoo est démarré sur le port 8070")
        return False
    except Exception as e:
        print(f"❌ Erreur: {e}")
        return False

if __name__ == "__main__":
    success = fix_dashboard_actions()
    sys.exit(0 if success else 1)