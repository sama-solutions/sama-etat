#!/bin/bash

# Script de démarrage robuste pour Sama Jokoo
# ===========================================

echo "🎨 Démarrage robuste de Sama Jokoo"
echo "=================================="

# Couleurs
GREEN='\033[0;32m'
RED='\033[0;31m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m'

# Fonction de nettoyage
cleanup() {
    echo -e "\n${BLUE}Arrêt en cours...${NC}"
    pkill -f "node simple_server.js" 2>/dev/null
    pkill -f "vite" 2>/dev/null
    exit 0
}

# Capturer Ctrl+C
trap cleanup SIGINT SIGTERM

echo -e "${BLUE}1. Nettoyage des processus existants...${NC}"
pkill -f "node simple_server.js" 2>/dev/null
pkill -f "vite" 2>/dev/null
sleep 2

echo -e "${BLUE}2. Vérification de Node.js...${NC}"
if ! command -v node &> /dev/null; then
    echo -e "${RED}❌ Node.js non trouvé${NC}"
    exit 1
fi

NODE_VERSION=$(node --version)
echo -e "${GREEN}✅ Node.js: $NODE_VERSION${NC}"

echo -e "${BLUE}3. Démarrage du serveur de test...${NC}"

# Démarrer le serveur simple en arrière-plan
node simple_server.js &
SERVER_PID=$!

# Attendre que le serveur démarre
sleep 3

# Vérifier si le serveur fonctionne
if kill -0 $SERVER_PID 2>/dev/null; then
    echo -e "${GREEN}✅ Serveur démarré (PID: $SERVER_PID)${NC}"
    
    # Tester la connexion
    if curl -s http://localhost:3000 >/dev/null 2>&1; then
        echo -e "${GREEN}✅ Serveur accessible${NC}"
    else
        echo -e "${YELLOW}⚠️ Serveur démarré mais pas encore accessible${NC}"
    fi
else
    echo -e "${RED}❌ Échec du démarrage${NC}"
    exit 1
fi

echo ""
echo -e "${GREEN}🎉 SAMA JOKOO FONCTIONNEL !${NC}"
echo ""
echo -e "${GREEN}Informations :${NC}"
echo -e "  📱 URL: ${BLUE}http://localhost:3000${NC}"
echo -e "  🎯 Type: ${BLUE}Serveur de test neumorphique${NC}"
echo -e "  🔧 Serveur: ${BLUE}Node.js simple${NC}"
echo -e "  📊 PID: ${BLUE}$SERVER_PID${NC}"
echo ""
echo -e "${YELLOW}Fonctionnalités :${NC}"
echo -e "  ✨ Design neumorphique"
echo -e "  🎨 Interface de test"
echo -e "  🔄 API de test"
echo -e "  📱 Responsive design"
echo ""
echo -e "${BLUE}Pour arrêter : Ctrl+C${NC}"
echo ""

# Attendre que le serveur se termine
wait $SERVER_PID