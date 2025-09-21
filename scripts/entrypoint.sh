#!/bin/bash
# Script d'entrée pour SAMA ÉTAT
# Auteurs: Mamadou Mbagnick DOGUE, Rassol DOGUE

set -e

# Couleurs pour les logs
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Fonction de logging
log() {
    echo -e "${BLUE}[SAMA ÉTAT]${NC} $1"
}

log_success() {
    echo -e "${GREEN}[SAMA ÉTAT]${NC} $1"
}

log_warning() {
    echo -e "${YELLOW}[SAMA ÉTAT]${NC} $1"
}

log_error() {
    echo -e "${RED}[SAMA ÉTAT]${NC} $1"
}

# Banner SAMA ÉTAT
echo -e "${BLUE}"
cat << "EOF"
   ____    _    __  __    _      _____ _____  _  _____ 
  / ___|  / \  |  \/  |  / \    | ____|_   _|/ \|_   _|
  \___ \ / _ \ | |\/| | / _ \   |  _|   | | / _ \ | |  
   ___) / ___ \| |  | |/ ___ \  | |___  | |/ ___ \| |  
  |____/_/   \_\_|  |_/_/   \_\ |_____| |_/_/   \_\_|  
                                                       
  Plateforme citoyenne de gouvernance stratégique
  Auteurs: Mamadou Mbagnick DOGUE, Rassol DOGUE
  Version: 1.0.0
EOF
echo -e "${NC}"

# Variables d'environnement par défaut
export ODOO_RC=${ODOO_RC:-/etc/odoo/odoo.conf}
export ODOO_ADDONS_PATH=${ODOO_ADDONS_PATH:-/usr/lib/python3/dist-packages/odoo/addons,/mnt/extra-addons}

log "Démarrage de SAMA ÉTAT..."

# Vérification des prérequis
log "Vérification des prérequis..."

# Vérifier que PostgreSQL est accessible
if [ -n "$HOST" ]; then
    log "Attente de la base de données PostgreSQL..."
    while ! nc -z "$HOST" "${PORT:-5432}"; do
        log_warning "En attente de PostgreSQL sur $HOST:${PORT:-5432}..."
        sleep 2
    done
    log_success "PostgreSQL est accessible"
fi

# Vérifier les permissions des répertoires
log "Vérification des permissions..."
for dir in "/var/lib/odoo" "/var/log/odoo"; do
    if [ ! -w "$dir" ]; then
        log_error "Pas de permission d'écriture sur $dir"
        exit 1
    fi
done

# Installer les dépendances Python si nécessaire
log "Vérification des dépendances Python..."
python3 -c "import qrcode, PIL" 2>/dev/null || {
    log_warning "Installation des dépendances Python manquantes..."
    pip3 install --no-cache-dir qrcode[pil] pillow
}

# Vérifier la configuration Odoo
if [ ! -f "$ODOO_RC" ]; then
    log_warning "Fichier de configuration Odoo non trouvé: $ODOO_RC"
    log "Utilisation de la configuration par défaut"
fi

# Initialiser la base de données si nécessaire
if [ "$1" = "odoo" ] && [ -n "$INIT_DB" ]; then
    log "Initialisation de la base de données..."
    odoo --addons-path="$ODOO_ADDONS_PATH" \
         --database="$POSTGRES_DB" \
         --init=sama_etat \
         --stop-after-init \
         --without-demo=False
    log_success "Base de données initialisée"
fi

# Mise à jour du module si demandé
if [ "$1" = "odoo" ] && [ -n "$UPDATE_MODULE" ]; then
    log "Mise à jour du module SAMA ÉTAT..."
    odoo --addons-path="$ODOO_ADDONS_PATH" \
         --database="$POSTGRES_DB" \
         --update=sama_etat \
         --stop-after-init
    log_success "Module mis à jour"
fi

# Configuration des logs
log "Configuration des logs..."
mkdir -p /var/log/odoo
touch /var/log/odoo/odoo.log
chmod 644 /var/log/odoo/odoo.log

# Affichage des informations de démarrage
log "Configuration:"
log "  - Addons path: $ODOO_ADDONS_PATH"
log "  - Config file: $ODOO_RC"
log "  - Database: ${POSTGRES_DB:-sama_etat}"
log "  - Host: ${HOST:-localhost}"
log "  - Port: ${PORT:-5432}"

# Démarrage d'Odoo avec les paramètres appropriés
if [ "$1" = "odoo" ]; then
    log_success "Démarrage d'Odoo avec SAMA ÉTAT..."
    
    # Construction des arguments Odoo
    ODOO_ARGS=(
        "--addons-path=$ODOO_ADDONS_PATH"
        "--config=$ODOO_RC"
    )
    
    # Ajout de la base de données si spécifiée
    if [ -n "$POSTGRES_DB" ]; then
        ODOO_ARGS+=("--database=$POSTGRES_DB")
    fi
    
    # Mode développement
    if [ "$DEV_MODE" = "true" ]; then
        log_warning "Mode développement activé"
        ODOO_ARGS+=(
            "--dev=reload,qweb,werkzeug,xml"
            "--log-level=debug"
        )
    fi
    
    # Exécution d'Odoo
    exec odoo "${ODOO_ARGS[@]}" "$@"
else
    # Exécution de la commande passée en paramètre
    log "Exécution de la commande: $*"
    exec "$@"
fi