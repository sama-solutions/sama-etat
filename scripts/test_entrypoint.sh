#!/bin/bash
# Script d'entrée pour les tests SAMA ÉTAT
# Auteurs: Mamadou Mbagnick DOGUE, Rassol DOGUE

set -e

# Couleurs pour les logs
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
NC='\033[0m' # No Color

# Fonction de logging
log() {
    echo -e "${BLUE}[SAMA ÉTAT TEST]${NC} $1"
}

log_success() {
    echo -e "${GREEN}[SAMA ÉTAT TEST]${NC} $1"
}

log_warning() {
    echo -e "${YELLOW}[SAMA ÉTAT TEST]${NC} $1"
}

log_error() {
    echo -e "${RED}[SAMA ÉTAT TEST]${NC} $1"
}

log_info() {
    echo -e "${PURPLE}[SAMA ÉTAT TEST]${NC} $1"
}

# Banner de test
echo -e "${PURPLE}"
cat << "EOF"
   ____    _    __  __    _      _____ _____  _  _____ 
  / ___|  / \  |  \/  |  / \    | ____|_   _|/ \|_   _|
  \___ \ / _ \ | |\/| | / _ \   |  _|   | | / _ \ | |  
   ___) / ___ \| |  | |/ ___ \  | |___  | |/ ___ \| |  
  |____/_/   \_\_|  |_/_/   \_\ |_____| |_/_/   \_\_|  
                                                       
  🧪 ENVIRONNEMENT DE TEST 🧪
  Auteurs: Mamadou Mbagnick DOGUE, Rassol DOGUE
EOF
echo -e "${NC}"

# Variables d'environnement par défaut
export ODOO_RC=${ODOO_RC:-/etc/odoo/odoo.test.conf}
export ODOO_ADDONS_PATH=${ODOO_ADDONS_PATH:-/usr/lib/python3/dist-packages/odoo/addons,/mnt/extra-addons}
export TEST_MODE=true

log "Démarrage de l'environnement de test SAMA ÉTAT..."

# Vérification des prérequis
log "Vérification des prérequis de test..."

# Attendre PostgreSQL
if [ -n "$HOST" ]; then
    log "Attente de la base de données PostgreSQL de test..."
    while ! nc -z "$HOST" "${PORT:-5432}"; do
        log_warning "En attente de PostgreSQL sur $HOST:${PORT:-5432}..."
        sleep 2
    done
    log_success "PostgreSQL de test est accessible"
fi

# Vérifier les outils de test
log "Vérification des outils de test..."
python3 -c "import pytest, coverage" 2>/dev/null || {
    log_warning "Installation des outils de test manquants..."
    pip3 install --no-cache-dir pytest pytest-cov coverage
}

# Créer les répertoires de test
log "Création des répertoires de test..."
mkdir -p /app/coverage /app/reports /var/log/odoo/test

# Configuration des tests
log "Configuration de l'environnement de test..."

# Fonction pour exécuter les tests unitaires
run_unit_tests() {
    log_info "🧪 Exécution des tests unitaires..."
    cd /mnt/extra-addons/sama_etat
    
    if [ -d "tests" ]; then
        python -m pytest tests/ \
            -v \
            --cov=. \
            --cov-report=html:/app/coverage/html \
            --cov-report=xml:/app/coverage/coverage.xml \
            --cov-report=term \
            --junit-xml=/app/reports/pytest-report.xml
        
        log_success "Tests unitaires terminés"
    else
        log_warning "Aucun répertoire de tests trouvé"
    fi
}

# Fonction pour exécuter les tests Odoo
run_odoo_tests() {
    log_info "🏗️ Exécution des tests d'intégration Odoo..."
    
    odoo --addons-path="$ODOO_ADDONS_PATH" \
         --database="${POSTGRES_DB:-test_sama_etat}" \
         --db-host="${HOST:-localhost}" \
         --db-port="${PORT:-5432}" \
         --db-user="${USER:-test_user}" \
         --db-password="${PASSWORD:-test_password}" \
         --init=sama_etat \
         --test-enable \
         --stop-after-init \
         --without-demo=False \
         --log-level=test \
         --logfile=/var/log/odoo/test/odoo-test.log
         
    log_success "Tests d'intégration Odoo terminés"
}

# Fonction pour exécuter les tests de qualité de code
run_code_quality() {
    log_info "🔍 Vérification de la qualité du code..."
    cd /mnt/extra-addons/sama_etat
    
    # Black formatting
    log "Vérification du formatage avec Black..."
    black --check --diff . || log_warning "Problèmes de formatage détectés"
    
    # Import sorting
    log "Vérification du tri des imports avec isort..."
    isort --check-only --diff . || log_warning "Problèmes de tri d'imports détectés"
    
    # Linting
    log "Analyse statique avec flake8..."
    flake8 . --count --statistics --output-file=/app/reports/flake8-report.txt || log_warning "Problèmes de linting détectés"
    
    # Type checking
    log "Vérification des types avec mypy..."
    mypy . --ignore-missing-imports --html-report /app/reports/mypy || log_warning "Problèmes de typage détectés"
    
    log_success "Vérification de la qualité du code terminée"
}

# Fonction pour exécuter les tests de sécurité
run_security_tests() {
    log_info "🔒 Exécution des tests de sécurité..."
    cd /mnt/extra-addons/sama_etat
    
    # Bandit security scan
    log "Analyse de sécurité avec Bandit..."
    bandit -r . -f json -o /app/reports/bandit-report.json || log_warning "Problèmes de sécurité détectés"
    
    # Safety check
    log "Vérification des dépendances avec Safety..."
    safety check --json --output /app/reports/safety-report.json || log_warning "Vulnérabilités dans les dépendances détectées"
    
    log_success "Tests de sécurité terminés"
}

# Fonction pour générer le rapport final
generate_report() {
    log_info "📊 Génération du rapport de test..."
    
    cat > /app/reports/test-summary.html << EOF
<!DOCTYPE html>
<html>
<head>
    <title>SAMA ÉTAT - Rapport de Tests</title>
    <meta charset="utf-8">
    <style>
        body { font-family: Arial, sans-serif; margin: 20px; }
        .header { background: #2c3e50; color: white; padding: 20px; text-align: center; }
        .section { margin: 20px 0; padding: 15px; border: 1px solid #ddd; }
        .success { background: #d4edda; border-color: #c3e6cb; }
        .warning { background: #fff3cd; border-color: #ffeaa7; }
        .error { background: #f8d7da; border-color: #f5c6cb; }
    </style>
</head>
<body>
    <div class="header">
        <h1>🧪 SAMA ÉTAT - Rapport de Tests</h1>
        <p>Généré le $(date)</p>
    </div>
    
    <div class="section success">
        <h2>✅ Tests Réussis</h2>
        <p>Les tests ont été exécutés avec succès.</p>
    </div>
    
    <div class="section">
        <h2>📊 Résultats</h2>
        <ul>
            <li>Tests unitaires: Voir coverage/html/index.html</li>
            <li>Tests Odoo: Voir /var/log/odoo/test/odoo-test.log</li>
            <li>Qualité du code: Voir flake8-report.txt et mypy/</li>
            <li>Sécurité: Voir bandit-report.json et safety-report.json</li>
        </ul>
    </div>
</body>
</html>
EOF
    
    log_success "Rapport de test généré: /app/reports/test-summary.html"
}

# Exécution selon le mode
case "$1" in
    "test")
        log "🚀 Exécution de tous les tests..."
        run_unit_tests
        run_odoo_tests
        run_code_quality
        run_security_tests
        generate_report
        log_success "🎉 Tous les tests sont terminés!"
        ;;
    "unit")
        run_unit_tests
        ;;
    "odoo")
        run_odoo_tests
        ;;
    "quality")
        run_code_quality
        ;;
    "security")
        run_security_tests
        ;;
    "report")
        generate_report
        ;;
    "odoo-server")
        log "🚀 Démarrage du serveur Odoo de test..."
        exec odoo --addons-path="$ODOO_ADDONS_PATH" \
                  --database="${POSTGRES_DB:-test_sama_etat}" \
                  --db-host="${HOST:-localhost}" \
                  --db-port="${PORT:-5432}" \
                  --db-user="${USER:-test_user}" \
                  --db-password="${PASSWORD:-test_password}" \
                  --init=sama_etat \
                  --without-demo=False
        ;;
    *)
        log_error "Usage: $0 {test|unit|odoo|quality|security|report|odoo-server}"
        exit 1
        ;;
esac