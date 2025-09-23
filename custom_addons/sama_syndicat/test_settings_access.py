#!/usr/bin/env python3
"""
Test d'accès aux paramètres après correction
"""

import subprocess
import time
import sys
import requests
import xmlrpc.client

def test_settings_access():
    """Tester l'accès aux paramètres"""
    print("🧪 TEST D'ACCÈS AUX PARAMÈTRES - APRÈS CORRECTION")
    print("=" * 60)
    
    # Configuration
    PORT = 8075
    DATABASE = "sama_syndicat_final_1756812346"
    ODOO_BIN = "/var/odoo/odoo18/odoo-bin"
    ADDONS_PATH = "/var/odoo/odoo18/odoo/addons,/var/odoo/odoo18/addons,/tmp/addons_sama_syndicat"
    
    # Arrêter les processus existants
    print("🛑 Arrêt des processus existants...")
    subprocess.run(['pkill', '-f', 'odoo-bin'], capture_output=True)
    time.sleep(3)
    
    # Démarrer Odoo
    cmd = [
        'python3', ODOO_BIN,
        f'--addons-path={ADDONS_PATH}',
        f'--database={DATABASE}',
        f'--xmlrpc-port={PORT}',
        '--log-level=warn'
    ]
    
    print("🚀 Démarrage d'Odoo...")
    process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    
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
            print("❌ Odoo s'est arrêté de manière inattendue")
            print(f"Erreur: {stderr.decode()[-500:]}")
            return False
    
    if wait_time >= max_wait:
        print("❌ Timeout - Odoo n'a pas démarré à temps")
        process.terminate()
        return False
    
    try:
        # Attendre stabilisation
        print("⏳ Attente de la stabilisation...")
        time.sleep(10)
        
        # Test XML-RPC
        print("\n🔌 Test XML-RPC...")
        common = xmlrpc.client.ServerProxy(f'http://localhost:{PORT}/xmlrpc/2/common')
        uid = common.authenticate(DATABASE, 'admin', 'admin', {})
        
        if not uid:
            print("❌ Impossible de s'authentifier")
            return False
        
        print(f"✅ Authentification réussie (UID: {uid})")
        
        models = xmlrpc.client.ServerProxy(f'http://localhost:{PORT}/xmlrpc/2/object')
        
        # Test res.config.settings
        print("\n📋 Test res.config.settings...")
        try:
            config_ids = models.execute_kw(DATABASE, uid, 'admin', 'res.config.settings', 'search', [[]])
            print(f"✅ Modèle res.config.settings accessible ({len(config_ids)} enregistrements)")
            
            # Test fields_get
            fields = models.execute_kw(DATABASE, uid, 'admin', 'res.config.settings', 'fields_get', [])
            print(f"✅ Champs accessibles ({len(fields)} champs)")
            
        except Exception as e:
            print(f"❌ Erreur avec res.config.settings: {e}")
            return False
        
        # Test ir.model.fields
        print("\n🔧 Test ir.model.fields...")
        try:
            field_ids = models.execute_kw(DATABASE, uid, 'admin', 'ir.model.fields', 'search', 
                                        [[['model', '=', 'res.config.settings']], {'limit': 5}])
            print(f"✅ Modèle ir.model.fields accessible ({len(field_ids)} champs trouvés)")
            
        except Exception as e:
            print(f"❌ Erreur avec ir.model.fields: {e}")
            return False
        
        # Test accès web
        print("\n🌐 Test accès web...")
        try:
            response = requests.get(f'http://localhost:{PORT}/web#action=base.action_res_config_settings', timeout=10)
            if response.status_code == 200:
                print("✅ Page des paramètres accessible via web")
            else:
                print(f"❌ Page des paramètres inaccessible: {response.status_code}")
                return False
        except Exception as e:
            print(f"❌ Erreur accès web: {e}")
            return False
        
        print("\n🎉 TOUS LES TESTS RÉUSSIS!")
        print("L'accès aux paramètres fonctionne correctement.")
        return True
        
    except Exception as e:
        print(f"❌ Erreur générale: {e}")
        return False
    
    finally:
        # Arrêter Odoo
        print("\n🛑 Arrêt d'Odoo...")
        process.terminate()
        try:
            process.wait(timeout=10)
        except subprocess.TimeoutExpired:
            process.kill()

if __name__ == "__main__":
    success = test_settings_access()
    if success:
        print("\n✅ PROBLÈME RÉSOLU!")
        print("Vous pouvez maintenant accéder aux paramètres normalement.")
        print("Démarrez Odoo avec: python3 start_odoo_final_optimized.py")
    else:
        print("\n❌ Le problème persiste")
    
    sys.exit(0 if success else 1)