#!/bin/bash

# Script de mise à jour du module Sama Jokoo
# ==========================================

echo "🔄 Mise à jour du module Sama Jokoo"
echo "==================================="

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

echo -e "${BLUE}1. Arrêt du serveur...${NC}"
PID=$(lsof -ti:$DEV_PORT 2>/dev/null)
if [ ! -z "$PID" ]; then
    kill -TERM $PID
    sleep 3
    echo -e "${GREEN}✅ Serveur arrêté${NC}"
else
    echo -e "${BLUE}ℹ Aucun serveur à arrêter${NC}"
fi

echo -e "${BLUE}2. Activation de l'environnement virtuel...${NC}"
source "$VENV_PATH/bin/activate"

echo -e "${BLUE}3. Mise à jour du module...${NC}"
cd "$ODOO_PATH"

python3 odoo-bin \
    --addons-path="$CUSTOM_ADDONS_PATH,addons" \
    --database="$DEV_DB" \
    --db_host="localhost" \
    --db_port="5432" \
    --db_user="odoo" \
    --db_password="odoo" \
    --xmlrpc-port="$DEV_PORT" \
    --update=sama_jokoo \
    --stop-after-init \
    --log-level=info \
    --without-demo=all

if [ $? -eq 0 ]; then
    echo -e "${GREEN}✅ Module mis à jour avec succès !${NC}"
    
    echo -e "${BLUE}4. Redémarrage du serveur...${NC}"
    python3 odoo-bin \
        --addons-path="$CUSTOM_ADDONS_PATH,addons" \
        --database="$DEV_DB" \
        --db_host="localhost" \
        --db_port="5432" \
        --db_user="odoo" \
        --db_password="odoo" \
        --xmlrpc-port="$DEV_PORT" \
        --log-level=info \
        --without-demo=all &
    
    SERVER_PID=$!
    mkdir -p "dev_scripts/logs"
    echo $SERVER_PID > "dev_scripts/logs/odoo_dev.pid"
    
    sleep 5
    
    if kill -0 $SERVER_PID 2>/dev/null; then
        echo -e "${GREEN}✅ Serveur redémarré avec succès !${NC}"
        echo -e "${GREEN}🎉 MISE À JOUR TERMINÉE !${NC}"
        echo ""
        echo -e "${GREEN}Informations :${NC}"
        echo -e "  URL: ${BLUE}http://localhost:$DEV_PORT${NC}"
        echo -e "  Menu: ${BLUE}Social > Posts${NC}"
        echo -e "  PID: ${BLUE}$SERVER_PID${NC}"
    else
        echo -e "${RED}❌ Erreur lors du redémarrage${NC}"
        exit 1
    fi
else
    echo -e "${RED}❌ Erreur lors de la mise à jour${NC}"
    exit 1
fi