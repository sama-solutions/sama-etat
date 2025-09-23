#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Script de lancement final pour SAMA SYNDICAT
Arrête les processus sur le port dédié et lance le module
"""

import os
import sys
import subprocess
import time
import psutil
import signal

# Configuration
ODOO_PATH = "/var/odoo/odoo18"
VENV_PATH = "/home/grand-as/odoo18-venv"
ADDONS_PATH = "/home/grand-as/psagsn/custom_addons"
DB_NAME = "sama_syndicat_prod"
DB_USER = "odoo"
DB_PASSWORD = "odoo"
PORT = 8070

def print_banner():
    """Affiche la bannière"""
    print("🏛️" + "=" * 58 + "🏛️")
    print("🏛️" + " " * 20 + "SAMA SYNDICAT" + " " * 25 + "🏛️")
    print("🏛️" + " " * 15 + "Gestion Zéro Papier" + " " * 20 + "🏛️")
    print("🏛️" + " " * 58 + "🏛️")
    print("🏛️" + " " * 15 + "POLITECH SÉNÉGAL" + " " * 22 + "🏛️")
    print("🏛️" + "=" * 58 + "🏛️")

def kill_processes_on_port():
    """Arrête tous les processus utilisant le port dédié"""
    print(f"🔍 Vérification du port {PORT}...")
    
    killed_processes = []
    for proc in psutil.process_iter(['pid', 'name', 'connections', 'cmdline']):
        try:
            for conn in proc.info['connections'] or []:
                if conn.laddr.port == PORT:
                    cmdline = ' '.join(proc.info['cmdline'] or [])
                    print(f"🔪 Arrêt du processus {proc.info['name']} (PID: {proc.info['pid']})")
                    proc.terminate()
                    killed_processes.append(proc.info['pid'])
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass
    
    if killed_processes:
        print(f"⏳ Attente de l'arrêt propre...")
        time.sleep(3)
        
        # Vérifier si les processus sont bien arrêtés
        for pid in killed_processes:
            try:
                proc = psutil.Process(pid)
                if proc.is_running():
                    print(f"🔪 Arrêt forcé du processus {pid}")
                    proc.kill()
            except:
                pass
        
        print(f"✅ Port {PORT} libéré")
    else:
        print(f"✅ Port {PORT} disponible")

def check_prerequisites():
    """Vérifie les prérequis"""
    print("🔧 Vérification des prérequis...")
    
    errors = []
    
    # Vérifier Odoo
    if not os.path.exists(ODOO_PATH):
        errors.append(f"Odoo introuvable: {ODOO_PATH}")
    
    # Vérifier l'environnement virtuel
    if not os.path.exists(VENV_PATH):
        errors.append(f"Environnement virtuel introuvable: {VENV_PATH}")
    
    # Vérifier les addons
    if not os.path.exists(ADDONS_PATH):
        errors.append(f"Répertoire addons introuvable: {ADDONS_PATH}")
    
    # Vérifier le module
    module_path = os.path.join(ADDONS_PATH, "sama_syndicat")
    if not os.path.exists(module_path):
        errors.append(f"Module sama_syndicat introuvable: {module_path}")
    
    if errors:
        print("❌ Erreurs de configuration:")
        for error in errors:
            print(f"  • {error}")
        return False
    
    print("✅ Prérequis vérifiés")
    return True

def setup_environment():
    """Configure l'environnement"""
    env = os.environ.copy()
    env['PATH'] = f"{VENV_PATH}/bin:{env['PATH']}"
    env['PYTHONPATH'] = f"{ODOO_PATH}:{ADDONS_PATH}"
    return env

def check_database_exists(env):
    """Vérifie si la base de données existe"""
    print(f"🗄️  Vérification de la base {DB_NAME}...")
    
    check_cmd = f"psql -U {DB_USER} -lqt | cut -d \\| -f 1 | grep -qw {DB_NAME}"
    result = subprocess.run(check_cmd, shell=True, env=env, capture_output=True)
    
    if result.returncode == 0:
        print(f"✅ Base de données {DB_NAME} trouvée")
        return True
    else:
        print(f"⚠️  Base de données {DB_NAME} non trouvée")
        return False

def create_database_if_needed(env):
    """Crée la base de données si nécessaire"""
    if not check_database_exists(env):
        print(f"🗄️  Création de la base {DB_NAME}...")
        
        create_cmd = f"createdb -U {DB_USER} -O {DB_USER} {DB_NAME}"
        result = subprocess.run(create_cmd, shell=True, env=env, capture_output=True)
        
        if result.returncode == 0:
            print(f"✅ Base {DB_NAME} créée")
            return True
        else:
            print(f"❌ Échec de création: {result.stderr.decode()}")
            return False
    return True

def install_module_if_needed(env):
    """Installe le module si nécessaire"""
    print("📦 Vérification de l'installation du module...")
    
    # Vérifier si le module est installé
    check_cmd = f"""psql -U {DB_USER} -d {DB_NAME} -tAc "SELECT state FROM ir_module_module WHERE name='sama_syndicat';" """
    result = subprocess.run(check_cmd, shell=True, env=env, capture_output=True, text=True)
    
    if result.returncode == 0 and 'installed' in result.stdout:
        print("✅ Module déjà installé")
        return True
    
    print("📦 Installation du module sama_syndicat...")
    
    install_cmd = f"""cd {ODOO_PATH} && python3 odoo-bin \
        --addons-path={ADDONS_PATH} \
        --database={DB_NAME} \
        --db_user={DB_USER} \
        --db_password={DB_PASSWORD} \
        --init=sama_syndicat \
        --stop-after-init \
        --log-level=info \
        --without-demo=all"""
    
    result = subprocess.run(install_cmd, shell=True, env=env, capture_output=True, text=True)
    
    if result.returncode == 0:
        print("✅ Module installé avec succès")
        return True
    else:
        print("❌ Erreur d'installation:")
        print(result.stderr[-500:])  # Dernières 500 caractères
        return False

def start_odoo_server(env):
    """Démarre le serveur Odoo"""
    print("🚀 Démarrage de SAMA SYNDICAT...")
    
    start_cmd = f"""cd {ODOO_PATH} && python3 odoo-bin \
        --addons-path={ADDONS_PATH} \
        --database={DB_NAME} \
        --db_user={DB_USER} \
        --db_password={DB_PASSWORD} \
        --xmlrpc-port={PORT} \
        --log-level=info \
        --dev=reload"""
    
    print(f"🌐 Serveur accessible sur: http://localhost:{PORT}")
    print(f"🔑 Base de données: {DB_NAME}")
    print(f"📁 Modules: {ADDONS_PATH}")
    print(f"🏛️  Module: SAMA SYNDICAT")
    print("🛑 Appuyez sur Ctrl+C pour arrêter")
    print("-" * 60)
    
    try:
        subprocess.run(start_cmd, shell=True, env=env)
    except KeyboardInterrupt:
        print("\n🛑 Arrêt de SAMA SYNDICAT demandé")
        kill_processes_on_port()
        print("✅ SAMA SYNDICAT arrêté proprement")

def main():
    """Fonction principale"""
    print_banner()
    
    try:
        # Vérifications préliminaires
        if not check_prerequisites():
            sys.exit(1)
        
        # Arrêt des processus sur le port
        kill_processes_on_port()
        
        # Configuration de l'environnement
        env = setup_environment()
        
        # Création de la base si nécessaire
        if not create_database_if_needed(env):
            sys.exit(1)
        
        # Installation du module si nécessaire
        if not install_module_if_needed(env):
            print("⚠️  Tentative de démarrage malgré l'erreur d'installation...")
        
        # Démarrage du serveur
        start_odoo_server(env)
        
    except Exception as e:
        print(f"💥 Erreur inattendue: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()