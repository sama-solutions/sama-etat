# -*- coding: utf-8 -*-

import base64
import os
from odoo import models, fields, api, _
from odoo.modules.module import get_module_path

class MembershipCardBackground(models.Model):
    _name = 'membership.card.background'
    _description = 'Fonds d\'écran pour cartes de membres'
    _order = 'sequence, name'

    name = fields.Char('Nom du fond', required=True)
    technical_name = fields.Char('Nom technique', required=True)
    description = fields.Text('Description')
    sequence = fields.Integer('Séquence', default=10)
    
    # Images
    image_portrait = fields.Binary('Image Portrait', required=True)
    image_landscape = fields.Binary('Image Paysage', required=True)
    
    # Métadonnées
    is_premium = fields.Boolean('Premium', default=False)
    category = fields.Selection([
        ('corporate', 'Corporate'),
        ('nature', 'Nature'),
        ('abstract', 'Abstrait'),
        ('cultural', 'Culturel'),
        ('sport', 'Sport'),
        ('tech', 'Technologie'),
    ], string='Catégorie', default='corporate')
    
    # Statistiques
    usage_count = fields.Integer('Nombre d\'utilisations', default=0)
    
    @api.model
    def load_default_backgrounds(self):
        """Charge les fonds d'écran par défaut depuis le dossier backgrounds"""
        module_path = get_module_path('sama_carte')
        backgrounds_path = os.path.join(module_path, 'backgrounds')
        
        if not os.path.exists(backgrounds_path):
            return
        
        # Définition des fonds par défaut
        default_backgrounds = [
            {
                'name': 'Dakar Gazelles',
                'technical_name': 'dakar_gazelles',
                'description': 'Fond d\'écran Dakar Gazelles - Élégant et sportif',
                'category': 'sport',
                'sequence': 1,
                'portrait_file': 'Dakar Gazelles portrait.png',
                'landscape_file': 'Dakar Gazelles paysage.png',
            },
            {
                'name': 'Jokkoo',
                'technical_name': 'jokkoo',
                'description': 'Fond d\'écran Jokkoo - Style moderne et professionnel',
                'category': 'corporate',
                'sequence': 2,
                'portrait_file': 'Jokkoo_portrait.png',
                'landscape_file': 'Jokkoo_paysage.png',
            },
            {
                'name': 'Teranga Corp',
                'technical_name': 'teranga_corp',
                'description': 'Fond d\'écran Teranga Corp - Corporate et institutionnel',
                'category': 'corporate',
                'sequence': 3,
                'portrait_file': 'Teranga Corp portrait.png',
                'landscape_file': 'Teranga Corp paysage.png',
            },
        ]
        
        for bg_data in default_backgrounds:
            # Vérifier si le fond existe déjà
            existing = self.search([('technical_name', '=', bg_data['technical_name'])])
            if existing:
                continue
            
            # Charger les images
            portrait_path = os.path.join(backgrounds_path, bg_data['portrait_file'])
            landscape_path = os.path.join(backgrounds_path, bg_data['landscape_file'])
            
            image_portrait = False
            image_landscape = False
            
            if os.path.exists(portrait_path):
                with open(portrait_path, 'rb') as f:
                    image_portrait = base64.b64encode(f.read())
            
            if os.path.exists(landscape_path):
                with open(landscape_path, 'rb') as f:
                    image_landscape = base64.b64encode(f.read())
            
            if image_portrait and image_landscape:
                self.create({
                    'name': bg_data['name'],
                    'technical_name': bg_data['technical_name'],
                    'description': bg_data['description'],
                    'category': bg_data['category'],
                    'sequence': bg_data['sequence'],
                    'image_portrait': image_portrait,
                    'image_landscape': image_landscape,
                })
    
    def action_preview_portrait(self):
        """Action pour prévisualiser en format portrait"""
        return {
            'type': 'ir.actions.act_url',
            'url': f'/background/preview/{self.id}/portrait',
            'target': 'new',
        }
    
    def action_preview_landscape(self):
        """Action pour prévisualiser en format paysage"""
        return {
            'type': 'ir.actions.act_url',
            'url': f'/background/preview/{self.id}/landscape',
            'target': 'new',
        }

class ResCompany(models.Model):
    _inherit = 'res.company'
    
    # Fond d'écran pour les cartes
    card_background_id = fields.Many2one(
        'membership.card.background', 
        string='Fond d\'écran des cartes'
    )
    card_background_orientation = fields.Selection([
        ('portrait', 'Portrait'),
        ('landscape', 'Paysage'),
        ('auto', 'Automatique')
    ], string='Orientation du fond', default='auto')
    
    def get_card_background_url(self, orientation='auto'):
        """Retourne l'URL du fond d'écran selon l'orientation"""
        if not self.card_background_id:
            return False
        
        if orientation == 'auto':
            orientation = self.card_background_orientation or 'portrait'
        
        if orientation == 'landscape':
            return f'/web/image/membership.card.background/{self.card_background_id.id}/image_landscape'
        else:
            return f'/web/image/membership.card.background/{self.card_background_id.id}/image_portrait'