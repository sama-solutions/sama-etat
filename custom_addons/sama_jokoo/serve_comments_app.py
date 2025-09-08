#!/usr/bin/env python3
"""
Serveur pour Sama Jokoo avec système de commentaires
"""

import http.server
import socketserver
import webbrowser
import os
import sys

PORT = 3000

class SamaJokooCommentsHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/' or self.path == '/index.html':
            # Servir le fichier HTML avec commentaires
            self.send_response(200)
            self.send_header('Content-type', 'text/html; charset=utf-8')
            self.send_header('Cache-Control', 'no-cache')
            self.end_headers()
            
            try:
                with open('sama_jokoo_with_comments.html', 'r', encoding='utf-8') as f:
                    content = f.read()
                self.wfile.write(content.encode('utf-8'))
            except FileNotFoundError:
                self.wfile.write(b'<h1>Erreur: fichier sama_jokoo_with_comments.html non trouve</h1>')
        else:
            # 404 pour les autres chemins
            self.send_response(404)
            self.send_header('Content-type', 'text/html; charset=utf-8')
            self.end_headers()
            self.wfile.write(b'<h1>404 - Page non trouvee</h1>')

def main():
    print("🎨 Serveur Sama Jokoo avec Commentaires")
    print("=" * 40)
    
    try:
        with socketserver.TCPServer(("", PORT), SamaJokooCommentsHandler) as httpd:
            print(f"✅ Serveur démarré avec succès !")
            print(f"📱 URL: http://localhost:{PORT}")
            print(f"🎯 Application: Sama Jokoo Neumorphique avec Commentaires")
            print(f"👤 Login: admin")
            print(f"🔑 Password: admin")
            print(f"💬 Fonctionnalité: Système de commentaires complet")
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
        print("👋 Merci d'avoir testé Sama Jokoo avec commentaires !")
        sys.exit(0)

if __name__ == "__main__":
    main()