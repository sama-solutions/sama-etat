#!/usr/bin/env python3
"""
Script de test pour installer web_studio_community
"""

import subprocess
import time
import sys
import os

def test_module_install():
    """Tester l'installation du module web_studio_community"""
    
    print("🧪 TEST D'INSTALLATION WEB STUDIO COMMUNITY")
    print("=" * 50)
    
    # Configuration
    PORT = 8070
    DATABASE = "sama_syndicat_final_1756812346"
    ODOO_BIN = "/var/odoo/odoo18/odoo-bin"
    ADDONS_PATH = "/var/odoo/odoo18/odoo/addons,/var/odoo/odoo18/addons,/tmp/addons_sama_syndicat"
    
    # Arrêter les processus existants
    print("🛑 Arrêt des processus existants...")
    subprocess.run(['pkill', '-f', 'odoo-bin'], capture_output=True)
    time.sleep(3)
    
    # Vérifier que le module existe
    studio_path = "/tmp/addons_sama_syndicat/web_studio_community/__manifest__.py"
    if not os.path.exists(studio_path):
        print(f"❌ Web Studio Community non trouvé à: {studio_path}")
        return False
    else:
        print("✅ Web Studio Community détecté")
    
    # Vérifier les fichiers de sécurité
    security_path = "/tmp/addons_sama_syndicat/web_studio_community/security/ir.model.access.csv"
    if not os.path.exists(security_path):
        print(f"❌ Fichier de sécurité manquant: {security_path}")
        return False
    else:
        print("✅ Fichier de sécurité détecté")
    
    # Commande pour installer le module
    cmd = [
        'python3', ODOO_BIN,
        f'--addons-path={ADDONS_PATH}',
        f'--database={DATABASE}',
        f'--xmlrpc-port={PORT}',
        '-i', 'web_studio_community',
        '--stop-after-init',
        '--log-level=info'
    ]
    
    print("⚡ Test d'installation du module...")
    print(f"Commande: {' '.join(cmd)}")
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=120)
        
        if result.returncode == 0:
            print("✅ Module installé avec succès !")
            print("📋 Sortie:")
            print(result.stdout[-1000:])  # Dernières 1000 caractères
            return True
        else:
            print("❌ Erreur lors de l'installation")
            print("📋 Erreur:")
            print(result.stderr[-1000:])  # Dernières 1000 caractères
            return False
            
    except subprocess.TimeoutExpired:
        print("⏰ Timeout - Installation trop longue")
        return False
    except Exception as e:
        print(f"❌ Erreur inattendue: {e}")
        return False

if __name__ == "__main__":
    success = test_module_install()
    if success:
        print("\n🎉 Test réussi ! Le module peut être installé")
    else:
        print("\n❌ Test échoué")
    sys.exit(0 if success else 1)