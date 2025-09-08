#!/bin/bash

# Script de démarrage simplifié pour Sama Jokoo avec Profils
# ==========================================================

echo "🚀 Démarrage de Sama Jokoo avec Profils (Version Mise à Jour)"
echo "============================================================="

# Couleurs
GREEN='\033[0;32m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
NC='\033[0m'

echo -e "${BLUE}1. Nettoyage des processus...${NC}"
pkill -f "serve_app.py" 2>/dev/null
pkill -f "serve_comments_app.py" 2>/dev/null
pkill -f "serve_profiles_app.py" 2>/dev/null
sleep 3

echo -e "${BLUE}2. Vérification des fichiers...${NC}"
if [ ! -f "sama_jokoo_with_profiles.html" ]; then
    echo "❌ Fichier sama_jokoo_with_profiles.html manquant"
    exit 1
fi

echo -e "${GREEN}✅ Fichiers présents${NC}"

echo -e "${BLUE}3. Démarrage du serveur...${NC}"

echo ""
echo -e "${PURPLE}🎨 SAMA JOKOO - VERSION AVEC PROFILS${NC}"
echo ""
echo -e "${GREEN}Fonctionnalités disponibles :${NC}"
echo -e "  📝 ${BLUE}Feed${NC} - Posts et commentaires neumorphiques"
echo -e "  👤 ${BLUE}Mon Profil${NC} - Profil utilisateur avec avatar"
echo -e "  📊 ${BLUE}Statistiques${NC} - Métriques détaillées"
echo -e "  🏆 ${BLUE}Badges${NC} - Système de réalisations"
echo ""
echo -e "${GREEN}Accès :${NC}"
echo -e "  📱 URL : ${BLUE}http://localhost:3000${NC}"
echo -e "  👤 Login : ${BLUE}admin${NC}"
echo -e "  🔑 Password : ${BLUE}admin${NC}"
echo ""
echo -e "${BLUE}Pour arrêter : Ctrl+C${NC}"
echo ""

# Démarrer directement le serveur Python
python3 -c "
import http.server
import socketserver
import webbrowser
import sys

PORT = 3000

class Handler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/' or self.path == '/index.html':
            self.send_response(200)
            self.send_header('Content-type', 'text/html; charset=utf-8')
            self.send_header('Cache-Control', 'no-cache')
            self.end_headers()
            
            try:
                with open('sama_jokoo_with_profiles.html', 'r', encoding='utf-8') as f:
                    content = f.read()
                self.wfile.write(content.encode('utf-8'))
            except FileNotFoundError:
                self.wfile.write(b'<h1>Erreur: fichier non trouve</h1>')
        else:
            self.send_response(404)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(b'<h1>404 - Not Found</h1>')

try:
    with socketserver.TCPServer(('', PORT), Handler) as httpd:
        print(f'✅ Serveur démarré sur http://localhost:{PORT}')
        httpd.serve_forever()
except KeyboardInterrupt:
    print('\n🛑 Serveur arrêté')
except Exception as e:
    print(f'❌ Erreur: {e}')
    sys.exit(1)
"