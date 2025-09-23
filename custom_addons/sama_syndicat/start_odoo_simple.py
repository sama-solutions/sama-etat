#!/usr/bin/env python3
"""
Script de démarrage simple pour Odoo avec Web Studio Community
"""

import subprocess
import time
import sys
import os

def start_odoo():
    """Démarrer Odoo simplement"""
    
    print("🚀 DÉMARRAGE ODOO AVEC WEB STUDIO COMMUNITY")
    print("=" * 50)
    
    # Configuration
    PORT = 8070
    DATABASE = "sama_syndicat_final_1756812346"
    ODOO_BIN = "/var/odoo/odoo18/odoo-bin"
    # Addon path incluant web_studio_community
    ADDONS_PATH = "/var/odoo/odoo18/odoo/addons,/var/odoo/odoo18/addons,/tmp/addons_sama_syndicat"
    
    # Arrêter les processus existants
    print("🛑 Arrêt des processus existants...")
    subprocess.run(['pkill', '-f', 'odoo-bin'], capture_output=True)
    time.sleep(3)
    
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
    
    print(f"📂 Addon paths: {ADDONS_PATH}")
    print(f"🗄️ Database: {DATABASE}")
    print(f"🌐 Port: {PORT}")
    
    # Commande Odoo
    cmd = [
        'python3', ODOO_BIN,
        f'--addons-path={ADDONS_PATH}',
        f'--database={DATABASE}',
        f'--xmlrpc-port={PORT}',
        '--log-level=info'
    ]
    
    print("⚡ Démarrage d'Odoo...")
    print(f"Commande: {' '.join(cmd)}")
    
    # Démarrer Odoo
    try:
        subprocess.run(cmd)
    except KeyboardInterrupt:
        print("\n🛑 Arrêt demandé par l'utilisateur")
        return True
    except Exception as e:
        print(f"❌ Erreur lors du démarrage: {e}")
        return False
    
    return True

if __name__ == "__main__":
    print("💡 Appuyez sur Ctrl+C pour arrêter Odoo")
    success = start_odoo()
    if success:
        print("\n✅ Odoo s'est arrêté proprement")
    else:
        print("\n❌ Problème lors du démarrage")
    sys.exit(0 if success else 1)