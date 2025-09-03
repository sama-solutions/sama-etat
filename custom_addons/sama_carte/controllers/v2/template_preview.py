# -*- coding: utf-8 -*-

from odoo import http, fields
from odoo.http import request
import uuid

class TemplatePreviewController(http.Controller):

    @http.route('/template/preview/<string:template_name>', type='http', auth='user', website=True)
    def preview_template(self, template_name, **kwargs):
        """Prévisualise un template de carte avec des données de démonstration"""
        
        # Récupérer le template
        template = request.env['membership.card.template'].search([
            ('technical_name', '=', template_name)
        ], limit=1)
        
        if not template:
            return request.not_found()
        
        # Créer un membre de démonstration temporaire
        demo_member_data = {
            'name': 'Membre Démonstration',
            'membership_number': 'DEMO-001',
            'expiration_date': fields.Date.today().replace(month=12, day=31),
            'company_id': request.env.company.id,
            'access_token': str(uuid.uuid4()),
        }
        
        # Simuler un membre sans le créer en base
        demo_member = request.env['membership.member'].new(demo_member_data)
        demo_member._compute_qr_code()
        demo_member._compute_card_status()
        
        # Récupérer la société avec le template appliqué
        company = request.env.company
        
        # Appliquer temporairement les couleurs du template pour la prévisualisation
        preview_company = company.copy_data()[0]
        preview_company.update({
            'primary_color': template.default_primary_color,
            'secondary_color': template.default_secondary_color,
            'text_color': template.default_text_color,
            'card_template_id': template.id,
        })
        
        # Créer un objet company temporaire pour la prévisualisation
        temp_company = request.env['res.company'].new(preview_company)
        demo_member.company_id = temp_company
        
        # Vérifier si la carte est valide
        is_valid = demo_member.is_card_valid()
        
        # Rendu du template avec les données de démonstration
        return request.render('sama_carte.template_preview_page', {
            'member': demo_member,
            'company': temp_company,
            'is_valid': is_valid,
            'template': template,
            'preview_mode': True,
        })
    
    @http.route('/template/preview/card/<string:template_name>', type='http', auth='user', website=True)
    def preview_card_only(self, template_name, **kwargs):
        """Prévisualise uniquement la carte sans la page complète"""
        
        # Récupérer le template
        template = request.env['membership.card.template'].search([
            ('technical_name', '=', template_name)
        ], limit=1)
        
        if not template:
            return request.not_found()
        
        # Créer un membre de démonstration
        demo_member_data = {
            'name': 'Membre Démonstration',
            'membership_number': 'DEMO-001',
            'expiration_date': fields.Date.today().replace(month=12, day=31),
            'company_id': request.env.company.id,
            'access_token': str(uuid.uuid4()),
        }
        
        demo_member = request.env['membership.member'].new(demo_member_data)
        demo_member._compute_qr_code()
        demo_member._compute_card_status()
        
        # Appliquer les couleurs du template
        company = request.env.company
        preview_company = company.copy_data()[0]
        preview_company.update({
            'primary_color': template.default_primary_color,
            'secondary_color': template.default_secondary_color,
            'text_color': template.default_text_color,
            'card_template_id': template.id,
        })
        
        temp_company = request.env['res.company'].new(preview_company)
        demo_member.company_id = temp_company
        
        is_valid = demo_member.is_card_valid()
        
        # Rendu de la carte seulement
        return request.render('sama_carte.card_preview_only', {
            'member': demo_member,
            'company': temp_company,
            'is_valid': is_valid,
            'template': template,
            'template_name': template_name,
        })
    
    @http.route('/template/gallery', type='http', auth='user', website=True)
    def template_gallery(self, **kwargs):
        """Galerie de tous les templates disponibles"""
        
        templates = request.env['membership.card.template'].search([
            ('active', '=', True)
        ], order='sequence, name')
        
        return request.render('sama_carte.template_gallery_page', {
            'templates': templates,
        })