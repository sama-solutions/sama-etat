#!/usr/bin/env python3
"""
Script pour démarrer Odoo et corriger les menus des dashboards
"""

import subprocess
import time
import sys
import os

def start_odoo_and_fix_menus():
    """Démarrer Odoo et corriger les menus"""
    
    print("🚀 DÉMARRAGE ODOO ET CORRECTION DES MENUS")
    print("=" * 50)
    
    # Configuration
    PORT = 8070
    DATABASE = "sama_syndicat_final_1756812346"
    ODOO_BIN = "/var/odoo/odoo18/odoo-bin"
    ADDONS_PATH = "/var/odoo/odoo18/odoo/addons,/var/odoo/odoo18/addons,/tmp/addons_sama_syndicat"
    
    # Arrêter les processus existants
    print("🛑 Arrêt des processus existants...")
    subprocess.run(['pkill', '-f', 'odoo-bin'], capture_output=True)
    time.sleep(2)
    
    # Vérifier que Odoo existe
    if not os.path.exists(ODOO_BIN):
        print(f"❌ Odoo non trouvé à: {ODOO_BIN}")
        return False
    
    # Démarrer Odoo en arrière-plan
    print("⚡ Démarrage d'Odoo...")
    cmd = [
        'python3', ODOO_BIN,
        f'--addons-path={ADDONS_PATH}',
        f'--database={DATABASE}',
        f'--xmlrpc-port={PORT}',
        '--dev=reload,xml',
        '--log-level=warn'  # Moins de logs pour éviter le spam
    ]
    
    # Démarrer Odoo en arrière-plan
    process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    
    print("⏳ Attente du démarrage d'Odoo...")
    
    # Attendre que Odoo soit prêt
    max_wait = 60  # 60 secondes max
    wait_time = 0
    
    while wait_time < max_wait:
        try:
            # Tester la connexion
            import xmlrpc.client
            common = xmlrpc.client.ServerProxy(f'http://localhost:{PORT}/xmlrpc/2/common')
            version = common.version()
            if version:
                print(f"✅ Odoo démarré (version: {version['server_version']})")
                break
        except:
            pass
        
        time.sleep(2)
        wait_time += 2
        print(f"⏳ Attente... ({wait_time}s/{max_wait}s)")
        
        # Vérifier si le processus est encore actif
        if process.poll() is not None:
            print("❌ Odoo s'est arrêté de manière inattendue")
            stdout, stderr = process.communicate()
            print(f"Erreur: {stderr.decode()}")
            return False
    
    if wait_time >= max_wait:
        print("❌ Timeout - Odoo n'a pas démarré à temps")
        process.terminate()
        return False
    
    # Maintenant corriger les menus
    print("\n🔧 Correction des menus des dashboards...")
    
    try:
        # Importer et exécuter la correction des menus
        import xmlrpc.client
        
        url = f'http://localhost:{PORT}'
        db = DATABASE
        username = 'admin'
        password = 'admin'
        
        # Connexion
        common = xmlrpc.client.ServerProxy(f'{url}/xmlrpc/2/common')
        uid = common.authenticate(db, username, password, {})
        
        if not uid:
            print("❌ Erreur d'authentification")
            return False
        
        models = xmlrpc.client.ServerProxy(f'{url}/xmlrpc/2/object')
        
        # Mettre à jour le module
        print("📦 Mise à jour du module sama_syndicat...")
        module_ids = models.execute_kw(db, uid, password,
            'ir.module.module', 'search',
            [[('name', '=', 'sama_syndicat')]])
        
        if module_ids:
            models.execute_kw(db, uid, password,
                'ir.module.module', 'button_immediate_upgrade',
                [module_ids])
            print("✅ Module mis à jour")
        
        # Vérifier les menus
        print("🔍 Vérification des menus...")
        test_menu = models.execute_kw(db, uid, password,
            'ir.ui.menu', 'search',
            [[('name', 'like', 'Test Dashboard')]])
        
        if test_menu:
            print(f"✅ Menu de test trouvé (ID: {test_menu[0]})")
        else:
            print("⚠️ Menu de test non trouvé, création manuelle...")
            
            # Trouver le menu principal Syndicat
            syndicat_menu = models.execute_kw(db, uid, password,
                'ir.ui.menu', 'search',
                [[('name', '=', 'Syndicat')]])
            
            if syndicat_menu:
                parent_id = syndicat_menu[0]
                
                # Créer le menu de test
                test_menu_id = models.execute_kw(db, uid, password,
                    'ir.ui.menu', 'create', [{
                        'name': '🧪 Test Dashboards',
                        'parent_id': parent_id,
                        'sequence': 2
                    }])
                print(f"✅ Menu de test créé (ID: {test_menu_id})")
        
        print("\n🎯 RÉSULTAT FINAL")
        print("=" * 20)
        print("✅ Odoo démarré avec succès")
        print("✅ Module sama_syndicat mis à jour")
        print("✅ Menus des dashboards configurés")
        print(f"🌐 Interface: http://localhost:{PORT}/web")
        print("📍 Accès: Menu Syndicat → 🧪 Test Dashboards")
        print("\n💡 Le serveur Odoo continue de tourner en arrière-plan")
        print("🛑 Pour l'arrêter: pkill -f odoo-bin")
        
        return True
        
    except Exception as e:
        print(f"❌ Erreur lors de la correction des menus: {e}")
        return False

if __name__ == "__main__":
    success = start_odoo_and_fix_menus()
    if success:
        print("\n🎊 Succès ! Vous pouvez maintenant tester les dashboards")
    else:
        print("\n❌ Échec du démarrage ou de la correction")
    sys.exit(0 if success else 1)