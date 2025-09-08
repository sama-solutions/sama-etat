#!/bin/bash

# Configuration pour le développement du module Sama Jokoo
# =========================================================

# Chemins
export ODOO_PATH="/var/odoo/odoo18"
export VENV_PATH="/home/grand-as/odoo18-venv"
export CUSTOM_ADDONS_PATH="/home/grand-as/psagsn/custom_addons"
export MODULE_PATH="$CUSTOM_ADDONS_PATH/sama_jokoo"

# Configuration PostgreSQL
export DB_USER="odoo"
export DB_PASSWORD="odoo"
export DB_HOST="localhost"
export DB_PORT="5432"

# Configuration Odoo pour développement
export DEV_PORT="8070"
export DEV_DB_NAME="sama_jokoo_dev"
export ADMIN_PASSWORD="admin123"

# Logs
export LOG_DIR="$MODULE_PATH/dev_scripts/logs"
export LOG_FILE="$LOG_DIR/odoo_dev.log"

# Couleurs pour les messages
export RED='\033[0;31m'
export GREEN='\033[0;32m'
export YELLOW='\033[1;33m'
export BLUE='\033[0;34m'
export NC='\033[0m' # No Color

# Fonctions utilitaires
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

# Vérifier si un processus Odoo tourne sur un port
check_odoo_process() {
    local port=$1
    local pid=$(lsof -ti:$port)
    if [ ! -z "$pid" ]; then
        echo $pid
    else
        echo ""
    fi
}

# Arrêter les processus Odoo sur un port spécifique
stop_odoo_on_port() {
    local port=$1
    local pid=$(check_odoo_process $port)
    
    if [ ! -z "$pid" ]; then
        log_warning "Arrêt du processus Odoo (PID: $pid) sur le port $port"
        kill -TERM $pid
        sleep 3
        
        # Vérifier si le processus est toujours actif
        if kill -0 $pid 2>/dev/null; then
            log_warning "Forçage de l'arrêt du processus $pid"
            kill -KILL $pid
        fi
        
        log_success "Processus arrêté sur le port $port"
    else
        log_info "Aucun processus Odoo trouvé sur le port $port"
    fi
}

# Créer les dossiers nécessaires
create_directories() {
    mkdir -p "$LOG_DIR"
    mkdir -p "$MODULE_PATH/temp"
}

# Activer l'environnement virtuel
activate_venv() {
    if [ -f "$VENV_PATH/bin/activate" ]; then
        source "$VENV_PATH/bin/activate"
        log_success "Environnement virtuel activé: $VENV_PATH"
    else
        log_error "Environnement virtuel non trouvé: $VENV_PATH"
        exit 1
    fi
}

# Vérifier la connexion à PostgreSQL
check_postgres() {
    if PGPASSWORD=$DB_PASSWORD psql -h $DB_HOST -p $DB_PORT -U $DB_USER -d postgres -c '\q' 2>/dev/null; then
        log_success "Connexion PostgreSQL OK"
        return 0
    else
        log_error "Impossible de se connecter à PostgreSQL"
        return 1
    fi
}

# Créer ou recréer la base de données
create_database() {
    local db_name=$1
    
    log_info "Création de la base de données: $db_name"
    
    # Supprimer la base si elle existe
    PGPASSWORD=$DB_PASSWORD dropdb -h $DB_HOST -p $DB_PORT -U $DB_USER --if-exists $db_name
    
    # Créer la nouvelle base
    PGPASSWORD=$DB_PASSWORD createdb -h $DB_HOST -p $DB_PORT -U $DB_USER $db_name
    
    if [ $? -eq 0 ]; then
        log_success "Base de données '$db_name' créée avec succès"
    else
        log_error "Erreur lors de la création de la base de données '$db_name'"
        exit 1
    fi
}

# Initialiser les variables
create_directories