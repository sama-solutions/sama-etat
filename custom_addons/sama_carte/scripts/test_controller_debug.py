#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Script pour tester le contrôleur directement
"""

import requests
import psycopg2

def test_controller():
    """Test le contrôleur directement"""
    
    # Configuration base de données
    db_config = {
        'host': 'localhost',
        'database': 'sama_carte_demo',
        'user': 'odoo',
        'password': 'odoo',
        'port': 5432
    }
    
    print("=== TEST CONTRÔLEUR ===")
    print()
    
    try:
        # Connexion à la base
        conn = psycopg2.connect(**db_config)
        cursor = conn.cursor()
        
        # Récupérer un token
        cursor.execute("SELECT access_token, name FROM membership_member LIMIT 1;")
        result = cursor.fetchone()
        
        if result:
            token, name = result
            print(f"Token: {token}")
            print(f"Nom: {name}")
            
            # Tester la page
            url = f"http://localhost:8071/member/{token}"
            print(f"URL: {url}")
            
            response = requests.get(url)
            print(f"Status: {response.status_code}")
            
            if response.status_code == 200:
                html = response.text
                
                # Chercher les éléments clés
                if 'member-photo' in html:
                    print("✅ CSS member-photo trouvé")
                else:
                    print("❌ CSS member-photo non trouvé")
                
                if 'data:image/jpeg' in html:
                    print("✅ Data URI image trouvé")
                else:
                    print("❌ Data URI image non trouvé")
                
                if 'placeholder.png' in html:
                    print("⚠️  Image placeholder utilisée")
                else:
                    print("✅ Pas d'image placeholder")
                
                if name in html:
                    print(f"✅ Nom '{name}' trouvé dans la page")
                else:
                    print(f"❌ Nom '{name}' non trouvé")
                
                # Sauvegarder pour inspection
                with open('/tmp/controller_test.html', 'w') as f:
                    f.write(html)
                print("📄 Page sauvegardée dans /tmp/controller_test.html")
                
                # Chercher spécifiquement la section image
                import re
                img_pattern = r'<img[^>]*class="member-photo"[^>]*>'
                matches = re.findall(img_pattern, html)
                
                print(f"\n🔍 Images member-photo trouvées: {len(matches)}")
                for i, match in enumerate(matches):
                    print(f"  {i+1}: {match}")
            
            else:
                print(f"❌ Erreur HTTP: {response.status_code}")
        
        cursor.close()
        conn.close()
        
    except Exception as e:
        print(f"❌ Erreur: {e}")

if __name__ == "__main__":
    test_controller()