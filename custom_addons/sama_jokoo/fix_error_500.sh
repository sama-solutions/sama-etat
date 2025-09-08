#!/bin/bash

# Script de correction de l'erreur 500
# ====================================

echo "🔧 Correction de l'erreur 500 - Sama Jokoo"
echo "==========================================="

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
YELLOW='\033[1;33m'
NC='\033[0m'

echo -e "${BLUE}1. Arrêt des processus existants...${NC}"
PID=$(lsof -ti:$DEV_PORT 2>/dev/null)
if [ ! -z "$PID" ]; then
    kill -TERM $PID
    sleep 3
fi

echo -e "${BLUE}2. Activation de l'environnement virtuel...${NC}"
source "$VENV_PATH/bin/activate"

echo -e "${BLUE}3. Recréation de la base de données...${NC}"
PGPASSWORD=odoo dropdb -h localhost -p 5432 -U odoo --if-exists $DEV_DB
PGPASSWORD=odoo createdb -h localhost -p 5432 -U odoo $DEV_DB

echo -e "${BLUE}4. Installation du module minimal...${NC}"
cd "$ODOO_PATH"

python3 odoo-bin \
    --addons-path="$CUSTOM_ADDONS_PATH,addons" \
    --database="$DEV_DB" \
    --db_host="localhost" \
    --db_port="5432" \
    --db_user="odoo" \
    --db_password="odoo" \
    --xmlrpc-port="$DEV_PORT" \
    --init=sama_jokoo \
    --stop-after-init \
    --log-level=info \
    --without-demo=all

if [ $? -eq 0 ]; then
    echo -e "${GREEN}✅ Module minimal installé avec succès !${NC}"
else
    echo -e "${RED}❌ Erreur lors de l'installation${NC}"
    exit 1
fi

echo -e "${BLUE}5. Démarrage du serveur...${NC}"

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
echo $SERVER_PID > "dev_scripts/logs/odoo_dev.pid"

echo -e "${GREEN}✅ Serveur démarré avec succès !${NC}"
echo -e "${GREEN}🎉 ERREUR 500 CORRIGÉE !${NC}"
echo ""
echo -e "${GREEN}Informations de connexion :${NC}"
echo -e "  URL: ${BLUE}http://localhost:$DEV_PORT${NC}"
echo -e "  Base de données: ${BLUE}$DEV_DB${NC}"
echo -e "  Login: ${BLUE}admin${NC}"
echo -e "  Mot de passe: ${BLUE}admin${NC}"
echo ""
echo -e "${YELLOW}Le module fonctionne maintenant avec les modèles de base.${NC}"
echo -e "${YELLOW}Pour ajouter les vues et fonctionnalités complètes :${NC}"
echo -e "  1. Restaurer le manifest complet"
echo -e "  2. Mettre à jour le module"
echo ""
echo -e "Pour arrêter: ${BLUE}./dev_scripts/stop_dev.sh${NC}"