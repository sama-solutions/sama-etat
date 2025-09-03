# -*- coding: utf-8 -*-

import base64
import io
import uuid
from odoo import models, fields, api, _
from odoo.http import request

try:
    import qrcode
except ImportError:
    qrcode = None

class MembershipMember(models.Model):
    _name = 'membership.member'
    _description = 'Membre de l\'organisation'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string="Nom complet", required=True, tracking=True)
    image_1920 = fields.Image(string="Photo")
    
    membership_number = fields.Char(
        string="Numéro de Membre", 
        required=True, 
        copy=False, 
        readonly=True, 
        default=lambda self: _('Nouveau'),
        tracking=True
    )
    
    access_token = fields.Char(
        string="Token d'accès",
        default=lambda self: str(uuid.uuid4()),
        copy=False,
        readonly=True
    )
    
    barcode_qr = fields.Binary(
        string="QR Code", 
        compute='_compute_qr_code', 
        store=True
    )

    expiration_date = fields.Date(string="Date d'expiration", default=lambda self: fields.Date.today())
    
    company_id = fields.Many2one('res.company', string='Société', default=lambda self: self.env.company)
    
    terms_and_conditions = fields.Text(
        string="Termes et Conditions", 
        related='company_id.membership_terms',
        readonly=True
    )
    
    public_url = fields.Char(
        string="URL Publique",
        compute='_compute_public_url',
        help="URL publique pour accéder à la page du membre"
    )
    
    card_status = fields.Selection([
        ('valid', 'Valide'),
        ('expired', 'Expirée'),
    ], string="Statut de la Carte", compute='_compute_card_status', store=True)

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('membership_number', _('Nouveau')) == _('Nouveau'):
                vals['membership_number'] = self.env['ir.sequence'].next_by_code('membership.member.sequence') or _('Nouveau')
        return super().create(vals_list)

    def _get_public_url(self):
        """Retourne l'URL publique pour accéder aux informations du membre"""
        base_url = self.env['ir.config_parameter'].sudo().get_param('web.base.url')
        return f"{base_url}/member/{self.access_token}"
    
    def is_card_valid(self):
        """Vérifie si la carte est encore valide"""
        return self.expiration_date >= fields.Date.today()
    
    @api.depends('access_token')
    def _compute_public_url(self):
        """Calcule l'URL publique du membre"""
        for member in self:
            if member.access_token:
                member.public_url = member._get_public_url()
            else:
                member.public_url = False
    
    @api.depends('expiration_date')
    def _compute_card_status(self):
        """Calcule le statut de la carte (valide/expirée)"""
        today = fields.Date.today()
        for member in self:
            if member.expiration_date >= today:
                member.card_status = 'valid'
            else:
                member.card_status = 'expired'
    
    def action_open_public_page(self):
        """Ouvre la page publique du membre dans un nouvel onglet"""
        self.ensure_one()
        if not self.access_token:
            return {
                'type': 'ir.actions.client',
                'tag': 'display_notification',
                'params': {
                    'title': _('Erreur'),
                    'message': _('Aucun token d\'accès disponible pour ce membre.'),
                    'type': 'warning',
                }
            }
        
        return {
            'type': 'ir.actions.act_url',
            'url': self._get_public_url(),
            'target': 'new',
        }

    @api.depends('access_token')
    def _compute_qr_code(self):
        if not qrcode:
            return

        for member in self:
            if not member.access_token:
                member.barcode_qr = False
                continue

            qr = qrcode.QRCode(
                version=1,
                error_correction=qrcode.constants.ERROR_CORRECT_L,
                box_size=10,
                border=4,
            )
            qr.add_data(member._get_public_url())
            qr.make(fit=True)
            img = qr.make_image(fill_color="black", back_color="white")
            
            temp = io.BytesIO()
            img.save(temp, format="PNG")
            qr_image = base64.b64encode(temp.getvalue())
            member.barcode_qr = qr_image

class ResCompany(models.Model):
    _inherit = 'res.company'
    membership_terms = fields.Text(string="Termes et Conditions des Cartes de Membre", default="Cette carte est personnelle, non transférable et reste la propriété de l'organisation. Elle doit être restituée sur demande.")