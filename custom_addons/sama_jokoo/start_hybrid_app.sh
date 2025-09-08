#!/bin/bash

# Script de démarrage hybride Sama Jokoo
# ======================================
# Lance l'application neumorphique avec détection automatique Odoo

echo "🔄 Démarrage hybride Sama Jokoo"
echo "==============================="

# Couleurs
GREEN='\033[0;32m'
RED='\033[0;31m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
PURPLE='\033[0;35m'
NC='\033[0m'

# Configuration
ODOO_PORT="8070"
APP_PORT="3000"
ODOO_DB="sama_jokoo_dev"

echo -e "${BLUE}1. Détection de l'environnement...${NC}"

# Test de connexion Odoo
ODOO_AVAILABLE=false
if curl -s --connect-timeout 3 "http://localhost:$ODOO_PORT/web/database/selector" >/dev/null 2>&1; then
    ODOO_AVAILABLE=true
    echo -e "${GREEN}✅ Serveur Odoo détecté sur le port $ODOO_PORT${NC}"
else
    echo -e "${YELLOW}⚠️ Serveur Odoo non accessible${NC}"
fi

# Test de l'API Odoo si disponible
ODOO_API_WORKING=false
if [ "$ODOO_AVAILABLE" = true ]; then
    echo -e "${BLUE}2. Test de l'API Odoo...${NC}"
    
    # Test d'authentification rapide
    AUTH_TEST=$(curl -s --connect-timeout 5 -X POST \
        -H "Content-Type: application/json" \
        -d '{
            "jsonrpc": "2.0",
            "method": "call",
            "params": {
                "service": "common",
                "method": "authenticate",
                "args": ["'$ODOO_DB'", "admin", "admin", {}]
            },
            "id": 1
        }' \
        "http://localhost:$ODOO_PORT/jsonrpc" 2>/dev/null)
    
    if echo "$AUTH_TEST" | grep -q '"result"' && ! echo "$AUTH_TEST" | grep -q '"error"'; then
        ODOO_API_WORKING=true
        echo -e "${GREEN}✅ API Odoo fonctionnelle${NC}"
    else
        echo -e "${YELLOW}⚠️ API Odoo non fonctionnelle${NC}"
    fi
else
    echo -e "${BLUE}2. Serveur Odoo non disponible, mode démo activé${NC}"
fi

# Déterminer le mode de fonctionnement
if [ "$ODOO_API_WORKING" = true ]; then
    MODE="PRODUCTION"
    MODE_COLOR="${GREEN}"
    MODE_ICON="🚀"
    MODE_DESC="Connecté au serveur Odoo réel"
else
    MODE="DEMO"
    MODE_COLOR="${PURPLE}"
    MODE_ICON="🎭"
    MODE_DESC="Mode démo avec données de test"
fi

echo ""
echo -e "${MODE_COLOR}${MODE_ICON} MODE DÉTECTÉ: $MODE${NC}"
echo -e "${MODE_COLOR}$MODE_DESC${NC}"
echo ""

# Arrêter les serveurs existants
echo -e "${BLUE}3. Nettoyage des processus existants...${NC}"
pkill -f "python3 serve_app.py" 2>/dev/null
pkill -f "node simple_server.js" 2>/dev/null
pkill -f "vite" 2>/dev/null
sleep 2

# Choisir le serveur approprié
if [ "$MODE" = "PRODUCTION" ]; then
    echo -e "${BLUE}4. Démarrage en mode PRODUCTION...${NC}"
    
    # Modifier l'application pour utiliser le vrai serveur
    cd neumorphic_app
    
    # Créer un fichier de configuration pour le mode production
    cat > src/config.js << EOF
export const API_CONFIG = {
  mode: 'production',
  baseURL: 'http://localhost:$ODOO_PORT',
  database: '$ODOO_DB',
  timeout: 10000
};
EOF
    
    echo -e "${GREEN}✅ Configuration production créée${NC}"
    
    # Démarrer l'application Vue.js
    echo -e "${BLUE}Démarrage de l'application Vue.js...${NC}"
    
    # Choisir un port libre
    PORT=$APP_PORT
    for test_port in 3000 3001 3002; do
        if ! lsof -i:$test_port >/dev/null 2>&1; then
            PORT=$test_port
            break
        fi
    done
    
    echo ""
    echo -e "${GREEN}🚀 SAMA JOKOO - MODE PRODUCTION${NC}"
    echo ""
    echo -e "${GREEN}Informations :${NC}"
    echo -e "  📱 Application : ${BLUE}http://localhost:$PORT${NC}"
    echo -e "  🔧 Serveur Odoo : ${BLUE}http://localhost:$ODOO_PORT${NC}"
    echo -e "  💾 Base de données : ${BLUE}$ODOO_DB${NC}"
    echo -e "  👤 Login : ${BLUE}admin${NC}"
    echo -e "  🔑 Mot de passe : ${BLUE}admin${NC}"
    echo ""
    echo -e "${YELLOW}Fonctionnalités PRODUCTION :${NC}"
    echo -e "  ✨ Design neumorphique complet"
    echo -e "  🔗 Connexion Odoo réelle"
    echo -e "  💾 Données persistantes"
    echo -e "  🔄 Synchronisation temps réel"
    echo -e "  📊 Modèles sociaux complets"
    echo ""
    echo -e "${BLUE}Pour arrêter : Ctrl+C${NC}"
    echo ""
    
    # Démarrer l'application Vue.js
    npm run dev -- --port $PORT
    
else
    echo -e "${BLUE}4. Démarrage en mode DÉMO...${NC}"
    
    # Créer un fichier de configuration pour le mode démo
    mkdir -p neumorphic_app/src
    cat > neumorphic_app/src/config.js << EOF
export const API_CONFIG = {
  mode: 'demo',
  baseURL: 'http://localhost:3000',
  database: 'demo',
  timeout: 5000
};
EOF
    
    echo -e "${PURPLE}✅ Configuration démo créée${NC}"
    
    # Démarrer le serveur HTML simple
    echo -e "${BLUE}Démarrage du serveur démo...${NC}"
    
    echo ""
    echo -e "${PURPLE}🎭 SAMA JOKOO - MODE DÉMO${NC}"
    echo ""
    echo -e "${GREEN}Informations :${NC}"
    echo -e "  📱 Application : ${BLUE}http://localhost:$APP_PORT${NC}"
    echo -e "  🎭 Mode : ${BLUE}Démo avec données de test${NC}"
    echo -e "  👤 Login : ${BLUE}admin${NC}"
    echo -e "  🔑 Mot de passe : ${BLUE}admin${NC}"
    echo ""
    echo -e "${YELLOW}Fonctionnalités DÉMO :${NC}"
    echo -e "  ✨ Design neumorphique complet"
    echo -e "  🎨 Interface de démonstration"
    echo -e "  📊 Données de test intégrées"
    echo -e "  🔄 Interactions simulées"
    echo -e "  📱 PWA installable"
    echo ""
    echo -e "${BLUE}Pour arrêter : Ctrl+C${NC}"
    echo ""
    
    # Démarrer le serveur HTML
    python3 serve_app.py
fi