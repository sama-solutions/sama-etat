#!/bin/bash

# Script d'ouverture directe de l'application mise à jour avec profils
# ====================================================================

echo "🎨 Ouverture de Sama Jokoo avec Profils (Version Mise à Jour)"
echo "============================================================="

# Couleurs
GREEN='\033[0;32m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
YELLOW='\033[1;33m'
NC='\033[0m'

echo -e "${BLUE}1. Vérification du fichier mis à jour...${NC}"

if [ ! -f "sama_jokoo_with_profiles.html" ]; then
    echo -e "❌ Fichier sama_jokoo_with_profiles.html manquant"
    exit 1
fi

FILE_SIZE=$(stat -c%s "sama_jokoo_with_profiles.html")
echo -e "${GREEN}✅ Fichier présent (${FILE_SIZE} bytes)${NC}"

echo -e "${BLUE}2. Création du lien d'accès...${NC}"

# Obtenir le chemin absolu
CURRENT_DIR=$(pwd)
FILE_PATH="file://${CURRENT_DIR}/sama_jokoo_with_profiles.html"

echo -e "${GREEN}✅ Chemin créé${NC}"

echo -e "${BLUE}3. Ouverture de l'application...${NC}"

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
echo -e "${PURPLE}🎨 SAMA JOKOO AVEC PROFILS - VERSION MISE À JOUR${NC}"
echo ""
echo -e "${GREEN}Nouvelles fonctionnalités :${NC}"
echo -e "  📝 ${BLUE}Feed amélioré${NC} - Posts et commentaires neumorphiques"
echo -e "  👤 ${BLUE}Profils complets${NC} - Avatar, bio, statistiques"
echo -e "  📊 ${BLUE}Statistiques détaillées${NC} - Métriques en temps réel"
echo -e "  🏆 ${BLUE}Système de badges${NC} - Réalisations et objectifs"
echo -e "  🎨 ${BLUE}Design neumorphique${NC} - Interface moderne et cohérente"
echo ""
echo -e "${GREEN}Navigation :${NC}"
echo -e "  📝 Onglet ${BLUE}Feed${NC} - Flux principal avec interactions"
echo -e "  👤 Onglet ${BLUE}Mon Profil${NC} - Informations personnelles"
echo -e "  📊 Onglet ${BLUE}Statistiques${NC} - Métriques d'activité"
echo -e "  🏆 Onglet ${BLUE}Badges${NC} - Réalisations débloquées"
echo ""

if [ "$OPENED" = true ]; then
    echo -e "${GREEN}✅ Application ouverte automatiquement dans le navigateur${NC}"
else
    echo -e "${YELLOW}⚠️ Ouverture automatique impossible${NC}"
    echo -e "${BLUE}Ouvrez manuellement le fichier dans votre navigateur :${NC}"
    echo -e "${YELLOW}${FILE_PATH}${NC}"
fi

echo ""
echo -e "${BLUE}Instructions d'utilisation :${NC}"
echo -e "  1. ${GREEN}Naviguez${NC} entre les onglets en haut de l'interface"
echo -e "  2. ${GREEN}Créez des posts${NC} dans l'onglet Feed"
echo -e "  3. ${GREEN}Consultez votre profil${NC} dans l'onglet Mon Profil"
echo -e "  4. ${GREEN}Suivez vos statistiques${NC} dans l'onglet Statistiques"
echo -e "  5. ${GREEN}Débloquez des badges${NC} en étant actif"
echo ""
echo -e "${YELLOW}Badges disponibles :${NC}"
echo -e "  🎉 Premier Post - Débloqué automatiquement"
echo -e "  ❤️ Populaire - 100 likes requis"
echo -e "  👥 Influenceur - 50 followers requis"
echo -e "  💬 Conversationnel - 50 commentaires requis"
echo -e "  🔥 En Feu - 30 posts requis"
echo -e "  ⭐ Superstar - 1000 likes requis"
echo ""

# Créer un fichier de raccourci mis à jour
cat > "Sama_Jokoo_Profils.desktop" << EOF
[Desktop Entry]
Version=1.0
Type=Application
Name=Sama Jokoo avec Profils
Comment=Application sociale neumorphique avec profils utilisateurs complets
Exec=xdg-open ${FILE_PATH}
Icon=applications-internet
Terminal=false
Categories=Network;WebBrowser;
EOF

chmod +x "Sama_Jokoo_Profils.desktop"

echo -e "${GREEN}✅ Raccourci bureau créé : Sama_Jokoo_Profils.desktop${NC}"
echo ""
echo -e "${PURPLE}🎉 L'application avec profils est prête ! Testez toutes les nouvelles fonctionnalités ! ✨${NC}"