# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class SyndicatFormation(models.Model):
    _name = 'syndicat.formation'
    _description = 'Formation Syndicale'
    _order = 'date_debut desc'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(
        string='Titre de la Formation',
        required=True,
        tracking=True,
        help="Titre de la formation"
    )
    
    reference = fields.Char(
        string='Référence',
        required=True,
        copy=False,
        default=lambda self: _('Nouveau'),
        tracking=True,
        help="Référence unique de la formation"
    )
    
    description = fields.Html(
        string='Description',
        required=True,
        help="Description détaillée de la formation"
    )
    
    # Classification
    type_formation = fields.Selection([
        ('initiation', 'Initiation Syndicale'),
        ('leadership', 'Leadership Syndical'),
        ('negociation', 'Techniques de Négociation'),
        ('droit_travail', 'Droit du Travail'),
        ('communication', 'Communication'),
        ('gestion_conflit', 'Gestion des Conflits'),
        ('comptabilite', 'Comptabilité Syndicale'),
        ('organisation', 'Organisation Syndicale'),
        ('securite_travail', 'Sécurité au Travail'),
        ('genre', 'Genre et Syndicat'),
        ('jeunesse', 'Syndicalisme et Jeunesse'),
        ('international', 'Syndicalisme International'),
        ('autre', 'Autre')
    ], string='Type de Formation',
       required=True,
       default='initiation',
       tracking=True)
    
    niveau = fields.Selection([
        ('debutant', 'Débutant'),
        ('intermediaire', 'Intermédiaire'),
        ('avance', 'Avancé'),
        ('expert', 'Expert')
    ], string='Niveau',
       required=True,
       default='debutant')
    
    # Dates et horaires
    date_debut = fields.Datetime(
        string='Date et Heure de Début',
        required=True,
        tracking=True
    )
    
    date_fin = fields.Datetime(
        string='Date et Heure de Fin',
        required=True,
        tracking=True
    )
    
    duree_totale = fields.Float(
        string='Durée Totale (heures)',
        compute='_compute_duree_totale',
        store=True,
        help="Durée totale de la formation en heures"
    )
    
    # Lieu
    lieu = fields.Char(
        string='Lieu',
        required=True,
        help="Lieu de la formation"
    )
    
    adresse_complete = fields.Text(
        string='Adresse Complète'
    )
    
    # Formateurs
    formateur_principal_id = fields.Many2one(
        'syndicat.adherent',
        string='Formateur Principal',
        tracking=True
    )
    
    formateurs_externes = fields.Text(
        string='Formateurs Externes',
        help="Formateurs externes (non-adhérents)"
    )
    
    # Participants
    participants_ids = fields.Many2many(
        'syndicat.adherent',
        'formation_participant_rel',
        'formation_id',
        'adherent_id',
        string='Participants'
    )
    
    nb_participants_max = fields.Integer(
        string='Nombre Maximum de Participants',
        default=20
    )
    
    nb_participants_inscrits = fields.Integer(
        string='Participants Inscrits',
        compute='_compute_nb_participants',
        store=True
    )
    
    nb_participants_presents = fields.Integer(
        string='Participants Présents',
        help="Nombre de participants effectivement présents"
    )
    
    # Statut
    statut = fields.Selection([
        ('planifiee', 'Planifiée'),
        ('inscriptions_ouvertes', 'Inscriptions Ouvertes'),
        ('confirmee', 'Confirmée'),
        ('en_cours', 'En Cours'),
        ('terminee', 'Terminée'),
        ('reportee', 'Reportée'),
        ('annulee', 'Annulée')
    ], string='Statut',
       default='planifiee',
       required=True,
       tracking=True)
    
    # Contenu pédagogique
    objectifs = fields.Html(
        string='Objectifs Pédagogiques',
        required=True,
        help="Objectifs de la formation"
    )
    
    programme = fields.Html(
        string='Programme',
        required=True,
        help="Programme détaillé de la formation"
    )
    
    prerequis = fields.Html(
        string='Prérequis',
        help="Prérequis pour participer à la formation"
    )
    
    methodes_pedagogiques = fields.Html(
        string='Méthodes Pédagogiques',
        help="Méthodes pédagogiques utilisées"
    )
    
    supports_formation = fields.Text(
        string='Supports de Formation',
        help="Liste des supports de formation"
    )
    
    # Évaluation
    evaluation_requise = fields.Boolean(
        string='Évaluation Requise',
        default=True,
        help="Évaluation des participants requise"
    )
    
    type_evaluation = fields.Selection([
        ('qcm', 'QCM'),
        ('oral', 'Oral'),
        ('pratique', 'Pratique'),
        ('projet', 'Projet'),
        ('mixte', 'Mixte')
    ], string='Type d\'Évaluation',
       default='qcm')
    
    note_passage = fields.Float(
        string='Note de Passage',
        default=10.0,
        help="Note minimum pour valider la formation"
    )
    
    # Certification
    certification = fields.Boolean(
        string='Certification',
        default=False,
        help="Formation certifiante"
    )
    
    organisme_certificateur = fields.Char(
        string='Organisme Certificateur',
        help="Organisme délivrant la certification"
    )
    
    # Budget
    budget_prevu = fields.Monetary(
        string='Budget Prévu',
        currency_field='currency_id'
    )
    
    budget_reel = fields.Monetary(
        string='Budget Réel',
        currency_field='currency_id'
    )
    
    currency_id = fields.Many2one(
        'res.currency',
        string='Devise',
        default=lambda self: self.env.company.currency_id
    )
    
    cout_par_participant = fields.Monetary(
        string='Coût par Participant',
        currency_field='currency_id',
        compute='_compute_cout_par_participant',
        store=True
    )
    
    # Résultats
    resultats_ids = fields.One2many(
        'syndicat.formation.resultat',
        'formation_id',
        string='Résultats'
    )
    
    taux_reussite = fields.Float(
        string='Taux de Réussite (%)',
        compute='_compute_taux_reussite',
        store=True
    )
    
    satisfaction_moyenne = fields.Float(
        string='Satisfaction Moyenne',
        compute='_compute_satisfaction_moyenne',
        store=True
    )
    
    # Suivi post-formation
    suivi_requis = fields.Boolean(
        string='Suivi Post-Formation',
        default=False,
        help="Suivi post-formation requis"
    )
    
    date_suivi = fields.Date(
        string='Date de Suivi',
        help="Date du suivi post-formation"
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
                vals['reference'] = self.env['ir.sequence'].next_by_code('syndicat.formation') or _('Nouveau')
        return super(SyndicatFormation, self).create(vals_list)

    @api.depends('date_debut', 'date_fin')
    def _compute_duree_totale(self):
        for record in self:
            if record.date_debut and record.date_fin:
                delta = record.date_fin - record.date_debut
                record.duree_totale = delta.total_seconds() / 3600
            else:
                record.duree_totale = 0.0

    @api.depends('participants_ids')
    def _compute_nb_participants(self):
        for record in self:
            record.nb_participants_inscrits = len(record.participants_ids)

    # Actions pour les boutons stat
    def action_view_participants(self):
        """Ouvre la liste des participants inscrits"""
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': _('Participants'),
            'res_model': 'syndicat.adherent',
            'view_mode': 'tree,form',
            'domain': [('id', 'in', self.participants_ids.ids)],
            'target': 'current',
        }

    def action_view_resultats(self):
        """Ouvre les résultats de la formation"""
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': _('Résultats'),
            'res_model': 'syndicat.formation.resultat',
            'view_mode': 'tree,form',
            'domain': [('formation_id', '=', self.id)],
            'context': {'default_formation_id': self.id},
            'target': 'current',
        }

    def action_view_budget(self):
        """Ouvre l'onglet budget (recentrer sur la fiche courante)"""
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': _('Budget'),
            'res_model': 'syndicat.formation',
            'view_mode': 'form',
            'res_id': self.id,
            'target': 'current',
        }

    @api.depends('budget_reel', 'nb_participants_presents')
    def _compute_cout_par_participant(self):
        for record in self:
            if record.nb_participants_presents > 0:
                record.cout_par_participant = record.budget_reel / record.nb_participants_presents
            else:
                record.cout_par_participant = 0.0

    @api.depends('resultats_ids', 'resultats_ids.reussi')
    def _compute_taux_reussite(self):
        for record in self:
            if record.resultats_ids:
                reussis = record.resultats_ids.filtered(lambda r: r.reussi)
                record.taux_reussite = (len(reussis) / len(record.resultats_ids)) * 100
            else:
                record.taux_reussite = 0.0

    @api.depends('resultats_ids', 'resultats_ids.satisfaction')
    def _compute_satisfaction_moyenne(self):
        for record in self:
            if record.resultats_ids:
                satisfactions = record.resultats_ids.mapped('satisfaction')
                satisfactions_numeriques = [int(s) for s in satisfactions if s]
                if satisfactions_numeriques:
                    record.satisfaction_moyenne = sum(satisfactions_numeriques) / len(satisfactions_numeriques)
                else:
                    record.satisfaction_moyenne = 0.0
            else:
                record.satisfaction_moyenne = 0.0

    @api.constrains('date_debut', 'date_fin')
    def _check_dates_coherence(self):
        for record in self:
            if record.date_debut and record.date_fin:
                if record.date_fin <= record.date_debut:
                    raise ValidationError(_("La date de fin doit être postérieure à la date de début."))

    @api.constrains('nb_participants_max', 'participants_ids')
    def _check_nb_participants_max(self):
        for record in self:
            if len(record.participants_ids) > record.nb_participants_max:
                raise ValidationError(_("Le nombre de participants dépasse la capacité maximale."))

    def action_ouvrir_inscriptions(self):
        """Ouvre les inscriptions"""
        self.ensure_one()
        if self.statut == 'planifiee':
            self.statut = 'inscriptions_ouvertes'
            self.message_post(body=_("Inscriptions ouvertes."))
        return True

    def action_confirmer(self):
        """Confirme la formation"""
        self.ensure_one()
        if self.statut == 'inscriptions_ouvertes':
            self.statut = 'confirmee'
            self.message_post(body=_("Formation confirmée."))
        return True

    def action_commencer(self):
        """Démarre la formation"""
        self.ensure_one()
        if self.statut == 'confirmee':
            self.statut = 'en_cours'
            self.message_post(body=_("Formation démarrée."))
        return True

    def action_terminer(self):
        """Termine la formation"""
        self.ensure_one()
        if self.statut == 'en_cours':
            self.statut = 'terminee'
            self.message_post(body=_("Formation terminée."))
            self._generer_resultats()
        return True

    def action_reporter(self):
        """Reporte la formation"""
        self.ensure_one()
        if self.statut in ['planifiee', 'inscriptions_ouvertes', 'confirmee']:
            self.statut = 'reportee'
            self.message_post(body=_("Formation reportée."))
        return True

    def action_annuler(self):
        """Annule la formation"""
        self.ensure_one()
        if self.statut in ['planifiee', 'inscriptions_ouvertes', 'confirmee']:
            self.statut = 'annulee'
            self.message_post(body=_("Formation annulée."))
        return True

    def action_inscrire_adherent(self, adherent_id):
        """Inscrit un adhérent à la formation"""
        self.ensure_one()
        if self.statut == 'inscriptions_ouvertes':
            if len(self.participants_ids) < self.nb_participants_max:
                adherent = self.env['syndicat.adherent'].browse(adherent_id)
                if adherent not in self.participants_ids:
                    self.participants_ids = [(4, adherent_id)]
                    self.message_post(body=_("Adhérent inscrit : %s.") % adherent.name)
                else:
                    raise ValidationError(_("Cet adhérent est déjà inscrit."))
            else:
                raise ValidationError(_("Capacité maximale atteinte."))
        else:
            raise ValidationError(_("Les inscriptions ne sont pas ouvertes."))

    def action_desinscrire_adherent(self, adherent_id):
        """Désinscrit un adhérent de la formation"""
        self.ensure_one()
        if self.statut == 'inscriptions_ouvertes':
            adherent = self.env['syndicat.adherent'].browse(adherent_id)
            if adherent in self.participants_ids:
                self.participants_ids = [(3, adherent_id)]
                self.message_post(body=_("Adhérent désinscrit : %s.") % adherent.name)
            else:
                raise ValidationError(_("Cet adhérent n'est pas inscrit."))
        else:
            raise ValidationError(_("Les inscriptions ne sont pas ouvertes."))

    def _generer_resultats(self):
        """Génère les résultats pour tous les participants"""
        self.ensure_one()
        for participant in self.participants_ids:
            existing = self.env['syndicat.formation.resultat'].search([
                ('formation_id', '=', self.id),
                ('adherent_id', '=', participant.id)
            ])
            if not existing:
                self.env['syndicat.formation.resultat'].create({
                    'formation_id': self.id,
                    'adherent_id': participant.id,
                    'present': True,  # À ajuster selon la présence réelle
                })

    @api.model
    def get_formations_disponibles(self):
        """Retourne les formations avec inscriptions ouvertes"""
        return self.search([('statut', '=', 'inscriptions_ouvertes')])

    @api.model
    def get_statistiques_formations(self):
        """Retourne les statistiques des formations"""
        total = self.search_count([])
        terminees = self.search_count([('statut', '=', 'terminee')])
        en_cours = self.search_count([('statut', 'in', ['inscriptions_ouvertes', 'confirmee', 'en_cours'])])
        
        return {
            'total': total,
            'terminees': terminees,
            'en_cours': en_cours
        }

    def name_get(self):
        result = []
        for record in self:
            name = f"[{record.reference}] {record.name}"
            if record.date_debut:
                name += f" - {record.date_debut.strftime('%d/%m/%Y')}"
            result.append((record.id, name))
        return result


class SyndicatFormationResultat(models.Model):
    _name = 'syndicat.formation.resultat'
    _description = 'Résultat de Formation'
    _order = 'formation_id, adherent_id'

    formation_id = fields.Many2one(
        'syndicat.formation',
        string='Formation',
        required=True,
        ondelete='cascade'
    )
    
    adherent_id = fields.Many2one(
        'syndicat.adherent',
        string='Adhérent',
        required=True
    )
    
    present = fields.Boolean(
        string='Présent',
        default=True,
        help="Adhérent présent à la formation"
    )
    
    note = fields.Float(
        string='Note',
        help="Note obtenue par l'adhérent"
    )
    
    reussi = fields.Boolean(
        string='Réussi',
        compute='_compute_reussi',
        store=True,
        help="Formation réussie"
    )
    
    satisfaction = fields.Selection([
        ('1', 'Très Insatisfait'),
        ('2', 'Insatisfait'),
        ('3', 'Neutre'),
        ('4', 'Satisfait'),
        ('5', 'Très Satisfait')
    ], string='Satisfaction',
       help="Niveau de satisfaction de l'adhérent")
    
    commentaires = fields.Text(
        string='Commentaires',
        help="Commentaires de l'adhérent sur la formation"
    )
    
    certificat_delivre = fields.Boolean(
        string='Certificat Délivré',
        default=False,
        help="Certificat délivré à l'adhérent"
    )
    
    date_certificat = fields.Date(
        string='Date du Certificat',
        help="Date de délivrance du certificat"
    )
    
    competences_acquises = fields.Text(
        string='Compétences Acquises',
        help="Compétences acquises par l'adhérent"
    )

    @api.depends('note', 'formation_id.note_passage', 'present')
    def _compute_reussi(self):
        for record in self:
            if record.present and record.formation_id.evaluation_requise:
                record.reussi = record.note >= record.formation_id.note_passage
            elif record.present and not record.formation_id.evaluation_requise:
                record.reussi = True
            else:
                record.reussi = False

    def action_delivrer_certificat(self):
        """Délivre le certificat"""
        self.ensure_one()
        if self.reussi and self.formation_id.certification:
            self.write({
                'certificat_delivre': True,
                'date_certificat': fields.Date.today()
            })
            self.formation_id.message_post(
                body=_("Certificat délivré à %s.") % self.adherent_id.name
            )