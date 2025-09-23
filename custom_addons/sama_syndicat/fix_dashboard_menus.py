#!/usr/bin/env python3
"""
Script pour corriger et créer les menus de test des dashboards
"""

import xmlrpc.client
import sys

def fix_dashboard_menus():
    """Corriger les menus des dashboards"""
    
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
        
        print("\n🔍 VÉRIFICATION DES MENUS DE TEST")
        print("=" * 40)
        
        # Vérifier le menu principal Syndicat
        syndicat_menu = models.execute_kw(db, uid, password,
            'ir.ui.menu', 'search',
            [[('name', '=', 'Syndicat')]])
        
        if syndicat_menu:
            print(f"✅ Menu principal Syndicat trouvé (ID: {syndicat_menu[0]})")
            parent_id = syndicat_menu[0]
        else:
            print("❌ Menu principal Syndicat non trouvé")
            return False
        
        # Vérifier les actions des dashboards
        dashboard_actions = [
            'action_syndicat_dashboard_v1',
            'action_syndicat_dashboard_v2', 
            'action_syndicat_dashboard_v3',
            'action_syndicat_dashboard_v4'
        ]
        
        action_ids = {}
        print("\n📋 Vérification des actions...")
        for action_name in dashboard_actions:
            # Rechercher par xml_id
            action_data = models.execute_kw(db, uid, password,
                'ir.model.data', 'search_read',
                [[('name', '=', action_name), ('model', '=', 'ir.actions.act_window')]],
                {'fields': ['res_id']})
            
            if action_data:
                action_ids[action_name] = action_data[0]['res_id']
                print(f"  ✅ {action_name} (ID: {action_data[0]['res_id']})")
            else:
                print(f"  ❌ {action_name} non trouvé")
        
        # Vérifier si le menu de test existe déjà
        test_menu = models.execute_kw(db, uid, password,
            'ir.ui.menu', 'search',
            [[('name', 'like', 'Test Dashboard')]])
        
        if test_menu:
            print(f"\n⚠️ Menu de test existant trouvé (ID: {test_menu[0]})")
            # Supprimer l'ancien menu
            models.execute_kw(db, uid, password,
                'ir.ui.menu', 'unlink', [test_menu])
            print("🗑️ Ancien menu supprimé")
        
        # Créer le menu principal de test
        print("\n🔨 Création du menu de test...")
        test_menu_id = models.execute_kw(db, uid, password,
            'ir.ui.menu', 'create', [{
                'name': '🧪 Test Dashboards',
                'parent_id': parent_id,
                'sequence': 2
            }])
        
        print(f"✅ Menu principal de test créé (ID: {test_menu_id})")
        
        # Créer les sous-menus
        menu_configs = [
            ('V1 - CSS Natif Odoo', 'action_syndicat_dashboard_v1', 1),
            ('V2 - Compact Organisé', 'action_syndicat_dashboard_v2', 2),
            ('V3 - Graphiques & Listes', 'action_syndicat_dashboard_v3', 3),
            ('V4 - Minimaliste', 'action_syndicat_dashboard_v4', 4)
        ]
        
        print("\n📂 Création des sous-menus...")
        for menu_name, action_name, sequence in menu_configs:
            if action_name in action_ids:
                submenu_id = models.execute_kw(db, uid, password,
                    'ir.ui.menu', 'create', [{
                        'name': menu_name,
                        'parent_id': test_menu_id,
                        'action': f'ir.actions.act_window,{action_ids[action_name]}',
                        'sequence': sequence
                    }])
                print(f"  ✅ {menu_name} (ID: {submenu_id})")
            else:
                print(f"  ❌ {menu_name} - Action manquante")
        
        # Vider le cache des menus
        print("\n🔄 Vidage du cache des menus...")
        try:
            models.execute_kw(db, uid, password,
                'ir.ui.menu', 'clear_caches', [])
            print("✅ Cache vidé")
        except:
            print("⚠️ Impossible de vider le cache (normal)")
        
        print("\n🎯 RÉSULTAT")
        print("=" * 15)
        print("✅ Menus de test des dashboards créés")
        print("📍 Accès: Menu Syndicat → 🧪 Test Dashboards")
        print("🔄 Rechargez la page pour voir les nouveaux menus")
        
        return True
        
    except Exception as e:
        print(f"❌ Erreur: {e}")
        return False

if __name__ == "__main__":
    success = fix_dashboard_menus()
    sys.exit(0 if success else 1)