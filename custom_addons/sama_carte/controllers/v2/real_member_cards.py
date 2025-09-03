# -*- coding: utf-8 -*-

from odoo import http
from odoo.http import request
from odoo.exceptions import AccessError, MissingError

class RealMemberCardsController(http.Controller):

    @http.route('/member/<string:access_token>', type='http', auth='public', website=True)
    def member_public_page(self, access_token, **kwargs):
        """Page publique d'un membre avec sa carte"""
        
        # Rechercher le membre par son token d'accès
        member = request.env['membership.member'].sudo().search([
            ('access_token', '=', access_token)
        ], limit=1)
        
        if not member:
            return request.not_found()
        
        # Vérifier si la carte est valide
        is_valid = member.is_card_valid()
        
        values = {
            'member': member,
            'company': member.company_id,
            'is_valid': is_valid,
            'page_title': f"Carte de {member.name}",
        }
        
        return request.render('sama_carte.member_public_card', values)

    @http.route('/member/<string:access_token>/card/<string:design>/<string:background>', type='http', auth='public', website=True)
    def member_card_with_design(self, access_token, design, background, **kwargs):
        """Carte d'un membre avec un design et background spécifique"""
        
        # Rechercher le membre par son token d'accès
        member = request.env['membership.member'].sudo().search([
            ('access_token', '=', access_token)
        ], limit=1)
        
        if not member:
            return request.not_found()
        
        # Vérifier si la carte est valide
        is_valid = member.is_card_valid()
        
        values = {
            'member': member,
            'company': member.company_id,
            'is_valid': is_valid,
            'background_name': background,
        }
        
        # APPROCHE SIMPLIFIÉE - Un seul template pour tout
        # Plus de complexité, plus de layers, plus de problèmes
        template = 'sama_carte.unified_simple_card'
        
        return request.render(template, values)

    @http.route('/member/<string:access_token>/card/portrait/<string:background>', type='http', auth='public', website=True)
    def member_card_portrait(self, access_token, background, **kwargs):
        """Carte d'un membre en format portrait"""
        
        # Rechercher le membre par son token d'accès
        member = request.env['membership.member'].sudo().search([
            ('access_token', '=', access_token)
        ], limit=1)
        
        if not member:
            return request.not_found()
        
        # Vérifier si la carte est valide
        is_valid = member.is_card_valid()
        
        values = {
            'member': member,
            'company': member.company_id,
            'is_valid': is_valid,
            'background_name': background,
        }
        
        # Sélectionner le template selon le background
        template_map = {
            'dakar_gazelles': 'sama_carte.design_portrait_real_member_dakar',
            'jokkoo': 'sama_carte.design_portrait_real_member_jokkoo',
            'teranga_corp': 'sama_carte.design_portrait_real_member_teranga',
        }
        
        template = template_map.get(background, 'sama_carte.design_portrait_real_member_dakar')
        
        return request.render(template, values)

    @http.route('/members/gallery', type='http', auth='user', website=True)
    def members_gallery(self, **kwargs):
        """Galerie des membres avec leurs cartes"""
        
        # Récupérer tous les membres
        members = request.env['membership.member'].search([])
        
        values = {
            'members': members,
            'page_title': 'Galerie des Membres',
        }
        
        return request.render('sama_carte.members_gallery', values)

    @http.route('/member/<int:member_id>/preview/<string:design>/<string:background>', type='http', auth='user', website=True)
    def member_card_preview(self, member_id, design, background, **kwargs):
        """Prévisualisation de la carte d'un membre (accès admin)"""
        
        try:
            member = request.env['membership.member'].browse(member_id)
            if not member.exists():
                return request.not_found()
            
            # Vérifier si la carte est valide
            is_valid = member.is_card_valid()
            
            values = {
                'member': member,
                'company': member.company_id,
                'is_valid': is_valid,
                'background_name': background,
                'is_preview': True,
            }
            
            # APPROCHE SIMPLIFIÉE - Un seul template uniforme
            template = 'sama_carte.unified_simple_card'
            
            return request.render(template, values)
            
        except (AccessError, MissingError):
            return request.not_found()