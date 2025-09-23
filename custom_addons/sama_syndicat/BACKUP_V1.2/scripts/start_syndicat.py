#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Script de démarrage pour le module sama_syndicat
Version de production - Port 8070
"""

import os
import sys
import subprocess
import time
import psutil

# Configuration
ODOO_PATH = "/var/odoo/odoo18"
VENV_PATH = "/home/grand-as/odoo18-venv"
ADDONS_PATH = "/home/grand-as/psagsn/custom_addons"
DB_NAME = "sama_syndicat_prod"
DB_USER = "odoo"
DB_PASSWORD = "odoo"
PORT = 8070

def kill_processes_on_port(port):
    """Tue tous les processus utilisant le port spécifié"""
    print(f"🔍 Vérification du port {port}...")
    killed = False
    
    for proc in psutil.process_iter(['pid', 'name', 'connections']):
        try:
            for conn in proc.info['connections'] or []:
                if conn.laddr.port == port:
                    print(f"🔪 Arrêt du processus {proc.info['name']} (PID: {proc.info['pid']})")
                    proc.kill()
                    killed = True
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass
    
    if killed:
        time.sleep(2)
        print(f"✅ Port {port} libéré")

def start_sama_syndicat():
    """Démarre SAMA SYNDICAT"""
    print("🏛️  DÉMARRAGE DE SAMA SYNDICAT")
    print("=" * 50)
    
    # Arrêter les processus sur le port
    kill_processes_on_port(PORT)
    
    # Configuration de l'environnement
    env = os.environ.copy()
    env['PATH'] = f"{VENV_PATH}/bin:{env['PATH']}"
    env['PYTHONPATH'] = f"{ODOO_PATH}:{ADDONS_PATH}"
    
    # Commande de démarrage
    start_cmd = f"""
    cd {ODOO_PATH} && python3 odoo-bin \
        --addons-path={ADDONS_PATH} \
        --database={DB_NAME} \
        --db_user={DB_USER} \
        --db_password={DB_PASSWORD} \
        --xmlrpc-port={PORT} \
        --log-level=info \
        --dev=reload
    """
    
    print(f"🌐 Serveur accessible sur: http://localhost:{PORT}")
    print(f"🔑 Base de données: {DB_NAME}")
    print(f"📁 Modules: {ADDONS_PATH}")
    print("🛑 Appuyez sur Ctrl+C pour arrêter")
    print("-" * 50)
    
    try:
        subprocess.run(start_cmd, shell=True, env=env)
    except KeyboardInterrupt:
        print("\n🛑 Arrêt de SAMA SYNDICAT")
        kill_processes_on_port(PORT)

if __name__ == "__main__":
    start_sama_syndicat()