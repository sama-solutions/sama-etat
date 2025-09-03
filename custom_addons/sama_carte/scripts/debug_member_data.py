#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Script pour déboguer les données du membre
"""

import os
import sys
import base64
import psycopg2

def debug_member_data():
    """Debug les données du membre"""
    
    # Configuration base de données
    db_config = {
        'host': 'localhost',
        'database': 'sama_carte_demo',
        'user': 'odoo',
        'password': 'odoo',
        'port': 5432
    }
    
    print("=== DEBUG DONNÉES MEMBRE ===")
    print()
    
    try:
        # Connexion à la base
        conn = psycopg2.connect(**db_config)
        cursor = conn.cursor()
        
        # Récupérer le premier membre
        cursor.execute("""
            SELECT id, name, access_token, image_1920, 
                   CASE WHEN image_1920 IS NOT NULL THEN 'OUI' ELSE 'NON' END as has_image,
                   LENGTH(image_1920) as image_size
            FROM membership_member 
            ORDER BY id LIMIT 1;
        """)
        
        result = cursor.fetchone()
        if result:
            member_id, name, token, image_data, has_image, size = result
            
            print(f"ID: {member_id}")
            print(f"Nom: {name}")
            print(f"Token: {token}")
            print(f"A une image: {has_image}")
            print(f"Taille image: {size} bytes")
            print()
            
            if image_data:
                # Vérifier le type de données
                print(f"Type de données image: {type(image_data)}")
                
                if isinstance(image_data, memoryview):
                    image_data = bytes(image_data)
                    print("Conversion memoryview -> bytes")
                
                if isinstance(image_data, bytes):
                    # Tenter de décoder comme base64
                    try:
                        decoded = base64.b64decode(image_data)
                        print(f"✅ Décodage base64 réussi: {len(decoded)} bytes")
                        
                        # Vérifier le format
                        if decoded.startswith(b'\xff\xd8\xff'):
                            print("✅ Format JPEG détecté")
                        elif decoded.startswith(b'\x89PNG'):
                            print("✅ Format PNG détecté")
                        else:
                            print("⚠️  Format non reconnu")
                            print(f"Premiers bytes: {decoded[:20].hex()}")
                        
                        # Créer un data URI pour test
                        data_uri = f"data:image/jpeg;base64,{image_data.decode('utf-8')}"
                        print(f"Data URI créé: {len(data_uri)} caractères")
                        print(f"Début: {data_uri[:100]}...")
                        
                    except Exception as e:
                        print(f"❌ Erreur décodage base64: {e}")
                        # Peut-être que c'est déjà du binaire
                        if image_data.startswith(b'\xff\xd8\xff'):
                            print("✅ Image JPEG en binaire brut détectée")
                            # Encoder en base64
                            encoded = base64.b64encode(image_data).decode('utf-8')
                            print(f"Encodage en base64: {len(encoded)} caractères")
                        else:
                            print(f"Format inconnu, premiers bytes: {image_data[:20].hex()}")
                
                elif isinstance(image_data, str):
                    print(f"Image stockée comme string: {len(image_data)} caractères")
                    print(f"Début: {image_data[:100]}...")
                    
                    # Tenter de décoder
                    try:
                        decoded = base64.b64decode(image_data)
                        print(f"✅ Décodage string base64 réussi: {len(decoded)} bytes")
                    except Exception as e:
                        print(f"❌ Erreur décodage string: {e}")
            
            print()
            print("=== TEST TEMPLATE ===")
            
            # Simuler la condition du template
            if image_data:
                print("✅ Condition t-if=\"member.image_1920\" serait VRAIE")
            else:
                print("❌ Condition t-if=\"member.image_1920\" serait FAUSSE")
        
        cursor.close()
        conn.close()
        
        return True
        
    except Exception as e:
        print(f"❌ Erreur: {e}")
        return False

if __name__ == "__main__":
    debug_member_data()