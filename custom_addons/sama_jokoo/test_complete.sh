#!/bin/bash

# Test complet : Démarrage + Test API
# ===================================

echo "🚀 Test complet Sama Jokoo"
echo "=========================="

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

echo -e "${BLUE}3. Démarrage du serveur en arrière-plan...${NC}"
cd "$ODOO_PATH"

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
echo -e "${GREEN}Serveur démarré (PID: $SERVER_PID)${NC}"

echo -e "${BLUE}4. Attente du démarrage complet...${NC}"
sleep 10

echo -e "${BLUE}5. Test de l'API...${NC}"
cd "/home/grand-as/psagsn/custom_addons/sama_jokoo"
python3 quick_api_test.py

echo -e "${BLUE}6. Arrêt du serveur...${NC}"
kill -TERM $SERVER_PID
sleep 3

echo -e "${GREEN}✅ Test terminé !${NC}"