#!/bin/bash

# Script de test rapide pour Sama Jokoo
# =====================================

echo "🚀 Test rapide de Sama Jokoo"
echo "=============================="

# Configuration
ODOO_PATH="/var/odoo/odoo18"
VENV_PATH="/home/grand-as/odoo18-venv"
CUSTOM_ADDONS_PATH="/home/grand-as/psagsn/custom_addons"
TEST_PORT="8073"
TEST_DB="sama_jokoo_quick_test"

# Couleurs
GREEN='\033[0;32m'
RED='\033[0;31m'
BLUE='\033[0;34m'
NC='\033[0m'

echo -e "${BLUE}1. Activation de l'environnement virtuel...${NC}"
source "$VENV_PATH/bin/activate"

echo -e "${BLUE}2. Arrêt des processus existants sur le port $TEST_PORT...${NC}"
PID=$(lsof -ti:$TEST_PORT 2>/dev/null)
if [ ! -z "$PID" ]; then
    kill -TERM $PID
    sleep 2
fi

echo -e "${BLUE}3. Suppression de la base de test existante...${NC}"
PGPASSWORD=odoo dropdb -h localhost -p 5432 -U odoo --if-exists $TEST_DB

echo -e "${BLUE}4. Création de la nouvelle base de test...${NC}"
PGPASSWORD=odoo createdb -h localhost -p 5432 -U odoo $TEST_DB

echo -e "${BLUE}5. Test d'installation du module...${NC}"
cd "$ODOO_PATH"

python3 odoo-bin \
    --addons-path="$CUSTOM_ADDONS_PATH,addons" \
    --database="$TEST_DB" \
    --db_host="localhost" \
    --db_port="5432" \
    --db_user="odoo" \
    --db_password="odoo" \
    --xmlrpc-port="$TEST_PORT" \
    --init=sama_jokoo \
    --stop-after-init \
    --log-level=info

if [ $? -eq 0 ]; then
    echo -e "${GREEN}✅ Installation réussie !${NC}"
    
    echo -e "${BLUE}6. Test de démarrage du serveur...${NC}"
    python3 odoo-bin \
        --addons-path="$CUSTOM_ADDONS_PATH,addons" \
        --database="$TEST_DB" \
        --db_host="localhost" \
        --db_port="5432" \
        --db_user="odoo" \
        --db_password="odoo" \
        --xmlrpc-port="$TEST_PORT" \
        --log-level=error &
    
    SERVER_PID=$!
    sleep 10
    
    # Test de l'API
    if curl -s "http://localhost:$TEST_PORT/social/api/health" > /dev/null; then
        echo -e "${GREEN}✅ Serveur démarré et API accessible !${NC}"
        echo -e "${GREEN}🎉 SAMA JOKOO FONCTIONNE !${NC}"
        echo ""
        echo "URL de test: http://localhost:$TEST_PORT"
        echo "Base de données: $TEST_DB"
        echo "Login: admin / admin"
        echo ""
        echo "Appuyez sur Entrée pour arrêter le serveur de test..."
        read
    else
        echo -e "${RED}❌ Serveur non accessible${NC}"
    fi
    
    # Arrêter le serveur
    kill $SERVER_PID 2>/dev/null
    
else
    echo -e "${RED}❌ Échec de l'installation${NC}"
fi

echo -e "${BLUE}7. Nettoyage...${NC}"
PGPASSWORD=odoo dropdb -h localhost -p 5432 -U odoo --if-exists $TEST_DB

echo -e "${GREEN}Test terminé !${NC}"