#!/bin/bash

# Script de cycle de débogage pour le développement
# =================================================

# Charger la configuration
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "$SCRIPT_DIR/config.sh"

log_info "=== Cycle de débogage Sama Jokoo ==="
log_info "Ce script va effectuer un cycle complet: démarrage -> test -> analyse -> correction"

# Fonction pour analyser les logs
analyze_logs() {
    log_info "Analyse des logs..."
    
    if [ ! -f "$LOG_FILE" ]; then
        log_warning "Aucun fichier de log trouvé"
        return 1
    fi
    
    # Compter les erreurs
    local errors=$(grep -c "ERROR" "$LOG_FILE")
    local warnings=$(grep -c "WARNING" "$LOG_FILE")
    
    log_info "Erreurs trouvées: $errors"
    log_info "Avertissements trouvés: $warnings"
    
    if [ $errors -gt 0 ]; then
        log_error "=== ERREURS DÉTECTÉES ==="
        grep "ERROR" "$LOG_FILE" | tail -10
        return 1
    elif [ $warnings -gt 0 ]; then
        log_warning "=== AVERTISSEMENTS DÉTECTÉS ==="
        grep "WARNING" "$LOG_FILE" | tail -5
    fi
    
    return 0
}

# Fonction pour vérifier l'état du module
check_module_status() {
    log_info "Vérification de l'état du module..."
    
    # Vérifier si Odoo répond
    local response=$(curl -s -o /dev/null -w "%{http_code}" "http://localhost:$DEV_PORT/web/database/selector" 2>/dev/null)
    
    if [ "$response" = "200" ] || [ "$response" = "303" ]; then
        log_success "Odoo répond correctement"
        return 0
    else
        log_error "Odoo ne répond pas (code: $response)"
        return 1
    fi
}

# Fonction pour effectuer des corrections automatiques
auto_fix() {
    log_info "Tentative de corrections automatiques..."
    
    # Vérifier les permissions des fichiers
    find "$MODULE_PATH" -name "*.py" -exec chmod 644 {} \;
    find "$MODULE_PATH" -name "*.xml" -exec chmod 644 {} \;
    
    # Vérifier la structure des dossiers
    local required_dirs=("models" "views" "controllers" "security" "data")
    for dir in "${required_dirs[@]}"; do
        if [ ! -d "$MODULE_PATH/$dir" ]; then
            log_warning "Dossier manquant: $dir"
            mkdir -p "$MODULE_PATH/$dir"
        fi
    done
    
    log_success "Corrections automatiques appliquées"
}

# Cycle principal
cycle_count=0
max_cycles=5

while [ $cycle_count -lt $max_cycles ]; do
    cycle_count=$((cycle_count + 1))
    log_info "=== CYCLE $cycle_count/$max_cycles ==="
    
    # Étape 1: Démarrage
    log_info "Étape 1: Démarrage du module"
    "$SCRIPT_DIR/stop_dev.sh" > /dev/null 2>&1
    sleep 2
    
    # Nettoyer les logs précédents
    > "$LOG_FILE"
    
    # Démarrer en mode test
    activate_venv
    cd "$ODOO_PATH"
    
    python3 odoo-bin \
        --addons-path="$CUSTOM_ADDONS_PATH,addons" \
        --database="$DEV_DB_NAME" \
        --db_host="$DB_HOST" \
        --db_port="$DB_PORT" \
        --db_user="$DB_USER" \
        --db_password="$DB_PASSWORD" \
        --xmlrpc-port="$DEV_PORT" \
        --update=sama_jokoo \
        --log-level=debug \
        --logfile="$LOG_FILE" \
        --stop-after-init
    
    # Étape 2: Test
    log_info "Étape 2: Tests"
    sleep 2
    
    # Étape 3: Analyse des logs
    log_info "Étape 3: Analyse des logs"
    if analyze_logs; then
        log_success "Aucune erreur détectée!"
        
        # Test final de fonctionnement
        python3 odoo-bin \
            --addons-path="$CUSTOM_ADDONS_PATH,addons" \
            --database="$DEV_DB_NAME" \
            --db_host="$DB_HOST" \
            --db_port="$DB_PORT" \
            --db_user="$DB_USER" \
            --db_password="$DB_PASSWORD" \
            --xmlrpc-port="$DEV_PORT" \
            --log-level=info \
            --logfile="$LOG_FILE" &
        
        FINAL_PID=$!
        sleep 10
        
        if check_module_status; then
            echo $FINAL_PID > "$LOG_DIR/odoo_dev.pid"
            log_success "=== MODULE FONCTIONNEL - CYCLE TERMINÉ ==="
            log_info "Odoo fonctionne sur http://localhost:$DEV_PORT"
            log_info "PID: $FINAL_PID"
            exit 0
        else
            kill $FINAL_PID 2>/dev/null
        fi
    fi
    
    # Étape 4: Corrections
    log_info "Étape 4: Corrections automatiques"
    auto_fix
    
    log_warning "Cycle $cycle_count terminé avec des erreurs. Nouveau cycle dans 5 secondes..."
    sleep 5
done

log_error "=== ÉCHEC APRÈS $max_cycles CYCLES ==="
log_error "Vérifiez manuellement les logs: $LOG_FILE"
exit 1