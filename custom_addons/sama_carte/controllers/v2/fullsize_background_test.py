# -*- coding: utf-8 -*-

from odoo import http
from odoo.http import request

class FullsizeBackgroundTestController(http.Controller):

    @http.route('/background/fullsize/<string:design_name>', type='http', auth='user', website=True)
    def test_fullsize_background_design(self, design_name, **kwargs):
        """Test des designs avec fonds d'écran pleine taille"""
        
        # Données de test
        company = request.env.company
        
        # Membre de test (premier membre SAMA)
        member = request.env['membership.member'].search([
            ('company_id', '=', company.id)
        ], limit=1)
        
        if not member:
            # Créer un membre de test si aucun n'existe
            member = request.env['membership.member'].create({
                'name': 'Test Fullsize Background User',
                'membership_number': 'TEST-FULL-001',
                'company_id': company.id,
            })
        
        # Vérifier la validité
        is_valid = member.is_card_valid() if hasattr(member, 'is_card_valid') else True
        
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

    @http.route('/background/fullsize/gallery', type='http', auth='user', website=True)
    def fullsize_background_gallery(self, **kwargs):
        """Galerie des designs avec fonds pleine taille"""
        
        company = request.env.company
        
        # Membre de test
        member = request.env['membership.member'].search([
            ('company_id', '=', company.id)
        ], limit=1)
        
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

    @http.route('/background/compare', type='http', auth='user', website=True)
    def compare_background_modes(self, **kwargs):
        """Comparaison entre mode crop et mode fullsize"""
        
        company = request.env.company
        
        # Membre de test
        member = request.env['membership.member'].search([
            ('company_id', '=', company.id)
        ], limit=1)
        
        values = {
            'member': member,
            'company': company,
            'is_valid': True,
        }
        
        return request.render('sama_carte.background_comparison_template', values)