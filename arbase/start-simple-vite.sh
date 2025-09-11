#!/bin/bash

# Script de démarrage simple avec Vite uniquement
echo "🚀 Démarrage Simple ARBase v2"
echo "============================="

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

# 1. Nettoyer les ports
log_info "Nettoyage des ports..."
for port in 3000 3001 3002 4000; do
    PID=$(lsof -ti:$port 2>/dev/null)
    if [ ! -z "$PID" ]; then
        log_warning "Arrêt du processus sur le port $port"
        kill -9 $PID 2>/dev/null || true
    fi
done

sleep 2

# 2. Démarrer le backend simple
log_info "Démarrage du backend..."
cd backend-v2

cat > simple-backend.js << 'EOF'
const express = require('express');
const cors = require('cors');

const app = express();
const PORT = 4000;

app.use(cors());
app.use(express.json());

app.get('/health', (req, res) => {
  res.json({ status: 'ok', timestamp: new Date().toISOString() });
});

app.get('/api/experiences/public', (req, res) => {
  res.json({
    experiences: [
      {
        id: 'demo1',
        title: 'Demo AR Experience',
        description: 'Une expérience de démonstration',
        category: 'demo'
      }
    ]
  });
});

app.get('/api/experiences/:id', (req, res) => {
  res.json({
    id: req.params.id,
    title: 'Demo Experience',
    description: 'Expérience de test',
    content: []
  });
});

app.listen(PORT, () => {
  console.log(`Backend démarré sur http://localhost:${PORT}`);
});
EOF

node simple-backend.js &
BACKEND_PID=$!
cd ..

sleep 2

# 3. Démarrer le frontend avec Vite seulement
log_info "Démarrage du frontend..."
cd frontend-v2

# Modifier package.json pour éviter TypeScript
cat > package.json << 'EOF'
{
  "name": "@arbase/frontend",
  "version": "2.0.0",
  "type": "module",
  "scripts": {
    "dev": "vite --host",
    "build": "vite build",
    "preview": "vite preview"
  },
  "dependencies": {
    "react": "^18.2.0",
    "react-dom": "^18.2.0",
    "react-router-dom": "^6.8.0",
    "zustand": "^4.4.0",
    "framer-motion": "^10.16.0",
    "lucide-react": "^0.294.0",
    "clsx": "^2.0.0",
    "tailwind-merge": "^2.0.0",
    "react-hot-toast": "^2.4.1"
  },
  "devDependencies": {
    "@vitejs/plugin-react": "^4.1.0",
    "autoprefixer": "^10.4.16",
    "postcss": "^8.4.31",
    "tailwindcss": "^3.3.5",
    "vite": "^4.5.0"
  }
}
EOF

npm run dev &
FRONTEND_PID=$!
cd ..

sleep 5

# 4. Afficher les informations
echo ""
log_success "ARBase v2 démarré!"
echo ""
echo "📱 URLs:"
echo "   Frontend: http://localhost:3000"
echo "   Backend:  http://localhost:4000"
echo ""

# IP mobile
if [ -f "get-local-ip.js" ]; then
    LOCAL_IP=$(node get-local-ip.js ip 2>/dev/null || echo "localhost")
    if [ "$LOCAL_IP" != "localhost" ]; then
        echo "📱 Mobile (IP: $LOCAL_IP):"
        echo "   Frontend: http://$LOCAL_IP:3000"
        echo "   Scanner:  http://$LOCAL_IP:3000/scanner"
        echo ""
    fi
fi

# Fonction de nettoyage
cleanup() {
    echo ""
    log_info "Arrêt des services..."
    
    if [ ! -z "$BACKEND_PID" ]; then
        kill $BACKEND_PID 2>/dev/null || true
    fi
    
    if [ ! -z "$FRONTEND_PID" ]; then
        kill $FRONTEND_PID 2>/dev/null || true
    fi
    
    pkill -f "simple-backend.js" 2>/dev/null || true
    
    log_success "Services arrêtés"
    exit 0
}

trap cleanup SIGINT SIGTERM

log_info "Services en cours... (Ctrl+C pour arrêter)"
wait