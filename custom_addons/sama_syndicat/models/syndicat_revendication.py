# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
from datetime import datetime, timedelta


class SyndicatRevendication(models.Model):
    _name = 'syndicat.revendication'
    _description = 'Revendication Syndicale'
    _order = 'date_creation desc'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(
        string='Titre de la Revendication',
        required=True,
        tracking=True,
        help="Titre de la revendication syndicale"
    )
    
    reference = fields.Char(
        string='Référence',
        required=True,
        copy=False,
        default=lambda self: _('Nouveau'),
        tracking=True,
        help="Référence unique de la revendication"
    )
    
    description = fields.Html(
        string='Description',
        required=True,
        help="Description détaillée de la revendication"
    )
    
    # Classification
    type_revendication = fields.Selection([
        ('salaire', 'Augmentation Salariale'),
        ('conditions_travail', 'Amélioration Conditions de Travail'),
        ('securite', 'Sécurité au Travail'),
        ('formation', 'Formation Professionnelle'),
        ('promotion', 'Promotion et Évolution'),
        ('temps_travail', 'Temps de Travail'),
        ('conges', 'Congés et Repos'),
        ('protection_sociale', 'Protection Sociale'),
        ('egalite', 'Égalité et Non-Discrimination'),
        ('dialogue_social', 'Dialogue Social'),
        ('emploi', 'Maintien de l\'Emploi'),
        ('restructuration', 'Opposition à Restructuration'),
        ('autre', 'Autre')
    ], string='Type de Revendication',
       required=True,
       default='salaire',
       tracking=True,
       help="Type de revendication syndicale")
    
    priorite = fields.Selection([
        ('faible', 'Faible'),
        ('normale', 'Normale'),
        ('elevee', 'Élevée'),
        ('critique', 'Critique'),
        ('urgente', 'Urgente')
    ], string='Priorité',
       default='normale',
       required=True,
       tracking=True,
       help="Niveau de priorité de la revendication")
    
    statut = fields.Selection([
        ('brouillon', 'Brouillon'),
        ('soumise', 'Soumise'),
        ('en_negociation', 'En Négociation'),
        ('acceptee_partiellement', 'Acceptée Partiellement'),
        ('acceptee', 'Acceptée'),
        ('rejetee', 'Rejetée'),
        ('suspendue', 'Suspendue'),
        ('abandonnee', 'Abandonnée')
    ], string='Statut',
       default='brouillon',
       required=True,
       tracking=True,
       help="Statut de la revendication")
    
    # Dates importantes
    date_creation = fields.Date(
        string='Date de Création',
        default=fields.Date.today,
        required=True,
        tracking=True
    )
    
    date_soumission = fields.Date(
        string='Date de Soumission',
        tracking=True,
        help="Date de soumission à l'employeur"
    )
    
    date_reponse_attendue = fields.Date(
        string='Date de Réponse Attendue',
        tracking=True,
        help="Date limite pour la réponse de l'employeur"
    )
    
    date_reponse_recue = fields.Date(
        string='Date de Réponse Reçue',
        tracking=True,
        help="Date de réception de la réponse"
    )
    
    date_resolution = fields.Date(
        string='Date de Résolution',
        tracking=True,
        help="Date de résolution finale"
    )
    
    # Parties concernées
    initiateur_id = fields.Many2one(
        'syndicat.adherent',
        string='Initiateur',
        required=True,
        tracking=True,
        help="Adhérent ayant initié la revendication"
    )
    
    adherents_soutien_ids = fields.Many2many(
        'syndicat.adherent',
        'revendication_soutien_rel',
        'revendication_id',
        'adherent_id',
        string='Adhérents Soutiens',
        help="Adhérents soutenant la revendication"
    )
    
    nb_soutiens = fields.Integer(
        string='Nombre de Soutiens',
        compute='_compute_nb_soutiens',
        store=True,
        help="Nombre d'adhérents soutenant la revendication"
    )
    
    # Employeur/Interlocuteur
    employeur_concerne = fields.Char(
        string='Employeur Concerné',
        required=True,
        help="Nom de l'employeur ou organisation concernée"
    )
    
    interlocuteur_principal = fields.Char(
        string='Interlocuteur Principal',
        help="Nom du responsable côté employeur"
    )
    
    contact_employeur = fields.Text(
        string='Contact Employeur',
        help="Coordonnées de contact de l'employeur"
    )
    
    # Contenu de la revendication
    objectifs = fields.Html(
        string='Objectifs',
        required=True,
        help="Objectifs précis de la revendication"
    )
    
    justification = fields.Html(
        string='Justification',
        required=True,
        help="Justification et arguments de la revendication"
    )
    
    propositions_concretes = fields.Html(
        string='Propositions Concrètes',
        help="Propositions concrètes et mesurables"
    )
    
    impact_attendu = fields.Html(
        string='Impact Attendu',
        help="Impact attendu de la revendication"
    )
    
    # Négociation
    negociation_ids = fields.One2many(
        'syndicat.negociation',
        'revendication_id',
        string='Négociations'
    )
    
    nb_negociations = fields.Integer(
        string='Nombre de Négociations',
        compute='_compute_nb_negociations',
        store=True
    )
    
    derniere_negociation = fields.Date(
        string='Dernière Négociation',
        compute='_compute_derniere_negociation',
        store=True
    )
    
    # Réponse de l'employeur
    reponse_employeur = fields.Html(
        string='Réponse de l\'Employeur',
        help="Réponse officielle de l'employeur"
    )
    
    contre_propositions = fields.Html(
        string='Contre-Propositions',
        help="Contre-propositions de l'employeur"
    )
    
    # Actions liées
    action_ids = fields.Many2many(
        'syndicat.action',
        'revendication_action_rel',
        'revendication_id',
        'action_id',
        string='Actions Liées',
        help="Actions syndicales liées à cette revendication"
    )
    
    # Résultats
    resultats_obtenus = fields.Html(
        string='Résultats Obtenus',
        help="Description des résultats obtenus"
    )
    
    taux_satisfaction = fields.Selection([
        ('0', 'Aucune satisfaction'),
        ('25', 'Satisfaction partielle (25%)'),
        ('50', 'Satisfaction moyenne (50%)'),
        ('75', 'Bonne satisfaction (75%)'),
        ('100', 'Satisfaction complète (100%)')
    ], string='Taux de Satisfaction',
       help="Niveau de satisfaction du résultat")
    
    # Suivi temporel
    delai_reponse = fields.Integer(
        string='Délai de Réponse (jours)',
        compute='_compute_delai_reponse',
        store=True,
        help="Délai de réponse de l'employeur en jours"
    )
    
    delai_resolution = fields.Integer(
        string='Délai de Résolution (jours)',
        compute='_compute_delai_resolution',
        store=True,
        help="Délai total de résolution en jours"
    )
    
    en_retard = fields.Boolean(
        string='En Retard',
        compute='_compute_en_retard',
        store=True,
        help="Indique si la réponse est en retard"
    )
    
    # Documents
    documents_support = fields.Text(
        string='Documents de Support',
        help="Liste des documents à l'appui de la revendication"
    )
    
    # Métadonnées
    active = fields.Boolean(
        string='Actif',
        default=True,
        help="Décocher pour archiver la revendication"
    )
    
    notes_internes = fields.Text(
        string='Notes Internes',
        help="Notes internes pour le suivi"
    )
    
    # Évaluation
    lecons_apprises = fields.Text(
        string='Leçons Apprises',
        help="Leçons tirées de cette revendication"
    )

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('reference', _('Nouveau')) == _('Nouveau'):
                vals['reference'] = self.env['ir.sequence'].next_by_code('syndicat.revendication') or _('Nouveau')
        return super(SyndicatRevendication, self).create(vals_list)

    @api.depends('adherents_soutien_ids')
    def _compute_nb_soutiens(self):
        for record in self:
            record.nb_soutiens = len(record.adherents_soutien_ids)

    @api.depends('negociation_ids')
    def _compute_nb_negociations(self):
        for record in self:
            record.nb_negociations = len(record.negociation_ids)

    @api.depends('negociation_ids', 'negociation_ids.date_negociation')
    def _compute_derniere_negociation(self):
        for record in self:
            if record.negociation_ids:
                record.derniere_negociation = max(record.negociation_ids.mapped('date_negociation'))
            else:
                record.derniere_negociation = False

    @api.depends('date_soumission', 'date_reponse_recue')
    def _compute_delai_reponse(self):
        for record in self:
            if record.date_soumission and record.date_reponse_recue:
                delta = record.date_reponse_recue - record.date_soumission
                record.delai_reponse = delta.days
            else:
                record.delai_reponse = 0

    @api.depends('date_creation', 'date_resolution')
    def _compute_delai_resolution(self):
        for record in self:
            if record.date_creation and record.date_resolution:
                delta = record.date_resolution - record.date_creation
                record.delai_resolution = delta.days
            else:
                record.delai_resolution = 0

    @api.depends('date_reponse_attendue', 'date_reponse_recue', 'statut')
    def _compute_en_retard(self):
        today = fields.Date.today()
        for record in self:
            if (record.date_reponse_attendue and 
                not record.date_reponse_recue and 
                record.statut in ['soumise', 'en_negociation']):
                record.en_retard = record.date_reponse_attendue < today
            else:
                record.en_retard = False

    @api.onchange('type_revendication')
    def _onchange_type_revendication(self):
        # Définir la priorité par défaut selon le type
        priorite_map = {
            'salaire': 'elevee',
            'conditions_travail': 'normale',
            'securite': 'critique',
            'formation': 'normale',
            'promotion': 'normale',
            'temps_travail': 'elevee',
            'conges': 'normale',
            'protection_sociale': 'elevee',
            'egalite': 'elevee',
            'dialogue_social': 'normale',
            'emploi': 'critique',
            'restructuration': 'urgente',
            'autre': 'normale'
        }
        if self.type_revendication in priorite_map:
            self.priorite = priorite_map[self.type_revendication]

    def action_soumettre(self):
        """Soumet la revendication à l'employeur"""
        self.ensure_one()
        if self.statut == 'brouillon':
            self.write({
                'statut': 'soumise',
                'date_soumission': fields.Date.today()
            })
            self.message_post(body=_("Revendication soumise à l'employeur."))
        return True

    def action_commencer_negociation(self):
        """Commence les négociations"""
        self.ensure_one()
        if self.statut == 'soumise':
            self.statut = 'en_negociation'
            self.message_post(body=_("Négociations commencées."))
        return True

    def action_accepter(self):
        """Marque la revendication comme acceptée"""
        self.ensure_one()
        if self.statut in ['soumise', 'en_negociation']:
            self.write({
                'statut': 'acceptee',
                'date_resolution': fields.Date.today(),
                'date_reponse_recue': fields.Date.today()
            })
            self.message_post(body=_("Revendication acceptée."))
        return True

    def action_accepter_partiellement(self):
        """Marque la revendication comme partiellement acceptée"""
        self.ensure_one()
        if self.statut in ['soumise', 'en_negociation']:
            self.write({
                'statut': 'acceptee_partiellement',
                'date_resolution': fields.Date.today(),
                'date_reponse_recue': fields.Date.today()
            })
            self.message_post(body=_("Revendication partiellement acceptée."))
        return True

    def action_rejeter(self):
        """Marque la revendication comme rejetée"""
        self.ensure_one()
        if self.statut in ['soumise', 'en_negociation']:
            self.write({
                'statut': 'rejetee',
                'date_resolution': fields.Date.today(),
                'date_reponse_recue': fields.Date.today()
            })
            self.message_post(body=_("Revendication rejetée."))
        return True

    def action_suspendre(self):
        """Suspend la revendication"""
        self.ensure_one()
        if self.statut in ['soumise', 'en_negociation']:
            self.statut = 'suspendue'
            self.message_post(body=_("Revendication suspendue."))
        return True

    def action_abandonner(self):
        """Abandonne la revendication"""
        self.ensure_one()
        if self.statut not in ['acceptee', 'rejetee']:
            self.write({
                'statut': 'abandonnee',
                'date_resolution': fields.Date.today()
            })
            self.message_post(body=_("Revendication abandonnée."))
        return True

    def action_ajouter_soutien(self, adherent_id):
        """Ajoute le soutien d'un adhérent"""
        self.ensure_one()
        adherent = self.env['syndicat.adherent'].browse(adherent_id)
        if adherent.statut_adhesion == 'actif' and adherent not in self.adherents_soutien_ids:
            self.adherents_soutien_ids = [(4, adherent_id)]
            self.message_post(body=_("Soutien ajouté de %s.") % adherent.name)

    def action_view_soutiens(self):
        """Ouvre la liste des adhérents soutiens"""
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': _('Soutiens'),
            'res_model': 'syndicat.adherent',
            'view_mode': 'tree,form',
            'domain': [('id', 'in', self.adherents_soutien_ids.ids)],
            'target': 'current',
        }

    def action_retirer_soutien(self, adherent_id):
        """Retire le soutien d'un adhérent"""
        self.ensure_one()
        adherent = self.env['syndicat.adherent'].browse(adherent_id)
        if adherent in self.adherents_soutien_ids:
            self.adherents_soutien_ids = [(3, adherent_id)]
            self.message_post(body=_("Soutien retiré de %s.") % adherent.name)

    def action_view_negociations(self):
        """Ouvre les négociations liées à cette revendication"""
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': _('Négociations'),
            'res_model': 'syndicat.negociation',
            'view_mode': 'tree,form',
            'domain': [('revendication_id', '=', self.id)],
            'context': {'default_revendication_id': self.id},
            'target': 'current',
        }

    @api.model
    def get_revendications_en_retard(self):
        """Retourne les revendications en retard"""
        return self.search([('en_retard', '=', True)])

    def action_view_actions(self):
        """Ouvre les actions liées à cette revendication"""
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': _('Actions Liées'),
            'res_model': 'syndicat.action',
            'view_mode': 'tree,form,calendar,graph,pivot',
            'domain': [('id', 'in', self.action_ids.ids)],
            'target': 'current',
        }

    @api.model
    def get_statistiques_revendications(self):
        """Retourne les statistiques des revendications"""
        total = self.search_count([])
        en_cours = self.search_count([('statut', 'in', ['soumise', 'en_negociation'])])
        acceptees = self.search_count([('statut', 'in', ['acceptee', 'acceptee_partiellement'])])
        rejetees = self.search_count([('statut', '=', 'rejetee')])
        en_retard = self.search_count([('en_retard', '=', True)])
        
        return {
            'total': total,
            'en_cours': en_cours,
            'acceptees': acceptees,
            'rejetees': rejetees,
            'en_retard': en_retard,
            'taux_succes': (acceptees / total * 100) if total > 0 else 0
        }

    @api.model
    def get_revendications_par_type(self):
        """Retourne la répartition des revendications par type"""
        result = []
        for type_rev in dict(self._fields['type_revendication'].selection):
            count = self.search_count([('type_revendication', '=', type_rev)])
            if count > 0:
                result.append({
                    'type': type_rev,
                    'label': dict(self._fields['type_revendication'].selection)[type_rev],
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


class SyndicatNegociation(models.Model):
    _name = 'syndicat.negociation'
    _description = 'Négociation Syndicale'
    _order = 'date_negociation desc'

    name = fields.Char(
        string='Titre de la Négociation',
        required=True,
        help="Titre de la séance de négociation"
    )
    
    revendication_id = fields.Many2one(
        'syndicat.revendication',
        string='Revendication',
        required=True,
        ondelete='cascade'
    )
    
    date_negociation = fields.Datetime(
        string='Date de Négociation',
        required=True,
        default=fields.Datetime.now
    )
    
    lieu = fields.Char(
        string='Lieu',
        required=True,
        help="Lieu de la négociation"
    )
    
    duree = fields.Float(
        string='Durée (heures)',
        help="Durée de la négociation en heures"
    )
    
    # Participants
    representants_syndicat_ids = fields.Many2many(
        'syndicat.adherent',
        'negociation_representant_rel',
        'negociation_id',
        'adherent_id',
        string='Représentants Syndicat',
        help="Représentants du syndicat"
    )
    
    representants_employeur = fields.Text(
        string='Représentants Employeur',
        help="Liste des représentants de l'employeur"
    )
    
    # Contenu
    ordre_du_jour = fields.Html(
        string='Ordre du Jour',
        help="Ordre du jour de la négociation"
    )
    
    points_abordes = fields.Html(
        string='Points Abordés',
        help="Points abordés durant la négociation"
    )
    
    positions_syndicat = fields.Html(
        string='Positions du Syndicat',
        help="Positions défendues par le syndicat"
    )
    
    positions_employeur = fields.Html(
        string='Positions de l\'Employeur',
        help="Positions exprimées par l'employeur"
    )
    
    # Résultats
    accords_obtenus = fields.Html(
        string='Accords Obtenus',
        help="Accords obtenus durant cette négociation"
    )
    
    desaccords = fields.Html(
        string='Désaccords',
        help="Points de désaccord persistants"
    )
    
    prochaines_etapes = fields.Html(
        string='Prochaines Étapes',
        help="Prochaines étapes convenues"
    )
    
    date_prochaine_negociation = fields.Datetime(
        string='Prochaine Négociation',
        help="Date de la prochaine négociation prévue"
    )
    
    # Évaluation
    satisfaction_syndicat = fields.Selection([
        ('1', 'Très Insatisfait'),
        ('2', 'Insatisfait'),
        ('3', 'Neutre'),
        ('4', 'Satisfait'),
        ('5', 'Très Satisfait')
    ], string='Satisfaction Syndicat',
       help="Niveau de satisfaction du syndicat")
    
    progres_realise = fields.Selection([
        ('aucun', 'Aucun Progrès'),
        ('faible', 'Faible Progrès'),
        ('moyen', 'Progrès Moyen'),
        ('bon', 'Bon Progrès'),
        ('excellent', 'Excellent Progrès')
    ], string='Progrès Réalisé',
       help="Évaluation du progrès réalisé")
    
    notes = fields.Text(
        string='Notes',
        help="Notes diverses sur la négociation"
    )

    def name_get(self):
        result = []
        for record in self:
            name = f"{record.name} - {record.date_negociation.strftime('%d/%m/%Y')}"
            result.append((record.id, name))
        return result