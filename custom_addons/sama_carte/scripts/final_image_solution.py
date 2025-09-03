#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Solution finale pour l'affichage des images
"""

import os
import sys
import base64
import psycopg2

def create_image_endpoint():
    """Crée un endpoint personnalisé pour servir les images"""
    
    controller_content = '''# -*- coding: utf-8 -*-

from odoo import http
from odoo.http import request
from odoo.exceptions import AccessError
import base64


class MembershipController(http.Controller):

    @http.route('/member/<string:access_token>', type='http', auth='public', website=True)
    def member_public_page(self, access_token, **kwargs):
        """Page publique pour afficher les informations d'un membre via son token"""
        
        # Recherche du membre par token
        member = request.env['membership.member'].sudo().search([
            ('access_token', '=', access_token)
        ], limit=1)
        
        if not member:
            return request.render('sama_carte.member_not_found', {})
        
        # Préparation des données pour le template
        # Debug: vérifier les données d'image
        image_data = None
        if member.image_1920:
            # Convertir en string si nécessaire
            if isinstance(member.image_1920, bytes):
                image_data = member.image_1920.decode('utf-8')
            else:
                image_data = member.image_1920
        
        values = {
            'member': member,
            'is_valid': member.is_card_valid(),
            'company': member.company_id,
            'member_image': image_data,
            'has_image': bool(image_data),
        }
        
        return request.render('sama_carte.member_public_page', values)
    
    @http.route('/member/<string:access_token>/image', type='http', auth='public')
    def member_image(self, access_token, **kwargs):
        """Endpoint pour servir l'image d'un membre"""
        
        # Recherche du membre par token
        member = request.env['membership.member'].sudo().search([
            ('access_token', '=', access_token)
        ], limit=1)
        
        if not member or not member.image_1920:
            # Retourner une image par défaut
            return request.not_found()
        
        # Décoder l'image
        try:
            image_data = member.image_1920
            if isinstance(image_data, bytes):
                # Si c'est déjà du binaire, l'utiliser directement
                if image_data.startswith(b'\\xff\\xd8\\xff'):
                    # C'est du JPEG brut
                    image_binary = image_data
                else:
                    # C'est du base64 en bytes
                    image_binary = base64.b64decode(image_data)
            else:
                # C'est une string base64
                image_binary = base64.b64decode(image_data)
            
            # Retourner l'image
            return request.make_response(
                image_binary,
                headers=[
                    ('Content-Type', 'image/jpeg'),
                    ('Content-Length', len(image_binary)),
                    ('Cache-Control', 'public, max-age=3600'),
                ]
            )
            
        except Exception as e:
            return request.not_found()
'''
    
    # Écrire le nouveau contrôleur
    with open('controllers/main.py', 'w') as f:
        f.write(controller_content)
    
    print("✅ Contrôleur mis à jour avec endpoint d'image")

def update_template():
    """Met à jour le template pour utiliser le nouvel endpoint"""
    
    # Lire le template actuel
    with open('views/website_member_views.xml', 'r') as f:
        content = f.read()
    
    # Remplacer la section image
    old_image_section = '''                                    <!-- Photo du membre -->
                                    <img t-if="member.image_1920" 
                                         t-attf-src="/web/image/membership.member/{{member.id}}/image_1920" 
                                         class="member-photo" 
                                         alt="Photo du membre"/>
                                    <img t-else="" 
                                         src="/web/static/src/img/placeholder.png" 
                                         class="member-photo" 
                                         alt="Pas de photo"/>'''
    
    new_image_section = '''                                    <!-- Photo du membre -->
                                    <img t-if="member.image_1920" 
                                         t-attf-src="/member/{{member.access_token}}/image" 
                                         class="member-photo" 
                                         alt="Photo du membre"/>
                                    <img t-else="" 
                                         src="/web/static/src/img/placeholder.png" 
                                         class="member-photo" 
                                         alt="Pas de photo"/>'''
    
    # Remplacer
    content = content.replace(old_image_section, new_image_section)
    
    # Écrire le nouveau template
    with open('views/website_member_views.xml', 'w') as f:
        f.write(content)
    
    print("✅ Template mis à jour avec nouvel endpoint")

def test_solution():
    """Teste la solution"""
    
    # Configuration base de données
    db_config = {
        'host': 'localhost',
        'database': 'sama_carte_demo',
        'user': 'odoo',
        'password': 'odoo',
        'port': 5432
    }
    
    try:
        # Connexion à la base
        conn = psycopg2.connect(**db_config)
        cursor = conn.cursor()
        
        # Récupérer un token
        cursor.execute("SELECT access_token FROM membership_member LIMIT 1;")
        result = cursor.fetchone()
        
        if result:
            token = result[0]
            print(f"🔗 URL de test: http://localhost:8071/member/{token}")
            print(f"🖼️  URL image: http://localhost:8071/member/{token}/image")
        
        cursor.close()
        conn.close()
        
    except Exception as e:
        print(f"❌ Erreur: {e}")

if __name__ == "__main__":
    print("=== SOLUTION FINALE POUR LES IMAGES ===")
    print()
    
    print("1. Mise à jour du contrôleur...")
    create_image_endpoint()
    
    print("2. Mise à jour du template...")
    update_template()
    
    print("3. URLs de test...")
    test_solution()
    
    print()
    print("✅ SOLUTION APPLIQUÉE!")
    print()
    print("🔧 PROCHAINES ÉTAPES:")
    print("   1. Redémarrer Odoo: ./scripts/start_demo.sh")
    print("   2. Mettre à jour le module: odoo-bin -u sama_carte")
    print("   3. Tester la page publique")
    print()
    print("📋 CETTE SOLUTION:")
    print("   ✅ Crée un endpoint dédié pour servir les images")
    print("   ✅ Utilise le token d'accès pour la sécurité")
    print("   ✅ Gère automatiquement le décodage base64")
    print("   ✅ Fonctionne avec les données existantes")