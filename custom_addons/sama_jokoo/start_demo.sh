#!/bin/bash

# Script de démarrage de l'application en mode démo
# =================================================

echo "🎨 Démarrage de Sama Jokoo en mode démo"
echo "======================================="

# Couleurs
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m'

APP_DIR="neumorphic_app"

echo -e "${BLUE}Préparation de l'application...${NC}"

cd "$APP_DIR"

# Vérifier si les dépendances sont installées
if [ ! -d "node_modules" ]; then
    echo -e "${BLUE}Installation des dépendances...${NC}"
    npm install
    
    if [ $? -eq 0 ]; then
        echo -e "${GREEN}✅ Dépendances installées${NC}"
    else
        echo -e "${RED}❌ Erreur installation${NC}"
        exit 1
    fi
else
    echo -e "${GREEN}✅ Dépendances OK${NC}"
fi

echo ""
echo -e "${GREEN}🎉 SAMA JOKOO NEUMORPHIQUE - MODE DÉMO${NC}"
echo ""
echo -e "${GREEN}Informations :${NC}"
echo -e "  📱 Application : ${BLUE}http://localhost:3000${NC}"
echo -e "  🎭 Mode : ${BLUE}Démo avec données de test${NC}"
echo -e "  👤 Login : ${BLUE}admin${NC}"
echo -e "  🔑 Mot de passe : ${BLUE}admin${NC}"
echo ""
echo -e "${YELLOW}Fonctionnalités :${NC}"
echo -e "  ✨ Design neumorphique complet"
echo -e "  🔐 Authentification démo"
echo -e "  📱 Interface responsive"
echo -e "  🚀 Progressive Web App"
echo -e "  📊 Posts et interactions de test"
echo ""
echo -e "${BLUE}Pour arrêter : Ctrl+C${NC}"
echo ""

# Démarrer l'application
npm run dev