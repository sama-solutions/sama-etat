# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class SyndicatCommunication(models.Model):
    _name = 'syndicat.communication'
    _description = 'Communication Syndicale'
    _order = 'date_creation desc'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(
        string='Titre de la Communication',
        required=True,
        tracking=True,
        help="Titre de la communication"
    )
    
    reference = fields.Char(
        string='Référence',
        required=True,
        copy=False,
        default=lambda self: _('Nouveau'),
        tracking=True,
        help="Référence unique de la communication"
    )
    
    # Type et canal
    type_communication = fields.Selection([
        ('communique', 'Communiqué'),
        ('newsletter', 'Newsletter'),
        ('email', 'Email'),
        ('sms', 'SMS'),
        ('affichage', 'Affichage'),
        ('site_web', 'Site Web'),
        ('reseaux_sociaux', 'Réseaux Sociaux'),
        ('presse', 'Communiqué de Presse'),
        ('radio_tv', 'Radio/TV'),
        ('tract', 'Tract'),
        ('autre', 'Autre')
    ], string='Type de Communication',
       required=True,
       default='email',
       tracking=True)
    
    canal_diffusion = fields.Selection([
        ('interne', 'Interne (Adhérents)'),
        ('public', 'Public'),
        ('media', 'Médias'),
        ('employeur', 'Employeur'),
        ('partenaires', 'Partenaires'),
        ('autorites', 'Autorités'),
        ('mixte', 'Mixte')
    ], string='Canal de Diffusion',
       required=True,
       default='interne',
       tracking=True)
    
    # Contenu
    contenu = fields.Html(
        string='Contenu',
        required=True,
        help="Contenu de la communication"
    )
    
    resume = fields.Text(
        string='Résumé',
        help="Résumé de la communication"
    )
    
    mots_cles = fields.Char(
        string='Mots-clés',
        help="Mots-clés pour la recherche"
    )
    
    # Dates
    date_creation = fields.Datetime(
        string='Date de Création',
        default=fields.Datetime.now,
        required=True,
        tracking=True
    )
    
    date_publication = fields.Datetime(
        string='Date de Publication',
        tracking=True,
        help="Date de publication/diffusion"
    )
    
    date_expiration = fields.Date(
        string='Date d\'Expiration',
        help="Date d'expiration de la communication"
    )
    
    # Statut
    statut = fields.Selection([
        ('brouillon', 'Brouillon'),
        ('en_attente', 'En Attente de Validation'),
        ('validee', 'Validée'),
        ('publiee', 'Publiée'),
        ('archivee', 'Archivée'),
        ('annulee', 'Annulée')
    ], string='Statut',
       default='brouillon',
       required=True,
       tracking=True)
    
    # Responsables
    auteur_id = fields.Many2one(
        'syndicat.adherent',
        string='Auteur',
        required=True,
        default=lambda self: self._get_current_adherent(),
        tracking=True
    )
    
    validateur_id = fields.Many2one(
        'syndicat.adherent',
        string='Validateur',
        tracking=True,
        help="Responsable ayant validé la communication"
    )
    
    date_validation = fields.Datetime(
        string='Date de Validation',
        tracking=True
    )
    
    # Destinataires
    destinataires_adherents_ids = fields.Many2many(
        'syndicat.adherent',
        'communication_adherent_rel',
        'communication_id',
        'adherent_id',
        string='Adhérents Destinataires'
    )
    
    destinataires_tous_adherents = fields.Boolean(
        string='Tous les Adhérents',
        default=False,
        help="Envoyer à tous les adhérents actifs"
    )
    
    destinataires_externes = fields.Text(
        string='Destinataires Externes',
        help="Liste des destinataires externes"
    )
    
    # Filtres pour destinataires
    filtre_statut_adhesion = fields.Selection([
        ('tous', 'Tous'),
        ('actif', 'Actifs seulement'),
        ('suspendu', 'Suspendus seulement')
    ], string='Filtre Statut',
       default='actif')
    
    filtre_responsabilite = fields.Selection([
        ('tous', 'Tous'),
        ('bureau', 'Bureau Exécutif'),
        ('delegues', 'Délégués'),
        ('adherents_simples', 'Adhérents Simples')
    ], string='Filtre Responsabilité',
       default='tous')
    
    # Relations
    action_id = fields.Many2one(
        'syndicat.action',
        string='Action Liée',
        help="Action syndicale liée à cette communication"
    )
    
    revendication_id = fields.Many2one(
        'syndicat.revendication',
        string='Revendication Liée',
        help="Revendication liée à cette communication"
    )
    
    assemblee_id = fields.Many2one(
        'syndicat.assemblee',
        string='Assemblée Liée',
        help="Assemblée liée à cette communication"
    )
    
    # Diffusion et suivi
    nb_destinataires = fields.Integer(
        string='Nombre de Destinataires',
        compute='_compute_nb_destinataires',
        store=True
    )
    
    nb_lectures = fields.Integer(
        string='Nombre de Lectures',
        default=0,
        help="Nombre de lectures/ouvertures"
    )
    
    nb_reponses = fields.Integer(
        string='Nombre de Réponses',
        default=0,
        help="Nombre de réponses reçues"
    )
    
    taux_ouverture = fields.Float(
        string='Taux d\'Ouverture (%)',
        compute='_compute_taux_ouverture',
        store=True
    )
    
    # Médias et pièces jointes
    pieces_jointes = fields.Text(
        string='Pièces Jointes',
        help="Liste des pièces jointes"
    )
    
    images = fields.Text(
        string='Images',
        help="Images incluses dans la communication"
    )
    
    # Paramètres de diffusion
    diffusion_immediate = fields.Boolean(
        string='Diffusion Immédiate',
        default=True,
        help="Diffuser immédiatement après validation"
    )
    
    date_diffusion_programmee = fields.Datetime(
        string='Date de Diffusion Programmée',
        help="Date de diffusion programmée"
    )
    
    rappel_automatique = fields.Boolean(
        string='Rappel Automatique',
        default=False,
        help="Envoyer un rappel automatique"
    )
    
    date_rappel = fields.Datetime(
        string='Date de Rappel',
        help="Date du rappel automatique"
    )
    
    # Évaluation
    importance = fields.Selection([
        ('faible', 'Faible'),
        ('normale', 'Normale'),
        ('elevee', 'Élevée'),
        ('critique', 'Critique')
    ], string='Importance',
       default='normale')
    
    confidentialite = fields.Selection([
        ('public', 'Public'),
        ('interne', 'Interne'),
        ('confidentiel', 'Confidentiel'),
        ('secret', 'Secret')
    ], string='Niveau de Confidentialité',
       default='interne')
    
    # Feedback
    feedback_ids = fields.One2many(
        'syndicat.communication.feedback',
        'communication_id',
        string='Retours'
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
                vals['reference'] = self.env['ir.sequence'].next_by_code('syndicat.communication') or _('Nouveau')
        return super(SyndicatCommunication, self).create(vals_list)

    def _get_current_adherent(self):
        """Retourne l'adhérent correspondant à l'utilisateur actuel"""
        user = self.env.user
        adherent = self.env['syndicat.adherent'].search([
            ('email', '=', user.email)
        ], limit=1)
        return adherent.id if adherent else False

    @api.depends('destinataires_adherents_ids', 'destinataires_tous_adherents')
    def _compute_nb_destinataires(self):
        for record in self:
            if record.destinataires_tous_adherents:
                # Compter selon les filtres
                domain = [('statut_adhesion', '=', 'actif')]
                if record.filtre_statut_adhesion != 'tous':
                    domain = [('statut_adhesion', '=', record.filtre_statut_adhesion)]
                
                if record.filtre_responsabilite == 'bureau':
                    domain.append(('responsabilite_syndicale', 'in', 
                                 ['president', 'vice_president', 'secretaire', 'tresorier']))
                elif record.filtre_responsabilite == 'delegues':
                    domain.append(('responsabilite_syndicale', 'in', 
                                 ['delegue', 'representant']))
                elif record.filtre_responsabilite == 'adherents_simples':
                    domain.append(('responsabilite_syndicale', '=', 'adherent'))
                
                record.nb_destinataires = self.env['syndicat.adherent'].search_count(domain)
            else:
                record.nb_destinataires = len(record.destinataires_adherents_ids)

    def action_view_destinataires(self):
        """Ouvre la liste des adhérents destinataires"""
        self.ensure_one()
        if self.destinataires_tous_adherents:
            # Reconstruire le domain des destinataires selon les filtres
            domain = [('statut_adhesion', '=', 'actif')]
            if self.filtre_statut_adhesion != 'tous':
                domain = [('statut_adhesion', '=', self.filtre_statut_adhesion)]
            if self.filtre_responsabilite == 'bureau':
                domain.append(('responsabilite_syndicale', 'in', ['president', 'vice_president', 'secretaire', 'tresorier']))
            elif self.filtre_responsabilite == 'delegues':
                domain.append(('responsabilite_syndicale', 'in', ['delegue', 'representant']))
            elif self.filtre_responsabilite == 'adherents_simples':
                domain.append(('responsabilite_syndicale', '=', 'adherent'))
            domain_action = domain
        else:
            domain_action = [('id', 'in', self.destinataires_adherents_ids.ids)]

        return {
            'type': 'ir.actions.act_window',
            'name': _('Destinataires'),
            'res_model': 'syndicat.adherent',
            'view_mode': 'tree,form',
            'domain': domain_action,
            'target': 'current',
        }

    def action_view_lectures(self):
        """Ouvre les 'lectures' (feedback de type lecture) liés à cette communication."""
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': _('Lectures'),
            'res_model': 'syndicat.communication.feedback',
            'view_mode': 'tree,form',
            'domain': [('communication_id', '=', self.id), ('type_feedback', '=', 'lecture')],
            'context': {'default_communication_id': self.id, 'default_type_feedback': 'lecture'},
            'target': 'current',
        }

    def action_view_reponses(self):
        """Ouvre les réponses (feedback de type commentaire/question/suggestion) liés à cette communication."""
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': _('Réponses'),
            'res_model': 'syndicat.communication.feedback',
            'view_mode': 'tree,form',
            'domain': [('communication_id', '=', self.id), ('type_feedback', 'in', ['commentaire', 'question', 'suggestion'])],
            'context': {'default_communication_id': self.id},
            'target': 'current',
        }

    def action_view_feedback(self):
        """Ouvre tous les retours liés à cette communication."""
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': _('Retours'),
            'res_model': 'syndicat.communication.feedback',
            'view_mode': 'tree,form',
            'domain': [('communication_id', '=', self.id)],
            'context': {'default_communication_id': self.id},
            'target': 'current',
        }

    @api.depends('nb_lectures', 'nb_destinataires')
    def _compute_taux_ouverture(self):
        for record in self:
            if record.nb_destinataires > 0:
                record.taux_ouverture = (record.nb_lectures / record.nb_destinataires) * 100
            else:
                record.taux_ouverture = 0.0

    @api.onchange('destinataires_tous_adherents')
    def _onchange_destinataires_tous_adherents(self):
        if self.destinataires_tous_adherents:
            self.destinataires_adherents_ids = [(5, 0, 0)]  # Vider la liste

    def action_valider(self):
        """Valide la communication"""
        self.ensure_one()
        if self.statut == 'en_attente':
            self.write({
                'statut': 'validee',
                'validateur_id': self._get_current_adherent(),
                'date_validation': fields.Datetime.now()
            })
            self.message_post(body=_("Communication validée."))
            
            if self.diffusion_immediate:
                self.action_publier()
        return True

    def action_soumettre_validation(self):
        """Soumet la communication pour validation"""
        self.ensure_one()
        if self.statut == 'brouillon':
            self.statut = 'en_attente'
            self.message_post(body=_("Communication soumise pour validation."))
        return True

    def action_publier(self):
        """Publie la communication"""
        self.ensure_one()
        if self.statut == 'validee':
            self.write({
                'statut': 'publiee',
                'date_publication': fields.Datetime.now()
            })
            self.message_post(body=_("Communication publiée."))
            self._diffuser_communication()
        return True

    def action_programmer_diffusion(self):
        """Programme la diffusion"""
        self.ensure_one()
        if self.statut == 'validee' and self.date_diffusion_programmee:
            # Logique de programmation (cron job)
            self.message_post(body=_("Diffusion programmée pour le %s.") % 
                            self.date_diffusion_programmee.strftime('%d/%m/%Y %H:%M'))
        return True

    def action_archiver(self):
        """Archive la communication"""
        self.ensure_one()
        if self.statut == 'publiee':
            self.statut = 'archivee'
            self.message_post(body=_("Communication archivée."))
        return True

    def action_annuler(self):
        """Annule la communication"""
        self.ensure_one()
        if self.statut in ['brouillon', 'en_attente', 'validee']:
            self.statut = 'annulee'
            self.message_post(body=_("Communication annulée."))
        return True

    def _diffuser_communication(self):
        """Diffuse la communication aux destinataires"""
        self.ensure_one()
        
        # Obtenir la liste des destinataires
        destinataires = self._get_destinataires()
        
        # Logique de diffusion selon le type
        if self.type_communication == 'email':
            self._envoyer_emails(destinataires)
        elif self.type_communication == 'sms':
            self._envoyer_sms(destinataires)
        # Autres types de diffusion...
        
        self.message_post(body=_("Communication diffusée à %d destinataires.") % len(destinataires))

    def _get_destinataires(self):
        """Retourne la liste des destinataires"""
        self.ensure_one()
        
        if self.destinataires_tous_adherents:
            # Appliquer les filtres
            domain = []
            if self.filtre_statut_adhesion != 'tous':
                domain.append(('statut_adhesion', '=', self.filtre_statut_adhesion))
            
            if self.filtre_responsabilite == 'bureau':
                domain.append(('responsabilite_syndicale', 'in', 
                             ['president', 'vice_president', 'secretaire', 'tresorier']))
            elif self.filtre_responsabilite == 'delegues':
                domain.append(('responsabilite_syndicale', 'in', 
                             ['delegue', 'representant']))
            elif self.filtre_responsabilite == 'adherents_simples':
                domain.append(('responsabilite_syndicale', '=', 'adherent'))
            
            return self.env['syndicat.adherent'].search(domain)
        else:
            return self.destinataires_adherents_ids

    def _envoyer_emails(self, destinataires):
        """Envoie des emails aux destinataires"""
        for destinataire in destinataires:
            if destinataire.email:
                # Logique d'envoi d'email
                pass

    def _envoyer_sms(self, destinataires):
        """Envoie des SMS aux destinataires"""
        for destinataire in destinataires:
            if destinataire.telephone:
                # Logique d'envoi de SMS
                pass

    def action_incrementer_lectures(self):
        """Incrémente le nombre de lectures"""
        self.ensure_one()
        self.nb_lectures += 1

    @api.model
    def get_communications_recentes(self, limit=10):
        """Retourne les communications récentes"""
        return self.search([
            ('statut', '=', 'publiee')
        ], limit=limit, order='date_publication desc')

    @api.model
    def get_statistiques_communications(self):
        """Retourne les statistiques des communications"""
        total = self.search_count([])
        publiees = self.search_count([('statut', '=', 'publiee')])
        en_attente = self.search_count([('statut', '=', 'en_attente')])
        brouillons = self.search_count([('statut', '=', 'brouillon')])
        
        return {
            'total': total,
            'publiees': publiees,
            'en_attente': en_attente,
            'brouillons': brouillons
        }

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
                ('contenu', operator, name),
                ('mots_cles', operator, name)
            ] + args
        return self._search(args, limit=limit, access_rights_uid=name_get_uid)


class SyndicatCommunicationFeedback(models.Model):
    _name = 'syndicat.communication.feedback'
    _description = 'Retour sur Communication'
    _order = 'date_feedback desc'

    communication_id = fields.Many2one(
        'syndicat.communication',
        string='Communication',
        required=True,
        ondelete='cascade'
    )
    
    adherent_id = fields.Many2one(
        'syndicat.adherent',
        string='Adhérent',
        required=True
    )
    
    date_feedback = fields.Datetime(
        string='Date du Retour',
        default=fields.Datetime.now,
        required=True
    )
    
    type_feedback = fields.Selection([
        ('lecture', 'Lecture'),
        ('like', 'J\'aime'),
        ('commentaire', 'Commentaire'),
        ('partage', 'Partage'),
        ('question', 'Question'),
        ('suggestion', 'Suggestion')
    ], string='Type de Retour',
       required=True,
       default='lecture')
    
    commentaire = fields.Text(
        string='Commentaire',
        help="Commentaire de l'adhérent"
    )
    
    note = fields.Selection([
        ('1', 'Très Mauvais'),
        ('2', 'Mauvais'),
        ('3', 'Moyen'),
        ('4', 'Bon'),
        ('5', 'Excellent')
    ], string='Note',
       help="Note attribuée à la communication")
    
    utile = fields.Boolean(
        string='Utile',
        default=True,
        help="Communication jugée utile"
    )