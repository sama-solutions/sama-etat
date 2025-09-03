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
    
    # Champs pour l'analyse de données
    days_until_expiration = fields.Integer(
        string="Jours avant expiration",
        compute='_compute_days_until_expiration',
        store=True,
        help="Nombre de jours avant l'expiration de la carte"
    )
    
    expiration_category = fields.Selection([
        ('expired', 'Expirée'),
        ('expires_soon', 'Expire bientôt (< 30 jours)'),
        ('expires_later', 'Expire plus tard (30-90 jours)'),
        ('valid_long_term', 'Valide long terme (> 90 jours)'),
    ], string="Catégorie d'expiration", compute='_compute_expiration_category', store=True)
    
    membership_age_days = fields.Integer(
        string="Âge du membre (jours)",
        compute='_compute_membership_age',
        store=True,
        help="Nombre de jours depuis la création du membre"
    )
    
    has_photo = fields.Boolean(
        string="A une photo",
        compute='_compute_has_photo',
        store=True,
        help="Indique si le membre a une photo"
    )

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
    
    @api.depends('expiration_date')
    def _compute_days_until_expiration(self):
        """Calcule le nombre de jours avant expiration"""
        today = fields.Date.today()
        for member in self:
            if member.expiration_date:
                delta = member.expiration_date - today
                member.days_until_expiration = delta.days
            else:
                member.days_until_expiration = 0
    
    @api.depends('days_until_expiration')
    def _compute_expiration_category(self):
        """Calcule la catégorie d'expiration"""
        for member in self:
            days = member.days_until_expiration
            if days < 0:
                member.expiration_category = 'expired'
            elif days < 30:
                member.expiration_category = 'expires_soon'
            elif days < 90:
                member.expiration_category = 'expires_later'
            else:
                member.expiration_category = 'valid_long_term'
    
    @api.depends('create_date')
    def _compute_membership_age(self):
        """Calcule l'âge du membre en jours"""
        today = fields.Date.today()
        for member in self:
            if member.create_date:
                create_date = member.create_date.date()
                delta = today - create_date
                member.membership_age_days = delta.days
            else:
                member.membership_age_days = 0
    
    @api.depends('image_1920')
    def _compute_has_photo(self):
        """Calcule si le membre a une photo"""
        for member in self:
            member.has_photo = bool(member.image_1920)
    
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