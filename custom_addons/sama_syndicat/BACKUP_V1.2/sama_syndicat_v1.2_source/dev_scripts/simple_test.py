#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Script de test simple pour sama_syndicat
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
DB_NAME = "sama_syndicat_test"
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

def setup_environment():
    """Configure l'environnement"""
    env = os.environ.copy()
    env['PATH'] = f"{VENV_PATH}/bin:{env['PATH']}"
    return env

def create_and_install():
    """Crée la base et installe le module"""
    print("🏛️  SAMA SYNDICAT - Installation")
    print("=" * 50)
    
    # Arrêter les processus sur le port
    kill_processes_on_port(PORT)
    
    env = setup_environment()
    
    # Supprimer et recréer la base
    print("🗄️  Préparation de la base de données...")
    subprocess.run(f"dropdb -U {DB_USER} --if-exists {DB_NAME}", shell=True, env=env)
    subprocess.run(f"createdb -U {DB_USER} -O {DB_USER} {DB_NAME}", shell=True, env=env)
    
    # Installation du module
    print("📦 Installation du module sama_syndicat...")
    install_cmd = f"""
    cd {ODOO_PATH} && python3 odoo-bin \
        --addons-path={ADDONS_PATH} \
        --database={DB_NAME} \
        --db_user={DB_USER} \
        --db_password={DB_PASSWORD} \
        --init=sama_syndicat \
        --stop-after-init \
        --log-level=info \
        --without-demo=all
    """
    
    result = subprocess.run(install_cmd, shell=True, env=env)
    
    if result.returncode == 0:
        print("✅ Module installé avec succès!")
        return True
    else:
        print("❌ Erreur lors de l'installation")
        return False

def start_server():
    """Démarre le serveur"""
    print("🚀 Démarrage du serveur...")
    
    env = setup_environment()
    
    start_cmd = f"""
    cd {ODOO_PATH} && python3 odoo-bin \
        --addons-path={ADDONS_PATH} \
        --database={DB_NAME} \
        --db_user={DB_USER} \
        --db_password={DB_PASSWORD} \
        --xmlrpc-port={PORT} \
        --log-level=info
    """
    
    print(f"🌐 Serveur accessible sur: http://localhost:{PORT}")
    print(f"🔑 Base de données: {DB_NAME}")
    print("🛑 Appuyez sur Ctrl+C pour arrêter")
    print("-" * 50)
    
    try:
        subprocess.run(start_cmd, shell=True, env=env)
    except KeyboardInterrupt:
        print("\n🛑 Arrêt du serveur")
        kill_processes_on_port(PORT)

def main():
    """Fonction principale"""
    if create_and_install():
        start_server()

if __name__ == "__main__":
    main()