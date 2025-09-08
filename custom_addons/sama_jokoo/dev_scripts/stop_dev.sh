#!/bin/bash

# Script d'arrêt pour le développement du module Sama Jokoo
# =========================================================

# Charger la configuration
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "$SCRIPT_DIR/config.sh"

log_info "=== Arrêt du développement Sama Jokoo ==="

# Arrêter les processus sur notre port
stop_odoo_on_port $DEV_PORT

# Supprimer le fichier PID s'il existe
if [ -f "$LOG_DIR/odoo_dev.pid" ]; then
    rm "$LOG_DIR/odoo_dev.pid"
    log_info "Fichier PID supprimé"
fi

log_success "=== Arrêt terminé ==="