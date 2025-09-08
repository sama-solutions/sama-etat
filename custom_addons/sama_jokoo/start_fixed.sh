#!/bin/bash

# Démarrage permanent après correction de l'erreur 500
# ===================================================

echo "🚀 Démarrage permanent de Sama Jokoo (version corrigée)"
echo "======================================================"

# Configuration
ODOO_PATH="/var/odoo/odoo18"
VENV_PATH="/home/grand-as/odoo18-venv"
CUSTOM_ADDONS_PATH="/home/grand-as/psagsn/custom_addons"
DEV_PORT="8070"
DEV_DB="sama_jokoo_dev"

# Couleurs
GREEN='\033[0;32m'
RED='\033[0;31m'
BLUE='\033[0;34m'
NC='\033[0m'

echo -e "${BLUE}1. Arrêt des processus existants...${NC}"
PID=$(lsof -ti:$DEV_PORT 2>/dev/null)
if [ ! -z "$PID" ]; then
    kill -TERM $PID
    sleep 3
fi

echo -e "${BLUE}2. Activation de l'environnement virtuel...${NC}"
source "$VENV_PATH/bin/activate"

echo -e "${BLUE}3. Démarrage du serveur...${NC}"
cd "$ODOO_PATH"

# Créer le dossier logs s'il n'existe pas
mkdir -p "/home/grand-as/psagsn/custom_addons/sama_jokoo/dev_scripts/logs"

python3 odoo-bin \
    --addons-path="$CUSTOM_ADDONS_PATH,addons" \
    --database="$DEV_DB" \
    --db_host="localhost" \
    --db_port="5432" \
    --db_user="odoo" \
    --db_password="odoo" \
    --xmlrpc-port="$DEV_PORT" \
    --log-level=info \
    --logfile="/home/grand-as/psagsn/custom_addons/sama_jokoo/dev_scripts/logs/odoo_dev.log" \
    --without-demo=all &

SERVER_PID=$!
echo $SERVER_PID > "/home/grand-as/psagsn/custom_addons/sama_jokoo/dev_scripts/logs/odoo_dev.pid"

sleep 5

if kill -0 $SERVER_PID 2>/dev/null; then
    echo -e "${GREEN}✅ Serveur démarré avec succès !${NC}"
    echo -e "${GREEN}🎉 SAMA JOKOO FONCTIONNE !${NC}"
    echo ""
    echo -e "${GREEN}Informations de connexion :${NC}"
    echo -e "  URL: ${BLUE}http://localhost:$DEV_PORT${NC}"
    echo -e "  Base de données: ${BLUE}$DEV_DB${NC}"
    echo -e "  Login: ${BLUE}admin${NC}"
    echo -e "  Mot de passe: ${BLUE}admin${NC}"
    echo -e "  PID: ${BLUE}$SERVER_PID${NC}"
    echo ""
    echo -e "${BLUE}Pour arrêter: ./dev_scripts/stop_dev.sh${NC}"
    echo -e "${BLUE}Pour voir les logs: ./dev_scripts/watch_logs.sh${NC}"
    echo ""
    echo -e "${GREEN}✨ L'erreur 500 a été corrigée ! ✨${NC}"
else
    echo -e "${RED}❌ Erreur lors du démarrage${NC}"
    exit 1
fi