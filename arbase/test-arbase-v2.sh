#!/bin/bash

# Script de test pour ARBase v2
echo "🧪 Test ARBase v2"
echo "=================="

# Couleurs
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

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Test du backend
test_backend() {
    log_info "Test du backend..."
    
    # Test health check
    if curl -s http://localhost:4000/health > /dev/null; then
        log_success "Backend accessible ✓"
        
        # Test API health
        if curl -s http://localhost:4000/api/health > /dev/null; then
            log_success "API health accessible ✓"
        else
            log_error "API health non accessible"
        fi
        
        # Test expériences
        if curl -s http://localhost:4000/api/experiences/public > /dev/null; then
            log_success "API expériences accessible ✓"
        else
            log_error "API expériences non accessible"
        fi
        
    else
        log_error "Backend non accessible"
        return 1
    fi
}

# Test du frontend
test_frontend() {
    log_info "Test du frontend..."
    
    # Vérifier les ports possibles
    FRONTEND_PORT=""
    for port in 3000 3001 3002; do
        if curl -s http://localhost:$port > /dev/null; then
            FRONTEND_PORT=$port
            break
        fi
    done
    
    if [ ! -z "$FRONTEND_PORT" ]; then
        log_success "Frontend accessible sur le port $FRONTEND_PORT ✓"
        echo "   URL: http://localhost:$FRONTEND_PORT"
        
        # Détecter l'IP pour mobile
        if [ -f "get-local-ip.js" ]; then
            LOCAL_IP=$(node get-local-ip.js ip 2>/dev/null || echo "localhost")
            if [ "$LOCAL_IP" != "localhost" ]; then
                echo "   Mobile: http://$LOCAL_IP:$FRONTEND_PORT"
                echo "   Scanner: http://$LOCAL_IP:$FRONTEND_PORT/scanner"
            fi
        fi
    else
        log_error "Frontend non accessible"
        return 1
    fi
}

# Test des APIs
test_apis() {
    log_info "Test des APIs..."
    
    # Test génération QR
    QR_RESPONSE=$(curl -s -X POST http://localhost:4000/api/qr/generate \
        -H "Content-Type: application/json" \
        -d '{"data":"test"}')
    
    if echo "$QR_RESPONSE" | grep -q "qrCode"; then
        log_success "API QR génération ✓"
    else
        log_error "API QR génération échouée"
    fi
    
    # Test expérience
    EXP_RESPONSE=$(curl -s http://localhost:4000/api/experiences/demo_test)
    
    if echo "$EXP_RESPONSE" | grep -q "title"; then
        log_success "API expérience ✓"
    else
        log_error "API expérience échouée"
    fi
}

# Afficher les informations de test
show_test_results() {
    echo ""
    echo "📊 Résultats des Tests"
    echo "====================="
    echo ""
    
    # Informations système
    echo "🖥️  Système:"
    echo "   Node.js: $(node --version)"
    echo "   npm: $(npm --version)"
    echo ""
    
    # URLs actives
    echo "🌐 URLs Actives:"
    
    # Backend
    if curl -s http://localhost:4000/health > /dev/null; then
        echo "   ✅ Backend: http://localhost:4000"
        echo "   ✅ API: http://localhost:4000/api"
    else
        echo "   ❌ Backend: Non accessible"
    fi
    
    # Frontend
    FRONTEND_PORT=""
    for port in 3000 3001 3002; do
        if curl -s http://localhost:$port > /dev/null; then
            FRONTEND_PORT=$port
            echo "   ✅ Frontend: http://localhost:$port"
            break
        fi
    done
    
    if [ -z "$FRONTEND_PORT" ]; then
        echo "   ❌ Frontend: Non accessible"
    fi
    
    echo ""
    
    # URLs mobiles
    if [ -f "get-local-ip.js" ]; then
        LOCAL_IP=$(node get-local-ip.js ip 2>/dev/null || echo "localhost")
        if [ "$LOCAL_IP" != "localhost" ] && [ ! -z "$FRONTEND_PORT" ]; then
            echo "📱 URLs Mobile (IP: $LOCAL_IP):"
            echo "   🌐 Frontend: http://$LOCAL_IP:$FRONTEND_PORT"
            echo "   📷 Scanner: http://$LOCAL_IP:$FRONTEND_PORT/scanner"
            echo "   🔧 API: http://$LOCAL_IP:4000"
            echo ""
        fi
    fi
}

# Fonction principale
main() {
    echo "🔍 Début des tests..."
    echo ""
    
    # Attendre un peu que les services se stabilisent
    sleep 2
    
    test_backend
    test_frontend
    test_apis
    show_test_results
    
    echo "✅ Tests terminés!"
    echo ""
    echo "🚀 Pour démarrer ARBase v2:"
    echo "   ./start-dev-simple.sh"
    echo ""
}

# Exécuter
main "$@"