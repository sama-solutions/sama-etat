#!/bin/bash

# Script de redémarrage pour Sama Jokoo
# =====================================

MODULE_PATH="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Couleurs
BLUE='\033[0;34m'
NC='\033[0m'

log_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

log_info "=== Redémarrage de Sama Jokoo ==="

# Arrêter
"$MODULE_PATH/stop_sama_jokoo.sh"

# Attendre
sleep 3

# Redémarrer
"$MODULE_PATH/start_sama_jokoo.sh"