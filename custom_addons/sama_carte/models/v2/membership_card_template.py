# -*- coding: utf-8 -*-

from odoo import models, fields, api, _

class MembershipCardTemplate(models.Model):
    _name = 'membership.card.template'
    _description = 'Modèle de Design de Carte de Membre'
    _order = 'sequence, name'

    name = fields.Char(
        string="Nom du Design", 
        required=True,
        help="Nom affiché du template (ex: 'Moderne & Épuré')"
    )
    
    technical_name = fields.Char(
        string="Nom Technique", 
        required=True,
        help="Nom technique utilisé dans les templates QWeb (ex: 'modern')"
    )
    
    thumbnail = fields.Image(
        string="Aperçu du Design",
        help="Image de prévisualisation du design (recommandé: 300x200px)"
    )
    
    description = fields.Text(
        string="Description du Style",
        help="Description détaillée du style et de l'ambiance du design"
    )
    
    category = fields.Selection([
        ('modern', 'Moderne'),
        ('corporate', 'Corporate'),
        ('artistic', 'Artistique'),
        ('minimalist', 'Minimaliste'),
        ('luxury', 'Luxe'),
        ('tech', 'Technologique'),
        ('nature', 'Nature'),
        ('retro', 'Rétro'),
    ], string="Catégorie", required=True, default='modern')
    
    is_premium = fields.Boolean(
        string="Design Premium", 
        default=False,
        help="Si coché, ce design nécessite un abonnement premium"
    )
    
    sequence = fields.Integer(
        string="Séquence", 
        default=10,
        help="Ordre d'affichage dans la liste"
    )
    
    active = fields.Boolean(
        string="Actif", 
        default=True,
        help="Si décoché, ce template ne sera pas disponible"
    )
    
    # Couleurs par défaut du template
    default_primary_color = fields.Char(
        string="Couleur Primaire par Défaut",
        default="#004a99",
        help="Couleur primaire suggérée pour ce design"
    )
    
    default_secondary_color = fields.Char(
        string="Couleur Secondaire par Défaut",
        default="#f7f32d",
        help="Couleur secondaire suggérée pour ce design"
    )
    
    default_text_color = fields.Char(
        string="Couleur Texte par Défaut",
        default="#333333",
        help="Couleur de texte suggérée pour ce design"
    )
    
    # Statistiques d'utilisation
    usage_count = fields.Integer(
        string="Nombre d'utilisations",
        compute='_compute_usage_count',
        store=True,
        help="Nombre d'organisations utilisant ce template"
    )
    
    @api.depends('technical_name')
    def _compute_usage_count(self):
        """Calcule le nombre d'organisations utilisant ce template"""
        for template in self:
            count = self.env['res.company'].search_count([
                ('card_template_id', '=', template.id)
            ])
            template.usage_count = count
    
    @api.model
    def get_default_template(self):
        """Retourne le template par défaut (moderne)"""
        default = self.search([('technical_name', '=', 'modern')], limit=1)
        if not default:
            # Si pas de template moderne, prendre le premier actif
            default = self.search([('active', '=', True)], limit=1)
        return default
    
    def preview_template(self):
        """Action pour prévisualiser le template"""
        self.ensure_one()
        return {
            'type': 'ir.actions.act_url',
            'url': f'/template/preview/{self.technical_name}',
            'target': 'new',
        }
    
    @api.model
    def create_default_templates(self):
        """Crée les 10 templates par défaut"""
        templates_data = [
            {
                'name': 'Moderne & Épuré',
                'technical_name': 'modern',
                'description': 'Design moderne avec lignes épurées et couleurs douces',
                'category': 'modern',
                'sequence': 1,
                'default_primary_color': '#004a99',
                'default_secondary_color': '#f8f9fa',
                'default_text_color': '#212529',
            },
            {
                'name': 'Prestige & Doré',
                'technical_name': 'prestige',
                'description': 'Design luxueux avec bordures dorées et fond sombre',
                'category': 'luxury',
                'sequence': 2,
                'is_premium': True,
                'default_primary_color': '#111111',
                'default_secondary_color': '#D4AF37',
                'default_text_color': '#ffffff',
            },
            {
                'name': 'Dynamique & Géométrique',
                'technical_name': 'dynamic',
                'description': 'Formes géométriques dynamiques avec couleurs vives',
                'category': 'modern',
                'sequence': 3,
                'default_primary_color': '#333333',
                'default_secondary_color': '#f0f3f5',
                'default_text_color': '#333333',
            },
            {
                'name': 'Corporate & Structuré',
                'technical_name': 'corporate',
                'description': 'Design professionnel avec structure claire',
                'category': 'corporate',
                'sequence': 4,
                'default_primary_color': '#0d6efd',
                'default_secondary_color': '#ffffff',
                'default_text_color': '#333333',
            },
            {
                'name': 'Nature & Organique',
                'technical_name': 'nature',
                'description': 'Couleurs naturelles et formes organiques',
                'category': 'nature',
                'sequence': 5,
                'default_primary_color': '#224B0C',
                'default_secondary_color': '#F0F3E8',
                'default_text_color': '#224B0C',
            },
            {
                'name': 'Tech & Futuriste',
                'technical_name': 'tech',
                'description': 'Design futuriste avec dégradés et effets néon',
                'category': 'tech',
                'sequence': 6,
                'is_premium': True,
                'default_primary_color': '#0f0c29',
                'default_secondary_color': '#302b63',
                'default_text_color': '#ffffff',
            },
            {
                'name': 'Artistique & Créatif',
                'technical_name': 'artistic',
                'description': 'Layout asymétrique avec typographie créative',
                'category': 'artistic',
                'sequence': 7,
                'is_premium': True,
                'default_primary_color': '#6a0dad',
                'default_secondary_color': '#f4f4f4',
                'default_text_color': '#333333',
            },
            {
                'name': 'Minimaliste Extrême',
                'technical_name': 'minimalist',
                'description': 'Design ultra-épuré avec beaucoup d\'espace blanc',
                'category': 'minimalist',
                'sequence': 8,
                'default_primary_color': '#000000',
                'default_secondary_color': '#ffffff',
                'default_text_color': '#000000',
            },
            {
                'name': 'Rétro & Vintage',
                'technical_name': 'retro',
                'description': 'Style vintage avec couleurs sépia et bordures pointillées',
                'category': 'retro',
                'sequence': 9,
                'default_primary_color': '#8B4513',
                'default_secondary_color': '#FDF5E6',
                'default_text_color': '#8B4513',
            },
            {
                'name': 'Photographique Plein Écran',
                'technical_name': 'photographic',
                'description': 'Image en arrière-plan avec overlay de texte',
                'category': 'artistic',
                'sequence': 10,
                'is_premium': True,
                'default_primary_color': '#ffffff',
                'default_secondary_color': '#000000',
                'default_text_color': '#ffffff',
            },
        ]
        
        for template_data in templates_data:
            existing = self.search([('technical_name', '=', template_data['technical_name'])])
            if not existing:
                self.create(template_data)
        
        return True