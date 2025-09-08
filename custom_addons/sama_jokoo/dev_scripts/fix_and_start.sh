#!/bin/bash

# Script de correction et démarrage pour Sama Jokoo
# =================================================

# Charger la configuration
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "$SCRIPT_DIR/config.sh"

log_info "=== Correction et démarrage Sama Jokoo ==="

# Arrêter les processus existants
stop_odoo_on_port $DEV_PORT

# Activer l'environnement virtuel
activate_venv

# Vérifier PostgreSQL
if ! check_postgres; then
    exit 1
fi

# Recréer la base de données proprement
log_info "Recréation de la base de données..."
PGPASSWORD=$DB_PASSWORD dropdb -h $DB_HOST -p $DB_PORT -U $DB_USER --if-exists $DEV_DB_NAME
PGPASSWORD=$DB_PASSWORD createdb -h $DB_HOST -p $DB_PORT -U $DB_USER $DEV_DB_NAME

# Aller dans le dossier Odoo
cd "$ODOO_PATH"

log_info "Initialisation de la base avec les modules de base..."

# Étape 1: Initialiser la base avec les modules de base
python3 odoo-bin \
    --addons-path="$CUSTOM_ADDONS_PATH,addons" \
    --database="$DEV_DB_NAME" \
    --db_host="$DB_HOST" \
    --db_port="$DB_PORT" \
    --db_user="$DB_USER" \
    --db_password="$DB_PASSWORD" \
    --xmlrpc-port="$DEV_PORT" \
    --init=base \
    --stop-after-init \
    --log-level=info \
    --logfile="$LOG_FILE" \
    --without-demo=all

if [ $? -eq 0 ]; then
    log_success "Base de données initialisée avec succès"
else
    log_error "Erreur lors de l'initialisation de la base"
    exit 1
fi

log_info "Installation du module Sama Jokoo..."

# Étape 2: Installer notre module
python3 odoo-bin \
    --addons-path="$CUSTOM_ADDONS_PATH,addons" \
    --database="$DEV_DB_NAME" \
    --db_host="$DB_HOST" \
    --db_port="$DB_PORT" \
    --db_user="$DB_USER" \
    --db_password="$DB_PASSWORD" \
    --xmlrpc-port="$DEV_PORT" \
    --init=sama_jokoo \
    --stop-after-init \
    --log-level=info \
    --logfile="$LOG_FILE" \
    --without-demo=all

if [ $? -eq 0 ]; then
    log_success "Module Sama Jokoo installé avec succès"
else
    log_error "Erreur lors de l'installation du module"
    exit 1
fi

log_info "Démarrage du serveur en mode normal..."

# Étape 3: Démarrer en mode normal
python3 odoo-bin \
    --addons-path="$CUSTOM_ADDONS_PATH,addons" \
    --database="$DEV_DB_NAME" \
    --db_host="$DB_HOST" \
    --db_port="$DB_PORT" \
    --db_user="$DB_USER" \
    --db_password="$DB_PASSWORD" \
    --xmlrpc-port="$DEV_PORT" \
    --log-level=info \
    --logfile="$LOG_FILE" \
    --without-demo=all &

ODOO_PID=$!
echo $ODOO_PID > "$LOG_DIR/odoo_dev.pid"

log_success "Serveur démarré avec le PID: $ODOO_PID"
log_success "=== Sama Jokoo prêt ! ==="
log_info "URL: http://localhost:$DEV_PORT"
log_info "Login: admin"
log_info "Mot de passe: admin"
log_info ""
log_info "Pour arrêter: ./dev_scripts/stop_dev.sh"
log_info "Pour voir les logs: ./dev_scripts/watch_logs.sh"