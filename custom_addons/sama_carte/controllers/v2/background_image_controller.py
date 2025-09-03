# -*- coding: utf-8 -*-

from odoo import http
from odoo.http import request
import base64
import os
from odoo.modules.module import get_module_path

class BackgroundImageController(http.Controller):

    @http.route('/background/image/<string:technical_name>/<string:orientation>', type='http', auth='public')
    def get_background_image(self, technical_name, orientation='landscape', **kwargs):
        """Retourne l'image de fond selon le nom technique et l'orientation"""
        
        # Mapping des noms techniques vers les fichiers
        background_files = {
            'dakar_gazelles': {
                'portrait': 'Dakar Gazelles portrait.png',
                'landscape': 'Dakar Gazelles paysage.png'
            },
            'jokkoo': {
                'portrait': 'Jokkoo_portrait.png',
                'landscape': 'Jokkoo_paysage.png'
            },
            'teranga_corp': {
                'portrait': 'Teranga Corp portrait.png',
                'landscape': 'Teranga Corp paysage.png'
            }
        }
        
        if technical_name not in background_files:
            return request.not_found()
        
        if orientation not in ['portrait', 'landscape']:
            orientation = 'landscape'
        
        filename = background_files[technical_name][orientation]
        
        # Chemin vers le fichier
        module_path = get_module_path('sama_carte')
        file_path = os.path.join(module_path, 'backgrounds', filename)
        
        if not os.path.exists(file_path):
            return request.not_found()
        
        # Lire et retourner l'image
        try:
            with open(file_path, 'rb') as f:
                image_data = f.read()
            
            # Déterminer le type MIME
            if filename.lower().endswith('.png'):
                mimetype = 'image/png'
            elif filename.lower().endswith('.jpg') or filename.lower().endswith('.jpeg'):
                mimetype = 'image/jpeg'
            else:
                mimetype = 'image/png'
            
            return request.make_response(
                image_data,
                headers=[
                    ('Content-Type', mimetype),
                    ('Cache-Control', 'public, max-age=3600'),
                ]
            )
        except Exception:
            return request.not_found()

    @http.route('/background/test/with-image/<string:design>/<string:background>', type='http', auth='public', website=True)
    def test_design_with_background(self, design, background, **kwargs):
        """Test d'un design avec une vraie image de fond"""
        
        from datetime import datetime, timedelta
        
        # Données de test statiques
        class MockMember:
            def __init__(self):
                self.id = 1
                self.name = 'Jean Dupont'
                self.membership_number = 'SN-MBR-00001'
                self.image_1920 = None
                self.barcode_qr = None
                self.expiration_date = datetime.now().date() + timedelta(days=365)
        
        class MockCompany:
            def __init__(self):
                self.id = 1
                self.name = 'SAMA - Société Africaine de Management'
                self.logo = None
                self.primary_color = '#0d6efd'
                self.secondary_color = '#6c757d'
                self.text_color = '#ffffff'
        
        class MockBackground:
            def __init__(self, technical_name):
                self.technical_name = technical_name
                self.name = technical_name.replace('_', ' ').title()
        
        member = MockMember()
        company = MockCompany()
        background_obj = MockBackground(background)
        
        values = {
            'member': member,
            'company': company,
            'background': background_obj,
            'is_valid': True,
        }
        
        # Sélectionner le template selon le design
        template_map = {
            'modern': 'sama_carte.design_modern_with_real_background',
            'corporate': 'sama_carte.design_corporate_with_real_background',
            'prestige': 'sama_carte.design_prestige_with_real_background',
        }
        
        template = template_map.get(design, 'sama_carte.design_modern_with_real_background')
        
        return request.render(template, values)

    @http.route('/background/real/gallery', type='http', auth='public', website=True)
    def real_background_gallery(self, **kwargs):
        """Galerie des designs avec vraies images"""
        return request.render('sama_carte.real_background_gallery', {})