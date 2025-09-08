#!/bin/bash

# Script de diagnostic et correction des commentaires
# ==================================================

echo "🔧 Diagnostic et correction du système de commentaires"
echo "====================================================="

# Couleurs
GREEN='\033[0;32m'
RED='\033[0;31m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m'

echo -e "${BLUE}1. Diagnostic des processus...${NC}"

# Vérifier les processus Python
PYTHON_PROCS=$(ps aux | grep python3 | grep -v grep | grep -v "networkd\|unattended")
if [ -n "$PYTHON_PROCS" ]; then
    echo -e "${GREEN}Processus Python détectés :${NC}"
    echo "$PYTHON_PROCS"
else
    echo -e "${YELLOW}Aucun processus Python de l'application détecté${NC}"
fi

echo -e "${BLUE}2. Vérification des ports...${NC}"

# Vérifier le port 3000
PORT_3000=$(lsof -i :3000 2>/dev/null)
if [ -n "$PORT_3000" ]; then
    echo -e "${GREEN}Port 3000 occupé :${NC}"
    echo "$PORT_3000"
else
    echo -e "${YELLOW}Port 3000 libre${NC}"
fi

echo -e "${BLUE}3. Test de connectivité...${NC}"

# Test de connexion
HTTP_CODE=$(curl -s -o /dev/null -w "%{http_code}" --connect-timeout 3 http://localhost:3000 2>/dev/null)
if [ "$HTTP_CODE" = "200" ]; then
    echo -e "${GREEN}✅ Serveur accessible (HTTP $HTTP_CODE)${NC}"
elif [ "$HTTP_CODE" = "000" ]; then
    echo -e "${RED}❌ Serveur non accessible (connexion refusée)${NC}"
else
    echo -e "${YELLOW}⚠️ Serveur répond avec code HTTP $HTTP_CODE${NC}"
fi

echo -e "${BLUE}4. Vérification des fichiers...${NC}"

FILES_TO_CHECK=(
    "sama_jokoo_with_comments.html"
    "serve_comments_app.py"
    "start_comments_app.sh"
)

for file in "${FILES_TO_CHECK[@]}"; do
    if [ -f "$file" ]; then
        SIZE=$(stat -c%s "$file")
        echo -e "${GREEN}✅ $file (${SIZE} bytes)${NC}"
    else
        echo -e "${RED}❌ $file manquant${NC}"
    fi
done

echo -e "${BLUE}5. Correction automatique...${NC}"

# Arrêter tous les processus liés
echo -e "${YELLOW}Arrêt des processus existants...${NC}"
pkill -f "serve_app.py" 2>/dev/null
pkill -f "serve_comments_app.py" 2>/dev/null
pkill -f "python3.*serve" 2>/dev/null
sleep 3

# Créer un serveur de test ultra-simple
echo -e "${YELLOW}Création d'un serveur de test simple...${NC}"

cat > test_server_simple.py << 'EOF'
#!/usr/bin/env python3
import http.server
import socketserver
import sys

PORT = 3000

class TestHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/' or self.path == '/index.html':
            self.send_response(200)
            self.send_header('Content-type', 'text/html; charset=utf-8')
            self.end_headers()
            
            html = '''<!DOCTYPE html>
<html><head><title>Test Sama Jokoo</title></head>
<body style="font-family: Arial; text-align: center; padding: 50px;">
<h1>🎨 Sama Jokoo - Test Serveur</h1>
<p>✅ Le serveur fonctionne correctement !</p>
<p>🔧 Port: 3000</p>
<p>📱 URL: http://localhost:3000</p>
</body></html>'''
            
            self.wfile.write(html.encode('utf-8'))
        else:
            self.send_response(404)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(b'<h1>404 - Not Found</h1>')

try:
    with socketserver.TCPServer(("", PORT), TestHandler) as httpd:
        print(f"🚀 Serveur de test démarré sur http://localhost:{PORT}")
        httpd.serve_forever()
except KeyboardInterrupt:
    print("\n🛑 Serveur arrêté")
except Exception as e:
    print(f"❌ Erreur: {e}")
    sys.exit(1)
EOF

chmod +x test_server_simple.py

echo -e "${BLUE}6. Démarrage du serveur de test...${NC}"

echo ""
echo -e "${GREEN}🚀 SERVEUR DE TEST SAMA JOKOO${NC}"
echo ""
echo -e "${GREEN}Informations :${NC}"
echo -e "  📱 URL de test : ${BLUE}http://localhost:3000${NC}"
echo -e "  🔧 Type : ${BLUE}Serveur Python simple${NC}"
echo -e "  🎯 Objectif : ${BLUE}Vérifier la connectivité${NC}"
echo ""
echo -e "${YELLOW}Si ce serveur fonctionne, le problème vient de l'application complexe.${NC}"
echo -e "${YELLOW}Sinon, il y a un problème de réseau ou de port.${NC}"
echo ""
echo -e "${BLUE}Pour arrêter : Ctrl+C${NC}"
echo ""

# Démarrer le serveur de test
python3 test_server_simple.py