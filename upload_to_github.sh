#!/bin/bash
# Script d'upload SAMA ÉTAT vers GitHub sama-solutions
# Auteurs: Mamadou Mbagnick DOGUE, Rassol DOGUE

set -e

# Couleurs pour l'affichage
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# Variables
GITHUB_ORG="sama-solutions"
REPO_NAME="sama-etat"
REPO_URL="https://github.com/${GITHUB_ORG}/${REPO_NAME}.git"
CURRENT_DIR=$(pwd)

# Banner
echo -e "${BLUE}"
cat << "EOF"
   ____    _    __  __    _      _____ _____  _  _____ 
  / ___|  / \  |  \/  |  / \    | ____|_   _|/ \|_   _|
  \___ \ / _ \ | |\/| | / _ \   |  _|   | | / _ \ | |  
   ___) / ___ \| |  | |/ ___ \  | |___  | |/ ___ \| |  
  |____/_/   \_\_|  |_/_/   \_\ |_____| |_/_/   \_\_|  
                                                       
  🚀 UPLOAD VERS GITHUB 🚀
EOF
echo -e "${NC}"

echo -e "${PURPLE}Auteurs: Mamadou Mbagnick DOGUE, Rassol DOGUE${NC}"
echo -e "${CYAN}Organisation: ${GITHUB_ORG}${NC}"
echo -e "${CYAN}Repository: ${REPO_NAME}${NC}"
echo ""

# Fonction de logging
log() {
    echo -e "${BLUE}[SAMA ÉTAT]${NC} $1"
}

log_success() {
    echo -e "${GREEN}[SAMA ÉTAT]${NC} ✅ $1"
}

log_warning() {
    echo -e "${YELLOW}[SAMA ÉTAT]${NC} ⚠️ $1"
}

log_error() {
    echo -e "${RED}[SAMA ÉTAT]${NC} ❌ $1"
}

log_info() {
    echo -e "${CYAN}[SAMA ÉTAT]${NC} ℹ️ $1"
}

# Vérifications préliminaires
log "🔍 Vérifications préliminaires..."

# Vérifier que nous sommes dans le bon répertoire
if [ ! -f "__manifest__.py" ]; then
    log_error "Ce script doit être exécuté depuis le répertoire sama_etat"
    echo -e "${YELLOW}Usage: cd sama_etat && ./upload_to_github.sh${NC}"
    exit 1
fi

# Vérifier que Git est configuré
if ! git config user.name > /dev/null 2>&1; then
    log_warning "Configuration Git manquante"
    echo -e "${YELLOW}Configuration automatique...${NC}"
    git config user.name "Mamadou Mbagnick & Rassol DOGUE"
    git config user.email "contact@sama-etat.sn"
    log_success "Configuration Git mise à jour"
fi

# Vérifier que nous avons des commits
if ! git rev-parse HEAD > /dev/null 2>&1; then
    log_error "Aucun commit trouvé dans le repository"
    exit 1
fi

log_success "Vérifications préliminaires terminées"

# Afficher les informations du repository
echo ""
log_info "📊 Informations du repository:"
echo -e "  ${GREEN}Organisation:${NC} ${GITHUB_ORG}"
echo -e "  ${GREEN}Repository:${NC} ${REPO_NAME}"
echo -e "  ${GREEN}URL:${NC} ${REPO_URL}"
echo -e "  ${GREEN}Branche locale:${NC} $(git branch --show-current)"

# Afficher les statistiques du projet
echo ""
log_info "📈 Statistiques du projet:"
COMMIT_COUNT=$(git rev-list --count HEAD)
PYTHON_FILES=$(find . -name "*.py" | wc -l)
XML_FILES=$(find . -name "*.xml" | wc -l)
MD_FILES=$(find . -name "*.md" | wc -l)
TOTAL_SIZE=$(du -sh . | cut -f1)

echo -e "  ${GREEN}Commits:${NC} ${COMMIT_COUNT}"
echo -e "  ${GREEN}Fichiers Python:${NC} ${PYTHON_FILES}"
echo -e "  ${GREEN}Fichiers XML:${NC} ${XML_FILES}"
echo -e "  ${GREEN}Fichiers Markdown:${NC} ${MD_FILES}"
echo -e "  ${GREEN}Taille totale:${NC} ${TOTAL_SIZE}"

# Afficher les derniers commits
echo ""
log_info "📝 Derniers commits:"
git log --oneline -5 | while read line; do
    echo -e "  ${CYAN}${line}${NC}"
done

# Vérifier si le remote existe déjà
echo ""
log "🔗 Vérification du remote GitHub..."

if git remote get-url origin > /dev/null 2>&1; then
    CURRENT_REMOTE=$(git remote get-url origin)
    if [ "$CURRENT_REMOTE" = "$REPO_URL" ]; then
        log_success "Remote GitHub déjà configuré correctement"
    else
        log_warning "Remote existant différent: $CURRENT_REMOTE"
        echo -e "${YELLOW}Mise à jour du remote...${NC}"
        git remote set-url origin "$REPO_URL"
        log_success "Remote mis à jour vers $REPO_URL"
    fi
else
    log "Ajout du remote GitHub..."
    git remote add origin "$REPO_URL"
    log_success "Remote GitHub ajouté"
fi

# Renommer la branche en main
log "🔄 Préparation de la branche principale..."
CURRENT_BRANCH=$(git branch --show-current)
if [ "$CURRENT_BRANCH" != "main" ]; then
    git branch -M main
    log_success "Branche renommée de '$CURRENT_BRANCH' vers 'main'"
else
    log_success "Branche 'main' déjà configurée"
fi

# Demander confirmation pour l'upload
echo ""
echo -e "${YELLOW}╔══════════════════════════════════════════════════════════════╗${NC}"
echo -e "${YELLOW}║                    ⚠️  CONFIRMATION REQUISE  ⚠️                ║${NC}"
echo -e "${YELLOW}╠══════════════════════════════════════════════════════════════╣${NC}"
echo -e "${YELLOW}║ Cette opération va publier SAMA ÉTAT sur GitHub public      ║${NC}"
echo -e "${YELLOW}║                                                              ║${NC}"
echo -e "${YELLOW}║ Organisation: sama-solutions                                 ║${NC}"
echo -e "${YELLOW}║ Repository: sama-etat                                       ║${NC}"
echo -e "${YELLOW}║ Commits: ${COMMIT_COUNT} commits prêts à être publiés                    ║${NC}"
echo -e "${YELLOW}║                                                              ║${NC}"
echo -e "${YELLOW}║ ⚠️  ASSUREZ-VOUS QUE LE REPOSITORY GITHUB EXISTE DÉJÀ !     ║${NC}"
echo -e "${YELLOW}╚══════════════════════════════════════════════════════════════╝${NC}"
echo ""
echo -e "${CYAN}Voulez-vous continuer avec l'upload ? (y/N)${NC}"
read -r response

if [[ ! "$response" =~ ^[Yy]$ ]]; then
    log "❌ Upload annulé par l'utilisateur"
    echo ""
    log_info "💡 Pour créer le repository GitHub d'abord:"
    echo "   1. Aller sur https://github.com/sama-solutions"
    echo "   2. Cliquer sur 'New repository'"
    echo "   3. Nom: sama-etat"
    echo "   4. Description: Plateforme citoyenne de gouvernance stratégique, opérationnelle et transparente"
    echo "   5. Public, sans initialisation"
    echo ""
    exit 0
fi

# Upload vers GitHub
echo ""
log "🚀 Démarrage de l'upload vers GitHub..."

# Push du code
log "📤 Upload du code vers GitHub..."
if git push -u origin main; then
    log_success "Code uploadé avec succès sur la branche main"
else
    log_error "Échec de l'upload du code"
    echo ""
    log_info "💡 Solutions possibles:"
    echo "   1. Vérifier que le repository GitHub existe"
    echo "   2. Vérifier vos permissions sur sama-solutions"
    echo "   3. Vérifier votre authentification GitHub"
    exit 1
fi

# Créer et pousser le tag de version
log "🏷️ Création du tag de version v1.0.0..."
if git tag -a v1.0.0 -m "🎉 SAMA ÉTAT v1.0.0 - Initial Release

✨ Plateforme citoyenne de gouvernance stratégique pour le Sénégal

🏛️ Fonctionnalités principales:
- Gestion complète des projets gouvernementaux
- Tableau de bord stratégique Plan Sénégal 2050
- Carte interactive des 14 régions du Sénégal
- Interface publique pour la transparence citoyenne
- Documentation bilingue français/anglais

🔧 Technologies:
- Odoo 18.0 avec Python 3.8+
- PostgreSQL, Docker, GitHub Actions CI/CD
- Tests automatisés et outils de qualité

🌍 Impact:
- Transparence totale des projets et budgets publics
- Participation citoyenne active et éclairée
- Efficacité gouvernementale décuplée
- Modèle pour l'Afrique entière

👥 Auteurs: Mamadou Mbagnick DOGUE, Rassol DOGUE
🇸🇳 Fait avec ❤️ au Sénégal pour une République transparente"; then
    log_success "Tag v1.0.0 créé"
else
    log_warning "Tag v1.0.0 existe déjà ou erreur de création"
fi

log "📤 Upload du tag vers GitHub..."
if git push origin v1.0.0; then
    log_success "Tag v1.0.0 uploadé avec succès"
else
    log_warning "Échec de l'upload du tag (peut-être existe déjà)"
fi

# Afficher le résumé final
echo ""
echo -e "${GREEN}╔══════════════════════════════════════════════════════════════╗${NC}"
echo -e "${GREEN}║                    🎉 UPLOAD RÉUSSI ! 🎉                     ║${NC}"
echo -e "${GREEN}╠══════════════════════════════════════════════════════════════╣${NC}"
echo -e "${GREEN}║ SAMA ÉTAT a été uploadé avec succès sur GitHub !            ║${NC}"
echo -e "${GREEN}║                                                              ║${NC}"
echo -e "${GREEN}║ 🌐 URL: https://github.com/sama-solutions/sama-etat         ║${NC}"
echo -e "${GREEN}║ 📦 Release: v1.0.0                                          ║${NC}"
echo -e "${GREEN}║ 📊 Commits: ${COMMIT_COUNT} commits publiés                              ║${NC}"
echo -e "${GREEN}║                                                              ║${NC}"
echo -e "${GREEN}║ 🇸🇳 Fait avec ❤️ au Sénégal                                 ║${NC}"
echo -e "${GREEN}╚══════════════════════════════════════════════════════════════╝${NC}"

echo ""
log_success "🎯 Prochaines étapes recommandées:"
echo ""
echo -e "${CYAN}1. Configuration du repository GitHub:${NC}"
echo "   • Aller sur https://github.com/sama-solutions/sama-etat"
echo "   • Ajouter la description et les topics"
echo "   • Activer Issues, Discussions, Wiki"
echo "   • Configurer GitHub Pages (optionnel)"
echo ""
echo -e "${CYAN}2. Topics recommandés:${NC}"
echo "   odoo, government, senegal, transparency, governance, public-sector"
echo ""
echo -e "${CYAN}3. Configuration avancée:${NC}"
echo "   • Secrets pour CI/CD (DOCKER_USERNAME, DOCKER_PASSWORD)"
echo "   • Labels et milestones selon GITHUB_SETUP.md"
echo "   • Protection de la branche main"
echo ""
echo -e "${CYAN}4. Promotion:${NC}"
echo "   • Partager sur les réseaux sociaux"
echo "   • Contacter la communauté Odoo"
echo "   • Présenter aux institutions sénégalaises"
echo ""

log_success "🚀 SAMA ÉTAT est maintenant public et prêt à transformer la gouvernance !"
echo -e "${PURPLE}Auteurs: Mamadou Mbagnick DOGUE, Rassol DOGUE${NC}"
echo -e "${CYAN}🇸🇳 Transformons ensemble la gouvernance publique au Sénégal ! 🇸🇳${NC}"

exit 0