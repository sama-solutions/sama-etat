#!/bin/bash

# Script de redémarrage forcé de l'application
# ============================================

echo "🔄 Redémarrage de Sama Jokoo"
echo "============================"

# Couleurs
GREEN='\033[0;32m'
RED='\033[0;31m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m'

echo -e "${BLUE}1. Arrêt des processus existants...${NC}"

# Tuer tous les processus Vite/Node liés à l'application
pkill -f "vite" 2>/dev/null
pkill -f "sama-jokoo-neumorphic" 2>/dev/null
pkill -f "node_modules/.bin/vite" 2>/dev/null

# Attendre que les processus se terminent
sleep 2

echo -e "${GREEN}✅ Processus arrêtés${NC}"

echo -e "${BLUE}2. Vérification des ports...${NC}"

# Libérer les ports si nécessaire
for port in 3000 3001 3002; do
    PID=$(lsof -ti:$port 2>/dev/null)
    if [ ! -z "$PID" ]; then
        echo -e "${YELLOW}Port $port occupé par PID $PID, libération...${NC}"
        kill -9 $PID 2>/dev/null
    fi
done

echo -e "${GREEN}✅ Ports libérés${NC}"

echo -e "${BLUE}3. Démarrage de l'application...${NC}"

cd neumorphic_app

# Choisir un port libre
PORT=3000
for test_port in 3000 3001 3002 3003; do
    if ! lsof -i:$test_port >/dev/null 2>&1; then
        PORT=$test_port
        break
    fi
done

echo -e "${GREEN}🚀 Démarrage sur le port $PORT...${NC}"
echo ""
echo -e "${GREEN}🎉 SAMA JOKOO NEUMORPHIQUE${NC}"
echo ""
echo -e "${GREEN}Informations :${NC}"
echo -e "  📱 Application : ${BLUE}http://localhost:$PORT${NC}"
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

# Démarrer l'application sur le port choisi
npm run dev -- --port $PORT