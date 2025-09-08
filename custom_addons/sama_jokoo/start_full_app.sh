#!/bin/bash

# Script de démarrage de l'application Vue.js complète
# ====================================================

echo "🎨 Démarrage de l'application Sama Jokoo complète"
echo "================================================="

# Couleurs
GREEN='\033[0;32m'
RED='\033[0;31m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m'

# Fonction de nettoyage
cleanup() {
    echo -e "\n${BLUE}Arrêt de l'application...${NC}"
    pkill -f "node simple_server.js" 2>/dev/null
    pkill -f "vite" 2>/dev/null
    exit 0
}

# Capturer Ctrl+C
trap cleanup SIGINT SIGTERM

echo -e "${BLUE}1. Arrêt du serveur de test...${NC}"
pkill -f "node simple_server.js" 2>/dev/null
sleep 2

echo -e "${BLUE}2. Préparation de l'application Vue.js...${NC}"

cd neumorphic_app

# Vérifier les dépendances
if [ ! -d "node_modules" ]; then
    echo -e "${BLUE}Installation des dépendances...${NC}"
    npm install
fi

echo -e "${GREEN}✅ Dépendances prêtes${NC}"

echo -e "${BLUE}3. Démarrage de l'application neumorphique complète...${NC}"

# Choisir un port libre
PORT=3000
for test_port in 3000 3001 3002; do
    if ! lsof -i:$test_port >/dev/null 2>&1; then
        PORT=$test_port
        break
    fi
done

echo ""
echo -e "${GREEN}🎉 SAMA JOKOO NEUMORPHIQUE COMPLET${NC}"
echo ""
echo -e "${GREEN}Informations :${NC}"
echo -e "  📱 Application : ${BLUE}http://localhost:$PORT${NC}"
echo -e "  🎭 Mode : ${BLUE}Démo avec données sociales${NC}"
echo -e "  👤 Login : ${BLUE}admin${NC}"
echo -e "  🔑 Mot de passe : ${BLUE}admin${NC}"
echo ""
echo -e "${YELLOW}Fonctionnalités complètes :${NC}"
echo -e "  ✨ Design neumorphique moderne"
echo -e "  🔐 Authentification démo"
echo -e "  📱 Interface responsive"
echo -e "  🚀 Progressive Web App"
echo -e "  📊 Feed des posts sociaux"
echo -e "  ❤️ Système de likes"
echo -e "  💬 Commentaires"
echo -e "  ➕ Création de posts"
echo ""
echo -e "${BLUE}Pour arrêter : Ctrl+C${NC}"
echo ""

# Démarrer l'application Vue.js
npm run dev -- --port $PORT