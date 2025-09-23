#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Script de test pour le module sama_syndicat
Utilise le port 8070 pour éviter les conflits
"""

import os
import sys
import subprocess
import time
import signal
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
    print(f"🔍 Recherche des processus sur le port {port}...")
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
        print(f"✅ Processus sur le port {port} arrêtés")
    else:
        print(f"ℹ️  Aucun processus trouvé sur le port {port}")

def run_command(command, cwd=None, env=None):
    """Exécute une commande et retourne le résultat"""
    print(f"🚀 Exécution: {command}")
    try:
        result = subprocess.run(
            command, 
            shell=True, 
            cwd=cwd, 
            env=env,
            capture_output=True, 
            text=True,
            timeout=300
        )
        if result.returncode != 0:
            print(f"❌ Erreur: {result.stderr}")
            return False, result.stderr
        else:
            print(f"✅ Succès: {result.stdout[:200]}...")
            return True, result.stdout
    except subprocess.TimeoutExpired:
        print("⏰ Timeout de la commande")
        return False, "Timeout"
    except Exception as e:
        print(f"💥 Exception: {e}")
        return False, str(e)

def setup_environment():
    """Configure l'environnement"""
    print("🔧 Configuration de l'environnement...")
    
    # Variables d'environnement
    env = os.environ.copy()
    env['PATH'] = f"{VENV_PATH}/bin:{env['PATH']}"
    env['PYTHONPATH'] = f"{ODOO_PATH}:{ADDONS_PATH}"
    
    return env

def create_database():
    """Crée la base de données de test"""
    print(f"🗄️  Création de la base de données {DB_NAME}...")
    
    env = setup_environment()
    
    # Supprimer la base si elle existe
    drop_cmd = f"dropdb -U {DB_USER} --if-exists {DB_NAME}"
    run_command(drop_cmd, env=env)
    
    # Créer la nouvelle base
    create_cmd = f"createdb -U {DB_USER} -O {DB_USER} {DB_NAME}"
    success, output = run_command(create_cmd, env=env)
    
    if success:
        print(f"✅ Base de données {DB_NAME} créée")
        return True
    else:
        print(f"❌ Échec de création de la base: {output}")
        return False

def install_module():
    """Installe le module sama_syndicat"""
    print("📦 Installation du module sama_syndicat...")
    
    env = setup_environment()
    
    # Commande d'installation
    install_cmd = f"""
    cd {ODOO_PATH} && python3 odoo-bin \
        --addons-path={ADDONS_PATH} \
        --database={DB_NAME} \
        --db_user={DB_USER} \
        --db_password={DB_PASSWORD} \
        --init=sama_syndicat \
        --stop-after-init \
        --log-level=info
    """
    
    success, output = run_command(install_cmd, env=env)
    
    if success:
        print("✅ Module installé avec succès")
        return True
    else:
        print(f"❌ Échec d'installation: {output}")
        return False

def start_odoo_server():
    """Démarre le serveur Odoo"""
    print(f"🚀 Démarrage du serveur Odoo sur le port {PORT}...")
    
    env = setup_environment()
    
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
    print("🛑 Appuyez sur Ctrl+C pour arrêter")
    
    try:
        subprocess.run(start_cmd, shell=True, env=env)
    except KeyboardInterrupt:
        print("\n🛑 Arrêt du serveur demandé")

def test_module_loading():
    """Teste le chargement du module"""
    print("🧪 Test de chargement du module...")
    
    env = setup_environment()
    
    # Test de chargement
    test_cmd = f"""
    cd {ODOO_PATH} && python3 -c "
import sys
sys.path.insert(0, '{ADDONS_PATH}')
try:
    import sama_syndicat
    print('✅ Module sama_syndicat importé avec succès')
    print(f'📍 Chemin: {{sama_syndicat.__file__}}')
except Exception as e:
    print(f'❌ Erreur d\\'import: {{e}}')
    sys.exit(1)
"
    """
    
    success, output = run_command(test_cmd, env=env)
    return success

def main():
    """Fonction principale"""
    print("🏛️  SAMA SYNDICAT - Script de Test")
    print("=" * 50)
    
    try:
        # 1. Arrêter les processus sur le port
        kill_processes_on_port(PORT)
        
        # 2. Tester l'import du module
        if not test_module_loading():
            print("❌ Échec du test d'import")
            return
        
        # 3. Créer la base de données
        if not create_database():
            print("❌ Échec de création de la base")
            return
        
        # 4. Installer le module
        if not install_module():
            print("❌ Échec d'installation du module")
            return
        
        # 5. Démarrer le serveur
        start_odoo_server()
        
    except KeyboardInterrupt:
        print("\n🛑 Arrêt du script")
    except Exception as e:
        print(f"💥 Erreur inattendue: {e}")
    finally:
        print("🧹 Nettoyage...")
        kill_processes_on_port(PORT)

if __name__ == "__main__":
    main()