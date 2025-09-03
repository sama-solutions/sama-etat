#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Script pour ajouter des photos aux membres existants dans la base de données
"""

import os
import sys
import base64
import psycopg2
from pathlib import Path

def add_photos_to_members():
    """Ajoute les photos aux membres existants"""
    
    # Configuration base de données
    db_config = {
        'host': 'localhost',
        'database': 'sama_carte_demo',
        'user': 'odoo',
        'password': 'odoo',
        'port': 5432
    }
    
    # Dossier des photos traitées
    photos_dir = Path("data/processed_headshots")
    
    if not photos_dir.exists():
        print(f"❌ Dossier {photos_dir} non trouvé")
        return False
    
    # Liste des photos
    photo_files = sorted([f for f in photos_dir.glob("*.jpg")])
    
    if not photo_files:
        print(f"❌ Aucune photo trouvée dans {photos_dir}")
        return False
    
    print(f"📁 {len(photo_files)} photos trouvées")
    
    try:
        # Connexion à la base
        conn = psycopg2.connect(**db_config)
        cursor = conn.cursor()
        
        # Récupérer les membres existants
        cursor.execute("""
            SELECT id, name, membership_number 
            FROM membership_member 
            ORDER BY membership_number
        """)
        
        members = cursor.fetchall()
        print(f"👥 {len(members)} membres trouvés en base")
        
        # Associer photos aux membres
        for i, (member_id, name, number) in enumerate(members):
            if i < len(photo_files):
                photo_file = photo_files[i]
                
                # Lire et encoder la photo
                with open(photo_file, 'rb') as f:
                    photo_data = f.read()
                    photo_base64 = base64.b64encode(photo_data).decode('utf-8')
                
                # Mettre à jour le membre
                cursor.execute("""
                    UPDATE membership_member 
                    SET image_1920 = %s 
                    WHERE id = %s
                """, (photo_base64, member_id))
                
                print(f"✅ Photo ajoutée pour {name} ({number}) - {photo_file.name}")
            else:
                print(f"⚠️  Pas de photo pour {name} ({number})")
        
        # Valider les changements
        conn.commit()
        print(f"💾 Changements sauvegardés")
        
        # Vérifier les résultats
        cursor.execute("""
            SELECT COUNT(*) FROM membership_member WHERE image_1920 IS NOT NULL
        """)
        count_with_photos = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM membership_member")
        total_members = cursor.fetchone()[0]
        
        print(f"📊 Résultat: {count_with_photos}/{total_members} membres avec photos")
        
        cursor.close()
        conn.close()
        
        return True
        
    except Exception as e:
        print(f"❌ Erreur: {e}")
        return False

if __name__ == "__main__":
    print("=== Ajout des photos aux membres ===")
    
    if add_photos_to_members():
        print("✅ Photos ajoutées avec succès!")
    else:
        print("❌ Échec de l'ajout des photos")
        sys.exit(1)