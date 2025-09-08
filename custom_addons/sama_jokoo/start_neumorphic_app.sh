#!/bin/bash

# Script de démarrage de l'application neumorphique Sama Jokoo
# ============================================================

echo "🎨 Démarrage de l'application neumorphique Sama Jokoo"
echo "====================================================="

# Couleurs
GREEN='\033[0;32m'
RED='\033[0;31m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m'

# Configuration
APP_DIR="neumorphic_app"
ODOO_PORT="8070"
APP_PORT="3000"

echo -e "${BLUE}1. Vérification des prérequis...${NC}"

# Vérifier Node.js
if ! command -v node &> /dev/null; then
    echo -e "${RED}❌ Node.js n'est pas installé${NC}"
    echo -e "${YELLOW}Installez Node.js depuis https://nodejs.org/${NC}"
    exit 1
fi

NODE_VERSION=$(node --version)
echo -e "${GREEN}✅ Node.js détecté: $NODE_VERSION${NC}"

# Vérifier npm
if ! command -v npm &> /dev/null; then
    echo -e "${RED}❌ npm n'est pas installé${NC}"
    exit 1
fi

NPM_VERSION=$(npm --version)
echo -e "${GREEN}✅ npm détecté: $NPM_VERSION${NC}"

echo -e "${BLUE}2. Vérification du serveur Odoo...${NC}"

# Vérifier si Odoo fonctionne
if curl -s "http://localhost:$ODOO_PORT/web/database/selector" > /dev/null; then
    echo -e "${GREEN}✅ Serveur Odoo accessible sur le port $ODOO_PORT${NC}"
else
    echo -e "${YELLOW}⚠️ Serveur Odoo non accessible${NC}"
    echo -e "${BLUE}Démarrage du serveur Odoo...${NC}"
    
    # Démarrer Odoo en arrière-plan
    ./test_complete.sh &
    ODOO_PID=$!
    
    echo -e "${BLUE}Attente du démarrage d'Odoo...${NC}"
    sleep 10
    
    if curl -s "http://localhost:$ODOO_PORT/web/database/selector" > /dev/null; then
        echo -e "${GREEN}✅ Serveur Odoo démarré avec succès${NC}"
    else
        echo -e "${RED}❌ Impossible de démarrer le serveur Odoo${NC}"
        exit 1
    fi
fi

echo -e "${BLUE}3. Préparation de l'application...${NC}"

cd "$APP_DIR"

# Vérifier si les dépendances sont installées
if [ ! -d "node_modules" ]; then
    echo -e "${BLUE}Installation des dépendances...${NC}"
    npm install
    
    if [ $? -eq 0 ]; then
        echo -e "${GREEN}✅ Dépendances installées avec succès${NC}"
    else
        echo -e "${RED}❌ Erreur lors de l'installation des dépendances${NC}"
        exit 1
    fi
else
    echo -e "${GREEN}✅ Dépendances déjà installées${NC}"
fi

echo -e "${BLUE}4. Démarrage de l'application neumorphique...${NC}"

# Démarrer l'application en mode développement
npm run dev &
APP_PID=$!

echo -e "${GREEN}✅ Application démarrée avec succès !${NC}"
echo ""
echo -e "${GREEN}🎉 SAMA JOKOO NEUMORPHIQUE PRÊT !${NC}"
echo ""
echo -e "${GREEN}Informations de connexion :${NC}"
echo -e "  📱 Application : ${BLUE}http://localhost:$APP_PORT${NC}"
echo -e "  🔧 API Odoo : ${BLUE}http://localhost:$ODOO_PORT${NC}"
echo -e "  👤 Login : ${BLUE}admin${NC}"
echo -e "  🔑 Mot de passe : ${BLUE}admin${NC}"
echo ""
echo -e "${YELLOW}Fonctionnalités disponibles :${NC}"
echo -e "  ✨ Design neumorphique moderne"
echo -e "  🔐 Authentification sécurisée"
echo -e "  📱 Interface responsive"
echo -e "  🚀 Progressive Web App (PWA)"
echo -e "  🔄 Connexion temps réel avec Odoo"
echo ""
echo -e "${BLUE}Pour arrêter l'application :${NC}"
echo -e "  Ctrl+C dans ce terminal"
echo ""
echo -e "${GREEN}🎨 Profitez de votre expérience neumorphique ! ✨${NC}"

# Attendre que l'utilisateur arrête l'application
wait $APP_PID