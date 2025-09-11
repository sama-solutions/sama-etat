#!/bin/bash

# Script de diagnostic et correction pour ARBase v2
# Identifie et corrige les problèmes de démarrage

set -e

echo "🔍 Diagnostic ARBase v2"
echo "======================="
echo ""

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

log_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# 1. Vérifier Node.js
check_node() {
    log_info "Vérification de Node.js..."
    
    if ! command -v node &> /dev/null; then
        log_error "Node.js n'est pas installé"
        exit 1
    fi
    
    NODE_VERSION=$(node --version | cut -d'v' -f2 | cut -d'.' -f1)
    if [ "$NODE_VERSION" -lt 18 ]; then
        log_error "Node.js version 18+ requis (version actuelle: $(node --version))"
        exit 1
    fi
    
    log_success "Node.js $(node --version) ✓"
}

# 2. Vérifier la structure des dossiers
check_structure() {
    log_info "Vérification de la structure..."
    
    REQUIRED_DIRS=("ar-engine-v2" "frontend-v2" "backend-v2")
    
    for dir in "${REQUIRED_DIRS[@]}"; do
        if [ ! -d "$dir" ]; then
            log_error "Dossier manquant: $dir"
            exit 1
        fi
        log_success "Dossier $dir ✓"
    done
}

# 3. Vérifier les fichiers package.json
check_package_files() {
    log_info "Vérification des fichiers package.json..."
    
    PACKAGES=("ar-engine-v2/package.json" "frontend-v2/package.json" "backend-v2/package.json")
    
    for pkg in "${PACKAGES[@]}"; do
        if [ ! -f "$pkg" ]; then
            log_error "Fichier manquant: $pkg"
            exit 1
        fi
        log_success "Package $pkg ✓"
    done
}

# 4. Installer les dépendances manquantes
install_dependencies() {
    log_info "Installation des dépendances..."
    
    # AR Engine
    if [ -d "ar-engine-v2" ]; then
        log_info "Installation AR Engine..."
        cd ar-engine-v2
        if [ ! -d "node_modules" ]; then
            npm install
        fi
        cd ..
        log_success "AR Engine installé ✓"
    fi
    
    # Backend
    if [ -d "backend-v2" ]; then
        log_info "Installation Backend..."
        cd backend-v2
        if [ ! -d "node_modules" ]; then
            npm install
        fi
        cd ..
        log_success "Backend installé ✓"
    fi
    
    # Frontend
    if [ -d "frontend-v2" ]; then
        log_info "Installation Frontend..."
        cd frontend-v2
        if [ ! -d "node_modules" ]; then
            npm install
        fi
        cd ..
        log_success "Frontend installé ✓"
    fi
}

# 5. Créer les fichiers de configuration manquants
create_config_files() {
    log_info "Création des fichiers de configuration..."
    
    # Backend .env
    if [ ! -f "backend-v2/.env" ]; then
        log_info "Création backend-v2/.env..."
        cat > backend-v2/.env << EOF
NODE_ENV=development
PORT=4000
MONGODB_URI=mongodb://localhost:27017/arbase_v2
JWT_SECRET=arbase-secret-key-change-in-production
FRONTEND_URL=http://localhost:3000
EOF
        log_success "Backend .env créé ✓"
    fi
    
    # Frontend .env
    if [ ! -f "frontend-v2/.env" ]; then
        log_info "Création frontend-v2/.env..."
        cat > frontend-v2/.env << EOF
VITE_API_URL=http://localhost:4000
VITE_WS_URL=ws://localhost:4000
VITE_APP_NAME=ARBase
VITE_APP_VERSION=2.0.0
EOF
        log_success "Frontend .env créé ✓"
    fi
    
    # Frontend index.html
    if [ ! -f "frontend-v2/index.html" ]; then
        log_info "Création frontend-v2/index.html..."
        cat > frontend-v2/index.html << EOF
<!doctype html>
<html lang="fr">
  <head>
    <meta charset="UTF-8" />
    <link rel="icon" type="image/svg+xml" href="/vite.svg" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>ARBase - Réalité Augmentée</title>
  </head>
  <body>
    <div id="root"></div>
    <script type="module" src="/src/main.tsx"></script>
  </body>
</html>
EOF
        log_success "Frontend index.html créé ✓"
    fi
}

# 6. Créer les dossiers nécessaires
create_directories() {
    log_info "Création des dossiers nécessaires..."
    
    mkdir -p backend-v2/uploads
    mkdir -p backend-v2/logs
    
    log_success "Dossiers créés ✓"
}

# 7. Tester les ports
check_ports() {
    log_info "Vérification des ports..."
    
    # Port 3000 (Frontend)
    if lsof -Pi :3000 -sTCP:LISTEN -t >/dev/null 2>&1; then
        log_warning "Port 3000 déjà utilisé"
        lsof -Pi :3000 -sTCP:LISTEN
    else
        log_success "Port 3000 disponible ✓"
    fi
    
    # Port 4000 (Backend)
    if lsof -Pi :4000 -sTCP:LISTEN -t >/dev/null 2>&1; then
        log_warning "Port 4000 déjà utilisé"
        lsof -Pi :4000 -sTCP:LISTEN
    else
        log_success "Port 4000 disponible ✓"
    fi
}

# 8. Test de compilation
test_compilation() {
    log_info "Test de compilation..."
    
    # Test Backend
    cd backend-v2
    if npm run type-check 2>/dev/null; then
        log_success "Backend compile ✓"
    else
        log_warning "Problème de compilation backend"
    fi
    cd ..
    
    # Test Frontend
    cd frontend-v2
    if npm run type-check 2>/dev/null; then
        log_success "Frontend compile ✓"
    else
        log_warning "Problème de compilation frontend"
    fi
    cd ..
}

# 9. Créer un script de démarrage simple
create_simple_start() {
    log_info "Création du script de démarrage simple..."
    
    cat > start-simple.sh << 'EOF'
#!/bin/bash

echo "🚀 Démarrage ARBase v2 (Mode Simple)"
echo "===================================="

# Démarrer le backend
echo "📡 Démarrage du backend..."
cd backend-v2
npm run dev &
BACKEND_PID=$!
cd ..

sleep 3

# Démarrer le frontend
echo "🌐 Démarrage du frontend..."
cd frontend-v2
npm run dev &
FRONTEND_PID=$!
cd ..

sleep 3

echo ""
echo "✅ ARBase v2 démarré!"
echo "📱 Frontend: http://localhost:3000"
echo "🔧 Backend:  http://localhost:4000"
echo ""
echo "Appuyez sur Ctrl+C pour arrêter"

# Fonction de nettoyage
cleanup() {
    echo ""
    echo "🔄 Arrêt des services..."
    kill $BACKEND_PID 2>/dev/null || true
    kill $FRONTEND_PID 2>/dev/null || true
    echo "✅ Services arrêtés"
    exit 0
}

trap cleanup SIGINT SIGTERM

# Attendre
wait
EOF
    
    chmod +x start-simple.sh
    log_success "Script start-simple.sh créé ✓"
}

# 10. Afficher les informations de diagnostic
show_diagnostic_info() {
    echo ""
    echo "📊 Informations de Diagnostic"
    echo "============================="
    echo ""
    
    # Version Node.js
    echo "🟢 Node.js: $(node --version)"
    echo "🟢 npm: $(npm --version)"
    
    # Espace disque
    echo "💾 Espace disque:"
    df -h . | tail -1
    
    # Mémoire
    echo "🧠 Mémoire:"
    free -h | head -2
    
    # Processus sur les ports
    echo ""
    echo "🔌 Ports utilisés:"
    netstat -tlnp 2>/dev/null | grep -E ':(3000|4000|27017|6379)' || echo "Aucun port ARBase utilisé"
    
    echo ""
}

# Fonction principale
main() {
    echo "🔍 Début du diagnostic..."
    echo ""
    
    check_node
    check_structure
    check_package_files
    install_dependencies
    create_config_files
    create_directories
    check_ports
    test_compilation
    create_simple_start
    show_diagnostic_info
    
    echo "🎉 Diagnostic terminé!"
    echo "===================="
    echo ""
    echo "✅ Tout semble prêt pour le démarrage"
    echo ""
    echo "🚀 Pour démarrer ARBase v2:"
    echo "   ./start-simple.sh"
    echo ""
    echo "📱 URLs d'accès:"
    echo "   Frontend: http://localhost:3000"
    echo "   Backend:  http://localhost:4000"
    echo ""
    
    # Détecter l'IP pour mobile
    if [ -f "get-local-ip.js" ]; then
        LOCAL_IP=$(node get-local-ip.js ip 2>/dev/null || echo "localhost")
        if [ "$LOCAL_IP" != "localhost" ]; then
            echo "📱 URLs Mobile (IP: $LOCAL_IP):"
            echo "   Frontend: http://$LOCAL_IP:3000"
            echo "   Scanner:  http://$LOCAL_IP:3000/scanner"
            echo ""
        fi
    fi
}

# Exécuter
main "$@"