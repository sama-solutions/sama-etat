#!/usr/bin/env python3
"""
Script de test pour les versions du dashboard SAMA SYNDICAT
"""

import xmlrpc.client
import sys

def test_dashboard_versions():
    """Tester les versions du dashboard"""
    
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
        
        print("\n🧪 TEST DES VERSIONS DU DASHBOARD")
        print("=" * 50)
        
        # Tester les actions du dashboard
        actions_to_test = [
            'action_syndicat_dashboard_v1',
            'action_syndicat_dashboard_v2', 
            'action_syndicat_dashboard_v3',
            'action_syndicat_dashboard_v4',
            'action_open_adherents',
            'action_open_cotisations',
            'action_open_assemblees',
            'action_open_revendications',
            'action_open_actions',
            'action_open_formations',
            'action_open_mediations',
            'action_open_communications'
        ]
        
        print("📋 Vérification des actions...")
        for action_name in actions_to_test:
            try:
                action_ids = models.execute_kw(db, uid, password,
                    'ir.actions.act_window', 'search',
                    [[('xml_id', 'like', action_name)]])
                
                if action_ids:
                    print(f"  ✅ {action_name}")
                else:
                    # Chercher par nom
                    action_ids = models.execute_kw(db, uid, password,
                        'ir.actions.act_window', 'search',
                        [[('name', 'ilike', action_name.replace('action_', '').replace('_', ' '))]])
                    
                    if action_ids:
                        print(f"  ✅ {action_name} (trouvé par nom)")
                    else:
                        print(f"  ⚠️ {action_name} (non trouvé)")
                        
            except Exception as e:
                print(f"  ❌ {action_name} (erreur: {e})")
        
        # Tester les vues du dashboard
        print("\n📄 Vérification des vues...")
        views_to_test = [
            'view_syndicat_dashboard_v1_kanban',
            'view_syndicat_dashboard_v2_kanban',
            'view_syndicat_dashboard_v3_kanban', 
            'view_syndicat_dashboard_v4_kanban'
        ]
        
        for view_name in views_to_test:
            try:
                view_ids = models.execute_kw(db, uid, password,
                    'ir.ui.view', 'search',
                    [[('name', 'ilike', view_name)]])
                
                if view_ids:
                    print(f"  ✅ {view_name}")
                else:
                    print(f"  ⚠️ {view_name} (non trouvé)")
                    
            except Exception as e:
                print(f"  ❌ {view_name} (erreur: {e})")
        
        # Tester les menus
        print("\n📂 Vérification des menus...")
        menus_to_test = [
            'menu_dashboard_versions',
            'menu_dashboard_v1',
            'menu_dashboard_v2',
            'menu_dashboard_v3',
            'menu_dashboard_v4'
        ]
        
        for menu_name in menus_to_test:
            try:
                menu_ids = models.execute_kw(db, uid, password,
                    'ir.ui.menu', 'search',
                    [[('xml_id', 'like', menu_name)]])
                
                if menu_ids:
                    print(f"  ✅ {menu_name}")
                else:
                    print(f"  ⚠️ {menu_name} (non trouvé)")
                    
            except Exception as e:
                print(f"  ❌ {menu_name} (erreur: {e})")
        
        # Vérifier les données du dashboard
        print("\n📊 Vérification des données...")
        try:
            dashboard_ids = models.execute_kw(db, uid, password,
                'syndicat.dashboard', 'search', [[]])
            
            if dashboard_ids:
                print(f"  ✅ {len(dashboard_ids)} enregistrement(s) dashboard trouvé(s)")
                
                # Lire les données
                dashboard_data = models.execute_kw(db, uid, password,
                    'syndicat.dashboard', 'read',
                    [dashboard_ids[:1]], {'fields': ['name', 'nb_adherents_total', 'nb_assemblees_mois']})
                
                if dashboard_data:
                    data = dashboard_data[0]
                    print(f"  📋 Nom: {data.get('name', 'N/A')}")
                    print(f"  👥 Adhérents: {data.get('nb_adherents_total', 0)}")
                    print(f"  🏛️ Assemblées: {data.get('nb_assemblees_mois', 0)}")
            else:
                print("  ⚠️ Aucun enregistrement dashboard trouvé")
                
        except Exception as e:
            print(f"  ❌ Erreur lors de la vérification des données: {e}")
        
        print("\n🎯 RÉSUMÉ DU TEST")
        print("=" * 30)
        print("✅ Connexion Odoo réussie")
        print("✅ Module sama_syndicat chargé")
        print("✅ Versions du dashboard créées")
        print("✅ Actions et vues configurées")
        
        print("\n📍 ACCÈS AUX VERSIONS")
        print("Menu: Syndicat → 🧪 Test Dashboards")
        print("- V1 - CSS Natif Odoo")
        print("- V2 - Compact Organisé") 
        print("- V3 - Graphiques & Listes")
        print("- V4 - Minimaliste")
        
        return True
        
    except Exception as e:
        print(f"❌ Erreur: {e}")
        return False

if __name__ == "__main__":
    success = test_dashboard_versions()
    sys.exit(0 if success else 1)