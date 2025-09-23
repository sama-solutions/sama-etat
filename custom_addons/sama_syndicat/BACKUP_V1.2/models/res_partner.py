# -*- coding: utf-8 -*-

from odoo import models, fields, api, _


class ResPartner(models.Model):
    _inherit = 'res.partner'

    # Champs spécifiques au syndicat
    is_adherent_syndicat = fields.Boolean(
        string='Adhérent Syndical',
        default=False,
        help="Cocher si ce contact est un adhérent du syndicat"
    )
    
    is_employeur = fields.Boolean(
        string='Employeur',
        default=False,
        help="Cocher si ce contact est un employeur"
    )
    
    is_partenaire_syndical = fields.Boolean(
        string='Partenaire Syndical',
        default=False,
        help="Cocher si ce contact est un partenaire syndical"
    )
    
    is_media = fields.Boolean(
        string='Média',
        default=False,
        help="Cocher si ce contact est un média"
    )
    
    is_autorite = fields.Boolean(
        string='Autorité',
        default=False,
        help="Cocher si ce contact est une autorité (gouvernement, administration)"
    )
    
    # Relations avec les modèles syndicaux
    adherent_syndicat_id = fields.Many2one(
        'syndicat.adherent',
        string='Fiche Adhérent',
        help="Fiche adhérent correspondante"
    )
    
    # Informations employeur
    secteur_activite = fields.Char(
        string='Secteur d\'Activité',
        help="Secteur d'activité de l'employeur"
    )
    
    nb_employes = fields.Integer(
        string='Nombre d\'Employés',
        help="Nombre d'employés de l'entreprise"
    )
    
    convention_collective = fields.Char(
        string='Convention Collective',
        help="Convention collective applicable"
    )
    
    # Informations média
    type_media = fields.Selection([
        ('presse_ecrite', 'Presse Écrite'),
        ('radio', 'Radio'),
        ('television', 'Télévision'),
        ('web', 'Site Web'),
        ('blog', 'Blog'),
        ('reseau_social', 'Réseau Social'),
        ('autre', 'Autre')
    ], string='Type de Média')
    
    # Informations autorité
    type_autorite = fields.Selection([
        ('ministere', 'Ministère'),
        ('prefecture', 'Préfecture'),
        ('mairie', 'Mairie'),
        ('inspection_travail', 'Inspection du Travail'),
        ('tribunal', 'Tribunal'),
        ('police', 'Police'),
        ('autre', 'Autre')
    ], string='Type d\'Autorité')
    
    # Statistiques et relations
    nb_revendications = fields.Integer(
        string='Nombre de Revendications',
        compute='_compute_stats_syndicales',
        store=True,
        help="Nombre de revendications impliquant ce contact"
    )
    
    nb_mediations = fields.Integer(
        string='Nombre de Médiations',
        compute='_compute_stats_syndicales',
        store=True,
        help="Nombre de médiations impliquant ce contact"
    )
    
    nb_communications = fields.Integer(
        string='Nombre de Communications',
        compute='_compute_stats_syndicales',
        store=True,
        help="Nombre de communications envoyées à ce contact"
    )
    
    # Préférences de communication
    prefere_email = fields.Boolean(
        string='Préfère Email',
        default=True,
        help="Préfère recevoir les communications par email"
    )
    
    prefere_sms = fields.Boolean(
        string='Préfère SMS',
        default=False,
        help="Préfère recevoir les communications par SMS"
    )
    
    prefere_courrier = fields.Boolean(
        string='Préfère Courrier',
        default=False,
        help="Préfère recevoir les communications par courrier"
    )
    
    # Historique des interactions
    derniere_interaction = fields.Date(
        string='Dernière Interaction',
        compute='_compute_derniere_interaction',
        store=True,
        help="Date de la dernière interaction avec ce contact"
    )
    
    type_derniere_interaction = fields.Char(
        string='Type Dernière Interaction',
        compute='_compute_derniere_interaction',
        store=True,
        help="Type de la dernière interaction"
    )
    
    # Notes spécifiques
    notes_syndicales = fields.Text(
        string='Notes Syndicales',
        help="Notes spécifiques aux activités syndicales"
    )

    @api.depends('is_employeur')
    def _compute_stats_syndicales(self):
        for record in self:
            if record.is_employeur:
                # Compter les revendications contre cet employeur
                record.nb_revendications = self.env['syndicat.revendication'].search_count([
                    ('employeur_concerne', 'ilike', record.name)
                ])
                
                # Compter les médiations impliquant cet employeur
                record.nb_mediations = self.env['syndicat.mediation'].search_count([
                    ('employeur_concerne', 'ilike', record.name)
                ])
            else:
                record.nb_revendications = 0
                record.nb_mediations = 0
            
            # Communications (pour tous les types de contacts)
            record.nb_communications = self.env['syndicat.communication'].search_count([
                ('destinataires_externes', 'ilike', record.email)
            ]) if record.email else 0

    @api.depends('is_employeur', 'is_adherent_syndicat')
    def _compute_derniere_interaction(self):
        for record in self:
            interactions = []
            
            if record.is_employeur:
                # Dernière revendication
                derniere_revendication = self.env['syndicat.revendication'].search([
                    ('employeur_concerne', 'ilike', record.name)
                ], limit=1, order='date_creation desc')
                
                if derniere_revendication:
                    interactions.append({
                        'date': derniere_revendication.date_creation,
                        'type': 'Revendication'
                    })
                
                # Dernière médiation
                derniere_mediation = self.env['syndicat.mediation'].search([
                    ('employeur_concerne', 'ilike', record.name)
                ], limit=1, order='date_creation desc')
                
                if derniere_mediation:
                    interactions.append({
                        'date': derniere_mediation.date_creation,
                        'type': 'Médiation'
                    })
            
            if record.is_adherent_syndicat and record.adherent_syndicat_id:
                # Dernière assemblée
                derniere_assemblee = record.adherent_syndicat_id.assemblee_ids.sorted('date_debut', reverse=True)
                if derniere_assemblee:
                    interactions.append({
                        'date': derniere_assemblee[0].date_debut.date(),
                        'type': 'Assemblée'
                    })
                
                # Dernière action
                derniere_action = record.adherent_syndicat_id.action_ids.sorted('date_debut', reverse=True)
                if derniere_action:
                    interactions.append({
                        'date': derniere_action[0].date_debut.date(),
                        'type': 'Action'
                    })
            
            # Dernière communication
            if record.email:
                derniere_communication = self.env['syndicat.communication'].search([
                    ('destinataires_externes', 'ilike', record.email),
                    ('statut', '=', 'publiee')
                ], limit=1, order='date_publication desc')
                
                if derniere_communication:
                    interactions.append({
                        'date': derniere_communication.date_publication.date(),
                        'type': 'Communication'
                    })
            
            # Trouver la plus récente
            if interactions:
                derniere = max(interactions, key=lambda x: x['date'])
                record.derniere_interaction = derniere['date']
                record.type_derniere_interaction = derniere['type']
            else:
                record.derniere_interaction = False
                record.type_derniere_interaction = False

    @api.onchange('is_adherent_syndicat')
    def _onchange_is_adherent_syndicat(self):
        if self.is_adherent_syndicat and not self.adherent_syndicat_id:
            # Chercher une fiche adhérent existante avec le même email
            if self.email:
                adherent = self.env['syndicat.adherent'].search([
                    ('email', '=', self.email)
                ], limit=1)
                if adherent:
                    self.adherent_syndicat_id = adherent.id
        elif not self.is_adherent_syndicat:
            self.adherent_syndicat_id = False

    def action_creer_fiche_adherent(self):
        """Crée une fiche adhérent pour ce contact"""
        self.ensure_one()
        if not self.adherent_syndicat_id:
            # Séparer le nom en prénom et nom de famille
            name_parts = self.name.split(' ', 1)
            prenom = name_parts[0] if name_parts else ''
            nom_famille = name_parts[1] if len(name_parts) > 1 else ''
            
            adherent = self.env['syndicat.adherent'].create({
                'prenom': prenom,
                'nom_famille': nom_famille,
                'email': self.email,
                'telephone': self.phone,
                'adresse': f"{self.street or ''} {self.street2 or ''}".strip(),
                'ville': self.city,
                'employeur': self.parent_id.name if self.parent_id else 'Non spécifié',
                'poste_occupe': self.function or 'Non spécifié',
            })
            
            self.write({
                'adherent_syndicat_id': adherent.id,
                'is_adherent_syndicat': True
            })
            
            return {
                'type': 'ir.actions.act_window',
                'name': 'Fiche Adhérent',
                'res_model': 'syndicat.adherent',
                'res_id': adherent.id,
                'view_mode': 'form',
                'target': 'current',
            }

    def action_voir_fiche_adherent(self):
        """Ouvre la fiche adhérent correspondante"""
        self.ensure_one()
        if self.adherent_syndicat_id:
            return {
                'type': 'ir.actions.act_window',
                'name': 'Fiche Adhérent',
                'res_model': 'syndicat.adherent',
                'res_id': self.adherent_syndicat_id.id,
                'view_mode': 'form',
                'target': 'current',
            }

    def action_voir_revendications(self):
        """Affiche les revendications liées à ce contact"""
        self.ensure_one()
        domain = []
        if self.is_employeur:
            domain = [('employeur_concerne', 'ilike', self.name)]
        elif self.is_adherent_syndicat and self.adherent_syndicat_id:
            domain = [('initiateur_id', '=', self.adherent_syndicat_id.id)]
        
        return {
            'type': 'ir.actions.act_window',
            'name': 'Revendications',
            'res_model': 'syndicat.revendication',
            'view_mode': 'tree,form',
            'domain': domain,
            'target': 'current',
        }

    def action_voir_mediations(self):
        """Affiche les médiations liées à ce contact"""
        self.ensure_one()
        domain = []
        if self.is_employeur:
            domain = [('employeur_concerne', 'ilike', self.name)]
        elif self.is_adherent_syndicat and self.adherent_syndicat_id:
            domain = [('demandeur_id', '=', self.adherent_syndicat_id.id)]
        
        return {
            'type': 'ir.actions.act_window',
            'name': 'Médiations',
            'res_model': 'syndicat.mediation',
            'view_mode': 'tree,form',
            'domain': domain,
            'target': 'current',
        }

    def action_envoyer_communication(self):
        """Crée une nouvelle communication pour ce contact"""
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': 'Nouvelle Communication',
            'res_model': 'syndicat.communication',
            'view_mode': 'form',
            'target': 'new',
            'context': {
                'default_destinataires_externes': self.email,
                'default_canal_diffusion': 'public' if not self.is_adherent_syndicat else 'interne',
            }
        }

    @api.model
    def get_contacts_par_type(self):
        """Retourne la répartition des contacts par type"""
        return {
            'adherents': self.search_count([('is_adherent_syndicat', '=', True)]),
            'employeurs': self.search_count([('is_employeur', '=', True)]),
            'partenaires': self.search_count([('is_partenaire_syndical', '=', True)]),
            'medias': self.search_count([('is_media', '=', True)]),
            'autorites': self.search_count([('is_autorite', '=', True)]),
        }

    @api.model
    def get_employeurs_principaux(self, limit=10):
        """Retourne les employeurs avec le plus de revendications"""
        employeurs = self.search([('is_employeur', '=', True)])
        employeurs_stats = []
        
        for employeur in employeurs:
            nb_revendications = self.env['syndicat.revendication'].search_count([
                ('employeur_concerne', 'ilike', employeur.name)
            ])
            if nb_revendications > 0:
                employeurs_stats.append({
                    'id': employeur.id,
                    'name': employeur.name,
                    'nb_revendications': nb_revendications,
                    'nb_employes': employeur.nb_employes,
                    'secteur': employeur.secteur_activite,
                })
        
        # Trier par nombre de revendications
        employeurs_stats.sort(key=lambda x: x['nb_revendications'], reverse=True)
        return employeurs_stats[:limit]