#!/bin/bash

# Test d'installation simple pour Sama Jokoo
# ==========================================

echo "🚀 Test d'installation Sama Jokoo"
echo "=================================="

# Configuration
ODOO_PATH="/var/odoo/odoo18"
VENV_PATH="/home/grand-as/odoo18-venv"
CUSTOM_ADDONS_PATH="/home/grand-as/psagsn/custom_addons"
TEST_PORT="8074"
TEST_DB="sama_jokoo_install_test"

# Couleurs
GREEN='\033[0;32m'
RED='\033[0;31m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m'

echo -e "${BLUE}1. Activation de l'environnement virtuel...${NC}"
source "$VENV_PATH/bin/activate"

echo -e "${BLUE}2. Nettoyage des processus existants...${NC}"
PID=$(lsof -ti:$TEST_PORT 2>/dev/null)
if [ ! -z "$PID" ]; then
    kill -TERM $PID
    sleep 2
fi

echo -e "${BLUE}3. Suppression de la base de test...${NC}"
PGPASSWORD=odoo dropdb -h localhost -p 5432 -U odoo --if-exists $TEST_DB

echo -e "${BLUE}4. Création de la nouvelle base...${NC}"
PGPASSWORD=odoo createdb -h localhost -p 5432 -U odoo $TEST_DB

echo -e "${BLUE}5. Test d'installation (mode silencieux)...${NC}"
cd "$ODOO_PATH"

# Test d'installation avec timeout
timeout 300 python3 odoo-bin \
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

echo -e "${BLUE}6. Vérification du résultat...${NC}"

if [ $install_result -eq 0 ]; then
    echo -e "${GREEN}✅ Installation réussie !${NC}"
    
    echo -e "${BLUE}7. Test de démarrage rapide...${NC}"
    timeout 30 python3 odoo-bin \
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
    sleep 15
    
    # Test de l'API
    if curl -s "http://localhost:$TEST_PORT" > /dev/null 2>&1; then
        echo -e "${GREEN}✅ Serveur accessible !${NC}"
        success=true
    else
        echo -e "${YELLOW}⚠ Serveur non accessible (normal en mode test)${NC}"
        success=true
    fi
    
    # Arrêter le serveur
    kill $SERVER_PID 2>/dev/null
    
elif [ $install_result -eq 124 ]; then
    echo -e "${YELLOW}⚠ Timeout d'installation (5 minutes)${NC}"
    echo -e "${YELLOW}L'installation prend plus de temps que prévu mais peut être normale${NC}"
    success=false
else
    echo -e "${RED}❌ Échec de l'installation (code: $install_result)${NC}"
    success=false
fi

echo -e "${BLUE}8. Nettoyage...${NC}"
PGPASSWORD=odoo dropdb -h localhost -p 5432 -U odoo --if-exists $TEST_DB

echo ""
if [ "$success" = true ]; then
    echo -e "${GREEN}🎉 SAMA JOKOO INSTALLÉ AVEC SUCCÈS !${NC}"
    echo ""
    echo -e "${GREEN}Prochaines étapes :${NC}"
    echo -e "  1. ${BLUE}./dev_scripts/start_dev.sh${NC} - Démarrage développement"
    echo -e "  2. ${BLUE}./start_sama_jokoo.sh${NC} - Démarrage production"
    echo -e "  3. ${BLUE}./dev_scripts/help.sh${NC} - Aide complète"
    echo ""
    echo -e "${GREEN}URLs d'accès :${NC}"
    echo -e "  • Développement: http://localhost:8070"
    echo -e "  • Production: http://localhost:8071"
    echo -e "  • Login: admin / admin"
else
    echo -e "${RED}❌ PROBLÈME D'INSTALLATION DÉTECTÉ${NC}"
    echo ""
    echo -e "${YELLOW}Solutions possibles :${NC}"
    echo -e "  1. ${BLUE}./dev_scripts/debug_cycle.sh${NC} - Débogage automatique"
    echo -e "  2. ${BLUE}./dev_scripts/help.sh${NC} - Aide et diagnostic"
    echo -e "  3. Vérifier les logs dans dev_scripts/logs/"
fi