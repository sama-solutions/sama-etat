#!/bin/bash
# Script d'upload SAMA ÉTAT vers GitHub (sans workflow)
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

# Banner
echo -e "${BLUE}"
cat << "EOF"
   ____    _    __  __    _      _____ _____  _  _____ 
  / ___|  / \  |  \/  |  / \    | ____|_   _|/ \|_   _|
  \___ \ / _ \ | |\/| | / _ \   |  _|   | | / _ \ | |  
   ___) / ___ \| |  | |/ ___ \  | |___  | |/ ___ \| |  
  |____/_/   \_\_|  |_/_/   \_\ |_____| |_/_/   \_\_|  
                                                       
  🚀 UPLOAD VERS GITHUB (SANS WORKFLOW) 🚀
EOF
echo -e "${NC}"

echo -e "${PURPLE}Auteurs: Mamadou Mbagnick DOGUE, Rassol DOGUE${NC}"
echo -e "${CYAN}Organisation: ${GITHUB_ORG}${NC}"
echo -e "${CYAN}Repository: ${REPO_NAME}${NC}"
echo ""

# Fonction de logging
log_success() {
    echo -e "${GREEN}[SAMA ÉTAT]${NC} ✅ $1"
}

log_error() {
    echo -e "${RED}[SAMA ÉTAT]${NC} ❌ $1"
}

log_info() {
    echo -e "${CYAN}[SAMA ÉTAT]${NC} ℹ️ $1"
}

# Vérifications
if [ ! -f "__manifest__.py" ]; then
    log_error "Ce script doit être exécuté depuis le répertoire sama_etat"
    exit 1
fi

log_info "🔧 Workflow GitHub Actions temporairement désactivé pour résoudre les permissions OAuth"
log_info "📤 Upload du code principal vers GitHub..."

# Upload vers GitHub
if git push -u origin main; then
    log_success "Code uploadé avec succès sur la branche main"
else
    log_error "Échec de l'upload du code"
    exit 1
fi

# Créer et pousser le tag
log_info "🏷️ Création du tag de version v1.0.0..."
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
- PostgreSQL, Docker
- Tests automatisés et outils de qualité

🌍 Impact:
- Transparence totale des projets et budgets publics
- Participation citoyenne active et éclairée
- Efficacité gouvernementale décuplée
- Modèle pour l'Afrique entière

👥 Auteurs: Mamadou Mbagnick DOGUE, Rassol DOGUE
🇸🇳 Fait avec ❤️ au Sénégal pour une République transparente

Note: GitHub Actions workflow sera ajouté ultérieurement avec les bonnes permissions."; then
    log_success "Tag v1.0.0 créé"
else
    log_info "Tag v1.0.0 existe déjà ou erreur de création"
fi

if git push origin v1.0.0; then
    log_success "Tag v1.0.0 uploadé avec succès"
else
    log_info "Tag existe déjà sur GitHub"
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
echo -e "${GREEN}║                                                              ║${NC}"
echo -e "${GREEN}║ 🇸🇳 Fait avec ❤️ au Sénégal                                 ║${NC}"
echo -e "${GREEN}╚══════════════════════════════════════════════════════════════╝${NC}"

echo ""
log_success "🎯 Prochaines étapes:"
echo ""
echo -e "${CYAN}1. Restaurer le workflow GitHub Actions:${NC}"
echo "   • Aller dans les paramètres du repository"
echo "   • Activer GitHub Actions"
echo "   • Restaurer le fichier depuis archive_files/ci.yml"
echo ""
echo -e "${CYAN}2. Configuration du repository:${NC}"
echo "   • Ajouter la description et les topics"
echo "   • Activer Issues, Discussions, Wiki"
echo ""
echo -e "${CYAN}3. Topics recommandés:${NC}"
echo "   odoo, government, senegal, transparency, governance, public-sector"
echo ""

log_success "🚀 SAMA ÉTAT est maintenant public et prêt à transformer la gouvernance !"
echo -e "${PURPLE}Auteurs: Mamadou Mbagnick DOGUE, Rassol DOGUE${NC}"
echo -e "${CYAN}🇸🇳 Transformons ensemble la gouvernance publique au Sénégal ! 🇸🇳${NC}"

exit 0