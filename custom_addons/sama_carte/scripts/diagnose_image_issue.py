#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Script de diagnostic pour les problèmes d'affichage des images
"""

import os
import sys
import base64
import psycopg2
from pathlib import Path

def diagnose_image_issue():
    """Diagnostique les problèmes d'affichage des images"""
    
    # Configuration base de données
    db_config = {
        'host': 'localhost',
        'database': 'sama_carte_demo',
        'user': 'odoo',
        'password': 'odoo',
        'port': 5432
    }
    
    print("=== DIAGNOSTIC PROBLÈME IMAGES ===")
    print()
    
    try:
        # Connexion à la base
        conn = psycopg2.connect(**db_config)
        cursor = conn.cursor()
        
        # 1. Vérifier la structure de la table
        print("1. STRUCTURE DE LA TABLE")
        print("========================")
        cursor.execute("""
            SELECT column_name, data_type, is_nullable 
            FROM information_schema.columns 
            WHERE table_name = 'membership_member' 
            AND column_name LIKE '%image%'
            ORDER BY column_name;
        """)
        
        image_columns = cursor.fetchall()
        if image_columns:
            for col_name, data_type, nullable in image_columns:
                print(f"✅ Colonne: {col_name} | Type: {data_type} | Nullable: {nullable}")
        else:
            print("❌ Aucune colonne image trouvée")
            return False
        
        print()
        
        # 2. Vérifier les données
        print("2. DONNÉES IMAGES")
        print("=================")
        cursor.execute("""
            SELECT id, name, 
                   CASE WHEN image_1920 IS NOT NULL THEN 'OUI' ELSE 'NON' END as has_image,
                   LENGTH(image_1920) as image_size,
                   LEFT(ENCODE(image_1920, 'base64'), 50) as image_preview
            FROM membership_member 
            ORDER BY id LIMIT 3;
        """)
        
        members = cursor.fetchall()
        for member_id, name, has_image, size, preview in members:
            print(f"ID: {member_id} | {name}")
            print(f"   Image: {has_image} | Taille: {size} bytes")
            if preview:
                print(f"   Aperçu: {preview}...")
            print()
        
        # 3. Vérifier les tokens d'accès
        print("3. TOKENS D'ACCÈS")
        print("=================")
        cursor.execute("""
            SELECT id, name, access_token 
            FROM membership_member 
            WHERE access_token IS NOT NULL 
            ORDER BY id LIMIT 3;
        """)
        
        tokens = cursor.fetchall()
        for member_id, name, token in tokens:
            print(f"ID: {member_id} | {name} | Token: {token[:8]}...")
        
        print()
        
        # 4. Test de décodage d'une image
        print("4. TEST DÉCODAGE IMAGE")
        print("======================")
        cursor.execute("""
            SELECT image_1920 FROM membership_member 
            WHERE image_1920 IS NOT NULL 
            LIMIT 1;
        """)
        
        result = cursor.fetchone()
        if result and result[0]:
            image_data = result[0]
            try:
                # Tenter de décoder l'image
                decoded = base64.b64decode(image_data)
                print(f"✅ Image décodée avec succès: {len(decoded)} bytes")
                
                # Vérifier le format
                if decoded.startswith(b'\xff\xd8\xff'):
                    print("✅ Format JPEG détecté")
                elif decoded.startswith(b'\x89PNG'):
                    print("✅ Format PNG détecté")
                else:
                    print("⚠️  Format d'image non reconnu")
                    print(f"   Premiers bytes: {decoded[:10].hex()}")
                
            except Exception as e:
                print(f"❌ Erreur de décodage: {e}")
        else:
            print("❌ Aucune image trouvée pour le test")
        
        print()
        
        # 5. Vérifier les champs calculés
        print("5. CHAMPS CALCULÉS")
        print("==================")
        cursor.execute("""
            SELECT id, name, card_status, 
                   CASE WHEN barcode_qr IS NOT NULL THEN 'OUI' ELSE 'NON' END as has_qr
            FROM membership_member 
            ORDER BY id LIMIT 3;
        """)
        
        computed_fields = cursor.fetchall()
        for member_id, name, status, has_qr in computed_fields:
            print(f"ID: {member_id} | {name} | Statut: {status} | QR: {has_qr}")
        
        cursor.close()
        conn.close()
        
        print()
        print("=== RECOMMANDATIONS ===")
        print()
        
        # Recommandations basées sur les résultats
        if not image_columns:
            print("❌ PROBLÈME: Colonne image_1920 manquante")
            print("   Solution: Exécuter la mise à jour du module")
            print("   Commande: odoo-bin -d sama_carte_demo -u sama_carte --stop-after-init")
        
        elif not any(size > 0 for _, _, _, size, _ in members if size):
            print("❌ PROBLÈME: Aucune image en base")
            print("   Solution: Relancer le script d'ajout des photos")
            print("   Commande: python3 scripts/add_photos_to_members.py")
        
        else:
            print("✅ DONNÉES OK: Images présentes en base")
            print()
            print("🔍 VÉRIFICATIONS SUPPLÉMENTAIRES:")
            print("   1. Redémarrer Odoo pour recharger le modèle")
            print("   2. Vider le cache du navigateur")
            print("   3. Vérifier les permissions d'accès aux images")
            print("   4. Tester en mode développeur Odoo")
        
        return True
        
    except Exception as e:
        print(f"❌ Erreur: {e}")
        return False

if __name__ == "__main__":
    diagnose_image_issue()