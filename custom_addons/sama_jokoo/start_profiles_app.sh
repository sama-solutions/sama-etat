#!/bin/bash

# Script de démarrage pour Sama Jokoo avec Profils Utilisateurs
# =============================================================

echo "👤 Démarrage de Sama Jokoo avec Profils Utilisateurs"
echo "===================================================="

# Couleurs
GREEN='\033[0;32m'
RED='\033[0;31m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
PURPLE='\033[0;35m'
NC='\033[0m'

echo -e "${BLUE}1. Arrêt des processus existants...${NC}"
pkill -f "serve_app.py" 2>/dev/null
pkill -f "serve_comments_app.py" 2>/dev/null
pkill -f "python3.*serve" 2>/dev/null
sleep 2

echo -e "${BLUE}2. Vérification des fichiers...${NC}"

if [ ! -f "sama_jokoo_with_profiles.html" ]; then
    echo -e "${RED}❌ Fichier sama_jokoo_with_profiles.html manquant${NC}"
    exit 1
fi

echo -e "${GREEN}✅ Fichiers présents${NC}"

echo -e "${BLUE}3. Création du serveur pour profils...${NC}"

# Créer un serveur Python spécialisé pour les profils
cat > serve_profiles_app.py << 'EOF'
#!/usr/bin/env python3
"""
Serveur pour Sama Jokoo avec système de profils utilisateurs
"""

import http.server
import socketserver
import webbrowser
import os
import sys

PORT = 3000

class SamaJokooProfilesHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/' or self.path == '/index.html':
            # Servir le fichier HTML avec profils
            self.send_response(200)
            self.send_header('Content-type', 'text/html; charset=utf-8')
            self.send_header('Cache-Control', 'no-cache')
            self.end_headers()
            
            try:
                with open('sama_jokoo_with_profiles.html', 'r', encoding='utf-8') as f:
                    content = f.read()
                self.wfile.write(content.encode('utf-8'))
            except FileNotFoundError:
                self.wfile.write(b'<h1>Erreur: fichier sama_jokoo_with_profiles.html non trouve</h1>')
        else:
            # 404 pour les autres chemins
            self.send_response(404)
            self.send_header('Content-type', 'text/html; charset=utf-8')
            self.end_headers()
            self.wfile.write(b'<h1>404 - Page non trouvee</h1>')

def main():
    print("👤 Serveur Sama Jokoo avec Profils Utilisateurs")
    print("=" * 45)
    
    try:
        with socketserver.TCPServer(("", PORT), SamaJokooProfilesHandler) as httpd:
            print(f"✅ Serveur démarré avec succès !")
            print(f"📱 URL: http://localhost:{PORT}")
            print(f"🎯 Application: Sama Jokoo avec Profils")
            print(f"👤 Login: admin")
            print(f"🔑 Password: admin")
            print(f"🏆 Fonctionnalité: Profils et badges complets")
            print(f"🔄 Pour arrêter: Ctrl+C")
            print()
            
            httpd.serve_forever()
            
    except OSError as e:
        if e.errno == 98:
            print(f"❌ Port {PORT} déjà utilisé")
            print("🔄 Arrêtez les autres processus ou changez de port")
        else:
            print(f"❌ Erreur: {e}")
        sys.exit(1)
    except KeyboardInterrupt:
        print("\n🛑 Serveur arrêté")
        print("👋 Merci d'avoir testé Sama Jokoo avec profils !")
        sys.exit(0)

if __name__ == "__main__":
    main()
EOF

chmod +x serve_profiles_app.py

echo -e "${GREEN}✅ Serveur créé${NC}"

echo -e "${BLUE}4. Démarrage du serveur avec profils...${NC}"

echo ""
echo -e "${PURPLE}👤 SAMA JOKOO AVEC PROFILS UTILISATEURS${NC}"
echo ""
echo -e "${GREEN}Informations :${NC}"
echo -e "  📱 Application : ${BLUE}http://localhost:3000${NC}"
echo -e "  👤 Fonctionnalité : ${BLUE}Profils utilisateurs complets${NC}"
echo -e "  🏆 Nouveauté : ${BLUE}Système de badges et réalisations${NC}"
echo -e "  📊 Statistiques : ${BLUE}Métriques détaillées${NC}"
echo -e "  👤 Login : ${BLUE}admin${NC}"
echo -e "  🔑 Mot de passe : ${BLUE}admin${NC}"
echo ""
echo -e "${YELLOW}Fonctionnalités des profils :${NC}"
echo -e "  ✨ Design neumorphique cohérent"
echo -e "  👤 Profil utilisateur complet avec avatar"
echo -e "  📊 Statistiques détaillées et graphiques"
echo -e "  🏆 Système de badges et réalisations"
echo -e "  📝 Historique des posts et activités"
echo -e "  💬 Commentaires et interactions sociales"
echo -e "  📱 Interface responsive multi-onglets"
echo ""
echo -e "${BLUE}Navigation :${NC}"
echo -e "  📝 ${GREEN}Feed${NC} - Flux principal avec posts et commentaires"
echo -e "  👤 ${GREEN}Mon Profil${NC} - Informations personnelles et édition"
echo -e "  📊 ${GREEN}Statistiques${NC} - Métriques détaillées d'activité"
echo -e "  🏆 ${GREEN}Badges${NC} - Réalisations et objectifs"
echo ""
echo -e "${BLUE}Instructions d'utilisation :${NC}"
echo -e "  1. ${GREEN}Naviguez${NC} entre les onglets avec les boutons du haut"
echo -e "  2. ${GREEN}Créez des posts${NC} dans l'onglet Feed"
echo -e "  3. ${GREEN}Consultez votre profil${NC} dans l'onglet Mon Profil"
echo -e "  4. ${GREEN}Suivez vos statistiques${NC} dans l'onglet Statistiques"
echo -e "  5. ${GREEN}Débloquez des badges${NC} en étant actif sur l'application"
echo ""
echo -e "${BLUE}Pour arrêter : Ctrl+C${NC}"
echo ""

# Démarrer le serveur
python3 serve_profiles_app.py