#!/usr/bin/env python3
"""
Script pour redémarrer le serveur SAMA SYNDICAT avec rechargement des contrôleurs
"""

import os
import signal
import subprocess
import time
import sys

def restart_sama_syndicat():
    """Redémarrer le serveur SAMA SYNDICAT"""
    
    print("🔄 Redémarrage du serveur SAMA SYNDICAT...")
    
    # Trouver le processus Odoo
    try:
        result = subprocess.run(['ps', 'aux'], capture_output=True, text=True)
        lines = result.stdout.split('\n')
        
        odoo_pid = None
        for line in lines:
            if 'python3 odoo-bin' in line and '8070' in line:
                parts = line.split()
                odoo_pid = int(parts[1])
                break
                
        if odoo_pid:
            print(f"📍 Processus Odoo trouvé (PID: {odoo_pid})")
            
            # Arrêter le processus
            print("⏹️ Arrêt du serveur...")
            os.kill(odoo_pid, signal.SIGTERM)
            
            # Attendre que le processus se termine
            time.sleep(3)
            
            # Vérifier si le processus est toujours actif
            try:
                os.kill(odoo_pid, 0)
                print("⚠️ Processus encore actif, force l'arrêt...")
                os.kill(odoo_pid, signal.SIGKILL)
                time.sleep(2)
            except ProcessLookupError:
                print("✅ Processus arrêté")
                
        else:
            print("ℹ️ Aucun processus Odoo trouvé")
            
    except Exception as e:
        print(f"❌ Erreur lors de l'arrêt: {e}")
        
    # Redémarrer le serveur
    print("🚀 Redémarrage du serveur...")
    
    cmd = [
        'python3', 'odoo-bin',
        '--addons-path=/var/odoo/odoo18/odoo/addons,/var/odoo/odoo18/addons,/tmp/addons_sama_syndicat',
        '--database=sama_syndicat_final_1756812346',
        '--xmlrpc-port=8070',
        '--dev=reload,xml',  # Mode développement avec rechargement
        '--log-level=info'
    ]
    
    print(f"📝 Commande: {' '.join(cmd)}")
    print("🔄 Démarrage en cours...")
    print("📋 Logs du serveur:")
    print("-" * 50)
    
    # Démarrer le serveur
    try:
        subprocess.run(cmd, cwd='/var/odoo/odoo18')
    except KeyboardInterrupt:
        print("\n⏹️ Arrêt demandé par l'utilisateur")
    except Exception as e:
        print(f"❌ Erreur lors du démarrage: {e}")

if __name__ == "__main__":
    restart_sama_syndicat()