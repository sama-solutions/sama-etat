# -*- coding: utf-8 -*-

from odoo import models, fields, api, _

class ResCompany(models.Model):
    _inherit = 'res.company'
    
    # Template de carte choisi
    card_template_id = fields.Many2one(
        'membership.card.template', 
        string="Modèle de Carte",
        help="Template de design utilisé pour les cartes de cette organisation"
    )
    
    # Couleurs personnalisables
    primary_color = fields.Char(
        string="Couleur Primaire", 
        default="#004a99",
        help="Couleur principale utilisée sur les cartes (format hex: #RRGGBB)"
    )
    
    secondary_color = fields.Char(
        string="Couleur Secondaire", 
        default="#f7f32d",
        help="Couleur d'accent utilisée sur les cartes (format hex: #RRGGBB)"
    )
    
    text_color = fields.Char(
        string="Couleur du Texte", 
        default="#333333",
        help="Couleur du texte principal (format hex: #RRGGBB)"
    )
    
    # Slogan personnalisé
    membership_slogan = fields.Char(
        string="Slogan de l'Organisation",
        help="Slogan affiché sur les cartes de membre"
    )
    
    # Paramètres avancés de personnalisation
    card_background_image = fields.Image(
        string="Image de Fond",
        help="Image de fond personnalisée pour certains templates"
    )
    
    use_custom_fonts = fields.Boolean(
        string="Utiliser Polices Personnalisées",
        default=False,
        help="Activer l'utilisation de polices personnalisées"
    )
    
    custom_font_family = fields.Char(
        string="Famille de Police",
        default="Arial, sans-serif",
        help="Famille de police CSS à utiliser"
    )
    
    # Paramètres de branding
    show_logo_on_card = fields.Boolean(
        string="Afficher Logo sur Carte",
        default=True,
        help="Afficher le logo de l'organisation sur les cartes"
    )
    
    show_slogan_on_card = fields.Boolean(
        string="Afficher Slogan sur Carte",
        default=True,
        help="Afficher le slogan sur les cartes"
    )
    
    # Statistiques
    total_members = fields.Integer(
        string="Total Membres",
        compute='_compute_member_stats',
        help="Nombre total de membres de cette organisation"
    )
    
    active_members = fields.Integer(
        string="Membres Actifs",
        compute='_compute_member_stats',
        help="Nombre de membres avec carte valide"
    )
    
    def _get_default_template(self):
        """Retourne le template par défaut"""
        try:
            template_model = self.env['membership.card.template']
            return template_model.get_default_template()
        except:
            return False
    
    @api.model
    def _set_default_templates(self):
        """Définit le template par défaut pour les sociétés sans template"""
        companies_without_template = self.search([('card_template_id', '=', False)])
        default_template = self._get_default_template()
        if default_template:
            companies_without_template.write({'card_template_id': default_template.id})
    
    @api.depends('name')
    def _compute_member_stats(self):
        """Calcule les statistiques des membres"""
        for company in self:
            members = self.env['membership.member'].search([('company_id', '=', company.id)])
            company.total_members = len(members)
            company.active_members = len(members.filtered(lambda m: m.card_status == 'valid'))
    
    @api.onchange('card_template_id')
    def _onchange_card_template_id(self):
        """Applique les couleurs par défaut du template sélectionné"""
        if self.card_template_id:
            template = self.card_template_id
            self.primary_color = template.default_primary_color
            self.secondary_color = template.default_secondary_color
            self.text_color = template.default_text_color
    
    def preview_card_design(self):
        """Action pour prévisualiser le design de carte"""
        self.ensure_one()
        # Trouver un membre de démonstration ou créer un membre temporaire
        demo_member = self.env['membership.member'].search([
            ('company_id', '=', self.id)
        ], limit=1)
        
        if not demo_member:
            # Créer un membre temporaire pour la prévisualisation
            demo_member = self.env['membership.member'].create({
                'name': 'Membre Démonstration',
                'company_id': self.id,
                'membership_number': 'DEMO-001',
            })
        
        return {
            'type': 'ir.actions.act_url',
            'url': f'/member/{demo_member.access_token}?preview=1',
            'target': 'new',
        }
    
    def reset_to_template_colors(self):
        """Remet les couleurs par défaut du template"""
        self.ensure_one()
        if self.card_template_id:
            template = self.card_template_id
            self.write({
                'primary_color': template.default_primary_color,
                'secondary_color': template.default_secondary_color,
                'text_color': template.default_text_color,
            })
        return {
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'params': {
                'title': _('Couleurs Réinitialisées'),
                'message': _('Les couleurs ont été remises aux valeurs par défaut du template.'),
                'type': 'success',
            }
        }