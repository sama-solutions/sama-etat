# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class SyndicatConvention(models.Model):
    _name = 'syndicat.convention'
    _description = 'Convention Collective'
    _order = 'date_signature desc'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(
        string='Titre de la Convention',
        required=True,
        tracking=True,
        help="Titre de la convention collective"
    )
    
    reference = fields.Char(
        string='Référence',
        required=True,
        copy=False,
        default=lambda self: _('Nouveau'),
        tracking=True,
        help="Référence unique de la convention"
    )
    
    description = fields.Html(
        string='Description',
        required=True,
        help="Description de la convention"
    )
    
    # Classification
    type_convention = fields.Selection([
        ('entreprise', 'Convention d\'Entreprise'),
        ('branche', 'Convention de Branche'),
        ('sectorielle', 'Convention Sectorielle'),
        ('nationale', 'Convention Nationale'),
        ('accord_cadre', 'Accord Cadre'),
        ('protocole', 'Protocole d\'Accord'),
        ('avenant', 'Avenant'),
        ('autre', 'Autre')
    ], string='Type de Convention',
       required=True,
       default='entreprise',
       tracking=True)
    
    secteur_activite = fields.Char(
        string='Secteur d\'Activité',
        help="Secteur d'activité concerné"
    )
    
    # Parties signataires
    employeur_principal = fields.Char(
        string='Employeur Principal',
        required=True,
        help="Nom de l'employeur principal"
    )
    
    employeurs_secondaires = fields.Text(
        string='Autres Employeurs',
        help="Autres employeurs signataires"
    )
    
    syndicats_signataires = fields.Text(
        string='Syndicats Signataires',
        help="Liste des syndicats signataires"
    )
    
    representants_syndicat_ids = fields.Many2many(
        'syndicat.adherent',
        'convention_representant_rel',
        'convention_id',
        'adherent_id',
        string='Représentants du Syndicat',
        help="Représentants du syndicat ayant négocié"
    )
    
    # Dates importantes
    date_negociation_debut = fields.Date(
        string='Début des Négociations',
        tracking=True
    )
    
    date_negociation_fin = fields.Date(
        string='Fin des Négociations',
        tracking=True
    )
    
    date_signature = fields.Date(
        string='Date de Signature',
        required=True,
        tracking=True
    )
    
    date_entree_vigueur = fields.Date(
        string='Date d\'Entrée en Vigueur',
        required=True,
        tracking=True
    )
    
    date_expiration = fields.Date(
        string='Date d\'Expiration',
        tracking=True,
        help="Date d'expiration de la convention"
    )
    
    duree_validite = fields.Integer(
        string='Durée de Validité (mois)',
        compute='_compute_duree_validite',
        store=True,
        help="Durée de validité en mois"
    )
    
    # Statut
    statut = fields.Selection([
        ('negociation', 'En Négociation'),
        ('signee', 'Signée'),
        ('en_vigueur', 'En Vigueur'),
        ('expiree', 'Expirée'),
        ('denoncee', 'Dénoncée'),
        ('suspendue', 'Suspendue'),
        ('annulee', 'Annulée')
    ], string='Statut',
       default='negociation',
       required=True,
       tracking=True)
    
    # Contenu de la convention
    domaines_couverts = fields.Selection([
        ('salaires', 'Salaires et Rémunérations'),
        ('temps_travail', 'Temps de Travail'),
        ('conditions_travail', 'Conditions de Travail'),
        ('formation', 'Formation Professionnelle'),
        ('promotion', 'Promotion et Carrière'),
        ('protection_sociale', 'Protection Sociale'),
        ('hygiene_securite', 'Hygiène et Sécurité'),
        ('conges', 'Congés et Repos'),
        ('discipline', 'Discipline et Sanctions'),
        ('representation', 'Représentation du Personnel'),
        ('mixte', 'Plusieurs Domaines')
    ], string='Domaines Couverts',
       default='mixte',
       required=True)
    
    clauses_principales = fields.Html(
        string='Clauses Principales',
        required=True,
        help="Principales clauses de la convention"
    )
    
    avantages_obtenus = fields.Html(
        string='Avantages Obtenus',
        help="Avantages obtenus pour les salariés"
    )
    
    obligations_syndicat = fields.Html(
        string='Obligations du Syndicat',
        help="Obligations du syndicat"
    )
    
    obligations_employeur = fields.Html(
        string='Obligations de l\'Employeur',
        help="Obligations de l'employeur"
    )
    
    # Champ d'application
    champ_application = fields.Html(
        string='Champ d\'Application',
        required=True,
        help="Champ d'application de la convention"
    )
    
    categories_personnel = fields.Text(
        string='Catégories de Personnel',
        help="Catégories de personnel concernées"
    )
    
    nb_salaries_concernes = fields.Integer(
        string='Nombre de Salariés Concernés',
        help="Nombre de salariés concernés par la convention"
    )
    
    # Révision et dénonciation
    clause_revision = fields.Html(
        string='Clause de Révision',
        help="Modalités de révision de la convention"
    )
    
    clause_denonciation = fields.Html(
        string='Clause de Dénonciation',
        help="Modalités de dénonciation de la convention"
    )
    
    preavis_denonciation = fields.Integer(
        string='Préavis de Dénonciation (mois)',
        default=3,
        help="Préavis requis pour la dénonciation en mois"
    )
    
    # Suivi et application
    commission_suivi = fields.Boolean(
        string='Commission de Suivi',
        default=False,
        help="Commission de suivi mise en place"
    )
    
    membres_commission_ids = fields.Many2many(
        'syndicat.adherent',
        'convention_commission_rel',
        'convention_id',
        'adherent_id',
        string='Membres Commission de Suivi'
    )
    
    reunions_suivi_ids = fields.One2many(
        'syndicat.convention.suivi',
        'convention_id',
        string='Réunions de Suivi'
    )
    
    # Évaluation
    niveau_satisfaction = fields.Selection([
        ('1', 'Très Insatisfaisant'),
        ('2', 'Insatisfaisant'),
        ('3', 'Moyen'),
        ('4', 'Satisfaisant'),
        ('5', 'Très Satisfaisant')
    ], string='Niveau de Satisfaction',
       help="Niveau de satisfaction global")
    
    respect_employeur = fields.Selection([
        ('mauvais', 'Mauvais'),
        ('moyen', 'Moyen'),
        ('bon', 'Bon'),
        ('excellent', 'Excellent')
    ], string='Respect par l\'Employeur',
       help="Niveau de respect de la convention par l'employeur")
    
    # Documents
    document_original = fields.Char(
        string='Document Original',
        help="Référence du document original"
    )
    
    documents_annexes = fields.Text(
        string='Documents Annexes',
        help="Liste des documents annexes"
    )
    
    # Relations
    convention_precedente_id = fields.Many2one(
        'syndicat.convention',
        string='Convention Précédente',
        help="Convention précédente remplacée"
    )
    
    avenants_ids = fields.One2many(
        'syndicat.convention',
        'convention_precedente_id',
        string='Avenants',
        domain=[('type_convention', '=', 'avenant')]
    )
    
    # Métadonnées
    active = fields.Boolean(
        string='Actif',
        default=True
    )
    
    notes_internes = fields.Text(
        string='Notes Internes'
    )

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('reference', _('Nouveau')) == _('Nouveau'):
                vals['reference'] = self.env['ir.sequence'].next_by_code('syndicat.convention') or _('Nouveau')
        return super(SyndicatConvention, self).create(vals_list)

    @api.depends('date_entree_vigueur', 'date_expiration')
    def _compute_duree_validite(self):
        for record in self:
            if record.date_entree_vigueur and record.date_expiration:
                delta = record.date_expiration - record.date_entree_vigueur
                record.duree_validite = int(delta.days / 30.44)  # Approximation en mois
            else:
                record.duree_validite = 0

    @api.constrains('date_entree_vigueur', 'date_expiration')
    def _check_dates_coherence(self):
        for record in self:
            if record.date_entree_vigueur and record.date_expiration:
                if record.date_expiration <= record.date_entree_vigueur:
                    raise ValidationError(_("La date d'expiration doit être postérieure à la date d'entrée en vigueur."))

    @api.constrains('date_signature', 'date_entree_vigueur')
    def _check_signature_vigueur(self):
        for record in self:
            if record.date_signature and record.date_entree_vigueur:
                if record.date_entree_vigueur < record.date_signature:
                    raise ValidationError(_("La date d'entrée en vigueur ne peut pas être antérieure à la signature."))

    def action_signer(self):
        """Marque la convention comme signée"""
        self.ensure_one()
        if self.statut == 'negociation':
            self.statut = 'signee'
            self.message_post(body=_("Convention signée."))
        return True

    def action_mettre_en_vigueur(self):
        """Met la convention en vigueur"""
        self.ensure_one()
        if self.statut == 'signee':
            self.statut = 'en_vigueur'
            self.message_post(body=_("Convention mise en vigueur."))
        return True

    def action_denoncer(self):
        """Dénonce la convention"""
        self.ensure_one()
        if self.statut == 'en_vigueur':
            self.statut = 'denoncee'
            self.message_post(body=_("Convention dénoncée."))
        return True

    def action_suspendre(self):
        """Suspend la convention"""
        self.ensure_one()
        if self.statut == 'en_vigueur':
            self.statut = 'suspendue'
            self.message_post(body=_("Convention suspendue."))
        return True

    def action_reactiver(self):
        """Réactive la convention"""
        self.ensure_one()
        if self.statut == 'suspendue':
            self.statut = 'en_vigueur'
            self.message_post(body=_("Convention réactivée."))
        return True

    def action_creer_avenant(self):
        """Crée un avenant à la convention"""
        self.ensure_one()
        avenant = self.copy({
            'name': f"Avenant à {self.name}",
            'type_convention': 'avenant',
            'convention_precedente_id': self.id,
            'statut': 'negociation',
            'date_signature': False,
            'date_entree_vigueur': False,
        })
        return {
            'type': 'ir.actions.act_window',
            'name': 'Nouvel Avenant',
            'res_model': 'syndicat.convention',
            'res_id': avenant.id,
            'view_mode': 'form',
            'target': 'current',
        }

    def action_view_representants(self):
        """Ouvre la vue des représentants du syndicat pour cette convention."""
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': _('Représentants du Syndicat'),
            'res_model': 'syndicat.adherent',
            'view_mode': 'tree,form',
            'domain': [('id', 'in', self.representants_syndicat_ids.ids)],
            'context': {'default_convention_id': self.id},
            'target': 'current',
        }

    def action_view_suivi(self):
        """Ouvre la vue des réunions de suivi de cette convention."""
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': _('Réunions de Suivi'),
            'res_model': 'syndicat.convention.suivi',
            'view_mode': 'tree,form',
            'domain': [('convention_id', '=', self.id)],
            'context': {'default_convention_id': self.id},
            'target': 'current',
        }

    def action_view_avenants(self):
        """Ouvre la vue des avenants de cette convention."""
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': _('Avenants'),
            'res_model': 'syndicat.convention',
            'view_mode': 'tree,form',
            'domain': [('convention_precedente_id', '=', self.id)],
            'context': {'default_convention_precedente_id': self.id, 'default_type_convention': 'avenant'},
            'target': 'current',
        }

    @api.model
    def check_expirations(self):
        """Vérifie les conventions qui expirent (à exécuter par cron)"""
        today = fields.Date.today()
        conventions_expirees = self.search([
            ('statut', '=', 'en_vigueur'),
            ('date_expiration', '<=', today)
        ])
        conventions_expirees.write({'statut': 'expiree'})
        
        # Alertes pour les conventions qui expirent bientôt (30 jours)
        date_limite = today + timedelta(days=30)
        conventions_bientot_expirees = self.search([
            ('statut', '=', 'en_vigueur'),
            ('date_expiration', '<=', date_limite),
            ('date_expiration', '>', today)
        ])
        
        for convention in conventions_bientot_expirees:
            convention.message_post(
                body=_("Attention : Cette convention expire le %s.") % 
                convention.date_expiration.strftime('%d/%m/%Y')
            )

    @api.model
    def get_conventions_en_vigueur(self):
        """Retourne les conventions en vigueur"""
        return self.search([('statut', '=', 'en_vigueur')])

    @api.model
    def get_statistiques_conventions(self):
        """Retourne les statistiques des conventions"""
        total = self.search_count([])
        en_vigueur = self.search_count([('statut', '=', 'en_vigueur')])
        expirees = self.search_count([('statut', '=', 'expiree')])
        en_negociation = self.search_count([('statut', '=', 'negociation')])
        
        return {
            'total': total,
            'en_vigueur': en_vigueur,
            'expirees': expirees,
            'en_negociation': en_negociation
        }

    def name_get(self):
        result = []
        for record in self:
            name = f"[{record.reference}] {record.name}"
            if record.date_signature:
                name += f" - {record.date_signature.strftime('%d/%m/%Y')}"
            result.append((record.id, name))
        return result


class SyndicatConventionSuivi(models.Model):
    _name = 'syndicat.convention.suivi'
    _description = 'Suivi de Convention Collective'
    _order = 'date_reunion desc'

    name = fields.Char(
        string='Titre de la Réunion',
        required=True,
        help="Titre de la réunion de suivi"
    )
    
    convention_id = fields.Many2one(
        'syndicat.convention',
        string='Convention',
        required=True,
        ondelete='cascade'
    )
    
    date_reunion = fields.Datetime(
        string='Date de la Réunion',
        required=True,
        default=fields.Datetime.now
    )
    
    lieu = fields.Char(
        string='Lieu',
        required=True
    )
    
    # Participants
    participants_syndicat_ids = fields.Many2many(
        'syndicat.adherent',
        'suivi_participant_rel',
        'suivi_id',
        'adherent_id',
        string='Participants Syndicat'
    )
    
    participants_employeur = fields.Text(
        string='Participants Employeur',
        help="Représentants de l'employeur présents"
    )
    
    # Contenu
    ordre_du_jour = fields.Html(
        string='Ordre du Jour',
        required=True
    )
    
    points_abordes = fields.Html(
        string='Points Abordés',
        help="Points abordés durant la réunion"
    )
    
    problemes_identifies = fields.Html(
        string='Problèmes Identifiés',
        help="Problèmes d'application identifiés"
    )
    
    solutions_proposees = fields.Html(
        string='Solutions Proposées',
        help="Solutions proposées pour résoudre les problèmes"
    )
    
    decisions_prises = fields.Html(
        string='Décisions Prises',
        help="Décisions prises durant la réunion"
    )
    
    actions_a_entreprendre = fields.Html(
        string='Actions à Entreprendre',
        help="Actions à entreprendre suite à la réunion"
    )
    
    # Évaluation
    niveau_application = fields.Selection([
        ('mauvais', 'Mauvais'),
        ('moyen', 'Moyen'),
        ('bon', 'Bon'),
        ('excellent', 'Excellent')
    ], string='Niveau d\'Application',
       help="Évaluation du niveau d'application de la convention")
    
    satisfaction_reunion = fields.Selection([
        ('1', 'Très Insatisfaisant'),
        ('2', 'Insatisfaisant'),
        ('3', 'Moyen'),
        ('4', 'Satisfaisant'),
        ('5', 'Très Satisfaisant')
    ], string='Satisfaction de la Réunion')
    
    # Suivi
    date_prochaine_reunion = fields.Datetime(
        string='Prochaine Réunion',
        help="Date de la prochaine réunion de suivi"
    )
    
    notes = fields.Text(
        string='Notes',
        help="Notes diverses"
    )