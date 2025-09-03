# -*- coding: utf-8 -*-

from odoo import http
from odoo.http import request
import json

class BackgroundTestController(http.Controller):

    @http.route('/background/test/<string:design_name>', type='http', auth='user', website=True)
    def test_background_design(self, design_name, **kwargs):
        """Test des designs avec fonds d'écran"""
        
        # Données de test
        company = request.env.company
        
        # Membre de test (premier membre SAMA)
        member = request.env['membership.member'].search([
            ('company_id', '=', company.id)
        ], limit=1)
        
        if not member:
            # Créer un membre de test si aucun n'existe
            member = request.env['membership.member'].create({
                'name': 'Test Background User',
                'membership_number': 'TEST-BG-001',
                'company_id': company.id,
            })
        
        # Vérifier la validité
        is_valid = member.is_card_valid() if hasattr(member, 'is_card_valid') else True
        
        # Sélectionner le template selon le design
        template_map = {
            'modern': 'sama_carte.design_modern_with_background',
            'corporate': 'sama_carte.design_corporate_with_background', 
            'prestige': 'sama_carte.design_prestige_with_background',
        }
        
        template_name = template_map.get(design_name, 'sama_carte.design_modern_with_background')
        
        values = {
            'member': member,
            'company': company,
            'is_valid': is_valid,
            'design_name': design_name,
        }
        
        return request.render(template_name, values)

    @http.route('/background/gallery', type='http', auth='user', website=True)
    def background_gallery(self, **kwargs):
        """Galerie des fonds d'écran disponibles"""
        
        backgrounds = request.env['membership.card.background'].search([])
        company = request.env.company
        
        values = {
            'backgrounds': backgrounds,
            'company': company,
        }
        
        return request.render('sama_carte.background_gallery_template', values)

    @http.route('/background/preview/<int:background_id>/<string:orientation>', 
                type='http', auth='user', website=True)
    def preview_background(self, background_id, orientation='portrait', **kwargs):
        """Prévisualisation d'un fond d'écran spécifique"""
        
        background = request.env['membership.card.background'].browse(background_id)
        if not background.exists():
            return request.not_found()
        
        company = request.env.company
        
        # Membre de test
        member = request.env['membership.member'].search([
            ('company_id', '=', company.id)
        ], limit=1)
        
        values = {
            'background': background,
            'orientation': orientation,
            'member': member,
            'company': company,
            'is_valid': True,
        }
        
        return request.render('sama_carte.background_preview_template', values)

    @http.route('/api/background/load_defaults', type='json', auth='user')
    def load_default_backgrounds(self, **kwargs):
        """API pour charger les fonds d'écran par défaut"""
        
        try:
            request.env['membership.card.background'].load_default_backgrounds()
            return {'success': True, 'message': 'Fonds d\'écran chargés avec succès'}
        except Exception as e:
            return {'success': False, 'error': str(e)}