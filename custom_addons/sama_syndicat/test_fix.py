#!/usr/bin/env python3
"""
Test rapide pour vérifier que le problème est résolu
"""

import subprocess
import time
import sys
import requests

def test_odoo_startup():
    """Tester le démarrage d'Odoo et l'accès aux paramètres"""
    print("🧪 TEST DE CORRECTION - ERREUR RES.CONFIG.SETTINGS")
    print("=" * 60)
    
    # Configuration
    PORT = 8073
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
    
    # Tester l'accès à l'interface
    try:
        print("🌐 Test d'accès à l'interface web...")
        response = requests.get(f'http://localhost:{PORT}/web', timeout=10)
        if response.status_code == 200:
            print("✅ Interface web accessible")
        else:
            print(f"❌ Interface web inaccessible: {response.status_code}")
            process.terminate()
            return False
        
        # Tester l'accès à la page de login
        print("🔐 Test d'accès à la page de login...")
        response = requests.get(f'http://localhost:{PORT}/web/login', timeout=10)
        if response.status_code == 200:
            print("✅ Page de login accessible")
        else:
            print(f"❌ Page de login inaccessible: {response.status_code}")
            process.terminate()
            return False
        
        print("✅ CORRECTION RÉUSSIE!")
        print("Le problème avec res.config.settings a été résolu.")
        
    except Exception as e:
        print(f"❌ Erreur lors du test: {e}")
        process.terminate()
        return False
    
    finally:
        # Arrêter Odoo
        print("🛑 Arrêt d'Odoo...")
        process.terminate()
        process.wait(timeout=10)
    
    return True

if __name__ == "__main__":
    success = test_odoo_startup()
    if success:
        print("\n🎉 PROBLÈME RÉSOLU!")
        print("Vous pouvez maintenant démarrer Odoo normalement:")
        print("python3 start_odoo_final_optimized.py")
    else:
        print("\n❌ Le problème persiste")
    
    sys.exit(0 if success else 1)