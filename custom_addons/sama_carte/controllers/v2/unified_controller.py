# -*- coding: utf-8 -*-

from odoo import http
from odoo.http import request
from odoo.exceptions import AccessError, MissingError

class UnifiedCardsController(http.Controller):
    """
    Contrôleur unifié simple - Un seul template pour tout
    Pas de complexité, pas de layers, juste une carte simple
    """

    def _get_member_data(self, member):
        """Prépare les données du membre de façon unifiée"""
        return {
            'member': member,
            'company': member.company_id,
            'is_valid': member.is_card_valid(),
            'page_title': f"Carte de {member.name}",
        }

    @http.route('/member/<string:access_token>/simple', type='http', auth='public', website=True)
    def member_simple_card(self, access_token, **kwargs):
        """Page publique simple avec le template unifié"""
        
        member = request.env['membership.member'].sudo().search([
            ('access_token', '=', access_token)
        ], limit=1)
        
        if not member:
            return request.not_found()
        
        values = self._get_member_data(member)
        values['is_preview'] = False
        
        return request.render('sama_carte.unified_simple_card', values)

    @http.route('/member/<int:member_id>/preview/unified/<string:background>', type='http', auth='user', website=True)
    def member_unified_preview(self, member_id, background, **kwargs):
        """Prévisualisation avec le template unifié"""
        
        try:
            member = request.env['membership.member'].browse(member_id)
            if not member.exists():
                return request.not_found()
            
            values = self._get_member_data(member)
            values['is_preview'] = True
            values['background_name'] = background
            
            return request.render('sama_carte.unified_simple_card', values)
            
        except (AccessError, MissingError):
            return request.not_found()

    @http.route('/debug/unified/<int:member_id>', type='http', auth='public', website=True)
    def debug_unified_card(self, member_id, **kwargs):
        """Debug public avec template unifié"""
        
        try:
            member = request.env['membership.member'].sudo().browse(member_id)
            if not member.exists():
                return request.not_found()
            
            values = self._get_member_data(member)
            values['is_preview'] = True
            values['background_name'] = 'debug'
            
            return request.render('sama_carte.unified_simple_card', values)
            
        except Exception as e:
            return request.make_response(f"Erreur: {str(e)}", status=500)

    @http.route('/debug/unified/test', type='http', auth='public', website=True)
    def debug_unified_test(self, **kwargs):
        """Test avec données fictives"""
        
        # Données de test
        test_member = type('TestMember', (), {
            'name': 'Membre Test Unifié',
            'membership_number': 'UNIFIED-001',
            'image_1920': None,
            'barcode_qr': None,
            'expiration_date': type('Date', (), {'strftime': lambda self, fmt: '31/12/2024'})(),
            'id': 999,
            'is_card_valid': lambda: True
        })()
        
        test_company = type('TestCompany', (), {
            'name': 'SAMA CARTE UNIFIÉ',
            'logo': None,
            'id': 1
        })()
        
        values = {
            'member': test_member,
            'company': test_company,
            'is_valid': True,
            'is_preview': True,
            'background_name': 'test',
            'page_title': 'Test Carte Unifiée',
        }
        
        return request.render('sama_carte.unified_simple_card', values)