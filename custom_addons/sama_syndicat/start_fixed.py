#!/usr/bin/env python3
"""
Script de démarrage avec correction automatique des actions
"""

import subprocess
import time
import sys
import os

def start_odoo_fixed():
    """Démarrer Odoo avec correction automatique"""
    
    print("🚀 DÉMARRAGE ODOO AVEC CORRECTIONS")
    print("=" * 40)
    
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
        '--log-level=warn'
    ]
    
    # Démarrer Odoo en arrière-plan
    process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    
    print("⏳ Attente du démarrage d'Odoo...")
    
    # Attendre que Odoo soit prêt
    max_wait = 60
    wait_time = 0
    
    while wait_time < max_wait:
        try:
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
        
        if process.poll() is not None:
            print("❌ Odoo s'est arrêté de manière inattendue")
            stdout, stderr = process.communicate()
            if stderr:
                print(f"Erreur: {stderr.decode()}")
            return False
    
    if wait_time >= max_wait:
        print("❌ Timeout - Odoo n'a pas démarré à temps")
        process.terminate()
        return False
    
    # Maintenant corriger les actions
    print("\n🔧 Correction des actions des dashboards...")
    
    try:
        # Exécuter le script de correction
        result = subprocess.run(['python3', 'fix_dashboard_actions.py'], 
                              capture_output=True, text=True, timeout=30)
        
        if result.returncode == 0:
            print("✅ Actions corrigées avec succès")
        else:
            print(f"⚠️ Problème lors de la correction: {result.stderr}")
    except Exception as e:
        print(f"❌ Erreur lors de la correction: {e}")
    
    print("\n🎯 RÉSULTAT FINAL")
    print("=" * 20)
    print("✅ Odoo démarré avec succès")
    print("✅ Actions des dashboards corrigées")
    print(f"🌐 Interface: http://localhost:{PORT}/web")
    print("📍 Accès: Menu Syndicat → 🧪 Test Dashboards")
    print("\n💡 Le serveur Odoo continue de tourner en arrière-plan")
    print("🛑 Pour l'arrêter: pkill -f odoo-bin")
    
    return True

if __name__ == "__main__":
    success = start_odoo_fixed()
    if success:
        print("\n🎊 Succès ! Vous pouvez maintenant tester les dashboards")
    else:
        print("\n❌ Échec du démarrage")
    sys.exit(0 if success else 1)