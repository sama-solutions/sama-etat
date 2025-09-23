#!/bin/bash

# Script de démarrage SAMA SYNDICAT
# Arrête le processus sur le port 8070 et démarre le module

# Configuration
PORT=8070
DATABASE="sama_syndicat_final_1756812346"
ODOO_BIN="/var/odoo/odoo18/odoo-bin"
ADDONS_PATH="/var/odoo/odoo18/odoo/addons,/var/odoo/odoo18/addons,/tmp/addons_sama_syndicat"

# Couleurs pour l'affichage
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Fonction d'affichage avec couleurs
print_info() {
    echo -e "${BLUE}ℹ️ $1${NC}"
}

print_success() {
    echo -e "${GREEN}✅ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠️ $1${NC}"
}

print_error() {
    echo -e "${RED}❌ $1${NC}"
}

print_banner() {
    echo "=================================================="
    echo "🚀 SAMA SYNDICAT - DÉMARRAGE AUTOMATIQUE"
    echo "=================================================="
    echo "📊 Module: SAMA SYNDICAT"
    echo "🌐 Port: $PORT"
    echo "💾 Base: $DATABASE"
    echo "=================================================="
}

stop_processes() {
    print_info "Arrêt des processus existants sur le port $PORT..."
    
    # Méthode 1: Arrêter tous les processus odoo-bin
    if pgrep -f "odoo-bin" > /dev/null; then
        print_info "Arrêt des processus odoo-bin..."
        pkill -f "odoo-bin"
        sleep 2
        print_success "Processus odoo-bin arrêtés"
    fi
    
    # Méthode 2: Arrêter par port avec lsof
    if command -v lsof > /dev/null; then
        PIDS=$(lsof -ti :$PORT 2>/dev/null)
        if [ ! -z "$PIDS" ]; then
            print_info "Arrêt des processus sur le port $PORT..."
            echo $PIDS | xargs kill 2>/dev/null
            sleep 2
            print_success "Processus sur le port $PORT arrêtés"
        fi
    fi
    
    # Méthode 3: fuser (si disponible)
    if command -v fuser > /dev/null; then
        fuser -k ${PORT}/tcp 2>/dev/null
        print_success "Port $PORT libéré avec fuser"
    fi
    
    # Vérification finale
    if command -v lsof > /dev/null; then
        if lsof -ti :$PORT > /dev/null 2>&1; then
            print_warning "Le port $PORT semble encore occupé"
        else
            print_success "Port $PORT disponible"
        fi
    fi
    
    print_info "Attente de la libération complète du port..."
    sleep 3
}

check_odoo() {
    if [ ! -f "$ODOO_BIN" ]; then
        print_error "Odoo non trouvé à: $ODOO_BIN"
        
        # Rechercher dans des emplacements communs
        print_info "Recherche d'Odoo dans les emplacements communs..."
        
        COMMON_PATHS=(
            "/usr/bin/odoo"
            "/usr/local/bin/odoo"
            "/opt/odoo/odoo-bin"
            "/home/odoo/odoo/odoo-bin"
        )
        
        for path in "${COMMON_PATHS[@]}"; do
            if [ -f "$path" ]; then
                print_success "Odoo trouvé à: $path"
                ODOO_BIN="$path"
                return 0
            fi
        done
        
        # Vérifier dans le PATH
        if command -v odoo > /dev/null; then
            ODOO_BIN=$(which odoo)
            print_success "Odoo trouvé dans le PATH: $ODOO_BIN"
            return 0
        fi
        
        print_error "Odoo non trouvé. Veuillez installer Odoo ou ajuster le chemin."
        return 1
    fi
    
    print_success "Odoo trouvé: $ODOO_BIN"
    return 0
}

start_odoo() {
    print_info "Démarrage d'Odoo avec SAMA SYNDICAT..."
    
    # Vérifier que Python3 est disponible
    if ! command -v python3 > /dev/null; then
        print_error "Python3 non trouvé"
        return 1
    fi
    
    # Construire la commande
    CMD="python3 \"$ODOO_BIN\" \
        --addons-path=\"$ADDONS_PATH\" \
        --database=\"$DATABASE\" \
        --xmlrpc-port=$PORT \
        --dev=reload,xml \
        --log-level=info \
        --workers=0 \
        --max-cron-threads=0"
    
    print_info "Commande de démarrage:"
    echo "$CMD"
    echo
    
    print_success "🌐 Interface disponible sur: http://localhost:$PORT"
    print_success "📊 Dashboard SAMA: http://localhost:$PORT/web"
    print_success "🔗 Accès direct: http://localhost:$PORT/web/login?db=$DATABASE"
    echo
    print_info "💡 Pour arrêter le serveur, utilisez Ctrl+C"
    echo "=================================================="
    
    # Démarrer Odoo
    eval $CMD
}

# Fonction de nettoyage en cas d'interruption
cleanup() {
    echo
    print_info "Arrêt demandé par l'utilisateur..."
    print_info "Nettoyage en cours..."
    pkill -f "odoo-bin" 2>/dev/null
    print_success "Nettoyage terminé"
    exit 0
}

# Capturer Ctrl+C
trap cleanup SIGINT SIGTERM

main() {
    print_banner
    
    # Étape 1: Arrêter les processus existants
    stop_processes
    
    # Étape 2: Vérifier Odoo
    if ! check_odoo; then
        exit 1
    fi
    
    # Étape 3: Démarrer Odoo
    start_odoo
}

# Exécuter le script principal
main