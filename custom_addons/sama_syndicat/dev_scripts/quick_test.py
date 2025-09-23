#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Test rapide pour sama_syndicat
"""

import os
import sys
import subprocess
import psutil
import time

# Configuration
ODOO_PATH = "/var/odoo/odoo18"
VENV_PATH = "/home/grand-as/odoo18-venv"
ADDONS_PATH = "/home/grand-as/psagsn/custom_addons"
DB_NAME = "sama_syndicat_quick"
DB_USER = "odoo"
DB_PASSWORD = "odoo"
PORT = 8070

def kill_port_processes():
    """Arrête les processus sur le port"""
    print(f"🔍 Arrêt des processus sur le port {PORT}")
    for proc in psutil.process_iter(['pid', 'name', 'connections']):
        try:
            for conn in proc.info['connections'] or []:
                if conn.laddr.port == PORT:
                    print(f"🔪 Arrêt du processus {proc.info['name']} (PID: {proc.info['pid']})")
                    proc.kill()
        except:
            pass
    time.sleep(2)

def setup_env():
    """Configure l'environnement"""
    env = os.environ.copy()
    env['PATH'] = f"{VENV_PATH}/bin:{env['PATH']}"
    return env

def test_syntax():
    """Test de syntaxe"""
    print("🔍 Test de syntaxe...")
    result = subprocess.run([
        sys.executable, 
        "sama_syndicat/dev_scripts/validate_syntax.py"
    ], capture_output=True, text=True)
    
    if result.returncode == 0:
        print("✅ Syntaxe OK")
        return True
    else:
        print("❌ Erreurs de syntaxe:")
        print(result.stderr)
        return False

def create_db(env):
    """Crée la base"""
    print(f"🗄️  Création de la base {DB_NAME}")
    subprocess.run(f"dropdb -U {DB_USER} --if-exists {DB_NAME}", shell=True, env=env)
    result = subprocess.run(f"createdb -U {DB_USER} -O {DB_USER} {DB_NAME}", shell=True, env=env)
    return result.returncode == 0

def install_module(env):
    """Installation du module"""
    print("📦 Installation du module...")
    
    cmd = f"""cd {ODOO_PATH} && timeout 120 python3 odoo-bin \
        --addons-path={ADDONS_PATH} \
        --database={DB_NAME} \
        --db_user={DB_USER} \
        --db_password={DB_PASSWORD} \
        --init=sama_syndicat \
        --stop-after-init \
        --log-level=error"""
    
    result = subprocess.run(cmd, shell=True, env=env, capture_output=True, text=True)
    
    if result.returncode == 0:
        print("✅ Installation réussie")
        return True
    else:
        print("❌ Erreur d'installation:")
        print(result.stderr[-1000:])  # Dernières 1000 caractères
        return False

def main():
    """Test principal"""
    print("🏛️  SAMA SYNDICAT - TEST RAPIDE")
    print("=" * 40)
    
    # Arrêt des processus
    kill_port_processes()
    
    # Configuration
    env = setup_env()
    
    # Test syntaxe
    if not test_syntax():
        return False
    
    # Création base
    if not create_db(env):
        print("❌ Échec création base")
        return False
    
    # Installation
    if not install_module(env):
        return False
    
    print("🎉 Test réussi!")
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)