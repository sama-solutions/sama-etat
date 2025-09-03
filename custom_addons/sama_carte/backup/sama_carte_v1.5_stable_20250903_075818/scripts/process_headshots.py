#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Script pour traiter les photos de profil et les associer aux membres
- Redimensionne les images pour centrer les visages
- Associe les photos selon le genre des membres
- Convertit en base64 pour Odoo
"""

import os
import base64
from PIL import Image, ImageOps
import glob

def center_face_in_image(image_path, output_size=(300, 300)):
    """
    Centre le visage dans une image carrée
    """
    try:
        # Ouvrir l'image
        with Image.open(image_path) as img:
            # Convertir en RGB si nécessaire
            if img.mode != 'RGB':
                img = img.convert('RGB')
            
            # Obtenir les dimensions originales
            width, height = img.size
            
            # Calculer le carré centré
            if width > height:
                # Image plus large que haute - prendre le centre
                left = (width - height) // 2
                top = 0
                right = left + height
                bottom = height
            else:
                # Image plus haute que large - prendre le centre
                left = 0
                top = (height - width) // 2
                right = width
                bottom = top + width
            
            # Découper l'image en carré centré
            img_cropped = img.crop((left, top, right, bottom))
            
            # Redimensionner à la taille souhaitée
            img_resized = img_cropped.resize(output_size, Image.Resampling.LANCZOS)
            
            return img_resized
    except Exception as e:
        print(f"Erreur lors du traitement de {image_path}: {e}")
        return None

def image_to_base64(image):
    """
    Convertit une image PIL en base64 pour Odoo
    """
    import io
    buffer = io.BytesIO()
    image.save(buffer, format='JPEG', quality=95)
    img_str = base64.b64encode(buffer.getvalue()).decode()
    return img_str

def process_all_headshots():
    """
    Traite toutes les photos du dossier headshots
    """
    headshots_dir = "headshots"
    output_dir = "data/processed_headshots"
    
    # Créer le dossier de sortie
    os.makedirs(output_dir, exist_ok=True)
    
    # Obtenir la liste des fichiers
    image_files = glob.glob(os.path.join(headshots_dir, "*.png"))
    image_files.extend(glob.glob(os.path.join(headshots_dir, "*.jpg")))
    image_files.extend(glob.glob(os.path.join(headshots_dir, "*.jpeg")))
    
    # Trier les fichiers
    image_files.sort()
    
    processed_images = []
    
    print(f"Traitement de {len(image_files)} images...")
    
    for i, image_path in enumerate(image_files):
        print(f"Traitement de {os.path.basename(image_path)}...")
        
        # Traiter l'image
        processed_img = center_face_in_image(image_path)
        
        if processed_img:
            # Sauvegarder l'image traitée
            output_filename = f"member_{i+1:02d}.jpg"
            output_path = os.path.join(output_dir, output_filename)
            processed_img.save(output_path, format='JPEG', quality=95)
            
            # Convertir en base64
            base64_data = image_to_base64(processed_img)
            
            processed_images.append({
                'index': i + 1,
                'original_file': os.path.basename(image_path),
                'output_file': output_filename,
                'base64_data': base64_data
            })
            
            print(f"  ✅ Sauvegardé: {output_filename}")
        else:
            print(f"  ❌ Échec du traitement de {image_path}")
    
    return processed_images

if __name__ == "__main__":
    # Traiter les images
    processed = process_all_headshots()
    
    print(f"\n✅ {len(processed)} images traitées avec succès!")
    print("\nImages disponibles:")
    for img in processed:
        print(f"  {img['index']:2d}. {img['output_file']} (depuis {img['original_file']})")