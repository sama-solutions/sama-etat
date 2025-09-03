# -*- coding: utf-8 -*-

from odoo import http
from odoo.http import request

class SimpleTestController(http.Controller):

    @http.route('/test/simple', type='http', auth='public', website=True)
    def simple_test(self, **kwargs):
        """Test simple pour diagnostiquer"""
        
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
        
        member = MockMember()
        company = MockCompany()
        
        values = {
            'member': member,
            'company': company,
            'is_valid': True,
        }
        
        return request.render('sama_carte.simple_test_template', values)

    @http.route('/test/modern', type='http', auth='public', website=True)
    def test_modern_only(self, **kwargs):
        """Test du design moderne uniquement"""
        
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
        
        member = MockMember()
        company = MockCompany()
        
        values = {
            'member': member,
            'company': company,
            'is_valid': True,
        }
        
        return request.render('sama_carte.design_modern_fullsize_background', values)

    @http.route('/test/modern/simple', type='http', auth='public', website=True)
    def test_modern_simple(self, **kwargs):
        """Test du design moderne simplifié"""
        
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
        
        member = MockMember()
        company = MockCompany()
        
        values = {
            'member': member,
            'company': company,
            'is_valid': True,
        }
        
        return request.render('sama_carte.simple_modern_template', values)

    @http.route('/test/modern/working', type='http', auth='public', website=True)
    def test_modern_working(self, **kwargs):
        """Test du design moderne fullsize qui fonctionne"""
        
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
        
        member = MockMember()
        company = MockCompany()
        
        values = {
            'member': member,
            'company': company,
            'is_valid': True,
        }
        
        return request.render('sama_carte.working_modern_fullsize_template', values)