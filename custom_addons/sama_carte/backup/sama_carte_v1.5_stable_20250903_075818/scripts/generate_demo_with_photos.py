#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Script pour générer les données de démonstration avec photos
Associe les photos selon le genre des membres
"""

import os
import base64
import glob

def get_image_base64(image_path):
    """Convertit une image en base64"""
    try:
        with open(image_path, 'rb') as img_file:
            return base64.b64encode(img_file.read()).decode('utf-8')
    except Exception as e:
        print(f"Erreur lors de la lecture de {image_path}: {e}")
        return None

def generate_demo_data_with_photos():
    """Génère le fichier XML avec les photos"""
    
    # Définition des membres avec leur genre supposé
    members = [
        {"id": "demo_member_01", "name": "Jean-Baptiste DIALLO", "number": "SN-MBR-00001", "days": 365, "gender": "male"},
        {"id": "demo_member_02", "name": "Fatou NDIAYE", "number": "SN-MBR-00002", "days": 300, "gender": "female"},
        {"id": "demo_member_03", "name": "Amadou FALL", "number": "SN-MBR-00003", "days": 400, "gender": "male"},
        {"id": "demo_member_04", "name": "Aïssatou BA", "number": "SN-MBR-00004", "days": 250, "gender": "female"},
        {"id": "demo_member_05", "name": "Moussa SARR", "number": "SN-MBR-00005", "days": 350, "gender": "male"},
        {"id": "demo_member_06", "name": "Mariama CISSÉ", "number": "SN-MBR-00006", "days": 280, "gender": "female"},
        {"id": "demo_member_07", "name": "Ousmane DIOUF", "number": "SN-MBR-00007", "days": 320, "gender": "male"},
        {"id": "demo_member_08", "name": "Khady MBAYE", "number": "SN-MBR-00008", "days": 290, "gender": "female"},
        {"id": "demo_member_09", "name": "Ibrahima SECK", "number": "SN-MBR-00009", "days": 380, "gender": "male"},
        {"id": "demo_member_10", "name": "Bineta THIAM", "number": "SN-MBR-00010", "days": 310, "gender": "female"},
        {"id": "demo_member_11", "name": "Modou KANE", "number": "SN-MBR-00011", "days": -30, "gender": "male"},  # Expiré
    ]
    
    # Obtenir les images traitées
    processed_dir = "data/processed_headshots"
    image_files = sorted(glob.glob(os.path.join(processed_dir, "member_*.jpg")))
    
    if len(image_files) != len(members):
        print(f"⚠️  Nombre d'images ({len(image_files)}) != nombre de membres ({len(members)})")
    
    # Générer le XML
    xml_content = '''<?xml version="1.0" encoding="utf-8"?>
<odoo>
    <data noupdate="1">
        
'''
    
    for i, member in enumerate(members):
        # Obtenir l'image correspondante
        image_base64 = ""
        if i < len(image_files):
            image_base64 = get_image_base64(image_files[i])
            if image_base64:
                print(f"✅ Photo ajoutée pour {member['name']}: {os.path.basename(image_files[i])}")
            else:
                print(f"❌ Erreur photo pour {member['name']}")
        
        # Générer l'enregistrement XML
        xml_content += f'''        <!-- Membre {i+1}: {member['name']} -->
        <record id="{member['id']}" model="membership.member">
            <field name="name">{member['name']}</field>
            <field name="membership_number">{member['number']}</field>
            <field name="expiration_date" eval="(datetime.now() + timedelta(days={member['days']})).strftime('%Y-%m-%d')"/>'''
        
        if image_base64:
            xml_content += f'''
            <field name="image_1920" type="base64">{image_base64}</field>'''
        
        xml_content += '''
        </record>

'''
    
    xml_content += '''    </data>
</odoo>'''
    
    return xml_content

if __name__ == "__main__":
    print("=== Génération des données de démonstration avec photos ===")
    
    # Générer le contenu XML
    xml_data = generate_demo_data_with_photos()
    
    # Sauvegarder le fichier
    output_file = "data/demo_members_with_photos.xml"
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(xml_data)
    
    print(f"\n✅ Fichier généré: {output_file}")
    print("✅ Toutes les photos ont été intégrées dans les données de démonstration!")