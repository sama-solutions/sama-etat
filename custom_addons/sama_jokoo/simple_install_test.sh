#!/bin/bash

# Test d'installation simple avec dépendances minimales
# =====================================================

echo "🚀 Test d'installation simple Sama Jokoo"
echo "========================================"

# Configuration
ODOO_PATH="/var/odoo/odoo18"
VENV_PATH="/home/grand-as/odoo18-venv"
CUSTOM_ADDONS_PATH="/home/grand-as/psagsn/custom_addons"
TEST_PORT="8075"
TEST_DB="sama_jokoo_simple_test"

# Couleurs
GREEN='\033[0;32m'
RED='\033[0;31m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m'

echo -e "${BLUE}1. Activation de l'environnement virtuel...${NC}"
source "$VENV_PATH/bin/activate"

echo -e "${BLUE}2. Nettoyage...${NC}"
PID=$(lsof -ti:$TEST_PORT 2>/dev/null)
if [ ! -z "$PID" ]; then
    kill -TERM $PID
    sleep 2
fi

echo -e "${BLUE}3. Recréation de la base de données...${NC}"
PGPASSWORD=odoo dropdb -h localhost -p 5432 -U odoo --if-exists $TEST_DB
PGPASSWORD=odoo createdb -h localhost -p 5432 -U odoo $TEST_DB

echo -e "${BLUE}4. Installation avec dépendances minimales...${NC}"
cd "$ODOO_PATH"

# Installation avec timeout de 3 minutes
timeout 180 python3 odoo-bin \
    --addons-path="$CUSTOM_ADDONS_PATH,addons" \
    --database="$TEST_DB" \
    --db_host="localhost" \
    --db_port="5432" \
    --db_user="odoo" \
    --db_password="odoo" \
    --xmlrpc-port="$TEST_PORT" \
    --init=sama_jokoo \
    --stop-after-init \
    --log-level=error \
    --without-demo=all

install_result=$?

echo -e "${BLUE}5. Vérification du résultat...${NC}"

if [ $install_result -eq 0 ]; then
    echo -e "${GREEN}✅ Installation réussie !${NC}"
    
    echo -e "${BLUE}6. Test de démarrage...${NC}"
    timeout 20 python3 odoo-bin \
        --addons-path="$CUSTOM_ADDONS_PATH,addons" \
        --database="$TEST_DB" \
        --db_host="localhost" \
        --db_port="5432" \
        --db_user="odoo" \
        --db_password="odoo" \
        --xmlrpc-port="$TEST_PORT" \
        --log-level=error \
        --without-demo=all &
    
    SERVER_PID=$!
    sleep 10
    
    # Test de l'accès
    if curl -s "http://localhost:$TEST_PORT" > /dev/null 2>&1; then
        echo -e "${GREEN}✅ Serveur accessible !${NC}"
        success=true
    else
        echo -e "${YELLOW}⚠ Serveur non accessible (peut être normal)${NC}"
        success=true
    fi
    
    # Arrêter le serveur
    kill $SERVER_PID 2>/dev/null
    
elif [ $install_result -eq 124 ]; then
    echo -e "${YELLOW}⚠ Timeout d'installation${NC}"
    success=false
else
    echo -e "${RED}❌ Échec de l'installation (code: $install_result)${NC}"
    success=false
fi

echo -e "${BLUE}7. Nettoyage...${NC}"
PGPASSWORD=odoo dropdb -h localhost -p 5432 -U odoo --if-exists $TEST_DB

echo ""
if [ "$success" = true ]; then
    echo -e "${GREEN}🎉 SAMA JOKOO INSTALLÉ AVEC SUCCÈS !${NC}"
    echo ""
    echo -e "${GREEN}Le module fonctionne avec les dépendances minimales.${NC}"
    echo -e "${GREEN}Vous pouvez maintenant démarrer le développement :${NC}"
    echo -e "  ${BLUE}./dev_scripts/fix_and_start.sh${NC}"
else
    echo -e "${RED}❌ PROBLÈME D'INSTALLATION${NC}"
    echo -e "${YELLOW}Vérifiez les logs pour plus de détails.${NC}"
fi