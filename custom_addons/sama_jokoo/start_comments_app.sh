#!/bin/bash

# Script de démarrage rapide pour l'application avec commentaires
# ==============================================================

echo "💬 Démarrage de Sama Jokoo avec Système de Commentaires"
echo "========================================================"

# Couleurs
GREEN='\033[0;32m'
RED='\033[0;31m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
PURPLE='\033[0;35m'
NC='\033[0m'

echo -e "${BLUE}1. Arrêt des processus existants...${NC}"
pkill -f "serve_app.py" 2>/dev/null
pkill -f "serve_comments_app.py" 2>/dev/null
pkill -f "python3 serve" 2>/dev/null
sleep 2

echo -e "${BLUE}2. Vérification des fichiers...${NC}"

if [ ! -f "sama_jokoo_with_comments.html" ]; then
    echo -e "${RED}❌ Fichier sama_jokoo_with_comments.html manquant${NC}"
    exit 1
fi

if [ ! -f "serve_comments_app.py" ]; then
    echo -e "${RED}❌ Fichier serve_comments_app.py manquant${NC}"
    exit 1
fi

echo -e "${GREEN}✅ Fichiers présents${NC}"

echo -e "${BLUE}3. Démarrage du serveur avec commentaires...${NC}"

echo ""
echo -e "${PURPLE}💬 SAMA JOKOO AVEC COMMENTAIRES${NC}"
echo ""
echo -e "${GREEN}Informations :${NC}"
echo -e "  📱 Application : ${BLUE}http://localhost:3000${NC}"
echo -e "  💬 Fonctionnalité : ${BLUE}Système de commentaires complet${NC}"
echo -e "  👤 Login : ${BLUE}admin${NC}"
echo -e "  🔑 Mot de passe : ${BLUE}admin${NC}"
echo ""
echo -e "${YELLOW}Fonctionnalités des commentaires :${NC}"
echo -e "  ✨ Design neumorphique cohérent"
echo -e "  💬 Création de commentaires"
echo -e "  ❤️ Likes sur commentaires"
echo -e "  🔄 Affichage/masquage dynamique"
echo -e "  📱 Interface responsive"
echo -e "  ⌨️ Support clavier (Enter)"
echo ""
echo -e "${BLUE}Instructions d'utilisation :${NC}"
echo -e "  1. Connectez-vous avec admin/admin"
echo -e "  2. Cliquez sur 💬 d'un post pour voir/masquer les commentaires"
echo -e "  3. Écrivez un commentaire et appuyez sur Enter ou cliquez Commenter"
echo -e "  4. Cliquez sur ❤️ pour aimer un commentaire"
echo ""
echo -e "${BLUE}Pour arrêter : Ctrl+C${NC}"
echo ""

# Démarrer le serveur
python3 serve_comments_app.py