#!/bin/bash

# Script de démarrage ARBase v2
# Démarre tous les services de la nouvelle plateforme AR

set -e

echo "🚀 Démarrage d'ARBase v2 - Plateforme de Réalité Augmentée"
echo "============================================================"

# Couleurs pour les logs
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

log_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

log_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

log_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Vérifier les prérequis
check_prerequisites() {
    log_info "Vérification des prérequis..."
    
    if ! command -v node &> /dev/null; then
        log_error "Node.js n'est pas installé"
        exit 1
    fi
    
    NODE_VERSION=$(node --version | cut -d'v' -f2 | cut -d'.' -f1)
    if [ "$NODE_VERSION" -lt 18 ]; then
        log_error "Node.js version 18+ requis (version actuelle: $(node --version))"
        exit 1
    fi
    
    log_success "Prérequis vérifiés"
}

# Installation des dépendances
install_dependencies() {
    log_info "Installation des dépendances..."
    
    if [ -d "ar-engine-v2" ]; then
        log_info "Installation du moteur AR..."
        cd ar-engine-v2
        npm install
        cd ..
        log_success "Moteur AR prêt"
    fi
    
    if [ -d "backend-v2" ]; then
        log_info "Installation du backend..."
        cd backend-v2
        npm install
        cd ..
        log_success "Backend prêt"
    fi
    
    if [ -d "frontend-v2" ]; then
        log_info "Installation du frontend..."
        cd frontend-v2
        npm install
        cd ..
        log_success "Frontend prêt"
    fi
}

# Configuration de l'environnement
setup_environment() {
    log_info "Configuration de l'environnement..."
    
    if [ -d "backend-v2" ] && [ ! -f "backend-v2/.env" ]; then
        cp backend-v2/.env.example backend-v2/.env
    fi
    
    if [ -d "frontend-v2" ] && [ ! -f "frontend-v2/.env" ]; then
        cat > frontend-v2/.env << EOF
VITE_API_URL=http://localhost:4000
VITE_WS_URL=ws://localhost:4000
VITE_APP_NAME=ARBase
VITE_APP_VERSION=2.0.0
EOF
    fi
    
    mkdir -p backend-v2/uploads
    log_success "Environnement configuré"
}

# Démarrage des services
start_services() {
    log_info "Démarrage des services..."
    
    if [ -d "backend-v2" ]; then
        log_info "Démarrage du backend..."
        cd backend-v2
        npm run dev &
        BACKEND_PID=$!
        cd ..
        sleep 3
        log_success "Backend démarré"
    fi
    
    if [ -d "frontend-v2" ]; then
        log_info "Démarrage du frontend..."
        cd frontend-v2
        npm run dev &
        FRONTEND_PID=$!
        cd ..
        sleep 3
        log_success "Frontend démarré"
    fi
    
    sleep 5
}

# Affichage des informations
show_info() {
    echo ""
    echo "🎉 ARBase v2 est maintenant opérationnel !"
    echo "=========================================="
    echo ""
    
    # Détecter le port frontend actuel
    FRONTEND_PORT="3000"
    for port in 3000 3001 3002; do
        if curl -s http://localhost:$port > /dev/null 2>&1; then
            FRONTEND_PORT=$port
            break
        fi
    done
    
    echo "💻 URLs Locales :"
    echo "   • Frontend : http://localhost:$FRONTEND_PORT"
    echo "   • Backend  : http://localhost:4000"
    echo "   • Scanner  : http://localhost:$FRONTEND_PORT/scanner"
    echo "   • Health   : http://localhost:4000/health"
    echo ""
    
    # Détecter l'IP locale pour les tests mobiles
    if command -v node &> /dev/null && [ -f "get-local-ip.js" ]; then
        log_info "Détection de l'adresse IP pour tests mobiles..."
        LOCAL_IP=$(node get-local-ip.js ip 2>/dev/null || echo "localhost")
        
        if [ "$LOCAL_IP" != "localhost" ]; then
            echo "📱 URLs Mobiles (IP: $LOCAL_IP) :"
            echo "   • Frontend : http://$LOCAL_IP:$FRONTEND_PORT"
            echo "   • Scanner  : http://$LOCAL_IP:$FRONTEND_PORT/scanner"
            echo "   • API      : http://$LOCAL_IP:4000"
            echo ""
            echo "📋 Instructions Mobile :"
            echo "   1. Connectez votre mobile au même réseau WiFi"
            echo "   2. Ouvrez http://$LOCAL_IP:$FRONTEND_PORT/scanner sur mobile"
            echo "   3. Autorisez l'accès caméra et scannez un QR code"
            echo ""
            
            # Générer QR code pour accès mobile rapide
            if command -v qrencode &> /dev/null; then
                echo "📱 QR Code d'accès mobile :"
                echo "http://$LOCAL_IP:$FRONTEND_PORT/scanner" | qrencode -t ANSIUTF8
                echo ""
            fi
        fi
    fi
    
    echo "🛠️  Fonctionnalités :"
    echo "   ✅ Moteur AR moderne avec QR codes"
    echo "   ✅ Scanner web avec WebXR"
    echo "   ✅ Interface utilisateur moderne"
    echo "   ✅ API REST complète"
    echo "   ✅ PWA (Progressive Web App)"
    echo "   ✅ Tests mobiles avec IP dynamique"
    echo ""
    
    echo "🚀 Démarrage Rapide :"
    echo "   • Mode Simple : ./start-dev-simple.sh"
    echo "   • Test Complet : ./test-arbase-v2.sh"
    echo "   • IP Mobile   : node get-local-ip.js display"
    echo ""
}

# Gestion de l'arrêt
cleanup() {
    echo ""
    log_info "Arrêt des services..."
    
    if [ ! -z "$BACKEND_PID" ]; then
        kill $BACKEND_PID 2>/dev/null || true
    fi
    
    if [ ! -z "$FRONTEND_PID" ]; then
        kill $FRONTEND_PID 2>/dev/null || true
    fi
    
    log_success "ARBase v2 arrêté"
    exit 0
}

trap cleanup SIGINT SIGTERM

# Fonction principale
main() {
    check_prerequisites
    install_dependencies
    setup_environment
    start_services
    show_info
    
    log_info "Services en cours... (Ctrl+C pour arrêter)"
    wait
}

main "$@"