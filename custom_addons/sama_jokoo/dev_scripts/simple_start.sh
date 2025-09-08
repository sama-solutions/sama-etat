#!/bin/bash

# Démarrage simple pour test rapide
# =================================

# Charger la configuration
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "$SCRIPT_DIR/config.sh"

log_info "=== Démarrage simple Sama Jokoo ==="

# Arrêter les processus existants
stop_odoo_on_port $DEV_PORT

# Activer l'environnement virtuel
activate_venv

# Vérifier PostgreSQL
if ! check_postgres; then
    exit 1
fi

# Aller dans le dossier Odoo
cd "$ODOO_PATH"

log_info "Démarrage d'Odoo avec Sama Jokoo..."
log_info "Port: $DEV_PORT"
log_info "Base: $DEV_DB_NAME"

# Commande simple sans init (pour tester avec une base existante)
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
    --without-demo=all

log_info "Arrêt du serveur"