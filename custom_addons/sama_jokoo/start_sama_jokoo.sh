#!/bin/bash

# Script de démarrage principal pour Sama Jokoo
# =============================================
# Ce script démarre le module Sama Jokoo en production

# Configuration
ODOO_PATH="/var/odoo/odoo18"
VENV_PATH="/home/grand-as/odoo18-venv"
CUSTOM_ADDONS_PATH="/home/grand-as/psagsn/custom_addons"
MODULE_PATH="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Configuration PostgreSQL
DB_USER="odoo"
DB_PASSWORD="odoo"
DB_HOST="localhost"
DB_PORT="5432"

# Configuration Odoo
PROD_PORT="8071"
PROD_DB_NAME="sama_jokoo_prod"

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

# Arrêter les processus existants sur notre port
stop_existing_processes() {
    local port=$1
    local pid=$(lsof -ti:$port 2>/dev/null)
    
    if [ ! -z "$pid" ]; then
        log_warning "Arrêt du processus existant (PID: $pid) sur le port $port"
        kill -TERM $pid
        sleep 3
        
        if kill -0 $pid 2>/dev/null; then
            log_warning "Forçage de l'arrêt du processus $pid"
            kill -KILL $pid
        fi
        
        log_success "Processus arrêté sur le port $port"
    else
        log_info "Aucun processus trouvé sur le port $port"
    fi
}

# Vérifications préliminaires
check_requirements() {
    log_info "Vérifications préliminaires..."
    
    # Vérifier les chemins
    if [ ! -d "$ODOO_PATH" ]; then
        log_error "Chemin Odoo non trouvé: $ODOO_PATH"
        exit 1
    fi
    
    if [ ! -d "$VENV_PATH" ]; then
        log_error "Environnement virtuel non trouvé: $VENV_PATH"
        exit 1
    fi
    
    if [ ! -f "$MODULE_PATH/__manifest__.py" ]; then
        log_error "Module Sama Jokoo non trouvé dans: $MODULE_PATH"
        exit 1
    fi
    
    # Vérifier PostgreSQL
    if ! PGPASSWORD=$DB_PASSWORD psql -h $DB_HOST -p $DB_PORT -U $DB_USER -d postgres -c '\q' 2>/dev/null; then
        log_error "Impossible de se connecter à PostgreSQL"
        exit 1
    fi
    
    log_success "Toutes les vérifications sont passées"
}

# Créer la base de données si elle n'existe pas
setup_database() {
    log_info "Configuration de la base de données..."
    
    # Vérifier si la base existe
    if PGPASSWORD=$DB_PASSWORD psql -h $DB_HOST -p $DB_PORT -U $DB_USER -lqt | cut -d \| -f 1 | grep -qw $PROD_DB_NAME; then
        log_info "Base de données '$PROD_DB_NAME' existe déjà"
    else
        log_info "Création de la base de données '$PROD_DB_NAME'"
        PGPASSWORD=$DB_PASSWORD createdb -h $DB_HOST -p $DB_PORT -U $DB_USER $PROD_DB_NAME
        
        if [ $? -eq 0 ]; then
            log_success "Base de données créée avec succès"
        else
            log_error "Erreur lors de la création de la base de données"
            exit 1
        fi
    fi
}

# Démarrer Sama Jokoo
start_sama_jokoo() {
    log_info "=== Démarrage de Sama Jokoo ==="
    
    # Activer l'environnement virtuel
    if [ -f "$VENV_PATH/bin/activate" ]; then
        source "$VENV_PATH/bin/activate"
        log_success "Environnement virtuel activé"
    else
        log_error "Impossible d'activer l'environnement virtuel"
        exit 1
    fi
    
    # Aller dans le dossier Odoo
    cd "$ODOO_PATH"
    
    # Arrêter les processus existants
    stop_existing_processes $PROD_PORT
    
    # Configurer la base de données
    setup_database
    
    # Démarrer Odoo
    log_info "Démarrage d'Odoo avec Sama Jokoo..."
    log_info "Port: $PROD_PORT"
    log_info "Base de données: $PROD_DB_NAME"
    
    python3 odoo-bin \
        --addons-path="$CUSTOM_ADDONS_PATH,addons" \
        --database="$PROD_DB_NAME" \
        --db_host="$DB_HOST" \
        --db_port="$DB_PORT" \
        --db_user="$DB_USER" \
        --db_password="$DB_PASSWORD" \
        --xmlrpc-port="$PROD_PORT" \
        --log-level=info \
        --logfile="$MODULE_PATH/logs/sama_jokoo.log" \
        --pidfile="$MODULE_PATH/logs/sama_jokoo.pid" \
        --auto-reload \
        --without-demo=all &
    
    ODOO_PID=$!
    
    # Attendre que le serveur démarre
    log_info "Attente du démarrage du serveur..."
    sleep 15
    
    # Vérifier si le processus est actif
    if kill -0 $ODOO_PID 2>/dev/null; then
        log_success "=== Sama Jokoo démarré avec succès ==="
        log_info "PID: $ODOO_PID"
        log_info "URL: http://localhost:$PROD_PORT"
        log_info "Base de données: $PROD_DB_NAME"
        log_info "Logs: $MODULE_PATH/logs/sama_jokoo.log"
        log_info ""
        log_info "Pour arrêter: ./stop_sama_jokoo.sh"
        log_info "Pour redémarrer: ./restart_sama_jokoo.sh"
    else
        log_error "Erreur lors du démarrage. Vérifiez les logs."
        exit 1
    fi
}

# Créer le dossier logs s'il n'existe pas
mkdir -p "$MODULE_PATH/logs"

# Exécuter le démarrage
check_requirements
start_sama_jokoo