from odoo import models, fields, api

class StrategicPlan(models.Model):
    _name = 'strategic.plan'
    _description = 'Plan Sénégal 2050'

    name = fields.Char(string="Plan Sénégal 2050", default="Plan Sénégal 2050", required=True)
    vision = fields.Text(string="Description de la Vision")
    start_date = fields.Date(string="Date de Début")
    end_date = fields.Date(string="Date de Fin")
    state = fields.Selection([
        ('draft', 'Brouillon'),
        ('validated', 'Validé'),
        ('archived', 'Archivé')
    ], string="Statut", default='draft')
    pillar_ids = fields.One2many('strategic.pillar', 'plan_id', string="Piliers Stratégiques")

class StrategicPillar(models.Model):
    _name = 'strategic.pillar'
    _description = 'Pilier Stratégique'

    name = fields.Char(string="Nom du Pilier", required=True)
    code = fields.Char(string="Code du Pilier")
    plan_id = fields.Many2one('strategic.plan', string="Plan Stratégique", required=True)
    description = fields.Html(string="Description")
    axis_ids = fields.One2many('strategic.axis', 'pillar_id', string="Axes Stratégiques")

class StrategicAxis(models.Model):
    _name = 'strategic.axis'
    _description = 'Axe Stratégique'

    name = fields.Char(string="Nom de l'Axe", required=True)
    code = fields.Char(string="Code de l'Axe")
    description = fields.Text(string="Description")
    pillar_id = fields.Many2one('strategic.pillar', string="Pilier Stratégique", required=True)
    objective_ids = fields.One2many('strategic.objective', 'axis_id', string="Objectifs/Actions Prioritaires")

class StrategicObjective(models.Model):
    _name = 'strategic.objective'
    _description = 'Objectif ou Action Prioritaire'

    name = fields.Char(string="Nom de l'Objectif", required=True)
    code = fields.Char(string="Code de l'Objectif")
    axis_id = fields.Many2one('strategic.axis', string="Axe Stratégique", required=True)
    description = fields.Text(string="Description")
    kpi_ids = fields.One2many('strategic.kpi', 'objective_id', string="Indicateurs Clés de Performance") # To be implemented later
    linked_projects = fields.One2many('government.project', 'strategic_objective_id', string="Projets Liés")
    linked_decisions = fields.One2many('government.decision', 'strategic_objective_id', string="Décisions Liées")
    linked_budgets = fields.One2many('government.budget', 'strategic_objective_id', string="Budgets Liés")
    linked_events = fields.One2many('government.event', 'strategic_objective_id', string="Événements Liés")


class StrategicKpi(models.Model):
    _name = 'strategic.kpi'
    _description = 'Indicateur Clé de Performance'

    name = fields.Char(string="Nom de l'Indicateur", required=True)
    code = fields.Char(string="Code de l'Indicateur")
    objective_id = fields.Many2one('strategic.objective', string="Objectif Stratégique", required=True)
    description = fields.Text(string="Description")
    target_value = fields.Float(string="Valeur Cible")
    current_value = fields.Float(string="Valeur Actuelle")
    unit_of_measure = fields.Char(string="Unité de Mesure")
    date_updated = fields.Date(string="Date de Mise à Jour", default=fields.Date.today)
