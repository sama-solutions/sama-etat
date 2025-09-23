#!/usr/bin/env python3
"""
Script de démarrage simple pour SAMA SYNDICAT
Arrête le processus sur le port 8070 et démarre le module
"""

import os
import sys
import time
import subprocess
import signal
import psutil
from pathlib import Path

# Configuration
PORT = 8070
DATABASE = "sama_syndicat_final_1756812346"
ODOO_BIN = "/var/odoo/odoo18/odoo-bin"
ADDONS_PATH = "/var/odoo/odoo18/odoo/addons,/var/odoo/odoo18/addons,/tmp/addons_sama_syndicat"

def print_banner():
    """Afficher la bannière de démarrage"""
    print("=" * 60)
    print("🚀 SAMA SYNDICAT - DÉMARRAGE AUTOMATIQUE")
    print("=" * 60)
    print(f"📊 Module: SAMA SYNDICAT")
    print(f"🌐 Port: {PORT}")
    print(f"💾 Base de données: {DATABASE}")
    print("=" * 60)

def find_process_by_port(port):
    """Trouver le processus utilisant un port spécifique"""
    try:
        for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
            try:
                connections = proc.connections()
                for conn in connections:
                    if conn.laddr.port == port:
                        return proc
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                continue
    except Exception as e:
        print(f"⚠️ Erreur lors de la recherche du processus: {e}")
    return None

def stop_process_on_port(port):
    """Arrêter le processus utilisant le port spécifié"""
    print(f"🔍 Recherche du processus sur le port {port}...")
    
    # Méthode 1: Recherche par psutil
    proc = find_process_by_port(port)
    if proc:
        try:
            print(f"📋 Processus trouvé: PID {proc.pid} - {proc.name()}")
            print(f"🛑 Arrêt du processus {proc.pid}...")
            proc.terminate()
            
            # Attendre que le processus se termine
            try:
                proc.wait(timeout=10)
                print(f"✅ Processus {proc.pid} arrêté avec succès")
                return True
            except psutil.TimeoutExpired:
                print(f"⚠️ Timeout - Force l'arrêt du processus {proc.pid}")
                proc.kill()
                proc.wait()
                print(f"✅ Processus {proc.pid} forcé à s'arrêter")
                return True
                
        except Exception as e:
            print(f"❌ Erreur lors de l'arrêt du processus: {e}")
    
    # Méthode 2: Utiliser lsof et kill
    try:
        print(f"🔍 Recherche alternative avec lsof...")
        result = subprocess.run(['lsof', '-ti', f':{port}'], 
                              capture_output=True, text=True, timeout=5)
        
        if result.returncode == 0 and result.stdout.strip():
            pids = result.stdout.strip().split('\n')
            for pid in pids:
                if pid:
                    print(f"🛑 Arrêt du processus PID {pid}...")
                    try:
                        os.kill(int(pid), signal.SIGTERM)
                        time.sleep(2)
                        # Vérifier si le processus est encore actif
                        try:
                            os.kill(int(pid), 0)  # Test si le processus existe
                            print(f"⚠️ Force l'arrêt du processus {pid}")
                            os.kill(int(pid), signal.SIGKILL)
                        except OSError:
                            pass  # Le processus est déjà arrêté
                        print(f"✅ Processus {pid} arrêté")
                    except Exception as e:
                        print(f"❌ Erreur lors de l'arrêt du PID {pid}: {e}")
            return True
        else:
            print(f"ℹ️ Aucun processus trouvé sur le port {port}")
            return True
            
    except subprocess.TimeoutExpired:
        print("⚠️ Timeout lors de la recherche avec lsof")
    except FileNotFoundError:
        print("⚠️ lsof non disponible, utilisation de netstat...")
        
        # Méthode 3: Utiliser netstat
        try:
            result = subprocess.run(['netstat', '-tlnp'], 
                                  capture_output=True, text=True, timeout=5)
            
            if result.returncode == 0:
                lines = result.stdout.split('\n')
                for line in lines:
                    if f':{port} ' in line and 'LISTEN' in line:
                        parts = line.split()
                        if len(parts) > 6 and '/' in parts[6]:
                            pid = parts[6].split('/')[0]
                            if pid.isdigit():
                                print(f"🛑 Arrêt du processus PID {pid}...")
                                try:
                                    os.kill(int(pid), signal.SIGTERM)
                                    time.sleep(2)
                                    print(f"✅ Processus {pid} arrêté")
                                    return True
                                except Exception as e:
                                    print(f"❌ Erreur lors de l'arrêt du PID {pid}: {e}")
        except Exception as e:
            print(f"⚠️ Erreur avec netstat: {e}")
    
    print(f"ℹ️ Aucun processus actif trouvé sur le port {port}")
    return True

def check_odoo_bin():
    """Vérifier que odoo-bin existe"""
    if not os.path.exists(ODOO_BIN):
        print(f"❌ Odoo non trouvé à: {ODOO_BIN}")
        
        # Rechercher odoo-bin dans des emplacements communs
        common_paths = [
            "/usr/bin/odoo",
            "/usr/local/bin/odoo",
            "/opt/odoo/odoo-bin",
            "/home/odoo/odoo/odoo-bin",
            "odoo-bin"  # Dans le PATH
        ]
        
        print("🔍 Recherche d'Odoo dans les emplacements communs...")
        for path in common_paths:
            if os.path.exists(path) or subprocess.run(['which', path], 
                                                    capture_output=True).returncode == 0:
                print(f"✅ Odoo trouvé à: {path}")
                return path
        
        print("❌ Odoo non trouvé. Veuillez installer Odoo ou ajuster le chemin.")
        return None
    
    return ODOO_BIN

def start_odoo():
    """Démarrer Odoo avec SAMA SYNDICAT"""
    odoo_path = check_odoo_bin()
    if not odoo_path:
        return False
    
    print("🚀 Démarrage d'Odoo avec SAMA SYNDICAT...")
    
    # Commande de démarrage
    cmd = [
        "python3", odoo_path,
        f"--addons-path={ADDONS_PATH}",
        f"--database={DATABASE}",
        f"--xmlrpc-port={PORT}",
        "--dev=reload,xml",
        "--log-level=info",
        "--workers=0",  # Mode développement
        "--max-cron-threads=0"  # Désactiver les crons en dev
    ]
    
    print("📋 Commande de démarrage:")
    print(" ".join(cmd))
    print()
    
    try:
        print("⏳ Démarrage en cours...")
        print(f"🌐 L'interface sera disponible sur: http://localhost:{PORT}")
        print(f"📊 Dashboard SAMA SYNDICAT: http://localhost:{PORT}/web")
        print()
        print("💡 Pour arrêter le serveur, utilisez Ctrl+C")
        print("=" * 60)
        
        # Démarrer Odoo
        process = subprocess.Popen(cmd)
        
        # Attendre quelques secondes puis vérifier si le processus est toujours actif
        time.sleep(3)
        if process.poll() is None:
            print("✅ Odoo démarré avec succès!")
            print(f"🔗 Accès direct: http://localhost:{PORT}/web/login?db={DATABASE}")
            
            # Attendre que le processus se termine
            try:
                process.wait()
            except KeyboardInterrupt:
                print("\n🛑 Arrêt demandé par l'utilisateur...")
                process.terminate()
                try:
                    process.wait(timeout=10)
                    print("✅ Odoo arrêté proprement")
                except subprocess.TimeoutExpired:
                    print("⚠️ Force l'arrêt d'Odoo...")
                    process.kill()
                    process.wait()
                    print("✅ Odoo arrêté")
        else:
            print("❌ Erreur lors du démarrage d'Odoo")
            return False
            
    except FileNotFoundError:
        print(f"❌ Python3 ou Odoo non trouvé")
        return False
    except Exception as e:
        print(f"❌ Erreur lors du démarrage: {e}")
        return False
    
    return True

def check_port_available(port):
    """Vérifier si le port est disponible"""
    import socket
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind(('localhost', port))
            return True
    except OSError:
        return False

def main():
    """Fonction principale"""
    print_banner()
    
    try:
        # Étape 1: Arrêter le processus sur le port
        if not stop_process_on_port(PORT):
            print("❌ Impossible d'arrêter le processus sur le port")
            return False
        
        # Attendre un peu que le port se libère
        print("⏳ Attente de la libération du port...")
        time.sleep(3)
        
        # Vérifier que le port est libre
        if not check_port_available(PORT):
            print(f"⚠️ Le port {PORT} semble encore occupé, tentative de démarrage quand même...")
        else:
            print(f"✅ Port {PORT} disponible")
        
        # Étape 2: Démarrer Odoo
        if start_odoo():
            print("🎊 SAMA SYNDICAT démarré avec succès!")
            return True
        else:
            print("❌ Échec du démarrage de SAMA SYNDICAT")
            return False
            
    except KeyboardInterrupt:
        print("\n🛑 Arrêt demandé par l'utilisateur")
        return False
    except Exception as e:
        print(f"❌ Erreur inattendue: {e}")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)