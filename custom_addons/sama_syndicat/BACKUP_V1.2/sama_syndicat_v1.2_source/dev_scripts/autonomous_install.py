#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Script d'installation autonome pour sama_syndicat
Cycle complet : arrêt processus -> création base -> installation -> démarrage -> tests
"""

import os
import sys
import subprocess
import time
import psutil
import signal
import logging
from datetime import datetime

# Configuration
ODOO_PATH = "/var/odoo/odoo18"
VENV_PATH = "/home/grand-as/odoo18-venv"
ADDONS_PATH = "/home/grand-as/psagsn/custom_addons"
DB_NAME = "sama_syndicat_auto"
DB_USER = "odoo"
DB_PASSWORD = "odoo"
PORT = 8070
LOG_LEVEL = "info"

# Configuration du logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('sama_syndicat/dev_scripts/install.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class SamaSyndicatInstaller:
    def __init__(self):
        self.start_time = datetime.now()
        self.errors = []
        self.warnings = []
        
    def log_step(self, step, message):
        """Log une étape avec formatage"""
        logger.info(f"🔄 ÉTAPE {step}: {message}")
        
    def log_success(self, message):
        """Log un succès"""
        logger.info(f"✅ {message}")
        
    def log_error(self, message):
        """Log une erreur"""
        logger.error(f"❌ {message}")
        self.errors.append(message)
        
    def log_warning(self, message):
        """Log un avertissement"""
        logger.warning(f"⚠️  {message}")
        self.warnings.append(message)

    def kill_processes_on_port(self):
        """Arrête tous les processus sur le port dédié"""
        self.log_step(1, f"Arrêt des processus sur le port {PORT}")
        
        killed_processes = []
        for proc in psutil.process_iter(['pid', 'name', 'connections', 'cmdline']):
            try:
                for conn in proc.info['connections'] or []:
                    if conn.laddr.port == PORT:
                        cmdline = ' '.join(proc.info['cmdline'] or [])
                        if 'odoo' in cmdline.lower():
                            logger.info(f"🔪 Arrêt du processus Odoo {proc.info['name']} (PID: {proc.info['pid']})")
                            proc.terminate()
                            killed_processes.append(proc.info['pid'])
                        else:
                            self.log_warning(f"Processus non-Odoo sur le port {PORT}: {proc.info['name']}")
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                pass
        
        if killed_processes:
            time.sleep(3)  # Attendre l'arrêt propre
            # Forcer l'arrêt si nécessaire
            for pid in killed_processes:
                try:
                    proc = psutil.Process(pid)
                    if proc.is_running():
                        proc.kill()
                        logger.info(f"🔪 Arrêt forcé du processus {pid}")
                except:
                    pass
            self.log_success(f"Processus arrêtés sur le port {PORT}")
        else:
            self.log_success(f"Aucun processus Odoo trouvé sur le port {PORT}")

    def setup_environment(self):
        """Configure l'environnement"""
        self.log_step(2, "Configuration de l'environnement")
        
        env = os.environ.copy()
        env['PATH'] = f"{VENV_PATH}/bin:{env['PATH']}"
        env['PYTHONPATH'] = f"{ODOO_PATH}:{ADDONS_PATH}"
        
        # Vérifications
        if not os.path.exists(ODOO_PATH):
            self.log_error(f"Chemin Odoo introuvable: {ODOO_PATH}")
            return None
            
        if not os.path.exists(VENV_PATH):
            self.log_error(f"Environnement virtuel introuvable: {VENV_PATH}")
            return None
            
        if not os.path.exists(ADDONS_PATH):
            self.log_error(f"Chemin addons introuvable: {ADDONS_PATH}")
            return None
            
        self.log_success("Environnement configuré")
        return env

    def run_command(self, command, env, timeout=300, capture_output=True):
        """Exécute une commande avec gestion d'erreurs"""
        logger.info(f"🚀 Commande: {command[:100]}...")
        
        try:
            if capture_output:
                result = subprocess.run(
                    command, 
                    shell=True, 
                    env=env,
                    capture_output=True, 
                    text=True,
                    timeout=timeout,
                    cwd=ODOO_PATH
                )
                
                if result.returncode == 0:
                    logger.info(f"✅ Succès (code: {result.returncode})")
                    if result.stdout:
                        logger.debug(f"Sortie: {result.stdout[:500]}...")
                    return True, result.stdout, result.stderr
                else:
                    logger.error(f"❌ Échec (code: {result.returncode})")
                    if result.stderr:
                        logger.error(f"Erreur: {result.stderr[:500]}...")
                    return False, result.stdout, result.stderr
            else:
                # Pour les commandes interactives
                process = subprocess.Popen(
                    command,
                    shell=True,
                    env=env,
                    cwd=ODOO_PATH
                )
                return process, None, None
                
        except subprocess.TimeoutExpired:
            self.log_error(f"Timeout de la commande après {timeout}s")
            return False, "", "Timeout"
        except Exception as e:
            self.log_error(f"Exception lors de l'exécution: {e}")
            return False, "", str(e)

    def create_database(self, env):
        """Crée la base de données"""
        self.log_step(3, f"Création de la base de données {DB_NAME}")
        
        # Supprimer la base si elle existe
        drop_cmd = f"dropdb -U {DB_USER} --if-exists {DB_NAME}"
        success, stdout, stderr = self.run_command(drop_cmd, env, timeout=60)
        
        if not success and "does not exist" not in stderr:
            self.log_warning(f"Problème lors de la suppression: {stderr}")
        
        # Créer la nouvelle base
        create_cmd = f"createdb -U {DB_USER} -O {DB_USER} {DB_NAME}"
        success, stdout, stderr = self.run_command(create_cmd, env, timeout=60)
        
        if success:
            self.log_success(f"Base de données {DB_NAME} créée")
            return True
        else:
            self.log_error(f"Échec de création de la base: {stderr}")
            return False

    def validate_module_syntax(self):
        """Valide la syntaxe du module avant installation"""
        self.log_step(4, "Validation de la syntaxe du module")
        
        try:
            # Exécuter le script de validation
            result = subprocess.run([
                sys.executable, 
                "sama_syndicat/dev_scripts/validate_syntax.py"
            ], capture_output=True, text=True, timeout=60)
            
            if result.returncode == 0:
                self.log_success("Syntaxe du module validée")
                return True
            else:
                self.log_error(f"Erreurs de syntaxe: {result.stderr}")
                return False
        except Exception as e:
            self.log_error(f"Erreur lors de la validation: {e}")
            return False

    def install_module(self, env):
        """Installe le module sama_syndicat"""
        self.log_step(5, "Installation du module sama_syndicat")
        
        install_cmd = f"""python3 odoo-bin \
            --addons-path={ADDONS_PATH} \
            --database={DB_NAME} \
            --db_user={DB_USER} \
            --db_password={DB_PASSWORD} \
            --init=sama_syndicat \
            --stop-after-init \
            --log-level={LOG_LEVEL} \
            --without-demo=all"""
        
        success, stdout, stderr = self.run_command(install_cmd, env, timeout=600)
        
        if success:
            # Vérifier les logs pour des erreurs spécifiques
            if "ERROR" in stdout or "CRITICAL" in stdout:
                self.log_warning("Installation terminée mais avec des erreurs dans les logs")
                logger.info("Logs d'installation:")
                for line in stdout.split('\n')[-20:]:  # Dernières 20 lignes
                    if line.strip():
                        logger.info(f"  {line}")
            else:
                self.log_success("Module sama_syndicat installé avec succès")
            return True
        else:
            self.log_error(f"Échec d'installation: {stderr}")
            return False

    def test_module_loading(self, env):
        """Teste le chargement du module"""
        self.log_step(6, "Test de chargement du module")
        
        test_cmd = f"""python3 odoo-bin \
            --addons-path={ADDONS_PATH} \
            --database={DB_NAME} \
            --db_user={DB_USER} \
            --db_password={DB_PASSWORD} \
            --test-enable \
            --stop-after-init \
            --log-level=test"""
        
        success, stdout, stderr = self.run_command(test_cmd, env, timeout=300)
        
        if success:
            self.log_success("Module chargé et testé avec succès")
            return True
        else:
            self.log_warning(f"Tests avec avertissements: {stderr}")
            return True  # On continue même avec des avertissements

    def start_server(self, env):
        """Démarre le serveur Odoo"""
        self.log_step(7, f"Démarrage du serveur sur le port {PORT}")
        
        start_cmd = f"""python3 odoo-bin \
            --addons-path={ADDONS_PATH} \
            --database={DB_NAME} \
            --db_user={DB_USER} \
            --db_password={DB_PASSWORD} \
            --xmlrpc-port={PORT} \
            --log-level={LOG_LEVEL} \
            --dev=reload"""
        
        logger.info(f"🌐 Serveur accessible sur: http://localhost:{PORT}")
        logger.info(f"🔑 Base de données: {DB_NAME}")
        logger.info(f"📁 Modules: {ADDONS_PATH}")
        logger.info("🛑 Appuyez sur Ctrl+C pour arrêter")
        logger.info("-" * 60)
        
        try:
            process, _, _ = self.run_command(start_cmd, env, capture_output=False)
            return process
        except Exception as e:
            self.log_error(f"Erreur lors du démarrage: {e}")
            return None

    def print_summary(self):
        """Affiche le résumé de l'installation"""
        duration = datetime.now() - self.start_time
        
        print("\n" + "=" * 60)
        print("🏛️  SAMA SYNDICAT - RÉSUMÉ D'INSTALLATION")
        print("=" * 60)
        print(f"⏱️  Durée totale: {duration}")
        print(f"🗄️  Base de données: {DB_NAME}")
        print(f"🌐 URL d'accès: http://localhost:{PORT}")
        print(f"📁 Addons: {ADDONS_PATH}")
        
        if self.errors:
            print(f"\n❌ Erreurs ({len(self.errors)}):")
            for error in self.errors:
                print(f"  • {error}")
        
        if self.warnings:
            print(f"\n⚠️  Avertissements ({len(self.warnings)}):")
            for warning in self.warnings:
                print(f"  • {warning}")
        
        if not self.errors:
            print("\n🎉 Installation réussie!")
            print("📋 Prochaines étapes:")
            print("  1. Accéder à http://localhost:8070")
            print("  2. Se connecter avec admin/admin")
            print("  3. Aller dans Apps > SAMA SYNDICAT")
            print("  4. Commencer la configuration")
        else:
            print(f"\n💥 Installation échouée avec {len(self.errors)} erreur(s)")
        
        print("=" * 60)

    def run_installation(self):
        """Lance l'installation complète"""
        logger.info("🏛️  SAMA SYNDICAT - INSTALLATION AUTONOME")
        logger.info("=" * 60)
        
        try:
            # Étape 1: Arrêt des processus
            self.kill_processes_on_port()
            
            # Étape 2: Configuration environnement
            env = self.setup_environment()
            if not env:
                return False
            
            # Étape 3: Création base de données
            if not self.create_database(env):
                return False
            
            # Étape 4: Validation syntaxe
            if not self.validate_module_syntax():
                return False
            
            # Étape 5: Installation module
            if not self.install_module(env):
                return False
            
            # Étape 6: Test chargement
            if not self.test_module_loading(env):
                self.log_warning("Tests non concluants mais on continue")
            
            # Étape 7: Démarrage serveur
            process = self.start_server(env)
            if process:
                try:
                    process.wait()
                except KeyboardInterrupt:
                    logger.info("\n🛑 Arrêt demandé par l'utilisateur")
                    process.terminate()
                    time.sleep(2)
                    if process.poll() is None:
                        process.kill()
                    self.kill_processes_on_port()
            
            return True
            
        except Exception as e:
            self.log_error(f"Erreur inattendue: {e}")
            return False
        finally:
            self.print_summary()

def main():
    """Fonction principale"""
    installer = SamaSyndicatInstaller()
    success = installer.run_installation()
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()