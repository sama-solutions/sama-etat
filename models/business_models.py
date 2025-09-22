from odoo import models, fields, api
from odoo.exceptions import ValidationError

class GovernmentProject(models.Model):
    _name = 'government.project'
    _description = 'Projet Gouvernemental - Plan Sénégal 2050'
    _inherit = ['mail.thread', 'mail.activity.mixin']  # AI mixin completely disabled - testing if file itself is the issue
    _order = 'project_code desc'
    
    @api.model
    def _valid_field_parameter(self, field, name):
        # Allow 'states' parameter for fields that need it
        return name == 'states' or super()._valid_field_parameter(field, name)

    # Numérotation automatique Plan Sénégal 2050
    project_code = fields.Char(
        string="Code Projet SN-2050", 
        required=True, 
        copy=False, 
        readonly=True, 
        default=lambda self: self._get_next_project_code()
    )
    
    # === IDENTIFICATION DU PROJET ===
    name = fields.Char(string="Nom du Projet", required=True, readonly=True, states={'draft': [('readonly', False)]})
    code_unique = fields.Char(string="Code d'Identification Unique", compute='_compute_code_unique', store=True, readonly=True)
    description_succincte = fields.Html(string="Description Succincte")
    description = fields.Html(string="Description Détaillée")
    objectifs_generaux = fields.Html(string="Objectifs Généraux")
    objectifs_specifiques = fields.Html(string="Objectifs Spécifiques")
    localisation_geographique = fields.Char(string="Localisation Géographique", readonly=True, states={'draft': [('readonly', False)]})
    secteur_intervention = fields.Selection([
        ('agriculture', 'Agriculture et Développement Rural'),
        ('education', 'Éducation et Formation'),
        ('sante', 'Santé et Action Sociale'),
        ('infrastructure', 'Infrastructures et Transport'),
        ('energie', 'Énergie et Mines'),
        ('environnement', 'Environnement et Développement Durable'),
        ('gouvernance', 'Gouvernance et Institutions'),
        ('economie', 'Économie et Finances'),
        ('culture', 'Culture et Communication'),
        ('jeunesse', 'Jeunesse et Sports'),
        ('autre', 'Autre')
    ], string="Secteur d'Intervention", readonly=True, states={'draft': [('readonly', False)]})
    duree_previsionnelle = fields.Integer(string="Durée Prévisionnelle (mois)", readonly=True, states={'draft': [('readonly', False)]})
    start_date = fields.Date(string="Date de Début Prévisionnelle", readonly=True, states={'draft': [('readonly', False)]})
    end_date = fields.Date(string="Date de Fin Prévisionnelle", readonly=True, states={'draft': [('readonly', False)]})
    
    # Statut aligné sur Plan Sénégal 2050
    status = fields.Selection([
        ('draft', 'Brouillon'),
        ('validated', 'Validé'),
        ('in_progress', 'En Cours'),
        ('suspended', 'Suspendu'),
        ('completed', 'Achevé'),
        ('cancelled', 'Annulé')
    ], string="Statut", default='draft', tracking=True)
    
    state = fields.Selection([('draft', 'Brouillon'), ('locked', 'Verrouillé')], string="État", default='locked', readonly=True, copy=False)

    def action_set_to_draft(self):
        self.write({'state': 'draft'})

    def action_set_to_locked(self):
        self.write({'state': 'locked'})
    
    # === CADRE INSTITUTIONNEL ===
    strategic_objective_id = fields.Many2one('strategic.objective', string="Objectif Stratégique", required=True)
    maitre_ouvrage_id = fields.Many2one('res.partner', string="Maître d'Ouvrage")
    maitre_ouvrage_delegue_id = fields.Many2one('res.partner', string="Maître d'Ouvrage Délégué")
    ministry_id = fields.Many2one('government.ministry', string="Ministère Responsable")
    manager_id = fields.Many2one('res.users', string="Chef de Projet")
    entites_partenaires_ids = fields.Many2many('res.partner', string="Entités Partenaires")
    structures_coordination = fields.Text(string="Structures de Coordination")
    roles_responsabilites = fields.Text(string="Rôles et Responsabilités")
    
    # === BUDGET & FINANCEMENT ===
    budget_id = fields.Many2one('government.budget', string="Budget Alloué")
    cout_total_projet = fields.Monetary(string="Coût Total du Projet", currency_field='currency_id', readonly=True, states={'draft': [('readonly', False)]})
    currency_id = fields.Many2one('res.currency', string='Devise', default=lambda self: self._get_default_currency(), readonly=True, states={'draft': [('readonly', False)]})
    modalites_gestion_financiere = fields.Text(string="Modalités de Gestion Financière", readonly=True, states={'draft': [('readonly', False)]})
    ligne_budgetaire_rattachement = fields.Char(string="Ligne Budgétaire de Rattachement", readonly=True, states={'draft': [('readonly', False)]})
    
    # === TRANSPARENCE & CONFORMITÉ ===
    obligations_publication_info = fields.Text(string="Obligations de Publication d'Informations")
    mecanismes_redevabilite = fields.Text(string="Mécanismes de Redevabilité")
    dispositifs_anti_corruption = fields.Text(string="Dispositifs Anti-Corruption")
    conformite_audits = fields.Text(string="Conformité aux Audits (Cour des Comptes/IGE)")
    standards_ptf = fields.Text(string="Standards des Partenaires Techniques et Financiers")
    
    # Connexion avec le module projet d'Odoo
    odoo_project_id = fields.Many2one(
        'project.project', 
        string="Projet Odoo Associé",
        help="Projet Odoo créé automatiquement pour la gestion opérationnelle"
    )
    
    # Priorité selon Plan Sénégal 2050
    priority = fields.Selection([
        ('0', 'Normale'),
        ('1', 'Importante'),
        ('2', 'Urgente'),
        ('3', 'Critique')
    ], string="Priorité", default='0')

    # === RELATIONS ONE2MANY === (temporairement désactivées)
    # Budget & Financement
    # ventilation_cout_composantes_ids = fields.One2many('project.cost.breakdown', 'project_id', string="Ventilation du Coût par Composante")
    # sources_financement_ids = fields.One2many('project.funding.source', 'project_id', string="Sources de Financement")
    # plan_decaissement_ids = fields.One2many('project.disbursement.plan', 'project_id', string="Plan de Décaissement")
    
    # Cadre Juridique
    # textes_legislatifs_specifiques_ids = fields.One2many('project.legal.text', 'project_id', string="Textes Législatifs Spécifiques")
    # conventions_accords_ids = fields.One2many('project.agreement', 'project_id', string="Conventions et Accords")
    
    # Marchés Publics
    # public_tenders_ids = fields.One2many('project.public.tender', 'project_id', string="Marchés Publics Associés")
    
    # Suivi-Évaluation
    # kpis_ids = fields.One2many('project.kpi', 'project_id', string="Indicateurs de Performance")
    # evaluation_plans_ids = fields.One2many('project.evaluation.plan', 'project_id', string="Plans d'Évaluation")
    
    # Risques & Environnement
    # risks_ids = fields.One2many('project.risk', 'project_id', string="Risques Identifiés")
    # pges_documents_ids = fields.One2many('project.pges', 'project_id', string="Documents PGES")
    
    # Geolocation
    latitude = fields.Float(string='Latitude', digits=(10, 7))
    longitude = fields.Float(string='Longitude', digits=(10, 7))
    
    # Informations sur l'avancement
    progress = fields.Float(string="Pourcentage d'avancement", compute='_compute_progress', store=True)
    task_count = fields.Integer(string="Nombre de tâches", compute='_compute_task_count')
    
    @api.model
    def _get_next_project_code(self):
        """Génère le prochain code de projet au format SN-2050-XXXXX"""
        # Rechercher le dernier numéro utilisé
        last_project = self.search([], order='id desc', limit=1)
        if last_project and last_project.project_code:
            try:
                # Extraire le numéro depuis le code existant
                code_parts = last_project.project_code.split('-')
                if len(code_parts) == 3 and code_parts[0] == 'SN' and code_parts[1] == '2050':
                    last_number = int(code_parts[2])
                    next_number = last_number + 1
                else:
                    next_number = 1
            except (ValueError, IndexError):
                next_number = 1
        else:
            next_number = 1
        
        return f"SN-2050-{next_number:05d}"
    
    @api.depends('project_code', 'name')
    def _compute_code_unique(self):
        """Génère un code unique basé sur le code projet et le nom"""
        for record in self:
            if record.project_code and record.name:
                # Créer un code unique en combinant le code projet et les premières lettres du nom
                name_code = ''.join([word[0].upper() for word in record.name.split()[:3] if word])
                record.code_unique = f"{record.project_code}-{name_code}"
            else:
                record.code_unique = record.project_code or ''
    
    def _get_default_currency(self):
        """Retourne la devise CFA (XOF) par défaut"""
        xof_currency = self.env['res.currency'].search([('name', '=', 'XOF')], limit=1)
        if xof_currency:
            return xof_currency.id
        # Fallback vers la devise de la société
        return self.env.company.currency_id.id
    
    @api.depends('odoo_project_id.tasks')
    def _compute_task_count(self):
        """Calcule le nombre de tâches du projet Odoo associé"""
        for record in self:
            if record.odoo_project_id:
                record.task_count = len(record.odoo_project_id.tasks)
            else:
                record.task_count = 0
    
    @api.depends('odoo_project_id.tasks.stage_id')
    def _compute_progress(self):
        """Calcule le pourcentage d'avancement basé sur les tâches Odoo"""
        for record in self:
            if record.odoo_project_id and record.odoo_project_id.tasks:
                total_tasks = len(record.odoo_project_id.tasks)
                # Dans Odoo 18, utiliser fold pour identifier les étapes fermées
                completed_tasks = len(record.odoo_project_id.tasks.filtered(lambda t: t.stage_id and t.stage_id.fold))
                record.progress = (completed_tasks / total_tasks) * 100 if total_tasks > 0 else 0.0
            else:
                record.progress = 0.0
    
    @api.model_create_multi
    def create(self, vals_list):
        """
        Surcharge de la création pour gérer la création par lots et générer automatiquement les codes projet
        """
        # S'assurer que nous avons une liste de dictionnaires
        if not isinstance(vals_list, list):
            vals_list = [vals_list]
            
        # Générer les codes projet pour chaque enregistrement
        for vals in vals_list:
            if not vals.get('project_code'):
                # Utiliser une nouvelle méthode pour générer un code unique par lot
                vals['project_code'] = self._get_next_project_code()
                
        # Appeler le create du parent avec la liste des valeurs
        projects = super(GovernmentProject, self).create(vals_list)
        
        # Si un seul enregistrement, retourner directement l'objet
        if len(projects) == 1:
            return projects[0]
        return projects
    
    def create_odoo_project(self):
        """Crée un projet Odoo associé pour la gestion opérationnelle"""
        for record in self:
            if not record.odoo_project_id:
                project_vals = {
                    'name': f"[{record.project_code}] {record.name}",
                    'description': record.description,
                    'date_start': record.start_date,
                    'date': record.end_date,
                    'user_id': record.manager_id.id if record.manager_id else False,
                    'privacy_visibility': 'employees',  # Visible aux employés
                    'active': True,
                }
                
                odoo_project = self.env['project.project'].create(project_vals)
                record.odoo_project_id = odoo_project.id
                
        return {
            'type': 'ir.actions.act_window',
            'name': 'Projet Odoo Créé',
            'res_model': 'project.project',
            'res_id': self.odoo_project_id.id,
            'view_mode': 'form',
            'target': 'current',
        }
    
    def sync_with_odoo_project(self):
        """Synchronise les données avec le projet Odoo associé"""
        for record in self:
            if record.odoo_project_id:
                # Synchroniser les informations de base
                record.odoo_project_id.write({
                    'name': f"[{record.project_code}] {record.name}",
                    'description': record.description,
                    'date_start': record.start_date,
                    'date': record.end_date,
                    'user_id': record.manager_id.id if record.manager_id else False,
                })
    
    def action_validate(self):
        """Valide le projet et crée automatiquement le projet Odoo associé"""
        for record in self:
            record.status = 'validated'
            if not record.odoo_project_id:
                record.create_odoo_project()
    
    def action_start(self):
        """Démarre le projet"""
        for record in self:
            record.status = 'in_progress'
            record.sync_with_odoo_project()
    
    def action_suspend(self):
        """Suspend le projet"""
        for record in self:
            record.status = 'suspended'
    
    def action_complete(self):
        """Marque le projet comme achevé"""
        for record in self:
            record.status = 'completed'
    
    def action_cancel(self):
        """Annule le projet"""
        for record in self:
            record.status = 'cancelled'
    
    def action_reset_to_draft(self):
        """Remet le projet en brouillon"""
        for record in self:
            record.status = 'draft'

    @api.model
    def action_validate_by_xmlid(self, xml_id):
        """Valide un projet par son XML ID"""
        project = self.env.ref(xml_id)
        if project:
            project.action_validate()
        else:
            raise ValidationError(f"Projet avec XML ID {xml_id} non trouvé.")

    def action_open_odoo_project(self):
        """Ouvre le projet Odoo associé"""
        self.ensure_one()
        if not self.odoo_project_id:
            raise ValidationError("Aucun projet Odoo associé. Veuillez d'abord valider le projet.")
        
        return {
            'type': 'ir.actions.act_window',
            'name': f'Projet Odoo - {self.project_code}',
            'res_model': 'project.project',
            'res_id': self.odoo_project_id.id,
            'view_mode': 'form',
            'target': 'current',
        }
    
    def action_open_odoo_tasks(self):
        """Ouvre les tâches du projet Odoo associé"""
        self.ensure_one()
        if not self.odoo_project_id:
            raise ValidationError("Aucun projet Odoo associé. Veuillez d'abord valider le projet.")
        
        return {
            'type': 'ir.actions.act_window',
            'name': f'Tâches - {self.project_code}',
            'res_model': 'project.task',
            'view_mode': 'list,form,kanban',
            'views': [(self.env.ref('project.view_task_tree2').id, 'list'),
                      (self.env.ref('project.view_task_form2').id, 'form'),
                      (self.env.ref('project.view_task_kanban').id, 'kanban')],
            'domain': [('project_id', '=', self.odoo_project_id.id)],
            'context': {
                'default_project_id': self.odoo_project_id.id,
                'search_default_project_id': self.odoo_project_id.id,
            },
            'target': 'current',
        }
    
    def get_public_url(self):
        """Retourne l'URL publique du projet"""
        base_url = self.env['ir.config_parameter'].sudo().get_param('web.base.url')
        return f"{base_url}/senegal2050/project/{self.id}"
    
    def get_qr_code_url(self):
        """Retourne l'URL pour générer le QR code du projet"""
        base_url = self.env['ir.config_parameter'].sudo().get_param('web.base.url')
        return f"{base_url}/senegal2050/qr/government.project/{self.id}"
    
    def action_share_public(self):
        """Action pour partager publiquement le projet"""
        self.ensure_one()
        public_url = self.get_public_url()
        return {
            'type': 'ir.actions.act_url',
            'url': public_url,
            'target': 'new',
        }
    
    def get_ai_suggestions(self):
        """Ouvre l'assistant IA pour générer du contenu"""
        self.ensure_one()
        field_name = self.env.context.get('field_name', 'description')
        
        # Construire le contexte pour l'IA
        context_data = {
            'nom_projet': self.name or '',
            'secteur': dict(self._fields['secteur_intervention'].selection).get(self.secteur_intervention, '') if self.secteur_intervention else '',
            'budget': f"{self.cout_total_projet:,.0f} FCFA" if self.cout_total_projet else '',
            'duree': f"{self.duree_previsionnelle} mois" if self.duree_previsionnelle else '',
            'ministere': self.ministry_id.name if self.ministry_id else '',
            'objectif_strategique': self.strategic_objective_id.name if self.strategic_objective_id else ''
        }
        
        return {
            'type': 'ir.actions.act_window',
            'name': f'Assistant IA - {self._fields[field_name].string}',
            'res_model': 'ai.content.helper',
            'view_mode': 'form',
            'target': 'new',
            'context': {
                'default_model_id': self.env['ai.model.config'].search([
                    ('is_default', '=', True),
                    ('active', '=', True)
                ], limit=1).id,
                'default_content_type': self._get_content_type_for_field(field_name),
                'default_project_context': self._build_context_for_ai(context_data),
                'field_name': field_name,
                'source_model': self._name,
                'source_id': self.id,
            }
        }
    
    def _get_content_type_for_field(self, field_name):
        """
        Mappe les noms de champs aux types de contenu IA
        """
        field_mapping = {
            'description_succincte': 'description',
            'objectifs_generaux': 'objectives_general',
            'objectifs_specifiques': 'objectives_specific',
            'structures_coordination': 'coordination',
            'mecanismes_redevabilite': 'accountability',
            'dispositifs_anti_corruption': 'anticorruption',
            'description': 'description',
            'summary': 'description',
            'objectives': 'objectives_general',
            'coordination_structure': 'coordination',
            'accountability_mechanisms': 'accountability',
            'anti_corruption_measures': 'anticorruption',
        }
        return field_mapping.get(field_name, 'custom')
    
    def _build_context_for_ai(self, context_data):
        """
        Construit le contexte pour l'IA basé sur les données du modèle
        """
        try:
            context_parts = []
            
            # Ajouter le nom/titre si disponible
            if hasattr(self, 'name') and getattr(self, 'name', None):
                context_parts.append(f"Nom: {self.name}")
            
            # Ajouter des informations spécifiques au modèle
            if hasattr(self, 'secteur_intervention') and getattr(self, 'secteur_intervention', None):
                context_parts.append(f"Secteur: {self.secteur_intervention}")
            
            if hasattr(self, 'cout_total_projet') and getattr(self, 'cout_total_projet', None):
                context_parts.append(f"Budget: {self.cout_total_projet}")
            
            if hasattr(self, 'duree_previsionnelle') and getattr(self, 'duree_previsionnelle', None):
                context_parts.append(f"Durée: {self.duree_previsionnelle} mois")
            
            # Ajouter le contexte fourni
            if context_data and isinstance(context_data, dict):
                for key, value in context_data.items():
                    if value:
                        context_parts.append(f"{key}: {value}")
            
            return "\n".join(context_parts)
        except Exception as e:
            return ""


class GovernmentDecision(models.Model):
    _name = 'government.decision'
    _description = 'Décision Officielle'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    
    @api.model
    def _valid_field_parameter(self, field, name):
        # Allow 'states' parameter for fields that need it
        return name == 'states' or super()._valid_field_parameter(field, name)  # , 'ai.widget.mixin']  # Testing: AI mixin disabled

    name = fields.Char(string="Nom", compute='_compute_name', store=True)
    title = fields.Char(string="Titre", required=True, tracking=True, readonly=True, states={'draft': [('readonly', False)]})
    reference = fields.Char(string="Référence", readonly=True, states={'draft': [('readonly', False)]})
    decision_type = fields.Selection([
        ('decree', 'Décret'),
        ('order', 'Arrêté'),
        ('circular', 'Circulaire'),
        ('instruction', 'Instruction'),
        ('other', 'Autre')
    ], string="Type de Décision", default='decree', readonly=True, states={'draft': [('readonly', False)]})
    decision_date = fields.Date(string="Date de la Décision", tracking=True, readonly=True, states={'draft': [('readonly', False)]})
    document = fields.Binary(string="Document", readonly=True, states={'draft': [('readonly', False)]})
    document_name = fields.Char(string="Nom du Document", readonly=True, states={'draft': [('readonly', False)]})
    description = fields.Html(string="Description", readonly=True, states={'draft': [('readonly', False)]})
    status = fields.Selection([
        ('draft', 'Brouillon'),
        ('published', 'Publiée'),
        ('archived', 'Archivée')
    ], string="Statut", default='draft', tracking=True)
    state = fields.Selection([('draft', 'Brouillon'), ('locked', 'Verrouillé')], string="État", default='locked', readonly=True, copy=False)
    strategic_objective_id = fields.Many2one('strategic.objective', string="Objectif Stratégique", required=True, readonly=True, states={'draft': [('readonly', False)]})
    project_id = fields.Many2one('government.project', string="Projet Associé", readonly=True, states={'draft': [('readonly', False)]})
    event_id = fields.Many2one('government.event', string="Événement Associé", readonly=True, states={'draft': [('readonly', False)]})
    ministry_id = fields.Many2one('government.ministry', string="Ministère Émetteur", readonly=True, states={'draft': [('readonly', False)]})
    is_public = fields.Boolean(string="Public", default=False, readonly=True, states={'draft': [('readonly', False)]})
    
    # Système de suivi des décisions
    implementation_status = fields.Selection([
        ('not_started', 'Non Commencée'),
        ('in_progress', 'En Cours'),
        ('partially_completed', 'Partiellement Réalisée'),
        ('completed', 'Réalisée'),
        ('delayed', 'Retardée'),
        ('blocked', 'Bloquée')
    ], string="État de Mise en Œuvre", default='not_started', tracking=True, readonly=True, states={'draft': [('readonly', False)]})
    
    implementation_deadline = fields.Date(string="Échéance de Mise en Œuvre", tracking=True, readonly=True, states={'draft': [('readonly', False)]})
    responsible_user_id = fields.Many2one('res.users', string="Responsable de Suivi", readonly=True, states={'draft': [('readonly', False)]})
    progress_percentage = fields.Float(string="Pourcentage d'Avancement", default=0.0, help="Pourcentage d'avancement de la mise en œuvre", readonly=True, states={'draft': [('readonly', False)]})
    
    # Champs pour les rapports de suivi
    last_follow_up_date = fields.Date(string="Dernière Date de Suivi", readonly=True, states={'draft': [('readonly', False)]})
    next_follow_up_date = fields.Date(string="Prochaine Date de Suivi", readonly=True, states={'draft': [('readonly', False)]})
    follow_up_notes = fields.Text(string="Notes de Suivi", readonly=True, states={'draft': [('readonly', False)]})
    
    # Indicateurs de performance
    is_on_track = fields.Boolean(string="Dans les Temps", compute='_compute_is_on_track', store=True)
    days_until_deadline = fields.Integer(string="Jours Avant Échéance", compute='_compute_days_until_deadline', store=True)

    # Geolocation
    latitude = fields.Float(string='Latitude', digits=(10, 7), readonly=True, states={'draft': [('readonly', False)]})
    longitude = fields.Float(string='Longitude', digits=(10, 7), readonly=True, states={'draft': [('readonly', False)]})

    def action_set_to_draft(self):
        self.write({'state': 'draft'})

    def action_set_to_locked(self):
        self.write({'state': 'locked'})
    
    @api.depends('implementation_deadline', 'implementation_status')
    def _compute_is_on_track(self):
        from datetime import date
        for record in self:
            if record.implementation_deadline and record.implementation_status not in ['completed', 'blocked']:
                days_left = (record.implementation_deadline - date.today()).days
                # Considérer comme "dans les temps" si plus de 30 jours restants ou déjà terminé
                record.is_on_track = days_left > 30 or record.implementation_status == 'completed'
            else:
                record.is_on_track = record.implementation_status == 'completed'
    
    @api.depends('implementation_deadline')
    def _compute_days_until_deadline(self):
        from datetime import date
        for record in self:
            if record.implementation_deadline:
                record.days_until_deadline = (record.implementation_deadline - date.today()).days
            else:
                record.days_until_deadline = 0
    
    def action_start_implementation(self):
        """Démarre la mise en œuvre de la décision"""
        for record in self:
            record.implementation_status = 'in_progress'
            record.last_follow_up_date = fields.Date.today()
    
    def action_complete_implementation(self):
        """Marque la décision comme complètement mise en œuvre"""
        for record in self:
            record.implementation_status = 'completed'
            record.progress_percentage = 100.0
            record.last_follow_up_date = fields.Date.today()
    
    def action_mark_delayed(self):
        """Marque la décision comme retardée"""
        for record in self:
            record.implementation_status = 'delayed'
            record.last_follow_up_date = fields.Date.today()
    
    def action_mark_blocked(self):
        """Marque la décision comme bloquée"""
        for record in self:
            record.implementation_status = 'blocked'
            record.last_follow_up_date = fields.Date.today()
    
    def action_create_follow_up_task(self):
        """Crée une tâche de suivi dans Odoo"""
        self.ensure_one()
        task_vals = {
            'name': f"Suivi Décision: {self.title}",
            'description': f"Suivi de la mise en œuvre de la décision {self.reference}\n\nDécision: {self.title}\nÉchéance: {self.implementation_deadline}\nStatut actuel: {dict(self._fields['implementation_status'].selection)[self.implementation_status]}",
            'user_ids': [(6, 0, [self.responsible_user_id.id])] if self.responsible_user_id else [],
            'date_deadline': self.next_follow_up_date or self.implementation_deadline,
            'project_id': self.project_id.odoo_project_id.id if self.project_id and self.project_id.odoo_project_id else False,
        }
        
        task = self.env['project.task'].create(task_vals)
        
        return {
            'type': 'ir.actions.act_window',
            'name': 'Tâche de Suivi Créée',
            'res_model': 'project.task',
            'res_id': task.id,
            'view_mode': 'form',
            'target': 'current',
        }
    
    @api.depends('title', 'reference')
    def _compute_name(self):
        for record in self:
            if record.reference and record.title:
                record.name = f"[{record.reference}] {record.title}"
            else:
                record.name = record.title or record.reference or "Nouvelle décision"

class GovernmentEvent(models.Model):
    _name = 'government.event'
    _description = 'Événement Public'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    
    @api.model
    def _valid_field_parameter(self, field, name):
        # Allow 'states' parameter for fields that need it
        return name == 'states' or super()._valid_field_parameter(field, name)  # , 'ai.widget.mixin']  # Testing: AI mixin disabled

    # Geolocation
    latitude = fields.Float(string='Latitude', digits=(10, 7), readonly=True, states={'draft': [('readonly', False)]})
    longitude = fields.Float(string='Longitude', digits=(10, 7), readonly=True, states={'draft': [('readonly', False)]})

    name = fields.Char(string="Nom de l'Événement", required=True, tracking=True, readonly=True, states={'draft': [('readonly', False)]})
    event_date = fields.Date(string="Date de l'Événement", tracking=True, readonly=True, states={'draft': [('readonly', False)]})
    date_start = fields.Datetime(string="Date et Heure de Début", readonly=True, states={'draft': [('readonly', False)]})
    date_end = fields.Datetime(string="Date et Heure de Fin", readonly=True, states={'draft': [('readonly', False)]})
    location = fields.Char(string="Lieu", tracking=True, readonly=True, states={'draft': [('readonly', False)]})
    organizer_id = fields.Many2one('government.ministry', string="Organisateur", tracking=True, readonly=True, states={'draft': [('readonly', False)]})
    event_type = fields.Selection([
        ('meeting', 'Réunion'),
        ('conference', 'Conférence'),
        ('workshop', 'Atelier'),
        ('ceremony', 'Cérémonie'),
        ('launch', 'Lancement'),
        ('other', 'Autre')
    ], string="Type d'Événement", default='meeting', readonly=True, states={'draft': [('readonly', False)]})
    description = fields.Html(string="Description", readonly=True, states={'draft': [('readonly', False)]})
    project_id = fields.Many2one('government.project', string="Projet Associé", readonly=True, states={'draft': [('readonly', False)]})
    strategic_objective_id = fields.Many2one('strategic.objective', string="Objectif Stratégique", required=True, readonly=True, states={'draft': [('readonly', False)]})
    status = fields.Selection([
        ('draft', 'Brouillon'),
        ('planned', 'Planifié'),
        ('validated', 'Validé'),
        ('ongoing', 'En cours'),
        ('completed', 'Terminé'),
        ('cancelled', 'Annulé')
    ], string="Statut", default='draft', tracking=True)
    state = fields.Selection([('draft', 'Brouillon'), ('locked', 'Verrouillé')], string="État", default='draft', readonly=True, copy=False)
    
    # Liaison avec les événements Odoo (module calendar)
    odoo_event_id = fields.Many2one(
        'calendar.event', 
        string="Événement Odoo Associé",
        help="Événement Odoo créé automatiquement pour la gestion du calendrier"
    )

    def action_set_to_draft(self):
        """Remet l'événement en brouillon pour modification"""
        for record in self:
            record.write({
                'state': 'draft',
                'status': 'draft'
            })

    def action_set_to_locked(self):
        """Verrouille l'événement après modification"""
        self.write({'state': 'locked'})
    
    def action_start(self):
        """Démarre l'événement (passe en cours)"""
        for record in self:
            if record.status == 'validated':
                record.status = 'ongoing'
    
    def action_complete(self):
        """Marque l'événement comme terminé"""
        for record in self:
            if record.status == 'ongoing':
                record.status = 'completed'
    
    def create_odoo_event(self):
        """Crée un événement Odoo associé pour la gestion calendaire"""
        for record in self:
            if not record.odoo_event_id:
                event_vals = {
                    'name': record.name,
                    'description': record.description,
                    'start': record.date_start,
                    'stop': record.date_end,
                    'location': record.location,
                    'privacy': 'public',  # Événement public
                    'show_as': 'busy',
                }
                
                odoo_event = self.env['calendar.event'].create(event_vals)
                record.odoo_event_id = odoo_event.id
                
        return {
            'type': 'ir.actions.act_window',
            'name': 'Événement Odoo Créé',
            'res_model': 'calendar.event',
            'res_id': self.odoo_event_id.id,
            'view_mode': 'form',
            'target': 'current',
        }
    
    def action_validate(self):
        """Valide l'événement et crée automatiquement l'événement Odoo associé"""
        for record in self:
            if record.status == 'draft':
                record.status = 'validated'
                if not record.odoo_event_id:
                    record.create_odoo_event()
    
    def action_open_public_profile(self):
        """Ouvre la page publique de l'événement"""
        self.ensure_one()
        base_url = self.env['ir.config_parameter'].sudo().get_param('web.base.url')
        return {
            'type': 'ir.actions.act_url',
            'url': f'{base_url}/senegal2050/event/{self.id}',
            'target': 'new',
        }
    
    def action_open_odoo_event(self):
        """Ouvre l'événement Odoo associé dans le calendrier"""
        self.ensure_one()
        if not self.odoo_event_id:
            raise ValidationError("Aucun événement Odoo associé. Veuillez d'abord valider l'événement.")
        
        return {
            'type': 'ir.actions.act_window',
            'name': f'Événement Odoo - {self.name}',
            'res_model': 'calendar.event',
            'res_id': self.odoo_event_id.id,
            'view_mode': 'form',
            'target': 'current',
        }
    
    def sync_with_odoo_event(self):
        """Synchronise les données avec l'événement Odoo associé"""
        for record in self:
            if record.odoo_event_id:
                # Synchroniser les informations de base
                record.odoo_event_id.write({
                    'name': record.name,
                    'description': record.description,
                    'start': record.date_start,
                    'stop': record.date_end,
                    'location': record.location,
                })

class GovernmentBudget(models.Model):
    _name = 'government.budget'
    _description = "Budget d'Investissement/Fonctionnement"
    _inherit = ['mail.thread', 'mail.activity.mixin']  # , 'ai.widget.mixin']  # Testing: AI mixin disabled

    name = fields.Char(string="Nom du Budget", required=True, tracking=True, readonly=True, states={'draft': [('readonly', False)]})
    fiscal_year = fields.Char(string="Année Fiscale", tracking=True, readonly=True, states={'draft': [('readonly', False)]})
    total_amount = fields.Monetary(string="Montant Total", currency_field='currency_id', compute='_compute_total_amount', store=True)
    allocated_amount = fields.Monetary(string="Montant Alloué", currency_field='currency_id', tracking=True, readonly=True, states={'draft': [('readonly', False)]})
    used_amount = fields.Monetary(string="Montant Utilisé", currency_field='currency_id', tracking=True, readonly=True, states={'draft': [('readonly', False)]})
    remaining_amount = fields.Monetary(string="Montant Restant", currency_field='currency_id', compute='_compute_remaining_amount', store=True)
    currency_id = fields.Many2one('res.currency', string='Devise', default=lambda self: self._get_default_currency(), readonly=True, states={'draft': [('readonly', False)]})

    @api.model
    def _get_default_currency(self):
        """Retourne la devise CFA (XOF) par défaut"""
        xof_currency = self.env['res.currency'].search([('name', '=', 'XOF')], limit=1)
        return xof_currency or self.env.company.currency_id
    budget_type = fields.Selection([
        ('investment', 'Investissement'),
        ('operating', 'Fonctionnement'),
        ('emergency', 'Urgence')
    ], string="Type de Budget", default='investment', tracking=True, readonly=True, states={'draft': [('readonly', False)]})
    status = fields.Selection([
        ('draft', 'Brouillon'),
        ('approved', 'Approuvé'),
        ('active', 'Actif'),
        ('closed', 'Clôturé')
    ], string="Statut", default='draft', tracking=True)
    state = fields.Selection([('draft', 'Brouillon'), ('locked', 'Verrouillé')], string="État", default='locked', readonly=True, copy=False)
    ministry_id = fields.Many2one('government.ministry', string="Ministère Bénéficiaire", tracking=True, readonly=True, states={'draft': [('readonly', False)]})
    strategic_objective_id = fields.Many2one('strategic.objective', string="Objectif Stratégique", required=True, readonly=True, states={'draft': [('readonly', False)]})
    description = fields.Html(string="Description", readonly=True, states={'draft': [('readonly', False)]})
    
    def action_set_to_draft(self):
        self.write({'state': 'draft'})

    def action_set_to_locked(self):
        self.write({'state': 'locked'})
    
    @api.depends('allocated_amount')
    def _compute_total_amount(self):
        for record in self:
            record.total_amount = record.allocated_amount
    
    @api.depends('allocated_amount', 'used_amount')
    def _compute_remaining_amount(self):
        for record in self:
            record.remaining_amount = record.allocated_amount - record.used_amount
