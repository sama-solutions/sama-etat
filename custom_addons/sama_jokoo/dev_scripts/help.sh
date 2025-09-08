#!/bin/bash

# Script d'aide pour Sama Jokoo
# =============================

# Couleurs
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
CYAN='\033[0;36m'
NC='\033[0m'

print_header() {
    echo -e "${BLUE}"
    echo "╔══════════════════════════════════════════════════════════════════════════════╗"
    echo "║                           🚀 SAMA JOKOO - AIDE                              ║"
    echo "║                     Application Sociale pour Odoo 18 CE                     ║"
    echo "╚══════════════════════════════════════════════════════════════════════════════╝"
    echo -e "${NC}"
}

print_section() {
    echo -e "\n${CYAN}▶ $1${NC}"
    echo -e "${CYAN}$(printf '─%.0s' {1..80})${NC}"
}

print_command() {
    echo -e "  ${GREEN}$1${NC} - $2"
}

print_info() {
    echo -e "  ${YELLOW}ℹ${NC} $1"
}

print_warning() {
    echo -e "  ${RED}⚠${NC} $1"
}

show_help() {
    print_header
    
    print_section "SCRIPTS DE DÉVELOPPEMENT"
    print_command "./start_dev.sh" "Démarre Odoo en mode développement (port 8070)"
    print_command "./stop_dev.sh" "Arrête le serveur de développement"
    print_command "./restart_dev.sh" "Redémarre le serveur de développement"
    print_command "./watch_logs.sh" "Surveille les logs en temps réel avec coloration"
    print_command "./test_module.sh" "Lance tous les tests du module"
    print_command "./debug_cycle.sh" "Cycle automatique de débogage et correction"
    
    print_section "SCRIPTS DE PRODUCTION"
    print_command "../start_sama_jokoo.sh" "Démarre Sama Jokoo en production (port 8071)"
    print_command "../stop_sama_jokoo.sh" "Arrête Sama Jokoo en production"
    print_command "../restart_sama_jokoo.sh" "Redémarre Sama Jokoo en production"
    
    print_section "DÉVELOPPEMENT MOBILE"
    print_command "../mobile_app/start_mobile_dev.sh" "Initialise et démarre l'application mobile Flutter"
    
    print_section "CONFIGURATION ACTUELLE"
    print_info "Odoo Path: /var/odoo/odoo18"
    print_info "Virtual Env: /home/grand-as/odoo18-venv"
    print_info "Custom Addons: /home/grand-as/psagsn/custom_addons"
    print_info "Port Dev: 8070 | Port Prod: 8071"
    print_info "DB Dev: sama_jokoo_dev | DB Prod: sama_jokoo_prod"
    
    print_section "WORKFLOW RECOMMANDÉ"
    echo -e "  ${PURPLE}1.${NC} Démarrage initial:"
    echo -e "     ${GREEN}./start_dev.sh${NC}"
    echo -e "  ${PURPLE}2.${NC} Surveillance des logs (nouveau terminal):"
    echo -e "     ${GREEN}./watch_logs.sh${NC}"
    echo -e "  ${PURPLE}3.${NC} Tests et débogage:"
    echo -e "     ${GREEN}./debug_cycle.sh${NC}"
    echo -e "  ${PURPLE}4.${NC} Développement mobile:"
    echo -e "     ${GREEN}../mobile_app/start_mobile_dev.sh${NC}"
    
    print_section "DÉPANNAGE RAPIDE"
    print_command "ps aux | grep odoo" "Voir les processus Odoo actifs"
    print_command "lsof -i :8070" "Vérifier le port de développement"
    print_command "lsof -i :8071" "Vérifier le port de production"
    print_command "tail -f logs/odoo_dev.log" "Voir les derniers logs"
    print_command "grep ERROR logs/odoo_dev.log" "Chercher les erreurs dans les logs"
    
    print_section "URLS D'ACCÈS"
    print_info "Développement: http://localhost:8070"
    print_info "Production: http://localhost:8071"
    print_info "Login: admin | Password: admin123"
    
    print_section "FICHIERS IMPORTANTS"
    print_info "Logs dev: dev_scripts/logs/odoo_dev.log"
    print_info "Logs prod: logs/sama_jokoo.log"
    print_info "Config: dev_scripts/config.sh"
    print_info "Documentation: dev_scripts/README.md"
    
    print_section "COMMANDES UTILES"
    print_command "./help.sh status" "Afficher l'état des services"
    print_command "./help.sh clean" "Nettoyer les fichiers temporaires"
    print_command "./help.sh reset" "Réinitialiser complètement l'environnement"
    
    print_warning "En cas de problème, lancez d'abord: ./debug_cycle.sh"
    
    echo -e "\n${GREEN}✨ Sama Jokoo - Développement simplifié ! ✨${NC}\n"
}

show_status() {
    print_header
    print_section "ÉTAT DES SERVICES"
    
    # Vérifier les processus Odoo
    DEV_PID=$(lsof -ti:8070 2>/dev/null)
    PROD_PID=$(lsof -ti:8071 2>/dev/null)
    
    if [ ! -z "$DEV_PID" ]; then
        echo -e "  ${GREEN}✓${NC} Développement actif (PID: $DEV_PID, Port: 8070)"
    else
        echo -e "  ${RED}✗${NC} Développement arrêté"
    fi
    
    if [ ! -z "$PROD_PID" ]; then
        echo -e "  ${GREEN}✓${NC} Production active (PID: $PROD_PID, Port: 8071)"
    else
        echo -e "  ${RED}✗${NC} Production arrêtée"
    fi
    
    # Vérifier PostgreSQL
    if PGPASSWORD=odoo psql -h localhost -p 5432 -U odoo -d postgres -c '\q' 2>/dev/null; then
        echo -e "  ${GREEN}✓${NC} PostgreSQL accessible"
    else
        echo -e "  ${RED}✗${NC} PostgreSQL non accessible"
    fi
    
    # Vérifier l'environnement virtuel
    if [ -f "/home/grand-as/odoo18-venv/bin/activate" ]; then
        echo -e "  ${GREEN}✓${NC} Environnement virtuel trouvé"
    else
        echo -e "  ${RED}✗${NC} Environnement virtuel non trouvé"
    fi
    
    # Vérifier les bases de données
    if PGPASSWORD=odoo psql -h localhost -p 5432 -U odoo -lqt | cut -d \| -f 1 | grep -qw sama_jokoo_dev; then
        echo -e "  ${GREEN}✓${NC} Base de données de développement existe"
    else
        echo -e "  ${YELLOW}!${NC} Base de données de développement n'existe pas"
    fi
    
    if PGPASSWORD=odoo psql -h localhost -p 5432 -U odoo -lqt | cut -d \| -f 1 | grep -qw sama_jokoo_prod; then
        echo -e "  ${GREEN}✓${NC} Base de données de production existe"
    else
        echo -e "  ${YELLOW}!${NC} Base de données de production n'existe pas"
    fi
}

clean_environment() {
    print_header
    print_section "NETTOYAGE DE L'ENVIRONNEMENT"
    
    echo -e "  ${YELLOW}Nettoyage des logs...${NC}"
    rm -f logs/*.log
    rm -f dev_scripts/logs/*.log
    
    echo -e "  ${YELLOW}Nettoyage des fichiers temporaires...${NC}"
    rm -rf temp/
    rm -rf __pycache__/
    find . -name "*.pyc" -delete
    find . -name "*.pyo" -delete
    
    echo -e "  ${YELLOW}Nettoyage des fichiers PID...${NC}"
    rm -f logs/*.pid
    rm -f dev_scripts/logs/*.pid
    
    echo -e "  ${GREEN}✓${NC} Nettoyage terminé"
}

reset_environment() {
    print_header
    print_section "RÉINITIALISATION COMPLÈTE"
    
    echo -e "  ${RED}⚠ Cette action va arrêter tous les services et supprimer les bases de données${NC}"
    read -p "Êtes-vous sûr ? (y/N): " -n 1 -r
    echo
    
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        echo -e "  ${YELLOW}Arrêt des services...${NC}"
        ./stop_dev.sh > /dev/null 2>&1
        ../stop_sama_jokoo.sh > /dev/null 2>&1
        
        echo -e "  ${YELLOW}Suppression des bases de données...${NC}"
        PGPASSWORD=odoo dropdb -h localhost -p 5432 -U odoo --if-exists sama_jokoo_dev
        PGPASSWORD=odoo dropdb -h localhost -p 5432 -U odoo --if-exists sama_jokoo_prod
        
        echo -e "  ${YELLOW}Nettoyage des fichiers...${NC}"
        clean_environment > /dev/null 2>&1
        
        echo -e "  ${GREEN}✓${NC} Réinitialisation terminée"
        echo -e "  ${BLUE}ℹ${NC} Utilisez ./start_dev.sh pour redémarrer"
    else
        echo -e "  ${BLUE}ℹ${NC} Réinitialisation annulée"
    fi
}

# Menu principal
case "${1:-help}" in
    "help"|"")
        show_help
        ;;
    "status")
        show_status
        ;;
    "clean")
        clean_environment
        ;;
    "reset")
        reset_environment
        ;;
    *)
        echo -e "${RED}Commande inconnue: $1${NC}"
        echo -e "Utilisez: ${GREEN}./help.sh${NC} pour voir l'aide"
        exit 1
        ;;
esac