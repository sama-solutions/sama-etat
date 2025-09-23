#!/usr/bin/env python3
"""
Script de démarrage avec Web Studio Community
"""

import subprocess
import time
import sys
import os

def start_odoo_with_studio():
    """Démarrer Odoo avec Web Studio Community"""
    
    print("🚀 DÉMARRAGE ODOO AVEC WEB STUDIO COMMUNITY")
    print("=" * 50)
    
    # Configuration
    PORT = 8070
    DATABASE = "sama_syndicat_final_1756812346"
    ODOO_BIN = "/var/odoo/odoo18/odoo-bin"
    # Addon path incluant le répertoire avec web_studio_community
    ADDONS_PATH = "/var/odoo/odoo18/odoo/addons,/var/odoo/odoo18/addons,/tmp/addons_sama_syndicat,/home/grand-as/psagsn/custom_addons"
    
    # Arrêter les processus existants
    print("🛑 Arrêt des processus existants...")
    subprocess.run(['pkill', '-f', 'odoo-bin'], capture_output=True)
    time.sleep(2)
    
    # Vérifier que Odoo existe
    if not os.path.exists(ODOO_BIN):
        print(f"❌ Odoo non trouvé à: {ODOO_BIN}")
        return False
    
    # Vérifier que web_studio_community est accessible
    studio_path = "/tmp/addons_sama_syndicat/web_studio_community/__manifest__.py"
    if not os.path.exists(studio_path):
        print(f"❌ Web Studio Community non trouvé à: {studio_path}")
        return False
    else:
        print("✅ Web Studio Community détecté")
    
    # Démarrer Odoo en arrière-plan
    print("⚡ Démarrage d'Odoo avec Web Studio...")
    cmd = [
        'python3', ODOO_BIN,
        f'--addons-path={ADDONS_PATH}',
        f'--database={DATABASE}',
        f'--xmlrpc-port={PORT}',
        '--dev=reload,xml',
        '--log-level=warn'
    ]
    
    print(f"📂 Addon paths: {ADDONS_PATH}")
    
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
    
    print("\n🎯 RÉSULTAT FINAL")
    print("=" * 20)
    print("✅ Odoo démarré avec succès")
    print("✅ Web Studio Community disponible")
    print(f"🌐 Interface: http://localhost:{PORT}/web")
    print("📍 Pour installer Web Studio:")
    print("   1. Allez dans Apps")
    print("   2. Cliquez sur 'Update Apps List'")
    print("   3. Recherchez 'Web Studio Community'")
    print("   4. Cliquez sur 'Install'")
    print("\n💡 Le serveur Odoo continue de tourner en arrière-plan")
    print("🛑 Pour l'arrêter: pkill -f odoo-bin")
    
    return True

if __name__ == "__main__":
    success = start_odoo_with_studio()
    if success:
        print("\n🎊 Succès ! Web Studio Community est maintenant disponible")
    else:
        print("\n❌ Échec du démarrage")
    sys.exit(0 if success else 1)