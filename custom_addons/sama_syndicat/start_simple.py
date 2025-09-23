#!/usr/bin/env python3
"""
Script de démarrage simple pour SAMA SYNDICAT (version basique)
Arrête le processus sur le port 8070 et démarre le module
"""

import os
import sys
import time
import subprocess
import signal

# Configuration
PORT = 8070
DATABASE = "sama_syndicat_final_1756812346"
ODOO_BIN = "/var/odoo/odoo18/odoo-bin"
ADDONS_PATH = "/var/odoo/odoo18/odoo/addons,/var/odoo/odoo18/addons,/tmp/addons_sama_syndicat"

def print_banner():
    """Afficher la bannière de démarrage"""
    print("=" * 50)
    print("🚀 SAMA SYNDICAT - DÉMARRAGE SIMPLE")
    print("=" * 50)
    print(f"Port: {PORT}")
    print(f"Base: {DATABASE}")
    print("=" * 50)

def stop_process_simple():
    """Arrêter le processus de manière simple"""
    print(f"🛑 Arrêt des processus sur le port {PORT}...")
    
    try:
        # Méthode 1: pkill odoo
        subprocess.run(['pkill', '-f', 'odoo-bin'], timeout=5)
        print("✅ Processus odoo-bin arrêtés")
        time.sleep(2)
    except:
        pass
    
    try:
        # Méthode 2: kill par port avec lsof
        result = subprocess.run(['lsof', '-ti', f':{PORT}'], 
                              capture_output=True, text=True, timeout=5)
        if result.stdout.strip():
            pids = result.stdout.strip().split('\n')
            for pid in pids:
                if pid:
                    subprocess.run(['kill', pid], timeout=2)
                    print(f"✅ Processus {pid} arrêté")
    except:
        pass
    
    try:
        # Méthode 3: fuser (si disponible)
        subprocess.run(['fuser', '-k', f'{PORT}/tcp'], timeout=5)
        print(f"✅ Port {PORT} libéré")
    except:
        pass
    
    print("⏳ Attente de la libération du port...")
    time.sleep(3)

def start_odoo_simple():
    """Démarrer Odoo de manière simple"""
    print("🚀 Démarrage d'Odoo...")
    
    # Vérifier si odoo-bin existe
    if not os.path.exists(ODOO_BIN):
        print(f"❌ Odoo non trouvé à: {ODOO_BIN}")
        print("💡 Essayez d'ajuster le chemin dans le script")
        return False
    
    # Commande de démarrage
    cmd = [
        "python3", ODOO_BIN,
        f"--addons-path={ADDONS_PATH}",
        f"--database={DATABASE}",
        f"--xmlrpc-port={PORT}",
        "--dev=reload,xml"
    ]
    
    print("📋 Commande:")
    print(" ".join(cmd))
    print()
    print(f"🌐 Interface: http://localhost:{PORT}")
    print("💡 Ctrl+C pour arrêter")
    print("=" * 50)
    
    try:
        # Démarrer Odoo
        subprocess.run(cmd)
        return True
    except KeyboardInterrupt:
        print("\n🛑 Arrêt demandé")
        return True
    except Exception as e:
        print(f"❌ Erreur: {e}")
        return False

def main():
    """Fonction principale"""
    print_banner()
    
    try:
        # Arrêter les processus existants
        stop_process_simple()
        
        # Démarrer Odoo
        start_odoo_simple()
        
    except KeyboardInterrupt:
        print("\n🛑 Arrêt")
    except Exception as e:
        print(f"❌ Erreur: {e}")

if __name__ == "__main__":
    main()