#!/bin/bash

# Script de démarrage pour le développement du module Sama Jokoo
# ==============================================================

# Charger la configuration
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "$SCRIPT_DIR/config.sh"

log_info "=== Démarrage du développement Sama Jokoo ==="
log_info "Port de développement: $DEV_PORT"
log_info "Base de données: $DEV_DB_NAME"

# Vérifications préliminaires
log_info "Vérifications préliminaires..."

# Vérifier que les chemins existent
if [ ! -d "$ODOO_PATH" ]; then
    log_error "Chemin Odoo non trouvé: $ODOO_PATH"
    exit 1
fi

if [ ! -d "$VENV_PATH" ]; then
    log_error "Environnement virtuel non trouvé: $VENV_PATH"
    exit 1
fi

if [ ! -d "$CUSTOM_ADDONS_PATH" ]; then
    log_error "Dossier custom_addons non trouvé: $CUSTOM_ADDONS_PATH"
    exit 1
fi

# Activer l'environnement virtuel
activate_venv

# Vérifier PostgreSQL
if ! check_postgres; then
    exit 1
fi

# Arrêter les processus existants sur notre port
log_info "Arrêt des processus existants sur le port $DEV_PORT..."
stop_odoo_on_port $DEV_PORT

# Créer/recréer la base de données
create_database $DEV_DB_NAME

# Démarrer Odoo en mode développement
log_info "Démarrage d'Odoo en mode développement..."

cd "$ODOO_PATH"

# Commande Odoo avec tous les paramètres de développement
python3 odoo-bin \
    --addons-path="$CUSTOM_ADDONS_PATH,addons" \
    --database="$DEV_DB_NAME" \
    --db_host="$DB_HOST" \
    --db_port="$DB_PORT" \
    --db_user="$DB_USER" \
    --db_password="$DB_PASSWORD" \
    --xmlrpc-port="$DEV_PORT" \
    --dev=all \
    --log-level=debug \
    --log-handler=odoo.addons.sama_jokoo:DEBUG \
    --logfile="$LOG_FILE" \
    --init=sama_jokoo \
    --stop-after-init &

# Récupérer le PID du processus
ODOO_PID=$!
echo $ODOO_PID > "$LOG_DIR/odoo_dev.pid"

log_success "Odoo démarré avec le PID: $ODOO_PID"
log_info "Logs disponibles dans: $LOG_FILE"
log_info "URL d'accès: http://localhost:$DEV_PORT"
log_info "Base de données: $DEV_DB_NAME"
log_info "Login admin: admin"
log_info "Mot de passe admin: $ADMIN_PASSWORD"

# Attendre que l'initialisation soit terminée
log_info "Attente de l'initialisation du module..."
sleep 10

# Vérifier si le processus est toujours actif
if kill -0 $ODOO_PID 2>/dev/null; then
    log_success "Initialisation terminée. Redémarrage en mode normal..."
    
    # Arrêter le processus d'initialisation
    kill -TERM $ODOO_PID
    sleep 3
    
    # Redémarrer en mode normal
    python3 odoo-bin \
        --addons-path="$CUSTOM_ADDONS_PATH,addons" \
        --database="$DEV_DB_NAME" \
        --db_host="$DB_HOST" \
        --db_port="$DB_PORT" \
        --db_user="$DB_USER" \
        --db_password="$DB_PASSWORD" \
        --xmlrpc-port="$DEV_PORT" \
        --dev=all \
        --log-level=info \
        --logfile="$LOG_FILE" &
    
    ODOO_PID=$!
    echo $ODOO_PID > "$LOG_DIR/odoo_dev.pid"
    
    log_success "Odoo redémarré en mode normal avec le PID: $ODOO_PID"
    log_success "=== Sama Jokoo prêt pour le développement ==="
    log_info "Pour arrêter: ./stop_dev.sh"
    log_info "Pour voir les logs: ./watch_logs.sh"
    log_info "Pour redémarrer: ./restart_dev.sh"
else
    log_error "Erreur lors de l'initialisation. Vérifiez les logs: $LOG_FILE"
    exit 1
fi