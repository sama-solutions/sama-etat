# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
from datetime import datetime, timedelta


class SyndicatAction(models.Model):
    _name = 'syndicat.action'
    _description = 'Action Syndicale'
    _order = 'date_debut desc'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(
        string='Titre de l\'Action',
        required=True,
        tracking=True,
        help="Titre de l'action syndicale"
    )
    
    reference = fields.Char(
        string='Référence',
        required=True,
        copy=False,
        default=lambda self: _('Nouveau'),
        tracking=True,
        help="Référence unique de l'action"
    )
    
    description = fields.Html(
        string='Description',
        required=True,
        help="Description détaillée de l'action"
    )
    
    # Classification
    type_action = fields.Selection([
        ('greve', 'Grève'),
        ('manifestation', 'Manifestation'),
        ('rassemblement', 'Rassemblement'),
        ('petition', 'Pétition'),
        ('boycott', 'Boycott'),
        ('sit_in', 'Sit-in'),
        ('marche', 'Marche'),
        ('conference_presse', 'Conférence de Presse'),
        ('campagne_sensibilisation', 'Campagne de Sensibilisation'),
        ('action_juridique', 'Action Juridique'),
        ('negociation_collective', 'Négociation Collective'),
        ('formation', 'Formation/Sensibilisation'),
        ('solidarite', 'Action de Solidarité'),
        ('autre', 'Autre')
    ], string='Type d\'Action',
       required=True,
       default='manifestation',
       tracking=True,
       help="Type d'action syndicale")
    
    statut = fields.Selection([
        ('planifiee', 'Planifiée'),
        ('approuvee', 'Approuvée'),
        ('en_preparation', 'En Préparation'),
        ('en_cours', 'En Cours'),
        ('terminee', 'Terminée'),
        ('reportee', 'Reportée'),
        ('annulee', 'Annulée'),
        ('suspendue', 'Suspendue')
    ], string='Statut',
       default='planifiee',
       required=True,
       tracking=True,
       help="Statut de l'action")
    
    urgence = fields.Selection([
        ('faible', 'Faible'),
        ('normale', 'Normale'),
        ('elevee', 'Élevée'),
        ('critique', 'Critique'),
        ('urgente', 'Urgente')
    ], string='Urgence',
       default='normale',
       tracking=True,
       help="Niveau d'urgence de l'action")
    
    # Dates et horaires
    date_debut = fields.Datetime(
        string='Date et Heure de Début',
        required=True,
        tracking=True,
        help="Date et heure de début de l'action"
    )
    
    date_fin = fields.Datetime(
        string='Date et Heure de Fin',
        tracking=True,
        help="Date et heure de fin prévue de l'action"
    )
    
    duree_prevue = fields.Float(
        string='Durée Prévue (heures)',
        compute='_compute_duree_prevue',
        store=True,
        help="Durée prévue de l'action en heures"
    )
    
    duree_reelle = fields.Float(
        string='Durée Réelle (heures)',
        compute='_compute_duree_reelle',
        store=True,
        help="Durée réelle de l'action en heures"
    )
    
    # Lieu et organisation
    lieu_principal = fields.Char(
        string='Lieu Principal',
        required=True,
        help="Lieu principal de l'action"
    )
    
    adresse_complete = fields.Text(
        string='Adresse Complète',
        help="Adresse complète du lieu de l'action"
    )
    
    lieux_secondaires = fields.Text(
        string='Lieux Secondaires',
        help="Autres lieux concernés par l'action"
    )
    
    itineraire = fields.Text(
        string='Itinéraire',
        help="Itinéraire prévu (pour marches, manifestations)"
    )
    
    # Responsables et organisation
    responsable_principal_id = fields.Many2one(
        'syndicat.adherent',
        string='Responsable Principal',
        required=True,
        tracking=True,
        help="Responsable principal de l'action"
    )
    
    responsables_secondaires_ids = fields.Many2many(
        'syndicat.adherent',
        'action_responsable_rel',
        'action_id',
        'adherent_id',
        string='Responsables Secondaires',
        help="Responsables secondaires de l'action"
    )
    
    comite_organisation_ids = fields.Many2many(
        'syndicat.adherent',
        'action_comite_rel',
        'action_id',
        'adherent_id',
        string='Comité d\'Organisation',
        help="Membres du comité d'organisation"
    )
    
    # Objectifs et revendications
    objectifs = fields.Html(
        string='Objectifs',
        required=True,
        help="Objectifs de l'action"
    )
    
    revendications_liees_ids = fields.Many2many(
        'syndicat.revendication',
        'action_revendication_rel',
        'action_id',
        'revendication_id',
        string='Revendications Liées',
        help="Revendications soutenues par cette action"
    )
    
    mots_ordre = fields.Text(
        string='Mots d\'Ordre',
        help="Mots d'ordre et slogans de l'action"
    )
    
    # Participants
    adherents_participants_ids = fields.Many2many(
        'syndicat.adherent',
        'action_participant_rel',
        'action_id',
        'adherent_id',
        string='Adhérents Participants',
        help="Adhérents participant à l'action"
    )
    
    nb_participants_prevu = fields.Integer(
        string='Participants Prévus',
        help="Nombre de participants prévus"
    )
    
    nb_participants_reel = fields.Integer(
        string='Participants Réels',
        compute='_compute_nb_participants',
        store=True,
        help="Nombre réel de participants"
    )
    
    participants_externes = fields.Text(
        string='Participants Externes',
        help="Participants externes (autres syndicats, associations)"
    )
    
    # Autorisations et légalité
    autorisation_requise = fields.Boolean(
        string='Autorisation Requise',
        default=True,
        help="Autorisation administrative requise"
    )
    
    autorisation_obtenue = fields.Boolean(
        string='Autorisation Obtenue',
        default=False,
        tracking=True,
        help="Autorisation administrative obtenue"
    )
    
    date_demande_autorisation = fields.Date(
        string='Date Demande Autorisation',
        tracking=True
    )
    
    date_reponse_autorisation = fields.Date(
        string='Date Réponse Autorisation',
        tracking=True
    )
    
    reference_autorisation = fields.Char(
        string='Référence Autorisation',
        help="Numéro ou référence de l'autorisation"
    )
    
    conditions_autorisation = fields.Text(
        string='Conditions d\'Autorisation',
        help="Conditions imposées par l'autorisation"
    )
    
    # Sécurité et service d'ordre
    service_ordre_requis = fields.Boolean(
        string='Service d\'Ordre Requis',
        default=True,
        help="Service d'ordre syndical requis"
    )
    
    responsables_securite_ids = fields.Many2many(
        'syndicat.adherent',
        'action_securite_rel',
        'action_id',
        'adherent_id',
        string='Responsables Sécurité',
        help="Responsables du service d'ordre"
    )
    
    consignes_securite = fields.Text(
        string='Consignes de Sécurité',
        help="Consignes de sécurité pour les participants"
    )
    
    # Communication et médias
    communication_ids = fields.One2many(
        'syndicat.communication',
        'action_id',
        string='Communications'
    )
    
    communique_presse = fields.Html(
        string='Communiqué de Presse',
        help="Communiqué de presse de l'action"
    )
    
    couverture_media = fields.Text(
        string='Couverture Médiatique',
        help="Médias ayant couvert l'action"
    )
    
    # Logistique
    materiel_requis = fields.Text(
        string='Matériel Requis',
        help="Liste du matériel nécessaire"
    )
    
    budget_prevu = fields.Monetary(
        string='Budget Prévu',
        currency_field='currency_id',
        help="Budget prévu pour l'action"
    )
    
    budget_reel = fields.Monetary(
        string='Budget Réel',
        currency_field='currency_id',
        help="Budget réellement dépensé"
    )

    # Coût par participant (calculé)
    cout_par_participant = fields.Monetary(
        string='Coût par Participant',
        currency_field='currency_id',
        compute='_compute_cout_par_participant',
        store=True,
        help="Budget réel divisé par le nombre de participants présents"
    )
    
    currency_id = fields.Many2one(
        'res.currency',
        string='Devise',
        default=lambda self: self.env.company.currency_id
    )
    
    # Résultats et évaluation
    resultats_obtenus = fields.Html(
        string='Résultats Obtenus',
        help="Description des résultats obtenus"
    )
    
    impact_media = fields.Selection([
        ('faible', 'Faible'),
        ('moyen', 'Moyen'),
        ('fort', 'Fort'),
        ('tres_fort', 'Très Fort')
    ], string='Impact Médiatique',
       help="Évaluation de l'impact médiatique")
    
    impact_revendications = fields.Selection([
        ('aucun', 'Aucun Impact'),
        ('faible', 'Faible Impact'),
        ('moyen', 'Impact Moyen'),
        ('fort', 'Fort Impact'),
        ('decisif', 'Impact Décisif')
    ], string='Impact sur Revendications',
       help="Impact sur les revendications")
    
    satisfaction_participants = fields.Selection([
        ('1', 'Très Insatisfait'),
        ('2', 'Insatisfait'),
        ('3', 'Neutre'),
        ('4', 'Satisfait'),
        ('5', 'Très Satisfait')
    ], string='Satisfaction Participants',
       help="Niveau de satisfaction des participants")
    
    # Incidents et problèmes
    incidents = fields.Text(
        string='Incidents',
        help="Description des incidents survenus"
    )
    
    problemes_rencontres = fields.Text(
        string='Problèmes Rencontrés',
        help="Problèmes rencontrés durant l'action"
    )
    
    # Suivi
    actions_suivi_ids = fields.One2many(
        'syndicat.action.suivi',
        'action_id',
        string='Actions de Suivi'
    )
    
    lecons_apprises = fields.Text(
        string='Leçons Apprises',
        help="Leçons tirées de cette action"
    )
    
    # Métadonnées
    active = fields.Boolean(
        string='Actif',
        default=True,
        help="Décocher pour archiver l'action"
    )
    
    notes_internes = fields.Text(
        string='Notes Internes',
        help="Notes internes pour l'organisation"
    )

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('reference', _('Nouveau')) == _('Nouveau'):
                vals['reference'] = self.env['ir.sequence'].next_by_code('syndicat.action') or _('Nouveau')
        return super(SyndicatAction, self).create(vals_list)

    @api.depends('date_debut', 'date_fin')
    def _compute_duree_prevue(self):
        for record in self:
            if record.date_debut and record.date_fin:
                delta = record.date_fin - record.date_debut
                record.duree_prevue = delta.total_seconds() / 3600
            else:
                record.duree_prevue = 0.0

    @api.depends('date_debut', 'date_fin', 'statut')
    def _compute_duree_reelle(self):
        for record in self:
            if record.statut == 'terminee' and record.date_debut and record.date_fin:
                delta = record.date_fin - record.date_debut
                record.duree_reelle = delta.total_seconds() / 3600
            else:
                record.duree_reelle = 0.0

    @api.depends('adherents_participants_ids')
    def _compute_nb_participants(self):
        for record in self:
            record.nb_participants_reel = len(record.adherents_participants_ids)

    def action_view_participants(self):
        """Ouvre la liste des adhérents participants"""
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': _('Participants'),
            'res_model': 'syndicat.adherent',
            'view_mode': 'tree,form',
            'domain': [('id', 'in', self.adherents_participants_ids.ids)],
            'target': 'current',
        }

    def action_view_communications(self):
        """Ouvre les communications liées à cette action"""
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': _('Communications'),
            'res_model': 'syndicat.communication',
            'view_mode': 'tree,form',
            'domain': [('action_id', '=', self.id)],
            'context': {'default_action_id': self.id},
            'target': 'current',
        }

    def action_view_revendications(self):
        """Ouvre les revendications liées à cette action"""
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': _('Revendications'),
            'res_model': 'syndicat.revendication',
            'view_mode': 'tree,form',
            'domain': [('id', 'in', self.revendications_liees_ids.ids)],
            'target': 'current',
        }

    @api.depends('budget_reel', 'nb_participants_reel')
    def _compute_cout_par_participant(self):
        for record in self:
            if record.nb_participants_reel:
                record.cout_par_participant = record.budget_reel / record.nb_participants_reel
            else:
                record.cout_par_participant = 0.0

    @api.constrains('date_debut', 'date_fin')
    def _check_dates_coherence(self):
        for record in self:
            if record.date_debut and record.date_fin:
                if record.date_fin <= record.date_debut:
                    raise ValidationError(_("La date de fin doit être postérieure à la date de début."))

    @api.onchange('type_action')
    def _onchange_type_action(self):
        # Définir l'urgence et les autorisations par défaut selon le type
        if self.type_action == 'greve':
            self.urgence = 'critique'
            self.autorisation_requise = True
            self.service_ordre_requis = True
        elif self.type_action in ['manifestation', 'marche', 'rassemblement']:
            self.urgence = 'elevee'
            self.autorisation_requise = True
            self.service_ordre_requis = True
        elif self.type_action in ['petition', 'campagne_sensibilisation']:
            self.urgence = 'normale'
            self.autorisation_requise = False
            self.service_ordre_requis = False
        elif self.type_action == 'conference_presse':
            self.urgence = 'normale'
            self.autorisation_requise = False
            self.service_ordre_requis = False

    def action_approuver(self):
        """Approuve l'action"""
        self.ensure_one()
        if self.statut == 'planifiee':
            self.statut = 'approuvee'
            self.message_post(body=_("Action approuvée."))
        return True

    def action_commencer_preparation(self):
        """Commence la préparation"""
        self.ensure_one()
        if self.statut == 'approuvee':
            self.statut = 'en_preparation'
            self.message_post(body=_("Préparation de l'action commencée."))
        return True

    def action_commencer(self):
        """Démarre l'action"""
        self.ensure_one()
        if self.statut == 'en_preparation':
            self.statut = 'en_cours'
            if not self.date_debut:
                self.date_debut = fields.Datetime.now()
            self.message_post(body=_("Action démarrée."))
        return True

    def action_terminer(self):
        """Termine l'action"""
        self.ensure_one()
        if self.statut == 'en_cours':
            self.statut = 'terminee'
            if not self.date_fin:
                self.date_fin = fields.Datetime.now()
            self.message_post(body=_("Action terminée."))
        return True

    def action_reporter(self):
        """Reporte l'action"""
        self.ensure_one()
        if self.statut in ['planifiee', 'approuvee', 'en_preparation']:
            self.statut = 'reportee'
            self.message_post(body=_("Action reportée."))
        return True

    def action_annuler(self):
        """Annule l'action"""
        self.ensure_one()
        if self.statut in ['planifiee', 'approuvee', 'en_preparation']:
            self.statut = 'annulee'
            self.message_post(body=_("Action annulée."))
        return True

    def action_suspendre(self):
        """Suspend l'action"""
        self.ensure_one()
        if self.statut == 'en_cours':
            self.statut = 'suspendue'
            self.message_post(body=_("Action suspendue."))
        return True

    def action_demander_autorisation(self):
        """Demande l'autorisation administrative"""
        self.ensure_one()
        if self.autorisation_requise and not self.date_demande_autorisation:
            self.date_demande_autorisation = fields.Date.today()
            self.message_post(body=_("Demande d'autorisation envoyée."))
        return True

    def action_autorisation_obtenue(self):
        """Marque l'autorisation comme obtenue"""
        self.ensure_one()
        if self.autorisation_requise:
            self.write({
                'autorisation_obtenue': True,
                'date_reponse_autorisation': fields.Date.today()
            })
            self.message_post(body=_("Autorisation obtenue."))
        return True

    def action_ajouter_participant(self, adherent_id):
        """Ajoute un participant"""
        self.ensure_one()
        adherent = self.env['syndicat.adherent'].browse(adherent_id)
        if adherent.statut_adhesion == 'actif' and adherent not in self.adherents_participants_ids:
            self.adherents_participants_ids = [(4, adherent_id)]
            self.message_post(body=_("Participant ajouté : %s.") % adherent.name)

    def action_retirer_participant(self, adherent_id):
        """Retire un participant"""
        self.ensure_one()
        adherent = self.env['syndicat.adherent'].browse(adherent_id)
        if adherent in self.adherents_participants_ids:
            self.adherents_participants_ids = [(3, adherent_id)]
            self.message_post(body=_("Participant retiré : %s.") % adherent.name)

    @api.model
    def get_actions_du_jour(self):
        """Retourne les actions du jour"""
        today = fields.Date.today()
        return self.search([
            ('date_debut', '>=', today),
            ('date_debut', '<', today + timedelta(days=1))
        ])

    @api.model
    def get_prochaines_actions(self, limit=5):
        """Retourne les prochaines actions"""
        return self.search([
            ('date_debut', '>', fields.Datetime.now()),
            ('statut', 'in', ['planifiee', 'approuvee', 'en_preparation'])
        ], limit=limit, order='date_debut asc')

    @api.model
    def get_statistiques_actions(self):
        """Retourne les statistiques des actions"""
        total = self.search_count([])
        en_cours = self.search_count([('statut', 'in', ['planifiee', 'approuvee', 'en_preparation', 'en_cours'])])
        terminees = self.search_count([('statut', '=', 'terminee')])
        annulees = self.search_count([('statut', 'in', ['annulee', 'reportee'])])
        
        return {
            'total': total,
            'en_cours': en_cours,
            'terminees': terminees,
            'annulees': annulees,
            'taux_reussite': (terminees / total * 100) if total > 0 else 0
        }

    @api.model
    def get_actions_par_type(self):
        """Retourne la répartition des actions par type"""
        result = []
        for type_action in dict(self._fields['type_action'].selection):
            count = self.search_count([('type_action', '=', type_action)])
            if count > 0:
                result.append({
                    'type': type_action,
                    'label': dict(self._fields['type_action'].selection)[type_action],
                    'count': count
                })
        return result

    def name_get(self):
        result = []
        for record in self:
            name = f"[{record.reference}] {record.name}"
            if record.date_debut:
                name += f" - {record.date_debut.strftime('%d/%m/%Y')}"
            result.append((record.id, name))
        return result

    @api.model
    def _name_search(self, name='', args=None, operator='ilike', limit=100, name_get_uid=None):
        args = args or []
        if name:
            args = [
                '|', '|', '|',
                ('name', operator, name),
                ('reference', operator, name),
                ('description', operator, name),
                ('lieu_principal', operator, name)
            ] + args
        return self._search(args, limit=limit, access_rights_uid=name_get_uid)


class SyndicatActionSuivi(models.Model):
    _name = 'syndicat.action.suivi'
    _description = 'Suivi d\'Action Syndicale'
    _order = 'date_suivi desc'

    name = fields.Char(
        string='Titre du Suivi',
        required=True,
        help="Titre de l'action de suivi"
    )
    
    action_id = fields.Many2one(
        'syndicat.action',
        string='Action',
        required=True,
        ondelete='cascade'
    )
    
    date_suivi = fields.Date(
        string='Date de Suivi',
        required=True,
        default=fields.Date.today
    )
    
    type_suivi = fields.Selection([
        ('evaluation', 'Évaluation'),
        ('communication', 'Communication'),
        ('negociation', 'Négociation'),
        ('action_complementaire', 'Action Complémentaire'),
        ('rapport', 'Rapport'),
        ('autre', 'Autre')
    ], string='Type de Suivi',
       required=True,
       default='evaluation')
    
    description = fields.Html(
        string='Description',
        required=True,
        help="Description du suivi effectué"
    )
    
    responsable_id = fields.Many2one(
        'syndicat.adherent',
        string='Responsable',
        required=True,
        help="Responsable du suivi"
    )
    
    statut = fields.Selection([
        ('planifie', 'Planifié'),
        ('en_cours', 'En Cours'),
        ('termine', 'Terminé'),
        ('reporte', 'Reporté')
    ], string='Statut',
       default='planifie',
       required=True)
    
    resultats = fields.Html(
        string='Résultats',
        help="Résultats du suivi"
    )
    
    prochaines_actions = fields.Html(
        string='Prochaines Actions',
        help="Actions à entreprendre suite à ce suivi"
    )
    
    notes = fields.Text(
        string='Notes',
        help="Notes diverses"
    )