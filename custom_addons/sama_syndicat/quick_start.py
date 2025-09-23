#!/usr/bin/env python3
"""
Démarrage ultra-rapide SAMA SYNDICAT
"""

import subprocess
import sys

# Configuration
PORT = 8070
DB = "sama_syndicat_final_1756812346"
ODOO = "/var/odoo/odoo18/odoo-bin"
ADDONS = "/var/odoo/odoo18/odoo/addons,/var/odoo/odoo18/addons,/tmp/addons_sama_syndicat"

print("🚀 SAMA SYNDICAT - DÉMARRAGE RAPIDE")
print("=" * 40)

# Arrêter les processus existants
print("🛑 Arrêt des processus...")
subprocess.run(['pkill', '-f', 'odoo-bin'], capture_output=True)

# Démarrer Odoo
print("⚡ Démarrage d'Odoo...")
print(f"🌐 Interface: http://localhost:{PORT}/web")
print("💡 Ctrl+C pour arrêter")
print("=" * 40)

try:
    subprocess.run([
        'python3', ODOO,
        f'--addons-path={ADDONS}',
        f'--database={DB}',
        f'--xmlrpc-port={PORT}',
        '--dev=reload,xml'
    ])
except KeyboardInterrupt:
    print("\n🛑 Arrêt")
    subprocess.run(['pkill', '-f', 'odoo-bin'], capture_output=True)
except Exception as e:
    print(f"❌ Erreur: {e}")
    sys.exit(1)