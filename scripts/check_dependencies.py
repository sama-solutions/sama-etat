#!/usr/bin/env python3
"""
Script de vérification des dépendances SAMA ÉTAT
Auteurs: Mamadou Mbagnick DOGUE, Rassol DOGUE
"""

import sys
import subprocess
import importlib
from pathlib import Path
import json

try:
    import pkg_resources
    HAS_PKG_RESOURCES = True
except ImportError:
    HAS_PKG_RESOURCES = False

# Couleurs pour l'affichage
class Colors:
    RED = '\033[0;31m'
    GREEN = '\033[0;32m'
    YELLOW = '\033[1;33m'
    BLUE = '\033[0;34m'
    PURPLE = '\033[0;35m'
    NC = '\033[0m'  # No Color

def print_banner():
    """Affiche le banner SAMA ÉTAT"""
    print(f"{Colors.BLUE}")
    print(r"""
   ____    _    __  __    _      _____ _____  _  _____ 
  / ___|  / \  |  \/  |  / \    | ____|_   _|/ \|_   _|
  \___ \ / _ \ | |\/| | / _ \   |  _|   | | / _ \ | |  
   ___) / ___ \| |  | |/ ___ \  | |___  | |/ ___ \| |  
  |____/_/   \_\_|  |_/_/   \_\ |_____| |_/_/   \_\_|  
                                                       
  🔍 VÉRIFICATION DES DÉPENDANCES 🔍
    """)
    print(f"{Colors.NC}")
    print(f"{Colors.PURPLE}Auteurs: Mamadou Mbagnick DOGUE, Rassol DOGUE{Colors.NC}")
    print()

def log_success(message):
    """Log de succès"""
    print(f"{Colors.GREEN}✅ {message}{Colors.NC}")

def log_error(message):
    """Log d'erreur"""
    print(f"{Colors.RED}❌ {message}{Colors.NC}")

def log_warning(message):
    """Log d'avertissement"""
    print(f"{Colors.YELLOW}⚠️ {message}{Colors.NC}")

def log_info(message):
    """Log d'information"""
    print(f"{Colors.BLUE}ℹ️ {message}{Colors.NC}")

def check_python_version():
    """Vérifier la version Python"""
    log_info("Vérification de la version Python...")
    
    version = sys.version_info
    if version.major == 3 and version.minor >= 8:
        log_success(f"Python {version.major}.{version.minor}.{version.micro} ✅")
        return True
    else:
        log_error(f"Python {version.major}.{version.minor}.{version.micro} - Minimum requis: Python 3.8")
        return False

def check_package(package_name, version_spec=None):
    """Vérifier qu'un package Python est installé"""
    try:
        if HAS_PKG_RESOURCES and version_spec:
            pkg_resources.require(f"{package_name}{version_spec}")
        else:
            importlib.import_module(package_name)
        
        if HAS_PKG_RESOURCES:
            try:
                version = pkg_resources.get_distribution(package_name).version
                log_success(f"{package_name} {version}")
            except:
                log_success(f"{package_name} (version inconnue)")
        else:
            log_success(f"{package_name} (installé)")
        return True
    except (ImportError, Exception) as e:
        log_error(f"{package_name} - {str(e)}")
        return False

def check_system_command(command):
    """Vérifier qu'une commande système est disponible"""
    try:
        result = subprocess.run([command, '--version'], 
                              capture_output=True, text=True, timeout=10)
        if result.returncode == 0:
            version_line = result.stdout.split('\n')[0]
            log_success(f"{command} - {version_line}")
            return True
        else:
            log_error(f"{command} - Non trouvé")
            return False
    except (subprocess.TimeoutExpired, FileNotFoundError):
        log_error(f"{command} - Non trouvé")
        return False

def check_odoo_dependencies():
    """Vérifier les dépendances Odoo principales"""
    log_info("Vérification des dépendances Odoo...")
    
    odoo_deps = [
        'lxml',
        'psycopg2',
        'babel',
        'decorator',
        'docutils',
        'gevent',
        'jinja2',
        'markupsafe',
        'passlib',
        'pillow',
        'polib',
        'psutil',
        'reportlab',
        'requests',
        'werkzeug'
    ]
    
    success_count = 0
    for dep in odoo_deps:
        if check_package(dep):
            success_count += 1
    
    log_info(f"Dépendances Odoo: {success_count}/{len(odoo_deps)} installées")
    return success_count == len(odoo_deps)

def check_sama_etat_dependencies():
    """Vérifier les dépendances spécifiques à SAMA ÉTAT"""
    log_info("Vérification des dépendances SAMA ÉTAT...")
    
    sama_deps = {
        'qrcode': '>=7.4.0',
        'PIL': None,  # Pillow
        'geopy': '>=2.3.0',
        'folium': '>=0.14.0',
        'requests': '>=2.31.0',
        'dateutil': '>=2.8.0'  # python-dateutil
    }
    
    success_count = 0
    for dep, version in sama_deps.items():
        if dep == 'PIL':
            # Pillow s'importe comme PIL
            if check_package('PIL'):
                success_count += 1
        elif dep == 'dateutil':
            # python-dateutil s'importe comme dateutil
            if check_package('dateutil'):
                success_count += 1
        else:
            if check_package(dep, version):
                success_count += 1
    
    log_info(f"Dépendances SAMA ÉTAT: {success_count}/{len(sama_deps)} installées")
    return success_count == len(sama_deps)

def check_development_dependencies():
    """Vérifier les dépendances de développement"""
    log_info("Vérification des dépendances de développement...")
    
    dev_deps = [
        'pytest',
        'coverage',
        'black',
        'flake8',
        'isort',
        'mypy',
        'bandit',
        'safety'
    ]
    
    success_count = 0
    for dep in dev_deps:
        if check_package(dep):
            success_count += 1
    
    log_info(f"Dépendances de développement: {success_count}/{len(dev_deps)} installées")
    return success_count >= len(dev_deps) // 2  # Au moins 50% pour être OK

def check_system_dependencies():
    """Vérifier les dépendances système"""
    log_info("Vérification des dépendances système...")
    
    system_deps = [
        'git',
        'curl',
        'python3',
        'pip3'
    ]
    
    success_count = 0
    for dep in system_deps:
        if check_system_command(dep):
            success_count += 1
    
    log_info(f"Dépendances système: {success_count}/{len(system_deps)} installées")
    return success_count == len(system_deps)

def check_docker_dependencies():
    """Vérifier Docker et Docker Compose"""
    log_info("Vérification de Docker...")
    
    docker_ok = check_system_command('docker')
    compose_ok = check_system_command('docker-compose') or check_system_command('docker compose')
    
    if docker_ok and compose_ok:
        log_success("Docker et Docker Compose sont disponibles")
        return True
    else:
        log_warning("Docker ou Docker Compose non trouvé (optionnel)")
        return False

def check_postgresql():
    """Vérifier PostgreSQL"""
    log_info("Vérification de PostgreSQL...")
    
    pg_ok = check_system_command('psql') or check_system_command('pg_config')
    
    if pg_ok:
        log_success("PostgreSQL est disponible")
        return True
    else:
        log_warning("PostgreSQL non trouvé (peut être dans Docker)")
        return False

def generate_report():
    """Générer un rapport de vérification"""
    log_info("Génération du rapport de vérification...")
    
    report = {
        "timestamp": subprocess.run(['date'], capture_output=True, text=True).stdout.strip(),
        "python_version": f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}",
        "checks": {
            "python_version": check_python_version(),
            "system_dependencies": check_system_dependencies(),
            "odoo_dependencies": check_odoo_dependencies(),
            "sama_etat_dependencies": check_sama_etat_dependencies(),
            "development_dependencies": check_development_dependencies(),
            "docker": check_docker_dependencies(),
            "postgresql": check_postgresql()
        }
    }
    
    # Sauvegarder le rapport
    report_file = Path("dependency_check_report.json")
    with open(report_file, 'w') as f:
        json.dump(report, f, indent=2)
    
    log_success(f"Rapport sauvegardé dans {report_file}")
    return report

def main():
    """Fonction principale"""
    print_banner()
    
    log_info("Démarrage de la vérification des dépendances SAMA ÉTAT...")
    print()
    
    # Générer le rapport complet
    report = generate_report()
    
    print()
    log_info("📊 RÉSUMÉ DE LA VÉRIFICATION")
    print("=" * 50)
    
    total_checks = len(report["checks"])
    passed_checks = sum(1 for check in report["checks"].values() if check)
    
    for check_name, result in report["checks"].items():
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{check_name.replace('_', ' ').title()}: {status}")
    
    print("=" * 50)
    
    success_rate = (passed_checks / total_checks) * 100
    
    if success_rate >= 80:
        log_success(f"🎉 VÉRIFICATION RÉUSSIE: {passed_checks}/{total_checks} ({success_rate:.1f}%)")
        log_success("SAMA ÉTAT est prêt pour le déploiement!")
    elif success_rate >= 60:
        log_warning(f"⚠️ VÉRIFICATION PARTIELLE: {passed_checks}/{total_checks} ({success_rate:.1f}%)")
        log_warning("Certaines dépendances manquent mais le projet peut fonctionner")
    else:
        log_error(f"❌ VÉRIFICATION ÉCHOUÉE: {passed_checks}/{total_checks} ({success_rate:.1f}%)")
        log_error("Des dépendances critiques manquent")
    
    print()
    log_info("💡 RECOMMANDATIONS:")
    
    if not report["checks"]["sama_etat_dependencies"]:
        print("   - Installer les dépendances SAMA ÉTAT: pip3 install -r requirements.txt")
    
    if not report["checks"]["development_dependencies"]:
        print("   - Installer les dépendances de développement: pip3 install -e '.[dev]'")
    
    if not report["checks"]["docker"]:
        print("   - Installer Docker pour un déploiement simplifié")
    
    if not report["checks"]["postgresql"]:
        print("   - Installer PostgreSQL ou utiliser Docker")
    
    print()
    log_info("🚀 Pour installer toutes les dépendances:")
    print("   make install-dev  # Ou")
    print("   docker-compose up -d")
    
    print()
    log_success("🇸🇳 SAMA ÉTAT - Fait avec ❤️ au Sénégal")
    
    return 0 if success_rate >= 80 else 1

if __name__ == "__main__":
    sys.exit(main())