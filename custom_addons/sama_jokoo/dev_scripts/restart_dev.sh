#!/bin/bash

# Script de redémarrage pour le développement du module Sama Jokoo
# ================================================================

# Charger la configuration
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "$SCRIPT_DIR/config.sh"

log_info "=== Redémarrage du développement Sama Jokoo ==="

# Arrêter d'abord
"$SCRIPT_DIR/stop_dev.sh"

# Attendre un peu
sleep 2

# Redémarrer
"$SCRIPT_DIR/start_dev.sh"