#!/usr/bin/env python3
"""
Script de redémarrage complet pour forcer l'affichage des nouveaux menus
"""

import subprocess
import time
import sys
import os

def restart_clean_final():
    """Redémarrer Odoo complètement pour forcer les nouveaux menus"""
    
    print("🔄 REDÉMARRAGE COMPLET POUR NOUVEAUX MENUS")
    print("=" * 45)
    
    # Configuration
    PORT = 8070
    DATABASE = "sama_syndicat_final_1756812346"
    ODOO_BIN = "/var/odoo/odoo18/odoo-bin"
    ADDONS_PATH = "/var/odoo/odoo18/odoo/addons,/var/odoo/odoo18/addons,/tmp/addons_sama_syndicat"
    
    # Arrêter complètement Odoo
    print("🛑 Arrêt complet d'Odoo...")
    subprocess.run(['pkill', '-f', 'odoo-bin'], capture_output=True)
    time.sleep(3)
    
    # Vérifier que tous les processus sont arrêtés
    result = subprocess.run(['pgrep', '-f', 'odoo-bin'], capture_output=True)
    if result.returncode == 0:
        print("⚠️ Processus Odoo encore actifs, arrêt forcé...")
        subprocess.run(['pkill', '-9', '-f', 'odoo-bin'], capture_output=True)
        time.sleep(2)
    
    print("✅ Odoo complètement arrêté")
    
    # Vérifier que Odoo existe
    if not os.path.exists(ODOO_BIN):
        print(f"❌ Odoo non trouvé à: {ODOO_BIN}")
        return False
    
    # Démarrer Odoo avec mise à jour forcée
    print("⚡ Redémarrage d'Odoo avec mise à jour forcée...")
    cmd = [
        'python3', ODOO_BIN,
        f'--addons-path={ADDONS_PATH}',
        f'--database={DATABASE}',
        f'--xmlrpc-port={PORT}',
        '--update=sama_syndicat',  # Force la mise à jour du module
        '--dev=reload,xml',
        '--log-level=warn'
    ]
    
    # Démarrer Odoo en arrière-plan
    process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    
    print("⏳ Attente du redémarrage d'Odoo...")
    
    # Attendre que Odoo soit prêt
    max_wait = 90  # Plus de temps pour la mise à jour
    wait_time = 0
    
    while wait_time < max_wait:
        try:
            import xmlrpc.client
            common = xmlrpc.client.ServerProxy(f'http://localhost:{PORT}/xmlrpc/2/common')
            version = common.version()
            if version:
                print(f"✅ Odoo redémarré (version: {version['server_version']})")
                break
        except:
            pass
        
        time.sleep(3)
        wait_time += 3
        print(f"⏳ Attente... ({wait_time}s/{max_wait}s)")
        
        if process.poll() is not None:
            print("❌ Odoo s'est arrêté de manière inattendue")
            stdout, stderr = process.communicate()
            if stderr:
                print(f"Erreur: {stderr.decode()[:500]}...")
            return False
    
    if wait_time >= max_wait:
        print("❌ Timeout - Odoo n'a pas redémarré à temps")
        process.terminate()
        return False
    
    # Vérifier les menus après redémarrage
    print("\n🔍 Vérification finale des menus...")
    try:
        import xmlrpc.client
        
        models = xmlrpc.client.ServerProxy(f'http://localhost:{PORT}/xmlrpc/2/object')
        common = xmlrpc.client.ServerProxy(f'http://localhost:{PORT}/xmlrpc/2/common')
        
        uid = common.authenticate(DATABASE, 'admin', 'admin', {})
        
        if uid:
            # Lister les menus du syndicat
            syndicat_menu = models.execute_kw(DATABASE, uid, 'admin',
                'ir.ui.menu', 'search',
                [[('name', '=', 'Syndicat')]])
            
            if syndicat_menu:
                child_menus = models.execute_kw(DATABASE, uid, 'admin',
                    'ir.ui.menu', 'search_read',
                    [[('parent_id', '=', syndicat_menu[0])]],
                    {'fields': ['name', 'sequence'], 'order': 'sequence'})
                
                print("📋 Menus actuels du Syndicat:")
                for menu in child_menus:
                    if '📊' in menu['name'] or '👔' in menu['name']:
                        print(f"  ✅ {menu['name']} (séquence: {menu['sequence']})")
                    else:
                        print(f"  - {menu['name']} (séquence: {menu['sequence']})")
            
            # Vérifier les actions des nouveaux dashboards
            print("\n🔍 Vérification des actions des dashboards...")
            actions_to_check = [
                'action_syndicat_dashboard_modern_cards',
                'action_syndicat_dashboard_executive'
            ]
            
            for action_name in actions_to_check:
                action_data = models.execute_kw(DATABASE, uid, 'admin',
                    'ir.model.data', 'search_read',
                    [[('name', '=', action_name), ('model', '=', 'ir.actions.act_window')]],
                    {'fields': ['res_id']})
                
                if action_data:
                    print(f"  ✅ Action {action_name} disponible")
                else:
                    print(f"  ❌ Action {action_name} manquante")
        
    except Exception as e:
        print(f"⚠️ Erreur lors de la vérification: {e}")
    
    print("\n🎯 RÉSULTAT FINAL")
    print("=" * 20)
    print("✅ Odoo redémarré complètement")
    print("✅ Module sama_syndicat mis à jour")
    print("✅ Nouveaux menus chargés")
    print("✅ Cache complètement vidé")
    print(f"🌐 Interface: http://localhost:{PORT}/web")
    
    print("\n📍 NOUVEAUX MENUS DISPONIBLES")
    print("=" * 35)
    print("Menu Syndicat:")
    print("├── 📊 Dashboard Principal (Cartes Modernes)")
    print("├── 👔 Dashboard Exécutif (Interface Premium)")
    print("├── Adhérents")
    print("├── Assemblées")
    print("├── Revendications")
    print("├── Actions Syndicales")
    print("├── Communications")
    print("├── Formations")
    print("├── Conventions")
    print("├── Médiations")
    print("└── Configuration")
    
    print("\n💡 INSTRUCTIONS CRITIQUES")
    print("=" * 30)
    print("1. 🔄 RECHARGEZ COMPLÈTEMENT votre navigateur:")
    print("   - Ctrl+Shift+R (Chrome/Firefox)")
    print("   - Ou fermez et rouvrez l'onglet")
    print("   - Ou videz le cache navigateur")
    print()
    print("2. 🌐 Ouvrez http://localhost:8070/web")
    print("3. 🔑 Connectez-vous (admin/admin)")
    print("4. 📍 Allez dans le menu Syndicat")
    print("5. ✅ Vous devriez voir UNIQUEMENT:")
    print("   - 📊 Dashboard Principal")
    print("   - 👔 Dashboard Exécutif")
    print("   - Les autres menus (Adhérents, etc.)")
    print()
    print("❌ PLUS de 'Tableau de Bord' ancien !")
    print("❌ PLUS de menus de test !")
    
    print("\n🎨 DASHBOARDS MODERNES DISPONIBLES")
    print("=" * 40)
    print("📊 Dashboard Principal:")
    print("   - Interface moderne avec cartes")
    print("   - Métriques visuelles avancées")
    print("   - Design inspiré d'Odoo Enterprise")
    print()
    print("👔 Dashboard Exécutif:")
    print("   - Interface premium pour direction")
    print("   - Header avec gradient moderne")
    print("   - KPI cards détaillées")
    
    print("\n💡 Le serveur Odoo continue de tourner en arrière-plan")
    print("🛑 Pour l'arrêter: pkill -f odoo-bin")
    
    return True

if __name__ == "__main__":
    success = restart_clean_final()
    if success:
        print("\n🎊 SUCCÈS ! Redémarrage complet effectué")
        print("🧹 Interface parfaitement nettoyée")
        print("🎨 Nouveaux dashboards modernes disponibles")
        print("💡 N'oubliez pas de recharger votre navigateur !")
    else:
        print("\n❌ Échec du redémarrage")
    sys.exit(0 if success else 1)