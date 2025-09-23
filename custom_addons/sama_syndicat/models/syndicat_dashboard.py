# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from datetime import datetime, timedelta


class SyndicatDashboard(models.Model):
    _name = 'syndicat.dashboard'
    _description = 'Tableau de Bord Syndical'
    _order = 'date_creation desc'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(
        string='Nom du Tableau de Bord',
        required=True,
        default='Tableau de Bord Syndical'
    )
    
    date_creation = fields.Datetime(
        string='Date de Création',
        default=fields.Datetime.now,
        required=True
    )
    
    date_derniere_maj = fields.Datetime(
        string='Dernière Mise à Jour',
        default=fields.Datetime.now
    )
    
    # Statistiques des adhérents
    nb_adherents_total = fields.Integer(
        string='Total Adhérents',
        compute='_compute_stats_adherents',
        store=True
    )
    
    nb_adherents_actifs = fields.Integer(
        string='Adhérents Actifs',
        compute='_compute_stats_adherents',
        store=True
    )
    
    nb_adherents_suspendus = fields.Integer(
        string='Adhérents Suspendus',
        compute='_compute_stats_adherents',
        store=True
    )
    
    nb_nouveaux_adherents_mois = fields.Integer(
        string='Nouveaux Adhérents ce Mois',
        compute='_compute_stats_adherents',
        store=True
    )
    
    taux_croissance_adherents = fields.Float(
        string='Taux de Croissance Adhérents (%)',
        compute='_compute_stats_adherents',
        store=True
    )
    
    # Statistiques des cotisations
    nb_cotisations_jour = fields.Integer(
        string='Cotisations à Jour',
        compute='_compute_stats_cotisations',
        store=True
    )
    
    nb_cotisations_retard = fields.Integer(
        string='Cotisations en Retard',
        compute='_compute_stats_cotisations',
        store=True
    )
    
    taux_cotisations_jour = fields.Float(
        string='Taux Cotisations à Jour (%)',
        compute='_compute_stats_cotisations',
        store=True
    )
    
    montant_cotisations_mois = fields.Monetary(
        string='Cotisations du Mois',
        currency_field='currency_id',
        compute='_compute_stats_cotisations',
        store=True
    )
    
    # Statistiques des assemblées
    nb_assemblees_total = fields.Integer(
        string='Total Assemblées',
        compute='_compute_stats_assemblees',
        store=True
    )
    
    nb_assemblees_mois = fields.Integer(
        string='Assemblées ce Mois',
        compute='_compute_stats_assemblees',
        store=True
    )
    
    taux_participation_moyen = fields.Float(
        string='Taux de Participation Moyen (%)',
        compute='_compute_stats_assemblees',
        store=True
    )
    
    prochaine_assemblee = fields.Char(
        string='Prochaine Assemblée',
        compute='_compute_stats_assemblees',
        store=True
    )
    
    # Statistiques des revendications
    nb_revendications_total = fields.Integer(
        string='Total Revendications',
        compute='_compute_stats_revendications',
        store=True
    )
    
    nb_revendications_en_cours = fields.Integer(
        string='Revendications en Cours',
        compute='_compute_stats_revendications',
        store=True
    )
    
    nb_revendications_acceptees = fields.Integer(
        string='Revendications Acceptées',
        compute='_compute_stats_revendications',
        store=True
    )
    
    taux_succes_revendications = fields.Float(
        string='Taux de Succès Revendications (%)',
        compute='_compute_stats_revendications',
        store=True
    )
    
    # Statistiques des actions
    nb_actions_total = fields.Integer(
        string='Total Actions',
        compute='_compute_stats_actions',
        store=True
    )
    
    nb_actions_en_cours = fields.Integer(
        string='Actions en Cours',
        compute='_compute_stats_actions',
        store=True
    )
    
    nb_actions_terminees = fields.Integer(
        string='Actions Terminées',
        compute='_compute_stats_actions',
        store=True
    )
    
    prochaine_action = fields.Char(
        string='Prochaine Action',
        compute='_compute_stats_actions',
        store=True
    )
    
    # Statistiques des formations
    nb_formations_total = fields.Integer(
        string='Total Formations',
        compute='_compute_stats_formations',
        store=True
    )
    
    nb_formations_en_cours = fields.Integer(
        string='Formations en Cours',
        compute='_compute_stats_formations',
        store=True
    )
    
    nb_adherents_formes = fields.Integer(
        string='Adhérents Formés',
        compute='_compute_stats_formations',
        store=True
    )
    
    # Statistiques des médiations
    nb_mediations_total = fields.Integer(
        string='Total Médiations',
        compute='_compute_stats_mediations',
        store=True
    )
    
    nb_mediations_en_cours = fields.Integer(
        string='Médiations en Cours',
        compute='_compute_stats_mediations',
        store=True
    )
    
    nb_mediations_resolues = fields.Integer(
        string='Médiations Résolues',
        compute='_compute_stats_mediations',
        store=True
    )
    
    taux_reussite_mediations = fields.Float(
        string='Taux de Réussite Médiations (%)',
        compute='_compute_stats_mediations',
        store=True
    )
    
    # Statistiques des communications
    nb_communications_mois = fields.Integer(
        string='Communications ce Mois',
        compute='_compute_stats_communications',
        store=True
    )
    
    taux_ouverture_moyen = fields.Float(
        string='Taux d\'Ouverture Moyen (%)',
        compute='_compute_stats_communications',
        store=True
    )
    
    # Alertes et notifications
    alertes_cotisations = fields.Integer(
        string='Alertes Cotisations',
        compute='_compute_alertes',
        store=True
    )
    
    alertes_assemblees = fields.Integer(
        string='Alertes Assemblées',
        compute='_compute_alertes',
        store=True
    )
    
    alertes_actions = fields.Integer(
        string='Alertes Actions',
        compute='_compute_alertes',
        store=True
    )
    
    alertes_mediations = fields.Integer(
        string='Alertes Médiations',
        compute='_compute_alertes',
        store=True
    )
    
    # Métadonnées
    currency_id = fields.Many2one(
        'res.currency',
        string='Devise',
        default=lambda self: self.env.company.currency_id
    )
    
    active = fields.Boolean(
        string='Actif',
        default=True
    )

    @api.depends()
    def _compute_stats_adherents(self):
        for record in self:
            # Total adhérents
            record.nb_adherents_total = self.env['syndicat.adherent'].search_count([])
            
            # Adhérents actifs
            record.nb_adherents_actifs = self.env['syndicat.adherent'].search_count([
                ('statut_adhesion', '=', 'actif')
            ])
            
            # Adhérents suspendus
            record.nb_adherents_suspendus = self.env['syndicat.adherent'].search_count([
                ('statut_adhesion', '=', 'suspendu')
            ])
            
            # Nouveaux adhérents ce mois
            debut_mois = fields.Date.today().replace(day=1)
            record.nb_nouveaux_adherents_mois = self.env['syndicat.adherent'].search_count([
                ('date_adhesion', '>=', debut_mois)
            ])
            
            # Taux de croissance (comparaison avec le mois précédent)
            debut_mois_precedent = (debut_mois - timedelta(days=1)).replace(day=1)
            fin_mois_precedent = debut_mois - timedelta(days=1)
            
            adherents_mois_precedent = self.env['syndicat.adherent'].search_count([
                ('date_adhesion', '>=', debut_mois_precedent),
                ('date_adhesion', '<=', fin_mois_precedent)
            ])
            
            if adherents_mois_precedent > 0:
                record.taux_croissance_adherents = (
                    (record.nb_nouveaux_adherents_mois - adherents_mois_precedent) / 
                    adherents_mois_precedent * 100
                )
            else:
                record.taux_croissance_adherents = 0.0

    @api.depends()
    def _compute_stats_cotisations(self):
        for record in self:
            # Cotisations à jour
            record.nb_cotisations_jour = self.env['syndicat.adherent'].search_count([
                ('statut_adhesion', '=', 'actif'),
                ('cotisations_a_jour', '=', True)
            ])
            
            # Cotisations en retard
            record.nb_cotisations_retard = self.env['syndicat.adherent'].search_count([
                ('statut_adhesion', '=', 'actif'),
                ('cotisations_a_jour', '=', False)
            ])
            
            # Taux de cotisations à jour
            if record.nb_adherents_actifs > 0:
                record.taux_cotisations_jour = (record.nb_cotisations_jour / record.nb_adherents_actifs) * 100
            else:
                record.taux_cotisations_jour = 0.0
            
            # Montant des cotisations du mois
            debut_mois = fields.Date.today().replace(day=1)
            cotisations_mois = self.env['syndicat.cotisation'].search([
                ('date_paiement', '>=', debut_mois),
                ('statut', '=', 'payee')
            ])
            record.montant_cotisations_mois = sum(cotisations_mois.mapped('montant'))

    @api.depends()
    def _compute_stats_assemblees(self):
        for record in self:
            # Total assemblées
            record.nb_assemblees_total = self.env['syndicat.assemblee'].search_count([])
            
            # Assemblées ce mois
            debut_mois = fields.Date.today().replace(day=1)
            record.nb_assemblees_mois = self.env['syndicat.assemblee'].search_count([
                ('date_debut', '>=', debut_mois)
            ])
            
            # Taux de participation moyen
            assemblees_terminees = self.env['syndicat.assemblee'].search([
                ('statut', '=', 'terminee')
            ])
            if assemblees_terminees:
                taux_moyens = assemblees_terminees.mapped('taux_presence')
                record.taux_participation_moyen = sum(taux_moyens) / len(taux_moyens)
            else:
                record.taux_participation_moyen = 0.0
            
            # Prochaine assemblée
            prochaine = self.env['syndicat.assemblee'].search([
                ('date_debut', '>', fields.Datetime.now()),
                ('statut', 'in', ['planifiee', 'confirmee'])
            ], limit=1, order='date_debut asc')
            
            if prochaine:
                record.prochaine_assemblee = f"{prochaine.name} - {prochaine.date_debut.strftime('%d/%m/%Y')}"
            else:
                record.prochaine_assemblee = "Aucune assemblée prévue"

    @api.depends()
    def _compute_stats_revendications(self):
        for record in self:
            # Total revendications
            record.nb_revendications_total = self.env['syndicat.revendication'].search_count([])
            
            # Revendications en cours
            record.nb_revendications_en_cours = self.env['syndicat.revendication'].search_count([
                ('statut', 'in', ['soumise', 'en_negociation'])
            ])
            
            # Revendications acceptées
            record.nb_revendications_acceptees = self.env['syndicat.revendication'].search_count([
                ('statut', 'in', ['acceptee', 'acceptee_partiellement'])
            ])
            
            # Taux de succès
            if record.nb_revendications_total > 0:
                record.taux_succes_revendications = (
                    record.nb_revendications_acceptees / record.nb_revendications_total * 100
                )
            else:
                record.taux_succes_revendications = 0.0

    @api.depends()
    def _compute_stats_actions(self):
        for record in self:
            # Total actions
            record.nb_actions_total = self.env['syndicat.action'].search_count([])
            
            # Actions en cours
            record.nb_actions_en_cours = self.env['syndicat.action'].search_count([
                ('statut', 'in', ['planifiee', 'approuvee', 'en_preparation', 'en_cours'])
            ])
            
            # Actions terminées
            record.nb_actions_terminees = self.env['syndicat.action'].search_count([
                ('statut', '=', 'terminee')
            ])
            
            # Prochaine action
            prochaine = self.env['syndicat.action'].search([
                ('date_debut', '>', fields.Datetime.now()),
                ('statut', 'in', ['planifiee', 'approuvee', 'en_preparation'])
            ], limit=1, order='date_debut asc')
            
            if prochaine:
                record.prochaine_action = f"{prochaine.name} - {prochaine.date_debut.strftime('%d/%m/%Y')}"
            else:
                record.prochaine_action = "Aucune action prévue"

    @api.depends()
    def _compute_stats_formations(self):
        for record in self:
            # Total formations
            record.nb_formations_total = self.env['syndicat.formation'].search_count([])
            
            # Formations en cours
            record.nb_formations_en_cours = self.env['syndicat.formation'].search_count([
                ('statut', 'in', ['inscriptions_ouvertes', 'confirmee', 'en_cours'])
            ])
            
            # Adhérents formés (formations terminées)
            formations_terminees = self.env['syndicat.formation'].search([
                ('statut', '=', 'terminee')
            ])
            adherents_formes = set()
            for formation in formations_terminees:
                adherents_formes.update(formation.participants_ids.ids)
            record.nb_adherents_formes = len(adherents_formes)

    @api.depends()
    def _compute_stats_mediations(self):
        for record in self:
            # Total médiations
            record.nb_mediations_total = self.env['syndicat.mediation'].search_count([])
            
            # Médiations en cours
            record.nb_mediations_en_cours = self.env['syndicat.mediation'].search_count([
                ('statut', 'in', ['nouveau', 'en_cours', 'mediation', 'conciliation'])
            ])
            
            # Médiations résolues
            record.nb_mediations_resolues = self.env['syndicat.mediation'].search_count([
                ('statut', '=', 'resolu')
            ])
            
            # Taux de réussite
            if record.nb_mediations_total > 0:
                record.taux_reussite_mediations = (
                    record.nb_mediations_resolues / record.nb_mediations_total * 100
                )
            else:
                record.taux_reussite_mediations = 0.0

    @api.depends()
    def _compute_stats_communications(self):
        for record in self:
            # Communications ce mois
            debut_mois = fields.Date.today().replace(day=1)
            record.nb_communications_mois = self.env['syndicat.communication'].search_count([
                ('date_publication', '>=', debut_mois),
                ('statut', '=', 'publiee')
            ])
            
            # Taux d'ouverture moyen
            communications_avec_stats = self.env['syndicat.communication'].search([
                ('statut', '=', 'publiee'),
                ('nb_destinataires', '>', 0)
            ])
            
            if communications_avec_stats:
                taux_ouvertures = communications_avec_stats.mapped('taux_ouverture')
                record.taux_ouverture_moyen = sum(taux_ouvertures) / len(taux_ouvertures)
            else:
                record.taux_ouverture_moyen = 0.0

    @api.depends()
    def _compute_alertes(self):
        for record in self:
            # Alertes cotisations (adhérents en retard)
            record.alertes_cotisations = self.env['syndicat.adherent'].search_count([
                ('statut_adhesion', '=', 'actif'),
                ('cotisations_a_jour', '=', False)
            ])
            
            # Alertes assemblées (assemblées sans quorum)
            record.alertes_assemblees = self.env['syndicat.assemblee'].search_count([
                ('statut', 'in', ['planifiee', 'confirmee']),
                ('date_debut', '<=', fields.Datetime.now() + timedelta(days=7)),  # Dans la semaine
                ('quorum_atteint', '=', False)
            ])
            
            # Alertes actions (actions en retard)
            record.alertes_actions = self.env['syndicat.action'].search_count([
                ('statut', 'in', ['planifiee', 'approuvee']),
                ('date_debut', '<', fields.Datetime.now())
            ])
            
            # Alertes médiations (médiations urgentes)
            record.alertes_mediations = self.env['syndicat.mediation'].search_count([
                ('statut', 'in', ['nouveau', 'en_cours']),
                ('urgence', 'in', ['elevee', 'urgente'])
            ])

    def action_actualiser(self):
        """Actualise les données du tableau de bord"""
        self.ensure_one()
        self.date_derniere_maj = fields.Datetime.now()
        # Forcer le recalcul des champs calculés
        self._compute_stats_adherents()
        self._compute_stats_cotisations()
        self._compute_stats_assemblees()
        self._compute_stats_revendications()
        self._compute_stats_actions()
        self._compute_stats_formations()
        self._compute_stats_mediations()
        self._compute_stats_communications()
        self._compute_alertes()
        
        return {
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'params': {
                'title': _("Succès"),
                'message': _("Tableau de bord actualisé avec succès."),
                'sticky': False,
                'type': 'success'
            }
        }

    @api.model
    def get_dashboard_data(self):
        """Retourne les données du tableau de bord pour l'interface"""
        dashboard = self.search([], limit=1, order='date_creation desc')
        if not dashboard:
            dashboard = self.create({'name': 'Tableau de Bord Principal'})
        
        return {
            'adherents': {
                'total': dashboard.nb_adherents_total,
                'actifs': dashboard.nb_adherents_actifs,
                'suspendus': dashboard.nb_adherents_suspendus,
                'nouveaux_mois': dashboard.nb_nouveaux_adherents_mois,
                'taux_croissance': dashboard.taux_croissance_adherents,
            },
            'cotisations': {
                'a_jour': dashboard.nb_cotisations_jour,
                'en_retard': dashboard.nb_cotisations_retard,
                'taux_jour': dashboard.taux_cotisations_jour,
                'montant_mois': dashboard.montant_cotisations_mois,
            },
            'assemblees': {
                'total': dashboard.nb_assemblees_total,
                'mois': dashboard.nb_assemblees_mois,
                'taux_participation': dashboard.taux_participation_moyen,
                'prochaine': dashboard.prochaine_assemblee,
            },
            'revendications': {
                'total': dashboard.nb_revendications_total,
                'en_cours': dashboard.nb_revendications_en_cours,
                'acceptees': dashboard.nb_revendications_acceptees,
                'taux_succes': dashboard.taux_succes_revendications,
            },
            'actions': {
                'total': dashboard.nb_actions_total,
                'en_cours': dashboard.nb_actions_en_cours,
                'terminees': dashboard.nb_actions_terminees,
                'prochaine': dashboard.prochaine_action,
            },
            'formations': {
                'total': dashboard.nb_formations_total,
                'en_cours': dashboard.nb_formations_en_cours,
                'adherents_formes': dashboard.nb_adherents_formes,
            },
            'mediations': {
                'total': dashboard.nb_mediations_total,
                'en_cours': dashboard.nb_mediations_en_cours,
                'resolues': dashboard.nb_mediations_resolues,
                'taux_reussite': dashboard.taux_reussite_mediations,
            },
            'communications': {
                'mois': dashboard.nb_communications_mois,
                'taux_ouverture': dashboard.taux_ouverture_moyen,
            },
            'alertes': {
                'cotisations': dashboard.alertes_cotisations,
                'assemblees': dashboard.alertes_assemblees,
                'actions': dashboard.alertes_actions,
                'mediations': dashboard.alertes_mediations,
            },
            'derniere_maj': dashboard.date_derniere_maj,
        }

    @api.model
    def get_graphiques_data(self):
        """Retourne les données pour les graphiques"""
        # Évolution des adhérents sur 12 mois
        adherents_evolution = []
        for i in range(12):
            date_fin = fields.Date.today().replace(day=1) - timedelta(days=i*30)
            date_debut = date_fin.replace(day=1)
            
            nb_adherents = self.env['syndicat.adherent'].search_count([
                ('date_adhesion', '<=', date_fin)
            ])
            
            adherents_evolution.append({
                'mois': date_debut.strftime('%m/%Y'),
                'nombre': nb_adherents
            })
        
        # Répartition des revendications par type
        revendications_par_type = self.env['syndicat.revendication'].get_revendications_par_type()
        
        # Répartition des actions par type
        actions_par_type = self.env['syndicat.action'].get_actions_par_type()
        
        return {
            'adherents_evolution': list(reversed(adherents_evolution)),
            'revendications_par_type': revendications_par_type,
            'actions_par_type': actions_par_type,
        }

    # Méthodes de navigation pour les cartes du dashboard
    def action_open_adherents(self):
        """Ouvre la vue des adhérents"""
        return {
            'type': 'ir.actions.act_window',
            'name': _('Adhérents'),
            'res_model': 'syndicat.adherent',
            'view_mode': 'kanban,list,form',
            'target': 'current',
            'context': {'search_default_actifs': 1},
        }

    def action_open_cotisations(self):
        """Ouvre la vue des cotisations"""
        return {
            'type': 'ir.actions.act_window',
            'name': _('Cotisations'),
            'res_model': 'syndicat.cotisation',
            'view_mode': 'list,form',
            'target': 'current',
        }

    def action_open_assemblees(self):
        """Ouvre la vue des assemblées"""
        return {
            'type': 'ir.actions.act_window',
            'name': _('Assemblées'),
            'res_model': 'syndicat.assemblee',
            'view_mode': 'kanban,calendar,list,form',
            'target': 'current',
        }

    def action_open_revendications(self):
        """Ouvre la vue des revendications"""
        return {
            'type': 'ir.actions.act_window',
            'name': _('Revendications'),
            'res_model': 'syndicat.revendication',
            'view_mode': 'kanban,list,form',
            'target': 'current',
        }

    def action_open_actions(self):
        """Ouvre la vue des actions"""
        return {
            'type': 'ir.actions.act_window',
            'name': _('Actions Syndicales'),
            'res_model': 'syndicat.action',
            'view_mode': 'kanban,calendar,list,form',
            'target': 'current',
        }

    def action_open_formations(self):
        """Ouvre la vue des formations"""
        return {
            'type': 'ir.actions.act_window',
            'name': _('Formations'),
            'res_model': 'syndicat.formation',
            'view_mode': 'kanban,calendar,list,form',
            'target': 'current',
        }

    def action_open_mediations(self):
        """Ouvre la vue des médiations"""
        return {
            'type': 'ir.actions.act_window',
            'name': _('Médiations'),
            'res_model': 'syndicat.mediation',
            'view_mode': 'kanban,list,form',
            'target': 'current',
        }

    def action_open_communications(self):
        """Ouvre la vue des communications"""
        return {
            'type': 'ir.actions.act_window',
            'name': _('Communications'),
            'res_model': 'syndicat.communication',
            'view_mode': 'kanban,list,form',
            'target': 'current',
        }

    def action_open_alertes_cotisations(self):
        """Ouvre les adhérents avec cotisations en retard"""
        return {
            'type': 'ir.actions.act_window',
            'name': _('Adhérents - Cotisations en Retard'),
            'res_model': 'syndicat.adherent',
            'view_mode': 'list,form',
            'target': 'current',
            'domain': [('statut_adhesion', '=', 'actif'), ('cotisations_a_jour', '=', False)],
        }

    def action_open_alertes_assemblees(self):
        """Ouvre les assemblées sans quorum"""
        return {
            'type': 'ir.actions.act_window',
            'name': _('Assemblées - Problèmes de Quorum'),
            'res_model': 'syndicat.assemblee',
            'view_mode': 'list,form',
            'target': 'current',
            'domain': [('statut', 'in', ['planifiee', 'confirmee']), ('quorum_atteint', '=', False)],
        }

    def action_open_alertes_actions(self):
        """Ouvre les actions en retard"""
        return {
            'type': 'ir.actions.act_window',
            'name': _('Actions - En Retard'),
            'res_model': 'syndicat.action',
            'view_mode': 'list,form',
            'target': 'current',
            'domain': [('statut', 'in', ['planifiee', 'approuvee']), ('date_debut', '<', fields.Datetime.now())],
        }

    def action_open_alertes_mediations(self):
        """Ouvre les médiations urgentes"""
        return {
            'type': 'ir.actions.act_window',
            'name': _('Médiations - Urgentes'),
            'res_model': 'syndicat.mediation',
            'view_mode': 'list,form',
            'target': 'current',
            'domain': [('statut', 'in', ['nouveau', 'en_cours']), ('urgence', 'in', ['elevee', 'urgente'])],
        }