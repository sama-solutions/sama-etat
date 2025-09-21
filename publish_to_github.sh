#!/bin/bash
# Script de publication SAMA ÉTAT sur GitHub
# Auteurs: Mamadou Mbagnick DOGUE, Rassol DOGUE

set -e

# Couleurs pour l'affichage
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
NC='\033[0m' # No Color

# Variables
GITHUB_ORG="sama-solutions"
REPO_NAME="sama-etat"
REPO_URL="https://github.com/${GITHUB_ORG}/${REPO_NAME}.git"

# Banner
echo -e "${BLUE}"
cat << "EOF"
   ____    _    __  __    _      _____ _____  _  _____ 
  / ___|  / \  |  \/  |  / \    | ____|_   _|/ \|_   _|
  \___ \ / _ \ | |\/| | / _ \   |  _|   | | / _ \ | |  
   ___) / ___ \| |  | |/ ___ \  | |___  | |/ ___ \| |  
  |____/_/   \_\_|  |_/_/   \_\ |_____| |_/_/   \_\_|  
                                                       
  🚀 PUBLICATION SUR GITHUB 🚀
  Organisation: sama-solutions
  Repository: sama-etat
EOF
echo -e "${NC}"

echo -e "${PURPLE}Auteurs: Mamadou Mbagnick DOGUE, Rassol DOGUE${NC}"
echo ""

# Fonction de logging
log() {
    echo -e "${BLUE}[SAMA ÉTAT]${NC} $1"
}

log_success() {
    echo -e "${GREEN}[SAMA ÉTAT]${NC} $1"
}

log_warning() {
    echo -e "${YELLOW}[SAMA ÉTAT]${NC} $1"
}

log_error() {
    echo -e "${RED}[SAMA ÉTAT]${NC} $1"
}

# Vérifications préliminaires
log "🔍 Vérifications préliminaires..."

# Vérifier que nous sommes dans le bon répertoire
if [ ! -f "__manifest__.py" ]; then
    log_error "❌ Erreur: Ce script doit être exécuté depuis le répertoire sama_etat"
    exit 1
fi

# Vérifier que Git est configuré
if ! git config user.name > /dev/null 2>&1; then
    log_warning "⚠️ Configuration Git manquante"
    echo -e "${YELLOW}Veuillez configurer Git:${NC}"
    echo "git config --global user.name 'Votre Nom'"
    echo "git config --global user.email 'votre.email@example.com'"
    exit 1
fi

# Vérifier que nous avons un commit
if ! git rev-parse HEAD > /dev/null 2>&1; then
    log_error "❌ Aucun commit trouvé. Veuillez d'abord faire un commit."
    exit 1
fi

log_success "✅ Vérifications préliminaires terminées"

# Afficher les informations du repository
echo ""
log "📊 Informations du repository:"
echo -e "  ${GREEN}Organisation:${NC} ${GITHUB_ORG}"
echo -e "  ${GREEN}Repository:${NC} ${REPO_NAME}"
echo -e "  ${GREEN}URL:${NC} ${REPO_URL}"
echo -e "  ${GREEN}Branche:${NC} main"

# Afficher les statistiques du projet
echo ""
log "📈 Statistiques du projet:"
echo -e "  ${GREEN}Fichiers Python:${NC} $(find . -name "*.py" | wc -l)"
echo -e "  ${GREEN}Fichiers XML:${NC} $(find . -name "*.xml" | wc -l)"
echo -e "  ${GREEN}Fichiers de documentation:${NC} $(find . -name "*.md" | wc -l)"
echo -e "  ${GREEN}Taille totale:${NC} $(du -sh . | cut -f1)"

# Demander confirmation
echo ""
log_warning "⚠️ ATTENTION: Cette opération va publier le code sur GitHub public"
echo -e "${YELLOW}Voulez-vous continuer? (y/N)${NC}"
read -r response
if [[ ! "$response" =~ ^[Yy]$ ]]; then
    log "❌ Publication annulée"
    exit 0
fi

# Instructions pour la publication manuelle
echo ""
log "📋 INSTRUCTIONS DE PUBLICATION MANUELLE:"
echo ""
echo -e "${GREEN}1. Créer le repository sur GitHub:${NC}"
echo "   - Aller sur https://github.com/sama-solutions"
echo "   - Cliquer sur 'New repository'"
echo "   - Nom: sama-etat"
echo "   - Description: Plateforme citoyenne de gouvernance stratégique, opérationnelle et transparente"
echo "   - Public repository"
echo "   - Ne pas initialiser avec README (nous avons déjà le nôtre)"
echo ""

echo -e "${GREEN}2. Configurer le remote et pousser:${NC}"
echo "   git remote add origin ${REPO_URL}"
echo "   git branch -M main"
echo "   git push -u origin main"
echo ""

echo -e "${GREEN}3. Configurer le repository:${NC}"
echo "   - Aller dans Settings > General"
echo "   - Ajouter les topics: odoo, government, senegal, transparency, governance"
echo "   - Configurer la description et le site web"
echo "   - Activer Issues et Discussions"
echo ""

echo -e "${GREEN}4. Configurer GitHub Pages (optionnel):${NC}"
echo "   - Aller dans Settings > Pages"
echo "   - Source: Deploy from a branch"
echo "   - Branch: main / docs"
echo ""

echo -e "${GREEN}5. Configurer les secrets pour CI/CD:${NC}"
echo "   - Aller dans Settings > Secrets and variables > Actions"
echo "   - Ajouter DOCKER_USERNAME et DOCKER_PASSWORD si nécessaire"
echo "   - Ajouter SLACK_WEBHOOK pour les notifications"
echo ""

# Préparer les commandes Git
echo -e "${GREEN}6. Commandes Git à exécuter:${NC}"
echo ""
echo -e "${BLUE}# Ajouter le remote GitHub${NC}"
echo "git remote add origin ${REPO_URL}"
echo ""
echo -e "${BLUE}# Renommer la branche principale${NC}"
echo "git branch -M main"
echo ""
echo -e "${BLUE}# Pousser le code${NC}"
echo "git push -u origin main"
echo ""
echo -e "${BLUE}# Créer et pousser le tag de version${NC}"
echo "git tag -a v1.0.0 -m 'Release version 1.0.0'"
echo "git push origin v1.0.0"
echo ""

# Vérifier si le remote existe déjà
if git remote get-url origin > /dev/null 2>&1; then
    log_warning "⚠️ Remote 'origin' existe déjà:"
    git remote get-url origin
    echo ""
    echo -e "${YELLOW}Pour changer le remote:${NC}"
    echo "git remote set-url origin ${REPO_URL}"
else
    log "📡 Ajout du remote GitHub..."
    git remote add origin "${REPO_URL}"
    log_success "✅ Remote ajouté"
fi

# Renommer la branche en main
log "🔄 Renommage de la branche en 'main'..."
git branch -M main
log_success "✅ Branche renommée"

# Afficher le statut final
echo ""
log "📊 Statut final du repository:"
git status --short
echo ""

log_success "🎉 Repository prêt pour la publication!"
echo ""
echo -e "${GREEN}Prochaines étapes:${NC}"
echo "1. Créer le repository sur https://github.com/sama-solutions"
echo "2. Exécuter: git push -u origin main"
echo "3. Créer la première release v1.0.0"
echo "4. Configurer les paramètres du repository"
echo ""

log "🚀 SAMA ÉTAT est prêt à transformer la gouvernance publique au Sénégal!"
echo -e "${PURPLE}Fait avec ❤️ par Mamadou Mbagnick DOGUE et Rassol DOGUE${NC}"