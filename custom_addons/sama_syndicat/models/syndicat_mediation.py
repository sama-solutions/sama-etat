# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class SyndicatMediation(models.Model):
    _name = 'syndicat.mediation'
    _description = 'Médiation et Gestion des Conflits'
    _order = 'date_creation desc'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(
        string='Titre du Conflit',
        required=True,
        tracking=True,
        help="Titre du conflit ou de la médiation"
    )
    
    reference = fields.Char(
        string='Référence',
        required=True,
        copy=False,
        default=lambda self: _('Nouveau'),
        tracking=True,
        help="Référence unique de la médiation"
    )
    
    description = fields.Html(
        string='Description du Conflit',
        required=True,
        help="Description détaillée du conflit"
    )
    
    # Classification
    type_conflit = fields.Selection([
        ('individuel', 'Conflit Individuel'),
        ('collectif', 'Conflit Collectif'),
        ('disciplinaire', 'Sanction Disciplinaire'),
        ('licenciement', 'Licenciement'),
        ('discrimination', 'Discrimination'),
        ('harcelement', 'Harcèlement'),
        ('conditions_travail', 'Conditions de Travail'),
        ('salaire', 'Conflit Salarial'),
        ('temps_travail', 'Temps de Travail'),
        ('promotion', 'Promotion/Mutation'),
        ('formation', 'Formation'),
        ('securite', 'Sécurité au Travail'),
        ('syndical', 'Conflit Syndical'),
        ('autre', 'Autre')
    ], string='Type de Conflit',
       required=True,
       default='individuel',
       tracking=True)
    
    gravite = fields.Selection([
        ('faible', 'Faible'),
        ('moyenne', 'Moyenne'),
        ('grave', 'Grave'),
        ('tres_grave', 'Très Grave'),
        ('critique', 'Critique')
    ], string='Gravité',
       required=True,
       default='moyenne',
       tracking=True)
    
    urgence = fields.Selection([
        ('faible', 'Faible'),
        ('normale', 'Normale'),
        ('elevee', 'Élevée'),
        ('urgente', 'Urgente')
    ], string='Urgence',
       default='normale',
       tracking=True)
    
    # Parties impliquées
    demandeur_id = fields.Many2one(
        'syndicat.adherent',
        string='Demandeur',
        required=True,
        tracking=True,
        help="Adhérent demandant la médiation"
    )
    
    autres_adherents_ids = fields.Many2many(
        'syndicat.adherent',
        'mediation_adherent_rel',
        'mediation_id',
        'adherent_id',
        string='Autres Adhérents Impliqués'
    )
    
    employeur_concerne = fields.Char(
        string='Employeur Concerné',
        required=True,
        help="Nom de l'employeur concerné"
    )
    
    representants_employeur = fields.Text(
        string='Représentants Employeur',
        help="Représentants de l'employeur impliqués"
    )
    
    temoins = fields.Text(
        string='Témoins',
        help="Témoins du conflit"
    )
    
    # Dates importantes
    date_creation = fields.Date(
        string='Date de Création',
        default=fields.Date.today,
        required=True,
        tracking=True
    )
    
    date_incident = fields.Date(
        string='Date de l\'Incident',
        tracking=True,
        help="Date de l'incident à l'origine du conflit"
    )
    
    date_saisine = fields.Date(
        string='Date de Saisine',
        tracking=True,
        help="Date de saisine du syndicat"
    )
    
    date_premiere_intervention = fields.Date(
        string='Première Intervention',
        tracking=True,
        help="Date de la première intervention du syndicat"
    )
    
    date_resolution = fields.Date(
        string='Date de Résolution',
        tracking=True,
        help="Date de résolution du conflit"
    )
    
    # Statut et processus
    statut = fields.Selection([
        ('nouveau', 'Nouveau'),
        ('en_cours', 'En Cours'),
        ('mediation', 'En Médiation'),
        ('conciliation', 'En Conciliation'),
        ('arbitrage', 'En Arbitrage'),
        ('juridique', 'Procédure Juridique'),
        ('resolu', 'Résolu'),
        ('abandonne', 'Abandonné'),
        ('echec', 'Échec')
    ], string='Statut',
       default='nouveau',
       required=True,
       tracking=True)
    
    mode_resolution = fields.Selection([
        ('negociation', 'Négociation Directe'),
        ('mediation_interne', 'Médiation Interne'),
        ('mediation_externe', 'Médiation Externe'),
        ('conciliation', 'Conciliation'),
        ('arbitrage', 'Arbitrage'),
        ('juridique', 'Procédure Juridique'),
        ('inspection_travail', 'Inspection du Travail'),
        ('autre', 'Autre')
    ], string='Mode de Résolution',
       tracking=True)
    
    # Médiateur
    mediateur_interne_id = fields.Many2one(
        'syndicat.adherent',
        string='Médiateur Interne',
        help="Médiateur interne du syndicat"
    )
    
    mediateur_externe = fields.Char(
        string='Médiateur Externe',
        help="Nom du médiateur externe"
    )
    
    organisme_mediation = fields.Char(
        string='Organisme de Médiation',
        help="Organisme de médiation externe"
    )
    
    # Contenu du conflit
    faits_reproche = fields.Html(
        string='Faits Reprochés',
        help="Description des faits reprochés"
    )
    
    position_adherent = fields.Html(
        string='Position de l\'Adhérent',
        help="Position et arguments de l'adhérent"
    )
    
    position_employeur = fields.Html(
        string='Position de l\'Employeur',
        help="Position et arguments de l'employeur"
    )
    
    enjeux = fields.Html(
        string='Enjeux',
        help="Enjeux du conflit"
    )
    
    # Interventions et actions
    interventions_ids = fields.One2many(
        'syndicat.mediation.intervention',
        'mediation_id',
        string='Interventions'
    )
    
    nb_interventions = fields.Integer(
        string='Nombre d\'Interventions',
        compute='_compute_nb_interventions',
        store=True
    )
    
    # Documents et preuves
    documents_support = fields.Text(
        string='Documents de Support',
        help="Documents à l'appui du dossier"
    )
    
    preuves = fields.Text(
        string='Preuves',
        help="Preuves disponibles"
    )
    
    # Résolution
    solution_proposee = fields.Html(
        string='Solution Proposée',
        help="Solution proposée par le syndicat"
    )
    
    accord_obtenu = fields.Html(
        string='Accord Obtenu',
        help="Accord obtenu entre les parties"
    )
    
    mesures_correctives = fields.Html(
        string='Mesures Correctives',
        help="Mesures correctives mises en place"
    )
    
    indemnisation = fields.Monetary(
        string='Indemnisation',
        currency_field='currency_id',
        help="Montant de l'indemnisation obtenue"
    )
    
    currency_id = fields.Many2one(
        'res.currency',
        string='Devise',
        default=lambda self: self.env.company.currency_id
    )
    
    # Évaluation
    satisfaction_adherent = fields.Selection([
        ('1', 'Très Insatisfait'),
        ('2', 'Insatisfait'),
        ('3', 'Neutre'),
        ('4', 'Satisfait'),
        ('5', 'Très Satisfait')
    ], string='Satisfaction Adhérent',
       help="Niveau de satisfaction de l'adhérent")
    
    efficacite_intervention = fields.Selection([
        ('faible', 'Faible'),
        ('moyenne', 'Moyenne'),
        ('bonne', 'Bonne'),
        ('excellente', 'Excellente')
    ], string='Efficacité de l\'Intervention',
       help="Évaluation de l'efficacité de l'intervention")
    
    # Suivi temporel
    delai_premiere_intervention = fields.Integer(
        string='Délai Première Intervention (jours)',
        compute='_compute_delais',
        store=True,
        help="Délai pour la première intervention en jours"
    )
    
    delai_resolution = fields.Integer(
        string='Délai de Résolution (jours)',
        compute='_compute_delais',
        store=True,
        help="Délai total de résolution en jours"
    )
    
    # Suivi post-résolution
    suivi_requis = fields.Boolean(
        string='Suivi Requis',
        default=False,
        help="Suivi post-résolution requis"
    )
    
    date_suivi = fields.Date(
        string='Date de Suivi',
        help="Date du suivi post-résolution"
    )
    
    respect_accord = fields.Boolean(
        string='Respect de l\'Accord',
        help="L'accord est-il respecté ?"
    )
    
    # Prévention
    mesures_prevention = fields.Html(
        string='Mesures de Prévention',
        help="Mesures de prévention recommandées"
    )
    
    formation_recommandee = fields.Boolean(
        string='Formation Recommandée',
        default=False,
        help="Formation recommandée pour éviter la récidive"
    )
    
    # Métadonnées
    active = fields.Boolean(
        string='Actif',
        default=True
    )
    
    notes_internes = fields.Text(
        string='Notes Internes'
    )
    
    confidentialite = fields.Selection([
        ('normale', 'Normale'),
        ('confidentiel', 'Confidentiel'),
        ('secret', 'Secret')
    ], string='Niveau de Confidentialité',
       default='normale')

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('reference', _('Nouveau')) == _('Nouveau'):
                vals['reference'] = self.env['ir.sequence'].next_by_code('syndicat.mediation') or _('Nouveau')
        return super(SyndicatMediation, self).create(vals_list)

    @api.depends('interventions_ids')
    def _compute_nb_interventions(self):
        for record in self:
            record.nb_interventions = len(record.interventions_ids)

    @api.depends('date_creation', 'date_premiere_intervention', 'date_resolution')
    def _compute_delais(self):
        for record in self:
            if record.date_creation and record.date_premiere_intervention:
                delta = record.date_premiere_intervention - record.date_creation
                record.delai_premiere_intervention = delta.days
            else:
                record.delai_premiere_intervention = 0
                
            if record.date_creation and record.date_resolution:
                delta = record.date_resolution - record.date_creation
                record.delai_resolution = delta.days
            else:
                record.delai_resolution = 0

    @api.constrains('date_incident', 'date_creation')
    def _check_dates_coherence(self):
        for record in self:
            if record.date_incident and record.date_creation:
                if record.date_creation < record.date_incident:
                    raise ValidationError(_("La date de création ne peut pas être antérieure à la date de l'incident."))

    def action_commencer_mediation(self):
        """Commence la médiation"""
        self.ensure_one()
        if self.statut == 'nouveau':
            self.write({
                'statut': 'mediation',
                'date_premiere_intervention': fields.Date.today()
            })
            self.message_post(body=_("Médiation commencée."))
        return True

    def action_resoudre(self):
        """Marque le conflit comme résolu"""
        self.ensure_one()
        if self.statut in ['en_cours', 'mediation', 'conciliation', 'arbitrage']:
            self.write({
                'statut': 'resolu',
                'date_resolution': fields.Date.today()
            })
            self.message_post(body=_("Conflit résolu."))
        return True

    def action_abandonner(self):
        """Abandonne la médiation"""
        self.ensure_one()
        if self.statut in ['nouveau', 'en_cours', 'mediation']:
            self.statut = 'abandonne'
            self.message_post(body=_("Médiation abandonnée."))
        return True

    def action_echec(self):
        """Marque la médiation comme un échec"""
        self.ensure_one()
        if self.statut in ['mediation', 'conciliation', 'arbitrage']:
            self.statut = 'echec'
            self.message_post(body=_("Échec de la médiation."))
        return True

    def action_procedure_juridique(self):
        """Lance une procédure juridique"""
        self.ensure_one()
        if self.statut in ['echec', 'en_cours']:
            self.statut = 'juridique'
            self.message_post(body=_("Procédure juridique lancée."))
        return True

    # Actions pour les boutons stat (vue)
    def action_view_interventions(self):
        """Ouvre la liste des interventions de la médiation"""
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': _('Interventions'),
            'res_model': 'syndicat.mediation.intervention',
            'view_mode': 'tree,form',
            'domain': [('mediation_id', '=', self.id)],
            'context': {'default_mediation_id': self.id},
            'target': 'current',
        }

    def action_view_adherents(self):
        """Ouvre les adhérents impliqués (autres adhérents)"""
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': _('Adhérents Impliqués'),
            'res_model': 'syndicat.adherent',
            'view_mode': 'tree,form',
            'domain': [('id', 'in', self.autres_adherents_ids.ids)],
            'target': 'current',
        }

    def action_view_delais(self):
        """Ouvre la fiche pour consulter les délais"""
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': _('Détails des Délais'),
            'res_model': 'syndicat.mediation',
            'res_id': self.id,
            'view_mode': 'form',
            'target': 'current',
        }

    def action_ajouter_intervention(self):
        """Ajoute une nouvelle intervention"""
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': 'Nouvelle Intervention',
            'res_model': 'syndicat.mediation.intervention',
            'view_mode': 'form',
            'target': 'new',
            'context': {'default_mediation_id': self.id}
        }

    @api.model
    def get_conflits_en_cours(self):
        """Retourne les conflits en cours"""
        return self.search([
            ('statut', 'in', ['nouveau', 'en_cours', 'mediation', 'conciliation', 'arbitrage'])
        ])

    @api.model
    def get_conflits_urgents(self):
        """Retourne les conflits urgents"""
        return self.search([
            ('urgence', 'in', ['elevee', 'urgente']),
            ('statut', 'in', ['nouveau', 'en_cours', 'mediation'])
        ])

    @api.model
    def get_statistiques_mediations(self):
        """Retourne les statistiques des médiations"""
        total = self.search_count([])
        en_cours = self.search_count([('statut', 'in', ['nouveau', 'en_cours', 'mediation', 'conciliation'])])
        resolus = self.search_count([('statut', '=', 'resolu')])
        echecs = self.search_count([('statut', '=', 'echec')])
        
        return {
            'total': total,
            'en_cours': en_cours,
            'resolus': resolus,
            'echecs': echecs,
            'taux_reussite': (resolus / total * 100) if total > 0 else 0
        }

    @api.model
    def get_conflits_par_type(self):
        """Retourne la répartition des conflits par type"""
        result = []
        for type_conflit in dict(self._fields['type_conflit'].selection):
            count = self.search_count([('type_conflit', '=', type_conflit)])
            if count > 0:
                result.append({
                    'type': type_conflit,
                    'label': dict(self._fields['type_conflit'].selection)[type_conflit],
                    'count': count
                })
        return result

    def name_get(self):
        result = []
        for record in self:
            name = f"[{record.reference}] {record.name}"
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
                ('employeur_concerne', operator, name)
            ] + args
        return self._search(args, limit=limit, access_rights_uid=name_get_uid)


class SyndicatMediationIntervention(models.Model):
    _name = 'syndicat.mediation.intervention'
    _description = 'Intervention de Médiation'
    _order = 'date_intervention desc'

    name = fields.Char(
        string='Titre de l\'Intervention',
        required=True,
        help="Titre de l'intervention"
    )
    
    mediation_id = fields.Many2one(
        'syndicat.mediation',
        string='Médiation',
        required=True,
        ondelete='cascade'
    )
    
    date_intervention = fields.Datetime(
        string='Date d\'Intervention',
        required=True,
        default=fields.Datetime.now
    )
    
    type_intervention = fields.Selection([
        ('entretien', 'Entretien'),
        ('reunion', 'Réunion'),
        ('negociation', 'Négociation'),
        ('mediation', 'Séance de Médiation'),
        ('enquete', 'Enquête'),
        ('courrier', 'Courrier'),
        ('telephone', 'Appel Téléphonique'),
        ('visite', 'Visite sur Site'),
        ('autre', 'Autre')
    ], string='Type d\'Intervention',
       required=True,
       default='entretien')
    
    lieu = fields.Char(
        string='Lieu',
        help="Lieu de l'intervention"
    )
    
    duree = fields.Float(
        string='Durée (heures)',
        help="Durée de l'intervention en heures"
    )
    
    # Participants
    intervenant_id = fields.Many2one(
        'syndicat.adherent',
        string='Intervenant',
        required=True,
        help="Représentant syndical intervenant"
    )
    
    participants_syndicat_ids = fields.Many2many(
        'syndicat.adherent',
        'intervention_participant_rel',
        'intervention_id',
        'adherent_id',
        string='Autres Participants Syndicat'
    )
    
    participants_externes = fields.Text(
        string='Participants Externes',
        help="Participants externes (employeur, médiateur, etc.)"
    )
    
    # Contenu
    objectif = fields.Html(
        string='Objectif',
        required=True,
        help="Objectif de l'intervention"
    )
    
    deroulement = fields.Html(
        string='Déroulement',
        help="Description du déroulement de l'intervention"
    )
    
    points_abordes = fields.Html(
        string='Points Abordés',
        help="Points abordés durant l'intervention"
    )
    
    positions_exprimees = fields.Html(
        string='Positions Exprimées',
        help="Positions exprimées par les différentes parties"
    )
    
    # Résultats
    resultats_obtenus = fields.Html(
        string='Résultats Obtenus',
        help="Résultats obtenus lors de l'intervention"
    )
    
    accords_partiels = fields.Html(
        string='Accords Partiels',
        help="Accords partiels obtenus"
    )
    
    points_blocage = fields.Html(
        string='Points de Blocage',
        help="Points de blocage identifiés"
    )
    
    prochaines_etapes = fields.Html(
        string='Prochaines Étapes',
        help="Prochaines étapes convenues"
    )
    
    # Évaluation
    efficacite = fields.Selection([
        ('faible', 'Faible'),
        ('moyenne', 'Moyenne'),
        ('bonne', 'Bonne'),
        ('excellente', 'Excellente')
    ], string='Efficacité',
       help="Évaluation de l'efficacité de l'intervention")
    
    progres_realise = fields.Selection([
        ('aucun', 'Aucun Progrès'),
        ('faible', 'Faible Progrès'),
        ('moyen', 'Progrès Moyen'),
        ('bon', 'Bon Progrès'),
        ('excellent', 'Excellent Progrès')
    ], string='Progrès Réalisé')
    
    # Suivi
    suivi_requis = fields.Boolean(
        string='Suivi Requis',
        default=False,
        help="Intervention de suivi requise"
    )
    
    date_suivi_prevue = fields.Date(
        string='Date de Suivi Prévue',
        help="Date prévue pour le suivi"
    )
    
    notes = fields.Text(
        string='Notes',
        help="Notes diverses sur l'intervention"
    )

    def name_get(self):
        result = []
        for record in self:
            name = f"{record.name} - {record.date_intervention.strftime('%d/%m/%Y')}"
            result.append((record.id, name))
        return result