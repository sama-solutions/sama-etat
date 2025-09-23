# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
from datetime import datetime, timedelta


class SyndicatAssemblee(models.Model):
    _name = 'syndicat.assemblee'
    _description = 'Assemblée Syndicale'
    _order = 'date_debut desc'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(
        string='Titre de l\'Assemblée',
        required=True,
        tracking=True,
        help="Titre de l'assemblée syndicale"
    )
    
    reference = fields.Char(
        string='Référence',
        required=True,
        copy=False,
        default=lambda self: _('Nouveau'),
        tracking=True,
        help="Référence unique de l'assemblée"
    )
    
    type_assemblee = fields.Selection([
        ('generale_ordinaire', 'Assemblée Générale Ordinaire'),
        ('generale_extraordinaire', 'Assemblée Générale Extraordinaire'),
        ('bureau_executif', 'Réunion Bureau Exécutif'),
        ('commission', 'Réunion de Commission'),
        ('section', 'Réunion de Section'),
        ('formation', 'Assemblée de Formation'),
        ('information', 'Réunion d\'Information'),
        ('negociation', 'Réunion de Négociation'),
        ('autre', 'Autre')
    ], string='Type d\'Assemblée',
       required=True,
       default='generale_ordinaire',
       tracking=True,
       help="Type d'assemblée syndicale")
    
    statut = fields.Selection([
        ('planifiee', 'Planifiée'),
        ('confirmee', 'Confirmée'),
        ('en_cours', 'En Cours'),
        ('suspendue', 'Suspendue'),
        ('terminee', 'Terminée'),
        ('reportee', 'Reportée'),
        ('annulee', 'Annulée')
    ], string='Statut',
       default='planifiee',
       required=True,
       tracking=True,
       help="Statut de l'assemblée")
    
    # Dates et horaires
    date_debut = fields.Datetime(
        string='Date et Heure de Début',
        required=True,
        tracking=True,
        help="Date et heure de début de l'assemblée"
    )
    
    date_fin = fields.Datetime(
        string='Date et Heure de Fin',
        tracking=True,
        help="Date et heure de fin prévue de l'assemblée"
    )
    
    duree_prevue = fields.Float(
        string='Durée Prévue (heures)',
        compute='_compute_duree_prevue',
        store=True,
        help="Durée prévue de l'assemblée en heures"
    )
    
    duree_reelle = fields.Float(
        string='Durée Réelle (heures)',
        compute='_compute_duree_reelle',
        store=True,
        help="Durée réelle de l'assemblée en heures"
    )
    
    # Lieu et organisation
    lieu = fields.Char(
        string='Lieu',
        required=True,
        help="Lieu de l'assemblée"
    )
    
    adresse_complete = fields.Text(
        string='Adresse Complète',
        help="Adresse complète du lieu de l'assemblée"
    )
    
    salle = fields.Char(
        string='Salle',
        help="Salle spécifique de l'assemblée"
    )
    
    capacite_max = fields.Integer(
        string='Capacité Maximale',
        help="Nombre maximum de participants"
    )
    
    # Responsables
    president_assemblee_id = fields.Many2one(
        'syndicat.adherent',
        string='Président d\'Assemblée',
        domain=[('responsabilite_syndicale', 'in', ['president', 'vice_president', 'secretaire'])],
        tracking=True,
        help="Responsable présidant l'assemblée"
    )
    
    secretaire_assemblee_id = fields.Many2one(
        'syndicat.adherent',
        string='Secrétaire d\'Assemblée',
        domain=[('responsabilite_syndicale', 'in', ['secretaire', 'adherent'])],
        tracking=True,
        help="Secrétaire de l'assemblée"
    )
    
    # Contenu de l'assemblée
    ordre_du_jour = fields.Html(
        string='Ordre du Jour',
        required=True,
        help="Ordre du jour détaillé de l'assemblée"
    )
    
    objectifs = fields.Html(
        string='Objectifs',
        help="Objectifs de l'assemblée"
    )
    
    resume_assemblee = fields.Html(
        string='Résumé de l\'Assemblée',
        help="Résumé des points abordés et décisions prises"
    )
    
    proces_verbal = fields.Html(
        string='Procès-Verbal',
        help="Procès-verbal détaillé de l'assemblée"
    )
    
    decisions_prises = fields.Html(
        string='Décisions Prises',
        help="Liste des décisions prises durant l'assemblée"
    )
    
    resolutions_adoptees = fields.Html(
        string='Résolutions Adoptées',
        help="Résolutions adoptées lors de l'assemblée"
    )
    
    # Relations avec autres modèles
    revendication_ids = fields.Many2many(
        'syndicat.revendication',
        'assemblee_revendication_rel',
        'assemblee_id',
        'revendication_id',
        string='Revendications à l\'Ordre du Jour',
        help="Revendications à examiner"
    )
    
    action_ids = fields.Many2many(
        'syndicat.action',
        'assemblee_action_rel',
        'assemblee_id',
        'action_id',
        string='Actions Planifiées',
        help="Actions planifiées lors de l'assemblée"
    )
    
    # Participants
    adherent_invites_ids = fields.Many2many(
        'syndicat.adherent',
        'assemblee_invite_rel',
        'assemblee_id',
        'adherent_id',
        string='Adhérents Invités',
        help="Adhérents invités à l'assemblée"
    )
    
    adherent_presents_ids = fields.Many2many(
        'syndicat.adherent',
        'assemblee_presence_rel',
        'assemblee_id',
        'adherent_id',
        string='Adhérents Présents',
        help="Adhérents présents à l'assemblée"
    )
    
    adherent_absents_ids = fields.Many2many(
        'syndicat.adherent',
        'assemblee_absence_rel',
        'assemblee_id',
        'adherent_id',
        string='Adhérents Absents',
        help="Adhérents absents à l'assemblée"
    )
    
    adherent_excuses_ids = fields.Many2many(
        'syndicat.adherent',
        'assemblee_excuse_rel',
        'assemblee_id',
        'adherent_id',
        string='Adhérents Excusés',
        help="Adhérents excusés pour l'assemblée"
    )
    
    # Invités externes
    invites_externes = fields.Text(
        string='Invités Externes',
        help="Liste des invités externes (non-adhérents)"
    )
    
    # Champs calculés
    nb_invites = fields.Integer(
        string='Nombre d\'Invités',
        compute='_compute_nb_participants',
        store=True,
        help="Nombre d'adhérents invités"
    )
    
    nb_presents = fields.Integer(
        string='Nombre de Présents',
        compute='_compute_nb_participants',
        store=True,
        help="Nombre d'adhérents présents"
    )
    
    nb_absents = fields.Integer(
        string='Nombre d\'Absents',
        compute='_compute_nb_participants',
        store=True,
        help="Nombre d'adhérents absents"
    )
    
    taux_presence = fields.Float(
        string='Taux de Présence (%)',
        compute='_compute_taux_presence',
        store=True,
        help="Taux de présence des adhérents"
    )
    
    quorum_atteint = fields.Boolean(
        string='Quorum Atteint',
        compute='_compute_quorum_atteint',
        store=True,
        help="Indique si le quorum est atteint"
    )
    
    quorum_requis = fields.Integer(
        string='Quorum Requis',
        compute='_compute_quorum_requis',
        store=True,
        help="Nombre minimum de participants requis"
    )
    
    # Votes et décisions
    votes_ids = fields.One2many(
        'syndicat.vote',
        'assemblee_id',
        string='Votes'
    )
    
    nb_votes = fields.Integer(
        string='Nombre de Votes',
        compute='_compute_nb_votes',
        store=True
    )
    
    # Communication
    convocation_envoyee = fields.Boolean(
        string='Convocation Envoyée',
        default=False,
        help="Convocation envoyée aux adhérents"
    )
    
    date_envoi_convocation = fields.Datetime(
        string='Date Envoi Convocation',
        tracking=True
    )
    
    rappel_envoye = fields.Boolean(
        string='Rappel Envoyé',
        default=False,
        help="Rappel d'assemblée envoyé"
    )
    
    date_envoi_rappel = fields.Datetime(
        string='Date Envoi Rappel',
        tracking=True
    )
    
    # Documents
    documents_preparatoires = fields.Text(
        string='Documents Préparatoires',
        help="Liste des documents à préparer"
    )
    
    # Diffusion
    diffusion_publique = fields.Boolean(
        string='Diffusion Publique',
        default=False,
        help="Assemblée diffusée publiquement"
    )
    
    lien_streaming = fields.Char(
        string='Lien de Diffusion',
        help="Lien de diffusion en direct"
    )
    
    enregistrement_disponible = fields.Boolean(
        string='Enregistrement Disponible',
        default=False,
        help="Enregistrement disponible"
    )
    
    lien_enregistrement = fields.Char(
        string='Lien Enregistrement',
        help="Lien vers l'enregistrement"
    )
    
    # Métadonnées
    active = fields.Boolean(
        string='Actif',
        default=True,
        help="Décocher pour archiver l'assemblée"
    )
    
    notes_internes = fields.Text(
        string='Notes Internes',
        help="Notes internes pour l'organisation"
    )

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('reference', _('Nouveau')) == _('Nouveau'):
                vals['reference'] = self.env['ir.sequence'].next_by_code('syndicat.assemblee') or _('Nouveau')
        return super(SyndicatAssemblee, self).create(vals_list)

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

    @api.depends('adherent_invites_ids', 'adherent_presents_ids', 'adherent_absents_ids')
    def _compute_nb_participants(self):
        for record in self:
            record.nb_invites = len(record.adherent_invites_ids)
            record.nb_presents = len(record.adherent_presents_ids)
            record.nb_absents = len(record.adherent_absents_ids)

    @api.depends('nb_presents', 'nb_invites')
    def _compute_taux_presence(self):
        for record in self:
            if record.nb_invites > 0:
                record.taux_presence = (record.nb_presents / record.nb_invites) * 100
            else:
                record.taux_presence = 0.0

    @api.depends('type_assemblee', 'nb_invites')
    def _compute_quorum_requis(self):
        for record in self:
            # Définir le quorum selon le type d'assemblée
            if record.type_assemblee in ['generale_ordinaire', 'generale_extraordinaire']:
                # AG : 50% + 1 des adhérents actifs
                total_adherents = self.env['syndicat.adherent'].search_count([('statut_adhesion', '=', 'actif')])
                record.quorum_requis = (total_adherents // 2) + 1
            elif record.type_assemblee == 'bureau_executif':
                # Bureau : 50% + 1 des membres du bureau
                membres_bureau = self.env['syndicat.adherent'].search_count([
                    ('statut_adhesion', '=', 'actif'),
                    ('responsabilite_syndicale', 'in', ['president', 'vice_president', 'secretaire', 'tresorier'])
                ])
                record.quorum_requis = (membres_bureau // 2) + 1
            else:
                # Autres : 1/3 des invités
                record.quorum_requis = max(1, record.nb_invites // 3)

    @api.depends('nb_presents', 'quorum_requis')
    def _compute_quorum_atteint(self):
        for record in self:
            record.quorum_atteint = record.nb_presents >= record.quorum_requis

    @api.depends('votes_ids')
    def _compute_nb_votes(self):
        for record in self:
            record.nb_votes = len(record.votes_ids)

    @api.constrains('date_debut', 'date_fin')
    def _check_dates_coherence(self):
        for record in self:
            if record.date_debut and record.date_fin:
                if record.date_fin <= record.date_debut:
                    raise ValidationError(_("La date de fin doit être postérieure à la date de début."))

    @api.constrains('adherent_presents_ids', 'adherent_absents_ids')
    def _check_presence_coherence(self):
        for record in self:
            presents = set(record.adherent_presents_ids.ids)
            absents = set(record.adherent_absents_ids.ids)
            if presents & absents:
                raise ValidationError(_("Un adhérent ne peut pas être à la fois présent et absent."))

    @api.onchange('type_assemblee')
    def _onchange_type_assemblee(self):
        if self.type_assemblee in ['generale_ordinaire', 'generale_extraordinaire']:
            # Inviter automatiquement tous les adhérents actifs pour les AG
            adherents_actifs = self.env['syndicat.adherent'].search([('statut_adhesion', '=', 'actif')])
            self.adherent_invites_ids = [(6, 0, adherents_actifs.ids)]
        elif self.type_assemblee == 'bureau_executif':
            # Inviter les membres du bureau
            membres_bureau = self.env['syndicat.adherent'].search([
                ('statut_adhesion', '=', 'actif'),
                ('responsabilite_syndicale', 'in', ['president', 'vice_president', 'secretaire', 'tresorier'])
            ])
            self.adherent_invites_ids = [(6, 0, membres_bureau.ids)]

    def action_confirmer(self):
        """Confirme l'assemblée"""
        self.ensure_one()
        if self.statut == 'planifiee':
            self.statut = 'confirmee'
            self.message_post(body=_("Assemblée confirmée."))
            self._send_convocation()
        return True

    def action_commencer(self):
        """Démarre l'assemblée"""
        self.ensure_one()
        if self.statut in ['planifiee', 'confirmee']:
            self.statut = 'en_cours'
            if not self.date_debut:
                self.date_debut = fields.Datetime.now()
            self.message_post(body=_("Assemblée démarrée."))
        return True

    def action_suspendre(self):
        """Suspend l'assemblée"""
        self.ensure_one()
        if self.statut == 'en_cours':
            self.statut = 'suspendue'
            self.message_post(body=_("Assemblée suspendue."))
        return True

    def action_reprendre(self):
        """Reprend l'assemblée"""
        self.ensure_one()
        if self.statut == 'suspendue':
            self.statut = 'en_cours'
            self.message_post(body=_("Assemblée reprise."))
        return True

    def action_terminer(self):
        """Termine l'assemblée"""
        self.ensure_one()
        if self.statut in ['en_cours', 'suspendue']:
            self.statut = 'terminee'
            if not self.date_fin:
                self.date_fin = fields.Datetime.now()
            self.message_post(body=_("Assemblée terminée."))
        return True

    def action_reporter(self):
        """Reporte l'assemblée"""
        self.ensure_one()
        if self.statut in ['planifiee', 'confirmee']:
            self.statut = 'reportee'
            self.message_post(body=_("Assemblée reportée."))
        return True

    def action_annuler(self):
        """Annule l'assemblée"""
        self.ensure_one()
        if self.statut in ['planifiee', 'confirmee']:
            self.statut = 'annulee'
            self.message_post(body=_("Assemblée annulée."))
        return True

    def _send_convocation(self):
        """Envoie les convocations aux adhérents"""
        self.ensure_one()
        if not self.convocation_envoyee:
            # Logique d'envoi de convocations
            for adherent in self.adherent_invites_ids:
                if adherent.email:
                    # Envoyer email de convocation
                    pass
            self.write({
                'convocation_envoyee': True,
                'date_envoi_convocation': fields.Datetime.now()
            })
            self.message_post(body=_("Convocations envoyées aux adhérents."))

    def action_send_reminder(self):
        """Envoie un rappel d'assemblée"""
        self.ensure_one()
        if not self.rappel_envoye:
            # Logique d'envoi de rappels
            self.write({
                'rappel_envoye': True,
                'date_envoi_rappel': fields.Datetime.now()
            })
            self.message_post(body=_("Rappels envoyés aux adhérents."))

    def action_marquer_presence(self, adherent_id):
        """Marque la présence d'un adhérent"""
        self.ensure_one()
        adherent = self.env['syndicat.adherent'].browse(adherent_id)
        if adherent in self.adherent_invites_ids:
            self.adherent_presents_ids = [(4, adherent_id)]
            self.adherent_absents_ids = [(3, adherent_id)]
            self.message_post(body=_("Présence marquée pour %s.") % adherent.name)

    def action_marquer_absence(self, adherent_id):
        """Marque l'absence d'un adhérent"""
        self.ensure_one()
        adherent = self.env['syndicat.adherent'].browse(adherent_id)
        if adherent in self.adherent_invites_ids:
            self.adherent_absents_ids = [(4, adherent_id)]
            self.adherent_presents_ids = [(3, adherent_id)]
            self.message_post(body=_("Absence marquée pour %s.") % adherent.name)

    @api.model
    def get_assemblees_du_jour(self):
        """Retourne les assemblées du jour"""
        today = fields.Date.today()
        return self.search([
            ('date_debut', '>=', today),
            ('date_debut', '<', today + timedelta(days=1))
        ])

    @api.model
    def get_prochaines_assemblees(self, limit=5):
        """Retourne les prochaines assemblées"""
        return self.search([
            ('date_debut', '>', fields.Datetime.now()),
            ('statut', 'in', ['planifiee', 'confirmee'])
        ], limit=limit, order='date_debut asc')

    def name_get(self):
        result = []
        for record in self:
            name = f"[{record.reference}] {record.name}"
            if record.date_debut:
                name += f" - {record.date_debut.strftime('%d/%m/%Y %H:%M')}"
            result.append((record.id, name))
        return result

    # Actions de vue (pour les boutons stat de la fiche)
    def action_view_votes(self):
        """Ouvre la liste des votes de l'assemblée"""
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': _('Votes'),
            'res_model': 'syndicat.vote',
            'view_mode': 'tree,form',
            'domain': [('assemblee_id', '=', self.id)],
            'context': {'default_assemblee_id': self.id},
            'target': 'current',
        }

    def action_view_participants(self):
        """Ouvre la liste des adhérents présents à l'assemblée"""
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': _('Participants'),
            'res_model': 'syndicat.adherent',
            'view_mode': 'tree,form',
            'domain': [('id', 'in', self.adherent_presents_ids.ids)],
            'target': 'current',
        }

    @api.model
    def _name_search(self, name='', args=None, operator='ilike', limit=100, name_get_uid=None):
        args = args or []
        if name:
            args = [
                '|', '|',
                ('name', operator, name),
                ('reference', operator, name),
                ('lieu', operator, name)
            ] + args
        return self._search(args, limit=limit, access_rights_uid=name_get_uid)


class SyndicatVote(models.Model):
    _name = 'syndicat.vote'
    _description = 'Vote en Assemblée'
    _order = 'date_vote desc'

    name = fields.Char(
        string='Objet du Vote',
        required=True,
        help="Objet ou question soumise au vote"
    )
    
    assemblee_id = fields.Many2one(
        'syndicat.assemblee',
        string='Assemblée',
        required=True,
        ondelete='cascade'
    )
    
    description = fields.Html(
        string='Description',
        help="Description détaillée de la question"
    )
    
    type_vote = fields.Selection([
        ('simple', 'Majorité Simple'),
        ('absolue', 'Majorité Absolue'),
        ('qualifiee', 'Majorité Qualifiée (2/3)'),
        ('unanimite', 'Unanimité')
    ], string='Type de Vote',
       default='simple',
       required=True)
    
    date_vote = fields.Datetime(
        string='Date du Vote',
        default=fields.Datetime.now,
        required=True
    )
    
    # Résultats
    nb_votants = fields.Integer(
        string='Nombre de Votants',
        compute='_compute_resultats',
        store=True
    )
    
    nb_pour = fields.Integer(
        string='Votes Pour',
        default=0
    )
    
    nb_contre = fields.Integer(
        string='Votes Contre',
        default=0
    )
    
    nb_abstentions = fields.Integer(
        string='Abstentions',
        default=0
    )
    
    nb_blancs = fields.Integer(
        string='Votes Blancs',
        default=0
    )
    
    resultat = fields.Selection([
        ('adopte', 'Adopté'),
        ('rejete', 'Rejeté'),
        ('reporte', 'Reporté')
    ], string='Résultat',
       compute='_compute_resultat',
       store=True)
    
    pourcentage_pour = fields.Float(
        string='% Pour',
        compute='_compute_pourcentages',
        store=True
    )
    
    pourcentage_contre = fields.Float(
        string='% Contre',
        compute='_compute_pourcentages',
        store=True
    )
    
    # Détails des votes
    vote_detail_ids = fields.One2many(
        'syndicat.vote.detail',
        'vote_id',
        string='Détail des Votes'
    )
    
    vote_secret = fields.Boolean(
        string='Vote Secret',
        default=False,
        help="Vote à bulletin secret"
    )
    
    notes = fields.Text(
        string='Notes',
        help="Notes sur le vote"
    )

    @api.depends('nb_pour', 'nb_contre', 'nb_abstentions', 'nb_blancs')
    def _compute_resultats(self):
        for record in self:
            record.nb_votants = record.nb_pour + record.nb_contre + record.nb_abstentions + record.nb_blancs

    @api.depends('nb_pour', 'nb_contre', 'nb_votants', 'type_vote')
    def _compute_resultat(self):
        for record in self:
            if record.nb_votants == 0:
                record.resultat = 'reporte'
                continue
                
            if record.type_vote == 'simple':
                # Majorité simple : plus de pour que de contre
                record.resultat = 'adopte' if record.nb_pour > record.nb_contre else 'rejete'
            elif record.type_vote == 'absolue':
                # Majorité absolue : plus de 50% des votants
                record.resultat = 'adopte' if record.nb_pour > (record.nb_votants / 2) else 'rejete'
            elif record.type_vote == 'qualifiee':
                # Majorité qualifiée : 2/3 des votants
                record.resultat = 'adopte' if record.nb_pour >= (record.nb_votants * 2 / 3) else 'rejete'
            elif record.type_vote == 'unanimite':
                # Unanimité : tous pour (abstentions autorisées)
                record.resultat = 'adopte' if record.nb_contre == 0 and record.nb_pour > 0 else 'rejete'

    @api.depends('nb_pour', 'nb_contre', 'nb_votants')
    def _compute_pourcentages(self):
        for record in self:
            if record.nb_votants > 0:
                record.pourcentage_pour = (record.nb_pour / record.nb_votants) * 100
                record.pourcentage_contre = (record.nb_contre / record.nb_votants) * 100
            else:
                record.pourcentage_pour = 0.0
                record.pourcentage_contre = 0.0


class SyndicatVoteDetail(models.Model):
    _name = 'syndicat.vote.detail'
    _description = 'Détail Vote Adhérent'

    vote_id = fields.Many2one(
        'syndicat.vote',
        string='Vote',
        required=True,
        ondelete='cascade'
    )
    
    adherent_id = fields.Many2one(
        'syndicat.adherent',
        string='Adhérent',
        required=True
    )
    
    choix_vote = fields.Selection([
        ('pour', 'Pour'),
        ('contre', 'Contre'),
        ('abstention', 'Abstention'),
        ('blanc', 'Blanc')
    ], string='Choix',
       required=True)
    
    date_vote = fields.Datetime(
        string='Date du Vote',
        default=fields.Datetime.now
    )
    
    notes = fields.Text(
        string='Notes',
        help="Notes sur ce vote spécifique"
    )