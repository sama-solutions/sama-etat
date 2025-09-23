# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
from datetime import datetime, timedelta


class SyndicatAdherent(models.Model):
    _name = 'syndicat.adherent'
    _description = 'Adhérent Syndical'
    _order = 'date_adhesion desc'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(
        string='Nom Complet',
        required=True,
        tracking=True,
        help="Nom complet de l'adhérent"
    )
    
    reference = fields.Char(
        string='Numéro d\'Adhérent',
        required=True,
        copy=False,
        default=lambda self: _('Nouveau'),
        tracking=True,
        help="Numéro unique d'adhérent"
    )
    
    # Informations personnelles
    prenom = fields.Char(
        string='Prénom',
        required=True,
        tracking=True
    )
    
    nom_famille = fields.Char(
        string='Nom de Famille',
        required=True,
        tracking=True
    )
    
    date_naissance = fields.Date(
        string='Date de Naissance',
        tracking=True
    )
    
    lieu_naissance = fields.Char(
        string='Lieu de Naissance',
        tracking=True
    )
    
    sexe = fields.Selection([
        ('masculin', 'Masculin'),
        ('feminin', 'Féminin'),
        ('autre', 'Autre')
    ], string='Sexe', tracking=True)
    
    situation_matrimoniale = fields.Selection([
        ('celibataire', 'Célibataire'),
        ('marie', 'Marié(e)'),
        ('divorce', 'Divorcé(e)'),
        ('veuf', 'Veuf/Veuve'),
        ('autre', 'Autre')
    ], string='Situation Matrimoniale')
    
    # Contact
    email = fields.Char(
        string='Email',
        tracking=True
    )
    
    telephone = fields.Char(
        string='Téléphone',
        tracking=True
    )
    
    telephone_urgence = fields.Char(
        string='Téléphone d\'Urgence',
        help="Contact en cas d'urgence"
    )
    
    adresse = fields.Text(
        string='Adresse Complète',
        tracking=True
    )
    
    ville = fields.Char(
        string='Ville',
        tracking=True
    )
    
    region = fields.Char(
        string='Région',
        tracking=True
    )
    
    # Informations professionnelles
    employeur = fields.Char(
        string='Employeur',
        required=True,
        tracking=True,
        help="Nom de l'employeur ou entreprise"
    )
    
    poste_occupe = fields.Char(
        string='Poste Occupé',
        required=True,
        tracking=True
    )
    
    service_departement = fields.Char(
        string='Service/Département',
        tracking=True
    )
    
    anciennete_poste = fields.Float(
        string='Ancienneté (années)',
        help="Ancienneté dans le poste en années"
    )
    
    salaire_mensuel = fields.Monetary(
        string='Salaire Mensuel',
        currency_field='currency_id',
        tracking=True
    )
    
    currency_id = fields.Many2one(
        'res.currency',
        string='Devise',
        default=lambda self: self.env.company.currency_id
    )
    
    type_contrat = fields.Selection([
        ('cdi', 'CDI'),
        ('cdd', 'CDD'),
        ('stage', 'Stage'),
        ('interim', 'Intérim'),
        ('freelance', 'Freelance'),
        ('fonctionnaire', 'Fonctionnaire'),
        ('autre', 'Autre')
    ], string='Type de Contrat', tracking=True)
    
    # Adhésion syndicale
    date_adhesion = fields.Date(
        string='Date d\'Adhésion',
        default=fields.Date.today,
        required=True,
        tracking=True
    )
    
    statut_adhesion = fields.Selection([
        ('actif', 'Actif'),
        ('suspendu', 'Suspendu'),
        ('demission', 'Démission'),
        ('exclusion', 'Exclusion'),
        ('retraite', 'Retraite')
    ], string='Statut d\'Adhésion',
       default='actif',
       required=True,
       tracking=True)
    
    motif_suspension = fields.Text(
        string='Motif de Suspension/Exclusion',
        help="Motif en cas de suspension ou exclusion"
    )
    
    date_fin_adhesion = fields.Date(
        string='Date de Fin d\'Adhésion',
        tracking=True
    )
    
    # Cotisations
    montant_cotisation_mensuelle = fields.Monetary(
        string='Cotisation Mensuelle',
        currency_field='currency_id',
        required=True,
        default=5000.0,
        tracking=True
    )
    
    mode_paiement_cotisation = fields.Selection([
        ('virement', 'Virement Bancaire'),
        ('prelevement', 'Prélèvement Automatique'),
        ('especes', 'Espèces'),
        ('cheque', 'Chèque'),
        ('mobile_money', 'Mobile Money')
    ], string='Mode de Paiement', default='virement')
    
    cotisations_a_jour = fields.Boolean(
        string='Cotisations à Jour',
        compute='_compute_cotisations_a_jour',
        store=True,
        help="Indique si les cotisations sont à jour"
    )
    
    derniere_cotisation_payee = fields.Date(
        string='Dernière Cotisation Payée',
        compute='_compute_derniere_cotisation',
        store=True
    )
    
    # Responsabilités syndicales
    responsabilite_syndicale = fields.Selection([
        ('adherent', 'Adhérent Simple'),
        ('delegue', 'Délégué du Personnel'),
        ('representant', 'Représentant Syndical'),
        ('secretaire', 'Secrétaire'),
        ('tresorier', 'Trésorier'),
        ('vice_president', 'Vice-Président'),
        ('president', 'Président'),
        ('autre', 'Autre')
    ], string='Responsabilité Syndicale',
       default='adherent',
       tracking=True)
    
    date_debut_responsabilite = fields.Date(
        string='Début de Responsabilité',
        tracking=True
    )
    
    date_fin_responsabilite = fields.Date(
        string='Fin de Responsabilité',
        tracking=True
    )
    
    # Formations et compétences
    formations_suivies = fields.Text(
        string='Formations Suivies (Liste)',
        help="Liste des formations syndicales suivies"
    )
    
    competences_particulieres = fields.Text(
        string='Compétences Particulières',
        help="Compétences particulières utiles au syndicat"
    )
    
    # Participation
    nb_assemblees_participees = fields.Integer(
        string='Nb. Assemblées Participées',
        compute='_compute_participation_stats',
        store=True
    )
    
    nb_actions_participees = fields.Integer(
        string='Nb. Actions Participées',
        compute='_compute_participation_stats',
        store=True
    )
    
    taux_participation = fields.Float(
        string='Taux de Participation (%)',
        compute='_compute_taux_participation',
        store=True
    )

    # Statistiques
    nb_cotisations = fields.Integer(
        string='Nombre de Cotisations',
        compute='_compute_nb_cotisations',
        store=True
    )
    
    # Relations
    cotisation_ids = fields.One2many(
        'syndicat.cotisation',
        'adherent_id',
        string='Cotisations'
    )
    
    assemblee_ids = fields.Many2many(
        'syndicat.assemblee',
        'assemblee_adherent_rel',
        'adherent_id',
        'assemblee_id',
        string='Assemblées Participées'
    )
    
    action_ids = fields.Many2many(
        'syndicat.action',
        'action_adherent_rel',
        'adherent_id',
        'action_id',
        string='Actions Participées'
    )
    
    formation_ids = fields.Many2many(
        'syndicat.formation',
        'formation_adherent_rel',
        'adherent_id',
        'formation_id',
        string='Formations Suivies'
    )
    
    # Métadonnées
    active = fields.Boolean(
        string='Actif',
        default=True,
        help="Décocher pour archiver l'adhérent"
    )
    
    notes = fields.Text(
        string='Notes',
        help="Notes diverses sur l'adhérent"
    )
    
    # Champs calculés
    age = fields.Integer(
        string='Âge',
        compute='_compute_age',
        store=True
    )
    
    anciennete_syndicat = fields.Float(
        string='Ancienneté Syndicat (années)',
        compute='_compute_anciennete_syndicat',
        store=True
    )

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('reference', _('Nouveau')) == _('Nouveau'):
                vals['reference'] = self.env['ir.sequence'].next_by_code('syndicat.adherent') or _('Nouveau')
            # Construire le nom complet
            if 'prenom' in vals and 'nom_famille' in vals:
                vals['name'] = f"{vals['prenom']} {vals['nom_famille']}"
        return super(SyndicatAdherent, self).create(vals_list)

    def write(self, vals):
        # Mettre à jour le nom complet si prénom ou nom changent
        if 'prenom' in vals or 'nom_famille' in vals:
            for record in self:
                prenom = vals.get('prenom', record.prenom)
                nom_famille = vals.get('nom_famille', record.nom_famille)
                vals['name'] = f"{prenom} {nom_famille}"
        return super(SyndicatAdherent, self).write(vals)

    @api.depends('date_naissance')
    def _compute_age(self):
        today = fields.Date.today()
        for record in self:
            if record.date_naissance:
                record.age = today.year - record.date_naissance.year - \
                           ((today.month, today.day) < (record.date_naissance.month, record.date_naissance.day))
            else:
                record.age = 0

    @api.depends('date_adhesion')
    def _compute_anciennete_syndicat(self):
        today = fields.Date.today()
        for record in self:
            if record.date_adhesion:
                delta = today - record.date_adhesion
                record.anciennete_syndicat = delta.days / 365.25
            else:
                record.anciennete_syndicat = 0.0

    @api.depends('cotisation_ids', 'cotisation_ids.date_paiement', 'cotisation_ids.statut')
    def _compute_cotisations_a_jour(self):
        for record in self:
            # Vérifier si les 3 derniers mois sont payés
            today = fields.Date.today()
            trois_mois_avant = today - timedelta(days=90)
            
            cotisations_recentes = record.cotisation_ids.filtered(
                lambda c: c.date_paiement >= trois_mois_avant and c.statut == 'payee'
            )
            
            # Considérer à jour si au moins 2 cotisations des 3 derniers mois
            record.cotisations_a_jour = len(cotisations_recentes) >= 2

    @api.depends('cotisation_ids', 'cotisation_ids.date_paiement')
    def _compute_derniere_cotisation(self):
        for record in self:
            cotisations_payees = record.cotisation_ids.filtered(lambda c: c.statut == 'payee')
            if cotisations_payees:
                record.derniere_cotisation_payee = max(cotisations_payees.mapped('date_paiement'))
            else:
                record.derniere_cotisation_payee = False

    @api.depends('assemblee_ids', 'action_ids')
    def _compute_participation_stats(self):
        for record in self:
            record.nb_assemblees_participees = len(record.assemblee_ids)
            record.nb_actions_participees = len(record.action_ids)

    @api.depends('cotisation_ids')
    def _compute_nb_cotisations(self):
        for record in self:
            record.nb_cotisations = len(record.cotisation_ids)

    @api.depends('nb_assemblees_participees', 'nb_actions_participees')
    def _compute_taux_participation(self):
        for record in self:
            # Calculer le taux basé sur le total d'événements disponibles
            total_assemblees = self.env['syndicat.assemblee'].search_count([])
            total_actions = self.env['syndicat.action'].search_count([])
            total_evenements = total_assemblees + total_actions
            
            if total_evenements > 0:
                participations = record.nb_assemblees_participees + record.nb_actions_participees
                record.taux_participation = (participations / total_evenements) * 100
            else:
                record.taux_participation = 0.0

    @api.constrains('email')
    def _check_email_unique(self):
        for record in self:
            if record.email:
                existing = self.search([
                    ('email', '=', record.email),
                    ('id', '!=', record.id),
                    ('statut_adhesion', '=', 'actif')
                ])
                if existing:
                    raise ValidationError(_("Un adhérent actif avec cet email existe déjà."))

    @api.constrains('date_adhesion', 'date_fin_adhesion')
    def _check_dates_coherence(self):
        for record in self:
            if record.date_adhesion and record.date_fin_adhesion:
                if record.date_fin_adhesion <= record.date_adhesion:
                    raise ValidationError(_("La date de fin d'adhésion doit être postérieure à la date d'adhésion."))

    def action_suspendre(self):
        """Suspend l'adhésion"""
        self.ensure_one()
        if self.statut_adhesion == 'actif':
            self.statut_adhesion = 'suspendu'
            self.message_post(body=_("Adhésion suspendue."))
        return True

    def action_reactiver(self):
        """Réactive l'adhésion"""
        self.ensure_one()
        if self.statut_adhesion == 'suspendu':
            self.statut_adhesion = 'actif'
            self.message_post(body=_("Adhésion réactivée."))
        return True

    def action_demission(self):
        """Enregistre la démission"""
        self.ensure_one()
        if self.statut_adhesion in ['actif', 'suspendu']:
            self.statut_adhesion = 'demission'
            self.date_fin_adhesion = fields.Date.today()
            self.message_post(body=_("Démission enregistrée."))
        return True

    def action_generer_cotisation_mensuelle(self):
        """Génère la cotisation mensuelle"""
        self.ensure_one()
        if self.statut_adhesion == 'actif':
            today = fields.Date.today()
            # Vérifier si une cotisation existe déjà pour ce mois
            existing = self.env['syndicat.cotisation'].search([
                ('adherent_id', '=', self.id),
                ('mois', '=', f"{today.month:02d}"),
                ('annee', '=', today.year)
            ])
            
            if not existing:
                self.env['syndicat.cotisation'].create({
                    'adherent_id': self.id,
                    'montant': self.montant_cotisation_mensuelle,
                    'mois': f"{today.month:02d}",
                    'annee': today.year,
                    'date_echeance': today.replace(day=28),  # Échéance fin de mois
                })
                self.message_post(body=_("Cotisation mensuelle générée."))

    def action_view_cotisations(self):
        """Ouvre les cotisations de l'adhérent"""
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': _('Cotisations'),
            'res_model': 'syndicat.cotisation',
            'view_mode': 'tree,form',
            'domain': [('adherent_id', '=', self.id)],
            'context': {'default_adherent_id': self.id},
            'target': 'current',
        }

    def action_view_assemblees(self):
        """Ouvre les assemblées auxquelles l'adhérent a participé"""
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': _('Assemblées'),
            'res_model': 'syndicat.assemblee',
            'view_mode': 'tree,form,calendar,graph,pivot',
            'domain': [('id', 'in', self.assemblee_ids.ids)],
            'target': 'current',
        }

    def action_view_actions(self):
        """Ouvre les actions auxquelles l'adhérent a participé"""
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': _('Actions'),
            'res_model': 'syndicat.action',
            'view_mode': 'tree,form,calendar,graph,pivot',
            'domain': [('id', 'in', self.action_ids.ids)],
            'target': 'current',
        }

    @api.model
    def get_adherents_cotisations_retard(self):
        """Retourne les adhérents en retard de cotisation"""
        return self.search([
            ('statut_adhesion', '=', 'actif'),
            ('cotisations_a_jour', '=', False)
        ])

    @api.model
    def get_statistiques_adherents(self):
        """Retourne les statistiques des adhérents"""
        total = self.search_count([])
        actifs = self.search_count([('statut_adhesion', '=', 'actif')])
        suspendus = self.search_count([('statut_adhesion', '=', 'suspendu')])
        cotisations_jour = self.search_count([
            ('statut_adhesion', '=', 'actif'),
            ('cotisations_a_jour', '=', True)
        ])
        
        return {
            'total': total,
            'actifs': actifs,
            'suspendus': suspendus,
            'cotisations_jour': cotisations_jour,
            'taux_cotisations_jour': (cotisations_jour / actifs * 100) if actifs > 0 else 0
        }

    def name_get(self):
        result = []
        for record in self:
            name = f"[{record.reference}] {record.name}"
            if record.employeur:
                name += f" - {record.employeur}"
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
                ('email', operator, name),
                ('employeur', operator, name)
            ] + args
        return self._search(args, limit=limit, access_rights_uid=name_get_uid)


class SyndicatCotisation(models.Model):
    _name = 'syndicat.cotisation'
    _description = 'Cotisation Syndicale'
    _order = 'annee desc, mois desc'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(
        string='Référence',
        compute='_compute_name',
        store=True
    )
    
    adherent_id = fields.Many2one(
        'syndicat.adherent',
        string='Adhérent',
        required=True,
        ondelete='cascade'
    )
    
    montant = fields.Monetary(
        string='Montant',
        currency_field='currency_id',
        required=True
    )
    
    currency_id = fields.Many2one(
        'res.currency',
        string='Devise',
        default=lambda self: self.env.company.currency_id
    )
    
    mois = fields.Selection([
        ('01', 'Janvier'), ('02', 'Février'), ('03', 'Mars'), ('04', 'Avril'),
        ('05', 'Mai'), ('06', 'Juin'), ('07', 'Juillet'), ('08', 'Août'),
        ('09', 'Septembre'), ('10', 'Octobre'), ('11', 'Novembre'), ('12', 'Décembre')
    ], string='Mois', required=True)
    
    annee = fields.Integer(
        string='Année',
        required=True,
        default=lambda self: fields.Date.today().year
    )
    
    date_echeance = fields.Date(
        string='Date d\'Échéance',
        required=True
    )
    
    date_paiement = fields.Date(
        string='Date de Paiement',
        tracking=True
    )
    
    statut = fields.Selection([
        ('en_attente', 'En Attente'),
        ('payee', 'Payée'),
        ('en_retard', 'En Retard'),
        ('annulee', 'Annulée')
    ], string='Statut',
       default='en_attente',
       required=True,
       tracking=True)
    
    mode_paiement = fields.Selection([
        ('virement', 'Virement Bancaire'),
        ('prelevement', 'Prélèvement Automatique'),
        ('especes', 'Espèces'),
        ('cheque', 'Chèque'),
        ('mobile_money', 'Mobile Money')
    ], string='Mode de Paiement')
    
    reference_paiement = fields.Char(
        string='Référence de Paiement',
        help="Numéro de transaction ou référence du paiement"
    )
    
    notes = fields.Text(
        string='Notes'
    )

    @api.depends('adherent_id', 'mois', 'annee')
    def _compute_name(self):
        mois_names = dict(self._fields['mois'].selection)
        for record in self:
            if record.adherent_id and record.mois and record.annee:
                record.name = f"Cotisation {mois_names.get(record.mois)} {record.annee} - {record.adherent_id.name}"
            else:
                record.name = "Nouvelle cotisation"

    def action_marquer_payee(self):
        """Marque la cotisation comme payée"""
        self.ensure_one()
        if self.statut in ['en_attente', 'en_retard']:
            self.write({
                'statut': 'payee',
                'date_paiement': fields.Date.today()
            })
            self.message_post(body=_("Cotisation marquée comme payée."))
        return True

    def action_annuler(self):
        """Annule la cotisation"""
        self.ensure_one()
        if self.statut != 'payee':
            self.statut = 'annulee'
            self.message_post(body=_("Cotisation annulée."))
        return True

    @api.model
    def update_statuts_retard(self):
        """Met à jour les statuts en retard (à exécuter par cron)"""
        today = fields.Date.today()
        cotisations_retard = self.search([
            ('statut', '=', 'en_attente'),
            ('date_echeance', '<', today)
        ])
        cotisations_retard.write({'statut': 'en_retard'})
        return True