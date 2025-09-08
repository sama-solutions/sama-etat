#!/bin/bash

# Script de validation de l'installation Sama Jokoo
# =================================================

# Charger la configuration
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "$SCRIPT_DIR/config.sh"

log_info "=== Validation de l'installation Sama Jokoo ==="

# Fonction de validation des fichiers
validate_files() {
    log_info "Validation de la structure des fichiers..."
    
    local required_files=(
        "__manifest__.py"
        "models/__init__.py"
        "models/social_post.py"
        "models/social_comment.py"
        "models/social_like.py"
        "models/social_follow.py"
        "models/social_notification.py"
        "models/social_media.py"
        "models/social_hashtag.py"
        "models/res_users.py"
        "models/mail_thread.py"
        "controllers/__init__.py"
        "controllers/api_auth.py"
        "controllers/api_social.py"
        "controllers/api_notification.py"
        "controllers/main.py"
        "security/social_security.xml"
        "security/ir.model.access.csv"
        "views/social_post_views.xml"
        "views/social_comment_views.xml"
        "views/social_notification_views.xml"
        "views/social_menus.xml"
        "views/res_users_views.xml"
        "views/social_dashboard.xml"
        "data/social_data.xml"
    )
    
    local missing_files=()
    
    for file in "${required_files[@]}"; do
        if [ ! -f "$MODULE_PATH/$file" ]; then
            missing_files+=("$file")
        fi
    done
    
    if [ ${#missing_files[@]} -eq 0 ]; then
        log_success "Tous les fichiers requis sont présents"
        return 0
    else
        log_error "Fichiers manquants:"
        for file in "${missing_files[@]}"; do
            log_error "  - $file"
        done
        return 1
    fi
}

# Fonction de validation de la syntaxe Python
validate_python_syntax() {
    log_info "Validation de la syntaxe Python..."
    
    local python_files=$(find "$MODULE_PATH" -name "*.py" -type f)
    local syntax_errors=0
    
    for file in $python_files; do
        if ! python3 -m py_compile "$file" 2>/dev/null; then
            log_error "Erreur de syntaxe dans: $file"
            syntax_errors=$((syntax_errors + 1))
        fi
    done
    
    if [ $syntax_errors -eq 0 ]; then
        log_success "Syntaxe Python correcte"
        return 0
    else
        log_error "$syntax_errors fichiers avec des erreurs de syntaxe"
        return 1
    fi
}

# Fonction de validation de la syntaxe XML
validate_xml_syntax() {
    log_info "Validation de la syntaxe XML..."
    
    local xml_files=$(find "$MODULE_PATH" -name "*.xml" -type f)
    local syntax_errors=0
    
    for file in $xml_files; do
        if ! xmllint --noout "$file" 2>/dev/null; then
            log_error "Erreur de syntaxe XML dans: $file"
            syntax_errors=$((syntax_errors + 1))
        fi
    done
    
    if [ $syntax_errors -eq 0 ]; then
        log_success "Syntaxe XML correcte"
        return 0
    else
        log_error "$syntax_errors fichiers XML avec des erreurs"
        return 1
    fi
}

# Fonction de validation du manifest
validate_manifest() {
    log_info "Validation du manifest..."
    
    local manifest="$MODULE_PATH/__manifest__.py"
    
    # Vérifier que le manifest est valide Python
    if ! python3 -c "exec(open('$manifest').read())" 2>/dev/null; then
        log_error "Manifest invalide"
        return 1
    fi
    
    # Vérifier les dépendances interdites
    if grep -q "account" "$manifest"; then
        log_error "Dépendance interdite 'account' trouvée dans le manifest"
        return 1
    fi
    
    if grep -q "social_media" "$manifest"; then
        log_error "Dépendance interdite 'social_media' trouvée dans le manifest"
        return 1
    fi
    
    log_success "Manifest valide et conforme aux directives Odoo 18 CE"
    return 0
}

# Fonction de validation des permissions
validate_permissions() {
    log_info "Validation des permissions des fichiers..."
    
    # Vérifier que les scripts sont exécutables
    local scripts=(
        "start_sama_jokoo.sh"
        "stop_sama_jokoo.sh"
        "restart_sama_jokoo.sh"
        "dev_scripts/start_dev.sh"
        "dev_scripts/stop_dev.sh"
        "dev_scripts/restart_dev.sh"
        "dev_scripts/watch_logs.sh"
        "dev_scripts/test_module.sh"
        "dev_scripts/debug_cycle.sh"
        "dev_scripts/help.sh"
        "mobile_app/start_mobile_dev.sh"
    )
    
    local permission_errors=0
    
    for script in "${scripts[@]}"; do
        if [ -f "$MODULE_PATH/$script" ] && [ ! -x "$MODULE_PATH/$script" ]; then
            log_error "Script non exécutable: $script"
            permission_errors=$((permission_errors + 1))
        fi
    done
    
    if [ $permission_errors -eq 0 ]; then
        log_success "Permissions des scripts correctes"
        return 0
    else
        log_error "$permission_errors scripts avec des problèmes de permissions"
        return 1
    fi
}

# Fonction de test de l'installation
test_installation() {
    log_info "Test d'installation du module..."
    
    # Activer l'environnement virtuel
    activate_venv
    
    # Aller dans le dossier Odoo
    cd "$ODOO_PATH"
    
    # Créer une base de données de test
    local test_db="sama_jokoo_validation"
    create_database "$test_db"
    
    # Tester l'installation
    python3 odoo-bin \
        --addons-path="$CUSTOM_ADDONS_PATH,addons" \
        --database="$test_db" \
        --db_host="$DB_HOST" \
        --db_port="$DB_PORT" \
        --db_user="$DB_USER" \
        --db_password="$DB_PASSWORD" \
        --init=sama_jokoo \
        --stop-after-init \
        --log-level=error \
        --logfile="$LOG_DIR/validation_test.log"
    
    local install_result=$?
    
    # Nettoyer la base de test
    PGPASSWORD=$DB_PASSWORD dropdb -h $DB_HOST -p $DB_PORT -U $DB_USER --if-exists "$test_db"
    
    if [ $install_result -eq 0 ]; then
        log_success "Installation du module réussie"
        return 0
    else
        log_error "Échec de l'installation du module"
        log_error "Vérifiez les logs: $LOG_DIR/validation_test.log"
        return 1
    fi
}

# Fonction de validation des APIs
validate_apis() {
    log_info "Validation des endpoints API..."
    
    # Démarrer Odoo temporairement
    activate_venv
    cd "$ODOO_PATH"
    
    local test_db="sama_jokoo_api_test"
    create_database "$test_db"
    
    python3 odoo-bin \
        --addons-path="$CUSTOM_ADDONS_PATH,addons" \
        --database="$test_db" \
        --db_host="$DB_HOST" \
        --db_port="$DB_PORT" \
        --db_user="$DB_USER" \
        --db_password="$DB_PASSWORD" \
        --xmlrpc-port="8072" \
        --init=sama_jokoo \
        --log-level=error \
        --logfile="$LOG_DIR/api_test.log" &
    
    local odoo_pid=$!
    sleep 15
    
    # Tester les endpoints
    local api_errors=0
    
    # Test health check
    if ! curl -s "http://localhost:8072/social/api/health" > /dev/null; then
        log_error "Endpoint health check non accessible"
        api_errors=$((api_errors + 1))
    fi
    
    # Arrêter Odoo
    kill $odoo_pid 2>/dev/null
    sleep 3
    
    # Nettoyer
    PGPASSWORD=$DB_PASSWORD dropdb -h $DB_HOST -p $DB_PORT -U $DB_USER --if-exists "$test_db"
    
    if [ $api_errors -eq 0 ]; then
        log_success "APIs accessibles"
        return 0
    else
        log_error "$api_errors endpoints non accessibles"
        return 1
    fi
}

# Fonction de génération du rapport
generate_report() {
    local validation_results=("$@")
    local total_tests=${#validation_results[@]}
    local passed_tests=0
    
    for result in "${validation_results[@]}"; do
        if [ "$result" = "0" ]; then
            passed_tests=$((passed_tests + 1))
        fi
    done
    
    log_info "=== RAPPORT DE VALIDATION ==="
    log_info "Tests passés: $passed_tests/$total_tests"
    
    if [ $passed_tests -eq $total_tests ]; then
        log_success "🎉 VALIDATION RÉUSSIE - Sama Jokoo est prêt !"
        log_info "Vous pouvez maintenant:"
        log_info "  1. Démarrer le développement: ./dev_scripts/start_dev.sh"
        log_info "  2. Démarrer la production: ./start_sama_jokoo.sh"
        log_info "  3. Développer l'app mobile: ./mobile_app/start_mobile_dev.sh"
        return 0
    else
        log_error "❌ VALIDATION ÉCHOUÉE - Corrections nécessaires"
        log_info "Consultez les erreurs ci-dessus et corrigez-les"
        return 1
    fi
}

# Exécution des validations
log_info "Début de la validation..."

results=()

validate_files
results+=($?)

validate_python_syntax
results+=($?)

validate_xml_syntax
results+=($?)

validate_manifest
results+=($?)

validate_permissions
results+=($?)

test_installation
results+=($?)

validate_apis
results+=($?)

# Générer le rapport final
generate_report "${results[@]}"