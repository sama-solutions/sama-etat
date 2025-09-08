#!/bin/bash

# Script de lancement complet SAMA CONAI avec intégration Odoo
# Application mobile révolutionnaire avec backend Odoo XML-RPC

echo "🚀 LANCEMENT COMPLET SAMA CONAI - INTÉGRATION ODOO + APPLICATION MOBILE"
echo "========================================================================"

# Variables
APP_DIR="mobile_app_ux_inspired"
MOBILE_PORT=3004
ODOO_PORT=8077
ODOO_DB="sama_conai_analytics"

# Couleurs
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
RED='\033[0;31m'
PURPLE='\033[0;35m'
CYAN='\033[0;36m'
WHITE='\033[1;37m'
NC='\033[0m'

print_status() {
    echo -e "${GREEN}✅${NC} $1"
}

print_info() {
    echo -e "${BLUE}ℹ️${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}⚠️${NC} $1"
}

print_error() {
    echo -e "${RED}❌${NC} $1"
}

print_header() {
    echo -e "${PURPLE}$1${NC}"
}

print_success() {
    echo -e "${GREEN}🎉${NC} $1"
}

# Bannière de démarrage
echo ""
echo -e "${PURPLE}╔══════════════════════════════════════════════════════════════╗${NC}"
echo -e "${PURPLE}║         SAMA CONAI INTÉGRATION COMPLÈTE v6.0 FINAL          ║${NC}"
echo -e "${PURPLE}║      Application Mobile + Backend Odoo XML-RPC Réel         ║${NC}"
echo -e "${PURPLE}║                                                              ║${NC}"
echo -e "${PURPLE}║  🇸🇳 République du Sénégal - Transparence Numérique         ║${NC}"
echo -e "${PURPLE}╚══════════════════════════════════════════════════════════════╝${NC}"
echo ""

# Vérification des prérequis
check_prerequisites() {
    print_info "Vérification des prérequis..."
    
    # Vérifier Node.js
    if ! command -v node &> /dev/null; then
        print_error "Node.js n'est pas installé"
        exit 1
    fi
    
    NODE_VERSION=$(node --version)
    print_status "Node.js détecté: $NODE_VERSION"
    
    # Vérifier Python3
    if ! command -v python3 &> /dev/null; then
        print_error "Python3 n'est pas installé"
        exit 1
    fi
    
    PYTHON_VERSION=$(python3 --version)
    print_status "Python3 détecté: $PYTHON_VERSION"
    
    # Vérifier le répertoire
    if [ ! -d "$APP_DIR" ]; then
        print_error "Répertoire $APP_DIR non trouvé"
        exit 1
    fi
    
    if [ ! -f "$APP_DIR/server_odoo_final.js" ]; then
        print_error "Fichier server_odoo_final.js non trouvé"
        exit 1
    fi
    
    print_status "Structure de l'application validée"
}

# Nettoyage des processus existants
cleanup_processes() {
    print_info "Nettoyage des processus existants..."
    
    # Arrêter les serveurs existants
    pkill -f "server_odoo_final.js" 2>/dev/null || true
    pkill -f "server_odoo_integrated.js" 2>/dev/null || true
    pkill -f "server_simple.js" 2>/dev/null || true
    
    # Attendre un peu
    sleep 2
    
    print_status "Nettoyage terminé"
}

# Vérification des ports
check_ports() {
    print_info "Vérification des ports..."
    
    # Port mobile
    if lsof -Pi :$MOBILE_PORT -sTCP:LISTEN -t >/dev/null 2>&1; then
        print_warning "Port $MOBILE_PORT déjà utilisé"
        PID=$(lsof -ti:$MOBILE_PORT)
        if [ ! -z "$PID" ]; then
            print_info "Arrêt du processus utilisant le port mobile (PID: $PID)"
            kill $PID 2>/dev/null || true
            sleep 3
        fi
    fi
    
    # Port Odoo
    if lsof -Pi :$ODOO_PORT -sTCP:LISTEN -t >/dev/null 2>&1; then
        print_info "Port Odoo $ODOO_PORT déjà utilisé (probablement Odoo en cours)"
    fi
    
    print_status "Ports vérifiés"
}

# Démarrage d'Odoo
start_odoo() {
    print_header "🔧 DÉMARRAGE D'ODOO AVEC MODULE SAMA CONAI"
    
    print_info "Lancement d'Odoo sur le port $ODOO_PORT..."
    
    # Démarrer Odoo en arrière-plan
    nohup python3 /var/odoo/odoo18/odoo-bin \
        -d $ODOO_DB \
        --addons-path=/var/odoo/odoo18/addons,/home/grand-as/psagsn/custom_addons \
        --db_host=localhost \
        --db_user=odoo \
        --db_password=odoo \
        --http-port=$ODOO_PORT \
        --log-level=info \
        > /tmp/odoo_sama_conai.log 2>&1 &
    
    ODOO_PID=$!
    echo $ODOO_PID > odoo.pid
    
    print_info "Odoo démarré avec PID: $ODOO_PID"
    print_info "Attente du démarrage d'Odoo..."
    
    # Attendre qu'Odoo soit prêt
    for i in {1..30}; do
        if curl -s --connect-timeout 2 "http://localhost:$ODOO_PORT" > /dev/null 2>&1; then
            print_status "Odoo est prêt et accessible"
            return 0
        fi
        echo -n "."
        sleep 2
    done
    
    print_warning "Odoo prend plus de temps que prévu à démarrer"
    print_info "L'application mobile fonctionnera en mode fallback si nécessaire"
    return 1
}

# Démarrage de l'application mobile
start_mobile_app() {
    print_header "📱 DÉMARRAGE DE L'APPLICATION MOBILE AVEC INTÉGRATION ODOO"
    
    cd "$APP_DIR"
    
    # Configuration des variables d'environnement
    export ODOO_URL="http://localhost:$ODOO_PORT"
    export ODOO_DB="$ODOO_DB"
    export ODOO_USER="admin"
    export ODOO_PASSWORD="admin"
    export PORT="$MOBILE_PORT"
    
    print_info "Démarrage du serveur mobile avec intégration Odoo..."
    
    # Démarrer le serveur mobile
    node server_odoo_final.js &
    MOBILE_PID=$!
    
    # Sauvegarder le PID
    echo $MOBILE_PID > mobile.pid
    
    print_info "Serveur mobile démarré avec PID: $MOBILE_PID"
    
    # Attendre le démarrage
    print_info "Attente du démarrage du serveur mobile..."
    sleep 8
    
    # Vérifier que le serveur fonctionne
    if ps -p $MOBILE_PID > /dev/null 2>&1; then
        # Tester la connexion HTTP
        if curl -s --connect-timeout 5 "http://localhost:$MOBILE_PORT" > /dev/null 2>&1; then
            print_status "Serveur mobile démarré avec succès !"
            return 0
        else
            print_error "Le serveur mobile ne répond pas sur le port $MOBILE_PORT"
            return 1
        fi
    else
        print_error "Le serveur mobile s'est arrêté de manière inattendue"
        return 1
    fi
    
    cd ..
}

# Test de l'intégration
test_integration() {
    print_info "Test de l'intégration Odoo..."
    
    # Test de l'API mobile
    if curl -s "http://localhost:$MOBILE_PORT/api/dashboard" > /dev/null; then
        print_status "API mobile fonctionnelle"
    else
        print_warning "API mobile non accessible"
    fi
    
    # Test de connexion Odoo
    ODOO_TEST=$(curl -s "http://localhost:$MOBILE_PORT/api/test-odoo" | grep -o '"connected":[^,]*' | cut -d':' -f2)
    if [ "$ODOO_TEST" = "true" ]; then
        print_status "Intégration Odoo active"
    else
        print_warning "Intégration Odoo en mode fallback"
    fi
}

# Affichage des informations finales
show_final_info() {
    echo ""
    print_header "🎉 SAMA CONAI INTÉGRATION COMPLÈTE LANCÉE AVEC SUCCÈS !"
    print_header "======================================================="
    echo ""
    
    print_success "🌐 Application Mobile: ${WHITE}http://localhost:$MOBILE_PORT${NC}"
    print_success "🔧 Interface Odoo: ${WHITE}http://localhost:$ODOO_PORT${NC}"
    print_success "🎨 Design: ${WHITE}UX Révolutionnaire avec Drilldown${NC}"
    print_success "📱 Interface: ${WHITE}Mobile-First Optimisée${NC}"
    print_success "✨ Backend: ${WHITE}Odoo XML-RPC + Fallback Intelligent${NC}"
    print_success "📊 Données: ${WHITE}Réelles depuis Odoo + Simulées Enrichies${NC}"
    
    echo ""
    print_header "🔧 GESTION DES SERVICES:"
    echo -e "${WHITE}   📊 Statut Odoo:${NC} ps -p $(cat odoo.pid 2>/dev/null || echo '0')"
    echo -e "${WHITE}   📱 Statut Mobile:${NC} ps -p $(cat $APP_DIR/mobile.pid 2>/dev/null || echo '0')"
    echo -e "${WHITE}   🛑 Arrêt Odoo:${NC} kill $(cat odoo.pid 2>/dev/null || echo 'PID_INCONNU')"
    echo -e "${WHITE}   🛑 Arrêt Mobile:${NC} kill $(cat $APP_DIR/mobile.pid 2>/dev/null || echo 'PID_INCONNU')"
    echo -e "${WHITE}   🔄 Redémarrage:${NC} ./launch_sama_conai_complete.sh"
    
    echo ""
    print_header "🎯 FONCTIONNALITÉS INTÉGRÉES:"
    echo -e "${CYAN}   📊 Dashboard avec données Odoo réelles${NC}"
    echo -e "${CYAN}   📄 Demandes d'information depuis Odoo${NC}"
    echo -e "${CYAN}   🚨 Alertes et signalements Odoo${NC}"
    echo -e "${CYAN}   🔍 Navigation drilldown complète${NC}"
    echo -e "${CYAN}   📱 Interface mobile révolutionnaire${NC}"
    echo -e "${CYAN}   🔄 Fallback intelligent si Odoo indisponible${NC}"
    echo -e "${CYAN}   🎨 Design system moderne et animations${NC}"
    
    echo ""
    print_header "🔑 COMPTES DE TEST:"
    echo -e "${WHITE}   👑 Admin:${NC} admin@sama-conai.sn / admin123"
    echo -e "${WHITE}   🛡️ Agent:${NC} agent@sama-conai.sn / agent123"
    echo -e "${WHITE}   👤 Citoyen:${NC} citoyen@email.com / citoyen123"
    
    echo ""
    print_header "📊 ENDPOINTS API DISPONIBLES:"
    echo -e "${WHITE}   🔐 POST /api/auth/login${NC} - Authentification"
    echo -e "${WHITE}   📊 GET /api/dashboard${NC} - Dashboard avec données Odoo"
    echo -e "${WHITE}   📄 GET /api/requests${NC} - Liste des demandes Odoo"
    echo -e "${WHITE}   📄 GET /api/requests/:id${NC} - Détail d'une demande"
    echo -e "${WHITE}   🚨 GET /api/alerts${NC} - Liste des alertes Odoo"
    echo -e "${WHITE}   🚨 GET /api/alerts/:id${NC} - Détail d'une alerte"
    echo -e "${WHITE}   🔧 GET /api/test-odoo${NC} - Test de connexion Odoo"
    
    echo ""
    print_success "💡 ${WHITE}Ouvrez http://localhost:$MOBILE_PORT dans votre navigateur${NC}"
    print_success "🇸🇳 ${WHITE}Découvrez l'application de transparence la plus avancée du Sénégal !${NC}"
    
    echo ""
    print_header "🌟 SAMA CONAI INTÉGRATION COMPLÈTE OPÉRATIONNELLE !"
    echo ""
}

# Fonction principale
main() {
    # Vérifications
    check_prerequisites
    cleanup_processes
    check_ports
    
    # Démarrage des services
    start_odoo
    ODOO_STATUS=$?
    
    start_mobile_app
    MOBILE_STATUS=$?
    
    if [ $MOBILE_STATUS -eq 0 ]; then
        test_integration
        show_final_info
        
        # Garder le script actif
        print_info "Appuyez sur Ctrl+C pour arrêter tous les services"
        wait
    else
        print_error "Échec du démarrage de l'application mobile"
        exit 1
    fi
}

# Gestion des signaux
cleanup_on_exit() {
    echo ""
    print_warning "Arrêt des services en cours..."
    
    # Arrêter l'application mobile
    if [ -f "$APP_DIR/mobile.pid" ]; then
        MOBILE_PID=$(cat "$APP_DIR/mobile.pid")
        if ps -p $MOBILE_PID > /dev/null 2>&1; then
            kill $MOBILE_PID 2>/dev/null || true
            print_status "Application mobile arrêtée (PID: $MOBILE_PID)"
        fi
        rm -f "$APP_DIR/mobile.pid"
    fi
    
    # Arrêter Odoo
    if [ -f "odoo.pid" ]; then
        ODOO_PID=$(cat "odoo.pid")
        if ps -p $ODOO_PID > /dev/null 2>&1; then
            kill $ODOO_PID 2>/dev/null || true
            print_status "Odoo arrêté (PID: $ODOO_PID)"
        fi
        rm -f "odoo.pid"
    fi
    
    print_success "Arrêt terminé"
    exit 0
}

trap cleanup_on_exit INT TERM

# Exécution
main "$@"