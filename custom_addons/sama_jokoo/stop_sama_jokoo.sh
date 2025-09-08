#!/bin/bash

# Script d'arrêt pour Sama Jokoo
# ==============================

MODULE_PATH="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROD_PORT="8071"

# Couleurs
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

log_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

log_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

log_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

log_info "=== Arrêt de Sama Jokoo ==="

# Arrêter via le fichier PID s'il existe
if [ -f "$MODULE_PATH/logs/sama_jokoo.pid" ]; then
    PID=$(cat "$MODULE_PATH/logs/sama_jokoo.pid")
    if kill -0 $PID 2>/dev/null; then
        log_info "Arrêt du processus PID: $PID"
        kill -TERM $PID
        sleep 5
        
        if kill -0 $PID 2>/dev/null; then
            log_warning "Forçage de l'arrêt"
            kill -KILL $PID
        fi
        
        log_success "Processus arrêté"
    else
        log_warning "Processus PID $PID non trouvé"
    fi
    
    rm "$MODULE_PATH/logs/sama_jokoo.pid"
fi

# Arrêter tous les processus sur le port
PID=$(lsof -ti:$PROD_PORT 2>/dev/null)
if [ ! -z "$PID" ]; then
    log_warning "Arrêt du processus sur le port $PROD_PORT (PID: $PID)"
    kill -TERM $PID
    sleep 3
    
    if kill -0 $PID 2>/dev/null; then
        kill -KILL $PID
    fi
fi

log_success "=== Sama Jokoo arrêté ==="