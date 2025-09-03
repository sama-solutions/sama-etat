#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Script pour corriger le format des images dans Odoo
"""

import os
import sys
import base64
import psycopg2
from pathlib import Path

def fix_image_format():
    """Corrige le format des images pour Odoo"""
    
    # Configuration base de données
    db_config = {
        'host': 'localhost',
        'database': 'sama_carte_demo',
        'user': 'odoo',
        'password': 'odoo',
        'port': 5432
    }
    
    print("=== CORRECTION FORMAT IMAGES ===")
    print()
    
    try:
        # Connexion à la base
        conn = psycopg2.connect(**db_config)
        cursor = conn.cursor()
        
        # Récupérer tous les membres avec images
        cursor.execute("""
            SELECT id, name, image_1920 
            FROM membership_member 
            WHERE image_1920 IS NOT NULL
            ORDER BY id;
        """)
        
        members = cursor.fetchall()
        print(f"📊 {len(members)} membres avec images trouvés")
        print()
        
        for member_id, name, image_data in members:
            try:
                # Décoder l'image actuelle
                if isinstance(image_data, memoryview):
                    image_data = bytes(image_data)
                
                # Si c'est déjà du binaire, on l'encode en base64
                if isinstance(image_data, bytes):
                    # Vérifier si c'est déjà du base64
                    try:
                        # Tenter de décoder comme base64
                        decoded = base64.b64decode(image_data)
                        # Si ça marche, c'est déjà en base64
                        print(f"✅ {name}: Image déjà en base64")
                        continue
                    except:
                        # Si ça échoue, c'est du binaire brut
                        image_base64 = base64.b64encode(image_data).decode('utf-8')
                        print(f"🔄 {name}: Conversion binaire -> base64")
                else:
                    # C'est déjà une string base64
                    image_base64 = image_data
                    print(f"✅ {name}: Image déjà en format string")
                
                # Mettre à jour avec le bon format
                cursor.execute("""
                    UPDATE membership_member 
                    SET image_1920 = %s 
                    WHERE id = %s
                """, (image_base64, member_id))
                
            except Exception as e:
                print(f"❌ Erreur pour {name}: {e}")
        
        # Valider les changements
        conn.commit()
        print()
        print("💾 Changements sauvegardés")
        
        cursor.close()
        conn.close()
        
        return True
        
    except Exception as e:
        print(f"❌ Erreur: {e}")
        return False

def test_image_access():
    """Teste l'accès aux images via l'API Odoo"""
    
    print()
    print("=== TEST ACCÈS IMAGES VIA API ===")
    
    # Test avec curl pour vérifier l'accès aux images
    import subprocess
    
    try:
        # Récupérer un token de test
        db_config = {
            'host': 'localhost',
            'database': 'sama_carte_demo',
            'user': 'odoo',
            'password': 'odoo',
            'port': 5432
        }
        
        conn = psycopg2.connect(**db_config)
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT id, access_token FROM membership_member 
            WHERE access_token IS NOT NULL 
            LIMIT 1;
        """)
        
        result = cursor.fetchone()
        if result:
            member_id, token = result
            
            # Test de la page publique
            cmd = f"curl -s http://localhost:8071/member/{token}"
            result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
            
            if result.returncode == 0:
                html_content = result.stdout
                if 'image_1920' in html_content:
                    print("✅ Page publique accessible et contient des références aux images")
                else:
                    print("⚠️  Page publique accessible mais pas de références aux images")
                
                # Sauvegarder pour inspection
                with open('/tmp/test_page.html', 'w') as f:
                    f.write(html_content)
                print("📄 Page sauvegardée dans /tmp/test_page.html")
            else:
                print("❌ Impossible d'accéder à la page publique")
        
        cursor.close()
        conn.close()
        
    except Exception as e:
        print(f"❌ Erreur test API: {e}")

if __name__ == "__main__":
    if fix_image_format():
        print("✅ Format des images corrigé!")
        test_image_access()
    else:
        print("❌ Échec de la correction")
        sys.exit(1)