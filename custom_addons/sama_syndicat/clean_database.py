#!/usr/bin/env python3
"""
Nettoyage de la base de données pour résoudre les problèmes avec ir.model.fields
"""

import subprocess
import time
import sys
import xmlrpc.client

def clean_database():
    """Nettoyer la base de données"""
    print("🧹 NETTOYAGE DE LA BASE DE DONNÉES")
    print("=" * 50)
    
    # Configuration
    PORT = 8076
    DATABASE = "sama_syndicat_final_1756812346"
    ODOO_BIN = "/var/odoo/odoo18/odoo-bin"
    ADDONS_PATH = "/var/odoo/odoo18/odoo/addons,/var/odoo/odoo18/addons,/tmp/addons_sama_syndicat"
    
    # Arrêter les processus existants
    print("🛑 Arrêt des processus existants...")
    subprocess.run(['pkill', '-f', 'odoo-bin'], capture_output=True)
    time.sleep(3)
    
    # Démarrer Odoo en mode shell pour nettoyer
    print("🚀 Démarrage d'Odoo en mode shell...")
    
    # Script de nettoyage
    cleanup_script = f"""
import odoo
from odoo import api, SUPERUSER_ID

# Connexion à la base de données
db = odoo.sql_db.db_connect('{DATABASE}')
with db.cursor() as cr:
    env = api.Environment(cr, SUPERUSER_ID, {{}})
    
    print("🔍 Recherche des enregistrements problématiques...")
    
    # Supprimer les enregistrements ir.model.data liés à web_studio_community
    try:
        model_data = env['ir.model.data'].search([
            ('module', '=', 'web_studio_community'),
            ('model', '=', 'ir.model.fields')
        ])
        if model_data:
            print(f"🗑️ Suppression de {{len(model_data)}} enregistrements ir.model.data...")
            model_data.unlink()
        else:
            print("✅ Aucun enregistrement ir.model.data problématique trouvé")
    except Exception as e:
        print(f"⚠️ Erreur lors du nettoyage ir.model.data: {{e}}")
    
    # Vérifier les champs personnalisés ajoutés par notre module
    try:
        custom_fields = env['ir.model.fields'].search([
            ('model', '=', 'ir.model.fields'),
            ('name', 'in', ['default_value', 'help', 'domain', 'context']),
            ('state', '=', 'manual')
        ])
        if custom_fields:
            print(f"🗑️ Suppression de {{len(custom_fields)}} champs personnalisés...")
            custom_fields.unlink()
        else:
            print("✅ Aucun champ personnalisé problématique trouvé")
    except Exception as e:
        print(f"⚠️ Erreur lors du nettoyage des champs: {{e}}")
    
    # Nettoyer le cache
    try:
        env.registry.clear_caches()
        print("✅ Cache nettoyé")
    except Exception as e:
        print(f"⚠️ Erreur lors du nettoyage du cache: {{e}}")
    
    # Valider les changements
    cr.commit()
    print("✅ Changements validés")

print("🎉 Nettoyage terminé")
"""
    
    # Écrire le script dans un fichier temporaire
    with open('/tmp/cleanup_script.py', 'w') as f:
        f.write(cleanup_script)
    
    # Exécuter le script de nettoyage
    cmd = [
        'python3', ODOO_BIN,
        'shell',
        f'--addons-path={ADDONS_PATH}',
        f'--database={DATABASE}',
        '--shell-interface=python',
        '--script=/tmp/cleanup_script.py'
    ]
    
    print("🧹 Exécution du nettoyage...")
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
        if result.returncode == 0:
            print("✅ Nettoyage réussi")
            print(result.stdout)
        else:
            print("❌ Erreur lors du nettoyage")
            print(result.stderr)
            return False
    except subprocess.TimeoutExpired:
        print("⏰ Timeout lors du nettoyage")
        return False
    except Exception as e:
        print(f"❌ Erreur: {e}")
        return False
    
    # Mettre à jour le module après nettoyage
    print("\n🔄 Mise à jour du module après nettoyage...")
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
            print("✅ Module mis à jour avec succès")
        else:
            print("❌ Erreur lors de la mise à jour")
            print(result.stderr[-500:])
            return False
    except Exception as e:
        print(f"❌ Erreur lors de la mise à jour: {e}")
        return False
    
    # Nettoyer le fichier temporaire
    try:
        subprocess.run(['rm', '/tmp/cleanup_script.py'], capture_output=True)
    except:
        pass
    
    return True

if __name__ == "__main__":
    success = clean_database()
    if success:
        print("\n🎉 NETTOYAGE RÉUSSI!")
        print("La base de données a été nettoyée.")
        print("Vous pouvez maintenant tester l'accès aux paramètres.")
    else:
        print("\n❌ Échec du nettoyage")
    
    sys.exit(0 if success else 1)