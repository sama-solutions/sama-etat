#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Script de test itératif pour sama_syndicat
Cycle: démarrage -> test -> revue logs -> correction -> redémarrage
"""

import os
import sys
import subprocess
import time
import psutil
import logging
from datetime import datetime

# Configuration
ODOO_PATH = "/var/odoo/odoo18"
VENV_PATH = "/home/grand-as/odoo18-venv"
ADDONS_PATH = "/home/grand-as/psagsn/custom_addons"
DB_NAME = "sama_syndicat_iter"
DB_USER = "odoo"
DB_PASSWORD = "odoo"
PORT = 8070
LOG_FILE = "sama_syndicat/dev_scripts/iterative.log"

# Configuration du logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(LOG_FILE),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class IterativeTester:
    def __init__(self):
        self.iteration = 0
        self.max_iterations = 10
        self.errors_found = []
        self.fixes_applied = []
        
    def kill_port_processes(self):
        """Arrête les processus sur le port"""
        logger.info(f"🔍 Arrêt des processus sur le port {PORT}")
        killed = False
        
        for proc in psutil.process_iter(['pid', 'name', 'connections']):
            try:
                for conn in proc.info['connections'] or []:
                    if conn.laddr.port == PORT:
                        logger.info(f"🔪 Arrêt du processus {proc.info['name']} (PID: {proc.info['pid']})")
                        proc.kill()
                        killed = True
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                pass
        
        if killed:
            time.sleep(2)
            logger.info("✅ Processus arrêtés")

    def setup_environment(self):
        """Configure l'environnement"""
        env = os.environ.copy()
        env['PATH'] = f"{VENV_PATH}/bin:{env['PATH']}"
        env['PYTHONPATH'] = f"{ODOO_PATH}:{ADDONS_PATH}"
        return env

    def run_syntax_validation(self):
        """Valide la syntaxe"""
        logger.info("🔍 Validation syntaxique...")
        
        try:
            result = subprocess.run([
                sys.executable, 
                "sama_syndicat/dev_scripts/validate_syntax.py"
            ], capture_output=True, text=True, timeout=60)
            
            if result.returncode == 0:
                logger.info("✅ Syntaxe validée")
                return True, []
            else:
                errors = result.stderr.split('\n')
                logger.error("❌ Erreurs de syntaxe trouvées")
                return False, errors
        except Exception as e:
            logger.error(f"❌ Erreur lors de la validation: {e}")
            return False, [str(e)]

    def attempt_installation(self, env):
        """Tente l'installation du module"""
        logger.info(f"📦 Tentative d'installation (itération {self.iteration})")
        
        # Recréer la base
        subprocess.run(f"dropdb -U {DB_USER} --if-exists {DB_NAME}", shell=True, env=env)
        subprocess.run(f"createdb -U {DB_USER} -O {DB_USER} {DB_NAME}", shell=True, env=env)
        
        install_cmd = f"""cd {ODOO_PATH} && python3 odoo-bin \
            --addons-path={ADDONS_PATH} \
            --database={DB_NAME} \
            --db_user={DB_USER} \
            --db_password={DB_PASSWORD} \
            --init=sama_syndicat \
            --stop-after-init \
            --log-level=info \
            --without-demo=all"""
        
        try:
            result = subprocess.run(
                install_cmd, 
                shell=True, 
                env=env,
                capture_output=True, 
                text=True,
                timeout=300
            )
            
            return result.returncode == 0, result.stdout, result.stderr
            
        except subprocess.TimeoutExpired:
            logger.error("⏰ Timeout lors de l'installation")
            return False, "", "Timeout"
        except Exception as e:
            logger.error(f"💥 Exception: {e}")
            return False, "", str(e)

    def analyze_logs(self, stdout, stderr):
        """Analyse les logs pour identifier les erreurs"""
        errors = []
        
        # Analyser stderr
        for line in stderr.split('\n'):
            if any(keyword in line.upper() for keyword in ['ERROR', 'CRITICAL', 'FAILED', 'EXCEPTION']):
                errors.append(line.strip())
        
        # Analyser stdout pour les erreurs Odoo
        for line in stdout.split('\n'):
            if any(keyword in line.upper() for keyword in ['ERROR', 'CRITICAL', 'FAILED']):
                errors.append(line.strip())
        
        return errors

    def suggest_fixes(self, errors):
        """Suggère des corrections basées sur les erreurs"""
        fixes = []
        
        for error in errors:
            error_lower = error.lower()
            
            if 'module not found' in error_lower or 'importerror' in error_lower:
                fixes.append("Vérifier les imports et dépendances dans __manifest__.py")
            
            elif 'syntax error' in error_lower or 'invalid syntax' in error_lower:
                fixes.append("Corriger les erreurs de syntaxe Python")
            
            elif 'xml' in error_lower and 'parse' in error_lower:
                fixes.append("Corriger les erreurs de syntaxe XML dans les vues")
            
            elif 'field' in error_lower and 'exist' in error_lower:
                fixes.append("Vérifier la définition des champs dans les modèles")
            
            elif 'access' in error_lower or 'permission' in error_lower:
                fixes.append("Vérifier les droits d'accès dans security/")
            
            elif 'sequence' in error_lower:
                fixes.append("Vérifier les séquences dans data/sequences.xml")
            
            elif 'view' in error_lower:
                fixes.append("Vérifier les définitions de vues XML")
            
            else:
                fixes.append(f"Analyser manuellement: {error[:100]}...")
        
        return list(set(fixes))  # Supprimer les doublons

    def apply_common_fixes(self):
        """Applique des corrections communes"""
        logger.info("🔧 Application de corrections communes...")
        
        fixes_applied = []
        
        # Vérifier que tous les fichiers __init__.py existent
        init_files = [
            "sama_syndicat/__init__.py",
            "sama_syndicat/models/__init__.py",
            "sama_syndicat/controllers/__init__.py"
        ]
        
        for init_file in init_files:
            if not os.path.exists(init_file):
                logger.warning(f"Fichier manquant: {init_file}")
                # Créer un fichier __init__.py minimal
                with open(init_file, 'w') as f:
                    f.write("# -*- coding: utf-8 -*-\n")
                fixes_applied.append(f"Créé {init_file}")
        
        return fixes_applied

    def run_iteration(self):
        """Lance une itération de test"""
        self.iteration += 1
        logger.info(f"\n🔄 ITÉRATION {self.iteration}/{self.max_iterations}")
        logger.info("=" * 50)
        
        # Arrêter les processus
        self.kill_port_processes()
        
        # Configurer l'environnement
        env = self.setup_environment()
        
        # Validation syntaxique
        syntax_ok, syntax_errors = self.run_syntax_validation()
        if not syntax_ok:
            logger.error("❌ Erreurs de syntaxe détectées")
            self.errors_found.extend(syntax_errors)
            return False
        
        # Tentative d'installation
        success, stdout, stderr = self.attempt_installation(env)
        
        if success:
            logger.info("✅ Installation réussie!")
            return True
        else:
            # Analyser les erreurs
            errors = self.analyze_logs(stdout, stderr)
            self.errors_found.extend(errors)
            
            logger.error(f"❌ Installation échouée avec {len(errors)} erreur(s)")
            for error in errors[:5]:  # Afficher les 5 premières erreurs
                logger.error(f"  • {error}")
            
            # Suggérer des corrections
            fixes = self.suggest_fixes(errors)
            logger.info("🔧 Corrections suggérées:")
            for fix in fixes:
                logger.info(f"  • {fix}")
            
            # Appliquer des corrections automatiques
            auto_fixes = self.apply_common_fixes()
            self.fixes_applied.extend(auto_fixes)
            
            return False

    def run_test_cycle(self):
        """Lance le cycle de test complet"""
        logger.info("🏛️  SAMA SYNDICAT - CYCLE DE TEST ITÉRATIF")
        logger.info("=" * 60)
        
        while self.iteration < self.max_iterations:
            if self.run_iteration():
                logger.info("🎉 Tests réussis!")
                self.print_summary()
                return True
            
            if self.iteration < self.max_iterations:
                logger.info(f"⏳ Pause avant la prochaine itération...")
                time.sleep(2)
        
        logger.error(f"💥 Échec après {self.max_iterations} itérations")
        self.print_summary()
        return False

    def print_summary(self):
        """Affiche le résumé des tests"""
        print("\n" + "=" * 60)
        print("📊 RÉSUMÉ DU CYCLE DE TESTS")
        print("=" * 60)
        print(f"🔄 Itérations: {self.iteration}/{self.max_iterations}")
        print(f"❌ Erreurs trouvées: {len(self.errors_found)}")
        print(f"🔧 Corrections appliquées: {len(self.fixes_applied)}")
        
        if self.errors_found:
            print("\n❌ Erreurs principales:")
            for error in list(set(self.errors_found))[:10]:
                print(f"  • {error}")
        
        if self.fixes_applied:
            print("\n🔧 Corrections appliquées:")
            for fix in self.fixes_applied:
                print(f"  • {fix}")
        
        print(f"\n📝 Log détaillé: {LOG_FILE}")
        print("=" * 60)

def main():
    """Fonction principale"""
    tester = IterativeTester()
    success = tester.run_test_cycle()
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()