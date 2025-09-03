# -*- coding: utf-8 -*-

from odoo import http
from odoo.http import request

class DebugCardsController(http.Controller):

    @http.route('/debug/card/test', type='http', auth='public', website=True)
    def debug_card_test(self, **kwargs):
        """Test de carte sans authentification pour diagnostic"""
        
        # Créer des données de test
        test_member = type('TestMember', (), {
            'name': 'Test Member',
            'membership_number': 'TEST-001',
            'image_1920': None,
            'barcode_qr': None,
            'expiration_date': type('Date', (), {'strftime': lambda self, fmt: '31/12/2024'})(),
            'id': 999
        })()
        
        test_company = type('TestCompany', (), {
            'name': 'SAMA CARTE TEST',
            'logo': None,
            'id': 1
        })()
        
        values = {
            'member': test_member,
            'company': test_company,
            'is_valid': True,
            'background_name': 'test',
            'is_preview': True,
        }
        
        return request.render('sama_carte.design_ultra_simple_member', values)

    @http.route('/debug/card/simple/<int:member_id>', type='http', auth='public', website=True)
    def debug_card_simple(self, member_id, **kwargs):
        """Test avec vrai membre mais sans auth"""
        
        try:
            # Essayer de récupérer le membre
            member = request.env['membership.member'].sudo().browse(member_id)
            if not member.exists():
                return request.not_found()
            
            # Vérifier si la carte est valide
            is_valid = member.is_card_valid()
            
            values = {
                'member': member,
                'company': member.company_id,
                'is_valid': is_valid,
                'background_name': 'test',
                'is_preview': True,
            }
            
            return request.render('sama_carte.design_ultra_simple_member', values)
            
        except Exception as e:
            return request.make_response(f"Erreur: {str(e)}", status=500)