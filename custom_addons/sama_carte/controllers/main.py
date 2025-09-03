# -*- coding: utf-8 -*-

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
        values = {
            'member': member,
            'is_valid': member.is_card_valid(),
            'company': member.company_id,
        }
        
        return request.render('sama_carte.member_public_page', values)
