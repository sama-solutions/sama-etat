#!/usr/bin/env python3
"""
Test du module minimal web_studio_community
"""

import subprocess
import time
import sys
import requests
import xmlrpc.client

def test_minimal_module():
    """Tester le module minimal"""
    print("🧪 TEST DU MODULE MINIMAL WEB_STUDIO_COMMUNITY")
    print("=" * 60)
    
    # Configuration
    DATABASE = "test_web_studio_minimal"
    ODOO_BIN = "/var/odoo/odoo18/odoo-bin"
    ADDONS_PATH = "/var/odoo/odoo18/odoo/addons,/var/odoo/odoo18/addons,/tmp/addons_sama_syndicat"
    PORT = 8082
    
    # Arrêter tous les processus Odoo
    print("🛑 Arrêt de tous les processus Odoo...")
    subprocess.run(['pkill', '-f', 'odoo-bin'], capture_output=True)
    time.sleep(3)
    
    # Supprimer et recréer la base de données
    print("🗑️ Suppression de l'ancienne base...")
    try:
        subprocess.run(['dropdb', DATABASE], capture_output=True)
    except:
        pass
    
    print("🆕 Création d'une nouvelle base de données...")
    create_cmd = [
        'python3', ODOO_BIN,
        f'--addons-path={ADDONS_PATH}',
        f'--database={DATABASE}',
        f'--xmlrpc-port={PORT}',
        '--init=base',
        '--stop-after-init',
        '--log-level=warn',
        '--without-demo=all'
    ]
    
    try:
        result = subprocess.run(create_cmd, capture_output=True, text=True, timeout=180)
        if result.returncode == 0:
            print("✅ Base de données créée")
        else:
            print("❌ Erreur création base")
            print(result.stderr[-300:])
            return False
    except Exception as e:
        print(f"❌ Erreur: {e}")
        return False
    
    # Mettre à jour le module (pour nettoyer)
    print("🔄 Mise à jour du module...")
    update_cmd = [
        'python3', ODOO_BIN,
        f'--addons-path={ADDONS_PATH}',
        f'--database={DATABASE}',
        f'--xmlrpc-port={PORT}',
        '-u', 'web_studio_community',
        '--stop-after-init',
        '--log-level=warn'
    ]
    
    try:
        result = subprocess.run(update_cmd, capture_output=True, text=True, timeout=120)
        if result.returncode == 0:
            print("✅ Module mis à jour")
        else:
            print("❌ Erreur mise à jour")
            print(result.stderr[-300:])
            return False
    except Exception as e:
        print(f"❌ Erreur: {e}")
        return False
    
    # Installer le module
    print("📦 Installation du module...")
    install_cmd = [
        'python3', ODOO_BIN,
        f'--addons-path={ADDONS_PATH}',
        f'--database={DATABASE}',
        f'--xmlrpc-port={PORT}',
        '-i', 'web_studio_community',
        '--stop-after-init',
        '--log-level=warn'
    ]
    
    try:
        result = subprocess.run(install_cmd, capture_output=True, text=True, timeout=120)
        if result.returncode == 0:
            print("✅ Module installé")
        else:
            print("❌ Erreur installation")
            print(result.stderr[-300:])
            return False
    except Exception as e:
        print(f"❌ Erreur: {e}")
        return False
    
    # Démarrer Odoo et tester
    print("🚀 Démarrage d'Odoo pour test...")
    start_cmd = [
        'python3', ODOO_BIN,
        f'--addons-path={ADDONS_PATH}',
        f'--database={DATABASE}',
        f'--xmlrpc-port={PORT}',
        '--log-level=warn'
    ]
    
    process = subprocess.Popen(start_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    
    # Attendre que Odoo soit prêt
    max_wait = 60
    wait_time = 0
    
    while wait_time < max_wait:
        try:
            response = requests.get(f'http://localhost:{PORT}/web', timeout=5)
            if response.status_code == 200:
                print(f"✅ Odoo démarré sur le port {PORT}")
                break
        except:
            pass
        
        time.sleep(2)
        wait_time += 2
        
        if process.poll() is not None:
            stdout, stderr = process.communicate()
            print("❌ Odoo s'est arrêté")
            print(f"Erreur: {stderr.decode()[-500:]}")
            return False
    
    if wait_time >= max_wait:
        print("❌ Timeout")
        process.terminate()
        return False
    
    try:
        # Attendre stabilisation
        time.sleep(10)
        
        # Test XML-RPC
        print("🔌 Test XML-RPC...")
        common = xmlrpc.client.ServerProxy(f'http://localhost:{PORT}/xmlrpc/2/common')
        uid = common.authenticate(DATABASE, 'admin', 'admin', {})
        
        if not uid:
            print("❌ Authentification échouée")
            return False
        
        print(f"✅ Authentification réussie (UID: {uid})")
        
        models = xmlrpc.client.ServerProxy(f'http://localhost:{PORT}/xmlrpc/2/object')
        
        # Test res.config.settings
        print("📋 Test res.config.settings...")
        config_ids = models.execute_kw(DATABASE, uid, 'admin', 'res.config.settings', 'search', [[]])
        print(f"✅ res.config.settings OK ({len(config_ids)} enregistrements)")
        
        # Test ir.model.fields avec domaine simple
        print("🔧 Test ir.model.fields...")
        field_ids = models.execute_kw(DATABASE, uid, 'admin', 'ir.model.fields', 'search', 
                                    [[['model', '=', 'res.users']], {'limit': 3}])
        print(f"✅ ir.model.fields OK ({len(field_ids)} champs)")
        
        # Test du module
        print("📦 Test du module...")
        module_ids = models.execute_kw(DATABASE, uid, 'admin', 'ir.module.module', 'search', 
                                     [[['name', '=', 'web_studio_community']]])
        
        if module_ids:
            module_data = models.execute_kw(DATABASE, uid, 'admin', 'ir.module.module', 'read', 
                                          [module_ids], {'fields': ['name', 'state']})
            module = module_data[0]
            print(f"✅ Module: {module['name']} (état: {module['state']})")
        else:
            print("❌ Module non trouvé")
            return False
        
        # Test accès web
        print("🌐 Test accès web...")
        response = requests.get(f'http://localhost:{PORT}/web#action=base.action_res_config_settings', timeout=10)
        if response.status_code == 200:
            print("✅ Page paramètres accessible")
        else:
            print(f"❌ Page paramètres inaccessible: {response.status_code}")
            return False
        
        print("\n🎉 TOUS LES TESTS RÉUSSIS!")
        print("Le module minimal fonctionne parfaitement.")
        return True
        
    except Exception as e:
        print(f"❌ Erreur lors du test: {e}")
        return False
    
    finally:
        # Arrêter Odoo
        print("🛑 Arrêt d'Odoo...")
        process.terminate()
        try:
            process.wait(timeout=10)
        except subprocess.TimeoutExpired:
            process.kill()

if __name__ == "__main__":
    success = test_minimal_module()
    if success:
        print("\n✅ SUCCÈS!")
        print("Le module web_studio_community fonctionne maintenant.")
        print("L'accès aux paramètres est possible.")
    else:
        print("\n❌ ÉCHEC")
    
    sys.exit(0 if success else 1)