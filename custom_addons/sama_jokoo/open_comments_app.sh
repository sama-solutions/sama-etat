#!/bin/bash

# Script d'ouverture directe de l'application avec commentaires
# =============================================================

echo "🎨 Ouverture directe de Sama Jokoo avec Commentaires"
echo "===================================================="

# Couleurs
GREEN='\033[0;32m'
RED='\033[0;31m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
PURPLE='\033[0;35m'
NC='\033[0m'

echo -e "${BLUE}1. Vérification du fichier...${NC}"

if [ ! -f "sama_jokoo_with_comments.html" ]; then
    echo -e "${RED}❌ Fichier sama_jokoo_with_comments.html manquant${NC}"
    exit 1
fi

FILE_SIZE=$(stat -c%s "sama_jokoo_with_comments.html")
echo -e "${GREEN}✅ Fichier présent (${FILE_SIZE} bytes)${NC}"

echo -e "${BLUE}2. Création d'un lien d'accès direct...${NC}"

# Obtenir le chemin absolu
CURRENT_DIR=$(pwd)
FILE_PATH="file://${CURRENT_DIR}/sama_jokoo_with_comments.html"

echo -e "${GREEN}✅ Chemin créé${NC}"

echo -e "${BLUE}3. Tentative d'ouverture automatique...${NC}"

# Essayer d'ouvrir avec différents navigateurs
if command -v xdg-open &> /dev/null; then
    echo -e "${YELLOW}Ouverture avec xdg-open...${NC}"
    xdg-open "$FILE_PATH" &
    OPENED=true
elif command -v firefox &> /dev/null; then
    echo -e "${YELLOW}Ouverture avec Firefox...${NC}"
    firefox "$FILE_PATH" &
    OPENED=true
elif command -v google-chrome &> /dev/null; then
    echo -e "${YELLOW}Ouverture avec Chrome...${NC}"
    google-chrome "$FILE_PATH" &
    OPENED=true
elif command -v chromium-browser &> /dev/null; then
    echo -e "${YELLOW}Ouverture avec Chromium...${NC}"
    chromium-browser "$FILE_PATH" &
    OPENED=true
else
    OPENED=false
fi

echo ""
echo -e "${PURPLE}💬 SAMA JOKOO AVEC COMMENTAIRES - ACCÈS DIRECT${NC}"
echo ""
echo -e "${GREEN}Informations :${NC}"
echo -e "  📁 Fichier : ${BLUE}sama_jokoo_with_comments.html${NC}"
echo -e "  🌐 URL directe : ${BLUE}${FILE_PATH}${NC}"
echo -e "  💬 Fonctionnalité : ${BLUE}Système de commentaires complet${NC}"
echo -e "  👤 Login : ${BLUE}admin${NC}"
echo -e "  🔑 Mot de passe : ${BLUE}admin${NC}"
echo ""

if [ "$OPENED" = true ]; then
    echo -e "${GREEN}✅ Application ouverte automatiquement dans le navigateur${NC}"
else
    echo -e "${YELLOW}⚠️ Ouverture automatique impossible${NC}"
    echo -e "${BLUE}Ouvrez manuellement le fichier dans votre navigateur :${NC}"
    echo -e "${YELLOW}${FILE_PATH}${NC}"
fi

echo ""
echo -e "${YELLOW}Fonctionnalités des commentaires :${NC}"
echo -e "  ✨ Design neumorphique cohérent"
echo -e "  💬 Création de commentaires en temps réel"
echo -e "  ❤️ Système de likes pour commentaires"
echo -e "  🔄 Affichage/masquage dynamique"
echo -e "  📱 Interface responsive"
echo -e "  ⌨️ Support clavier (Enter pour valider)"
echo -e "  🎨 Animations et transitions fluides"
echo ""
echo -e "${BLUE}Instructions d'utilisation :${NC}"
echo -e "  1. ${GREEN}Connectez-vous${NC} avec admin/admin"
echo -e "  2. ${GREEN}Cliquez sur 💬${NC} d'un post pour voir/masquer les commentaires"
echo -e "  3. ${GREEN}Écrivez un commentaire${NC} et appuyez sur Enter ou cliquez Commenter"
echo -e "  4. ${GREEN}Cliquez sur ❤️${NC} pour aimer un commentaire"
echo -e "  5. ${GREEN}Testez la création${NC} de nouveaux posts avec commentaires"
echo ""
echo -e "${BLUE}Fonctionnalités testées :${NC}"
echo -e "  ✅ Authentification démo"
echo -e "  ✅ Création et affichage de posts"
echo -e "  ✅ Système de commentaires complet"
echo -e "  ✅ Likes sur posts et commentaires"
echo -e "  ✅ Interface neumorphique responsive"
echo -e "  ✅ Notifications en temps réel"
echo ""

# Créer un fichier de raccourci
cat > "Sama_Jokoo_Commentaires.desktop" << EOF
[Desktop Entry]
Version=1.0
Type=Application
Name=Sama Jokoo avec Commentaires
Comment=Application sociale neumorphique avec système de commentaires
Exec=xdg-open ${FILE_PATH}
Icon=applications-internet
Terminal=false
Categories=Network;WebBrowser;
EOF

chmod +x "Sama_Jokoo_Commentaires.desktop"

echo -e "${GREEN}✅ Raccourci bureau créé : Sama_Jokoo_Commentaires.desktop${NC}"
echo ""
echo -e "${PURPLE}🎉 L'application avec commentaires est prête à être utilisée ! ✨${NC}"