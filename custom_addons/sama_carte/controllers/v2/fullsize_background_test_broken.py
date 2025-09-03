# -*- coding: utf-8 -*-

from odoo import http
from odoo.http import request

class FullsizeBackgroundTestController(http.Controller):

    @http.route('/background/fullsize/<string:design_name>', type='http', auth='public', website=True)
    def test_fullsize_background_design(self, design_name, **kwargs):
        """Test des designs avec fonds d'écran pleine taille"""
        
        # Données de test statiques pour éviter les problèmes d'accès
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
                self.primary_color = '#0d6efd'
                self.secondary_color = '#6c757d'
                self.text_color = '#ffffff'
        
        member = MockMember()
        company = MockCompany()
        is_valid = True
        
        # Sélectionner le template selon le design
        template_map = {
            'modern': 'sama_carte.design_modern_fullsize_background',
            'corporate': 'sama_carte.design_corporate_fullsize_background', 
            'prestige': 'sama_carte.design_prestige_fullsize_background',
        }
        
        template_name = template_map.get(design_name, 'sama_carte.design_modern_fullsize_background')
        
        values = {
            'member': member,
            'company': company,
            'is_valid': is_valid,
            'design_name': design_name,
        }
        
        return request.render(template_name, values)

    @http.route('/background/fullsize/gallery', type='http', auth='public', website=True)
    def fullsize_background_gallery(self, **kwargs):
        """Galerie des designs avec fonds pleine taille"""
        
        # Données de test statiques
        from datetime import datetime, timedelta
        
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
        
        member = MockMember()
        company = MockCompany()
        
        designs = [
            {
                'name': 'Moderne',
                'technical_name': 'modern',
                'description': 'Design moderne avec positionnement intelligent des éléments',
                'background': 'Dakar Gazelles',
                'features': ['Grille de positionnement', 'Animations séquentielles', 'Overlay adaptatif']
            },
            {
                'name': 'Corporate',
                'technical_name': 'corporate',
                'description': 'Design professionnel avec header et footer',
                'background': 'Jokkoo',
                'features': ['Header fixe', 'QR flottant', 'Contenu structuré']
            },
            {
                'name': 'Prestige',
                'technical_name': 'prestige',
                'description': 'Design luxueux avec contenu central',
                'background': 'Teranga Corp',
                'features': ['Coins décoratifs', 'Effets dorés', 'Centre glassmorphism']
            }
        ]
        
        values = {
            'designs': designs,
            'member': member,
            'company': company,
        }
        
        return request.render('sama_carte.fullsize_background_gallery_template', values)

    @http.route('/background/compare', type='http', auth='public', website=True)
    def compare_background_modes(self, **kwargs):
        """Comparaison entre mode crop et mode fullsize"""
        
        # Données de test statiques
        from datetime import datetime, timedelta
        
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
        
        member = MockMember()
        company = MockCompany()
        
        values = {
            'member': member,
            'company': company,
            'is_valid': True,
        }
        
        return request.render('sama_carte.background_comparison_template', values)