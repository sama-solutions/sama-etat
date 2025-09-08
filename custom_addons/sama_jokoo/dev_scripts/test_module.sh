#!/bin/bash

# Script de test pour le module Sama Jokoo
# ========================================

# Charger la configuration
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "$SCRIPT_DIR/config.sh"

log_info "=== Tests du module Sama Jokoo ==="

# Activer l'environnement virtuel
activate_venv

# Aller dans le dossier Odoo
cd "$ODOO_PATH"

# Fonction pour tester l'installation du module
test_module_install() {
    log_info "Test d'installation du module..."
    
    python3 odoo-bin \
        --addons-path="$CUSTOM_ADDONS_PATH,addons" \
        --database="$DEV_DB_NAME" \
        --db_host="$DB_HOST" \
        --db_port="$DB_PORT" \
        --db_user="$DB_USER" \
        --db_password="$DB_PASSWORD" \
        --test-enable \
        --test-tags=sama_jokoo \
        --log-level=test \
        --stop-after-init \
        --logfile="$LOG_DIR/test_install.log"
    
    if [ $? -eq 0 ]; then
        log_success "Test d'installation réussi"
    else
        log_error "Échec du test d'installation"
        return 1
    fi
}

# Fonction pour tester la mise à jour du module
test_module_upgrade() {
    log_info "Test de mise à jour du module..."
    
    python3 odoo-bin \
        --addons-path="$CUSTOM_ADDONS_PATH,addons" \
        --database="$DEV_DB_NAME" \
        --db_host="$DB_HOST" \
        --db_port="$DB_PORT" \
        --db_user="$DB_USER" \
        --db_password="$DB_PASSWORD" \
        --update=sama_jokoo \
        --test-enable \
        --test-tags=sama_jokoo \
        --log-level=test \
        --stop-after-init \
        --logfile="$LOG_DIR/test_upgrade.log"
    
    if [ $? -eq 0 ]; then
        log_success "Test de mise à jour réussi"
    else
        log_error "Échec du test de mise à jour"
        return 1
    fi
}

# Fonction pour vérifier la syntaxe Python
test_python_syntax() {
    log_info "Vérification de la syntaxe Python..."
    
    find "$MODULE_PATH" -name "*.py" -exec python3 -m py_compile {} \;
    
    if [ $? -eq 0 ]; then
        log_success "Syntaxe Python correcte"
    else
        log_error "Erreurs de syntaxe Python détectées"
        return 1
    fi
}

# Fonction pour vérifier la syntaxe XML
test_xml_syntax() {
    log_info "Vérification de la syntaxe XML..."
    
    find "$MODULE_PATH" -name "*.xml" -exec xmllint --noout {} \;
    
    if [ $? -eq 0 ]; then
        log_success "Syntaxe XML correcte"
    else
        log_error "Erreurs de syntaxe XML détectées"
        return 1
    fi
}

# Fonction pour tester les APIs
test_apis() {
    log_info "Test des APIs..."
    
    # Démarrer Odoo en arrière-plan pour les tests API
    python3 odoo-bin \
        --addons-path="$CUSTOM_ADDONS_PATH,addons" \
        --database="$DEV_DB_NAME" \
        --db_host="$DB_HOST" \
        --db_port="$DB_PORT" \
        --db_user="$DB_USER" \
        --db_password="$DB_PASSWORD" \
        --xmlrpc-port="$DEV_PORT" \
        --log-level=error \
        --logfile="$LOG_DIR/test_api.log" &
    
    API_PID=$!
    sleep 10
    
    # Test de l'API d'authentification
    curl -s -X POST "http://localhost:$DEV_PORT/api/social/auth/check" \
         -H "Content-Type: application/json" \
         -d '{}' > /dev/null
    
    if [ $? -eq 0 ]; then
        log_success "API accessible"
    else
        log_error "API non accessible"
    fi
    
    # Arrêter le serveur de test
    kill $API_PID 2>/dev/null
}

# Exécuter tous les tests
log_info "Début des tests..."

# Test de syntaxe
test_python_syntax || exit 1
test_xml_syntax || exit 1

# Tests fonctionnels
test_module_install || exit 1
test_module_upgrade || exit 1

# Test API
test_apis

log_success "=== Tous les tests sont passés avec succès ==="