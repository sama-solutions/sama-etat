from odoo import models, fields, api
from odoo.exceptions import ValidationError

class ProjectCostBreakdown(models.Model):
    _name = 'project.cost.breakdown'
    _description = 'Ventilation du Coût par Composante - Conformité Légale Sénégal'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'sequence, component_name'

    # Champs principaux
    name = fields.Char(string="Nom", compute='_compute_name', store=True)
    project_id = fields.Many2one(
        'government.project', 
        string="Projet", 
        required=True, 
        ondelete='cascade',
        tracking=True
    )
    sequence = fields.Integer(string="Séquence", default=10)
    component_name = fields.Char(
        string="Nom de la Composante", 
        required=True, 
        tracking=True,
        help="Ex: Travaux de construction, Équipements, Formation, etc."
    )
    component_type = fields.Selection([
        ('travaux', 'Travaux'),
        ('equipements', 'Équipements'),
        ('services', 'Services'),
        ('formation', 'Formation'),
        ('assistance_technique', 'Assistance Technique'),
        ('fonctionnement', 'Fonctionnement'),
        ('autre', 'Autre')
    ], string="Type de Composante", required=True, tracking=True)
    
    estimated_cost = fields.Monetary(
        string="Coût Estimé", 
        currency_field='currency_id', 
        required=True, 
        tracking=True
    )
    actual_cost = fields.Monetary(
        string="Coût Réel", 
        currency_field='currency_id', 
        tracking=True,
        help="Coût réellement engagé (à remplir pendant l'exécution)"
    )
    currency_id = fields.Many2one(
        'res.currency', 
        string='Devise', 
        default=lambda self: self._get_default_currency(),
        required=True
    )
    
    description = fields.Text(
        string="Description Détaillée",
        help="Description précise de la composante et des activités incluses"
    )
    
    # Pourcentages et calculs
    percentage_of_total = fields.Float(
        string="% du Coût Total", 
        compute='_compute_percentage_of_total', 
        store=True,
        help="Pourcentage par rapport au coût total du projet"
    )
    variance = fields.Monetary(
        string="Écart (Réel - Estimé)", 
        compute='_compute_variance', 
        store=True,
        currency_field='currency_id'
    )
    variance_percentage = fields.Float(
        string="% Écart", 
        compute='_compute_variance_percentage', 
        store=True
    )
    
    # Conformité et suivi
    budget_line_reference = fields.Char(
        string="Référence Ligne Budgétaire",
        help="Référence de la ligne budgétaire dans le budget national"
    )
    procurement_method = fields.Selection([
        ('appel_offres_ouvert', 'Appel d\'Offres Ouvert'),
        ('appel_offres_restreint', 'Appel d\'Offres Restreint'),
        ('demande_prix', 'Demande de Prix'),
        ('entente_directe', 'Entente Directe'),
        ('regie', 'Régie'),
        ('autre', 'Autre')
    ], string="Mode de Passation", tracking=True)
    
    responsible_entity = fields.Char(
        string="Entité Responsable",
        help="Entité responsable de la mise en œuvre de cette composante"
    )
    
    # Statut d'exécution
    execution_status = fields.Selection([
        ('not_started', 'Non Commencée'),
        ('in_progress', 'En Cours'),
        ('completed', 'Achevée'),
        ('suspended', 'Suspendue'),
        ('cancelled', 'Annulée')
    ], string="Statut d'Exécution", default='not_started', tracking=True)
    
    completion_percentage = fields.Float(
        string="% d'Achèvement", 
        default=0.0,
        help="Pourcentage d'achèvement physique de la composante"
    )
    
    # Dates
    planned_start_date = fields.Date(string="Date de Début Prévue")
    planned_end_date = fields.Date(string="Date de Fin Prévue")
    actual_start_date = fields.Date(string="Date de Début Réelle")
    actual_end_date = fields.Date(string="Date de Fin Réelle")
    
    # Méthodes de calcul
    @api.depends('component_name', 'estimated_cost')
    def _compute_name(self):
        """Génère le nom affiché de l'enregistrement"""
        for record in self:
            if record.component_name and record.estimated_cost:
                record.name = f"{record.component_name} - {record.estimated_cost:,.0f} {record.currency_id.symbol or 'XOF'}"
            else:
                record.name = record.component_name or "Nouvelle Composante"
    
    @api.depends('estimated_cost', 'project_id.cout_total_projet')
    def _compute_percentage_of_total(self):
        """Calcule le pourcentage par rapport au coût total du projet"""
        for record in self:
            if record.project_id.cout_total_projet and record.estimated_cost:
                record.percentage_of_total = (record.estimated_cost / record.project_id.cout_total_projet) * 100
            else:
                record.percentage_of_total = 0.0
    
    @api.depends('estimated_cost', 'actual_cost')
    def _compute_variance(self):
        """Calcule l'écart entre coût réel et estimé"""
        for record in self:
            if record.actual_cost and record.estimated_cost:
                record.variance = record.actual_cost - record.estimated_cost
            else:
                record.variance = 0.0
    
    @api.depends('variance', 'estimated_cost')
    def _compute_variance_percentage(self):
        """Calcule le pourcentage d'écart"""
        for record in self:
            if record.estimated_cost and record.variance:
                record.variance_percentage = (record.variance / record.estimated_cost) * 100
            else:
                record.variance_percentage = 0.0
    
    def _get_default_currency(self):
        """Retourne la devise CFA (XOF) par défaut"""
        xof_currency = self.env['res.currency'].search([('name', '=', 'XOF')], limit=1)
        if xof_currency:
            return xof_currency.id
        return self.env.company.currency_id.id
    
    # Contraintes de validation
    @api.constrains('estimated_cost', 'actual_cost')
    def _check_positive_amounts(self):
        """Vérifie que les montants sont positifs"""
        for record in self:
            if record.estimated_cost < 0:
                raise ValidationError("Le coût estimé doit être positif.")
            if record.actual_cost and record.actual_cost < 0:
                raise ValidationError("Le coût réel doit être positif.")
    
    @api.constrains('completion_percentage')
    def _check_completion_percentage(self):
        """Vérifie que le pourcentage d'achèvement est valide"""
        for record in self:
            if not (0 <= record.completion_percentage <= 100):
                raise ValidationError("Le pourcentage d'achèvement doit être entre 0 et 100.")
    
    @api.constrains('planned_start_date', 'planned_end_date')
    def _check_planned_dates(self):
        """Vérifie la cohérence des dates prévues"""
        for record in self:
            if record.planned_start_date and record.planned_end_date:
                if record.planned_start_date > record.planned_end_date:
                    raise ValidationError("La date de début prévue doit être antérieure à la date de fin prévue.")
    
    @api.constrains('actual_start_date', 'actual_end_date')
    def _check_actual_dates(self):
        """Vérifie la cohérence des dates réelles"""
        for record in self:
            if record.actual_start_date and record.actual_end_date:
                if record.actual_start_date > record.actual_end_date:
                    raise ValidationError("La date de début réelle doit être antérieure à la date de fin réelle.")
    
    # Actions
    def action_start_execution(self):
        """Démarre l'exécution de la composante"""
        self.write({
            'execution_status': 'in_progress',
            'actual_start_date': fields.Date.today()
        })
    
    def action_complete_execution(self):
        """Marque la composante comme achevée"""
        self.write({
            'execution_status': 'completed',
            'completion_percentage': 100.0,
            'actual_end_date': fields.Date.today()
        })
    
    def action_suspend_execution(self):
        """Suspend l'exécution de la composante"""
        self.write({'execution_status': 'suspended'})
    
    def action_cancel_execution(self):
        """Annule l'exécution de la composante"""
        self.write({'execution_status': 'cancelled'})
