from odoo import models, fields, api
from odoo.exceptions import ValidationError

class ProjectLegalText(models.Model):
    _name = 'project.legal.text'
    _description = 'Textes Législatifs et Réglementaires - Conformité Légale Sénégal'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'hierarchy_level, text_type, title'

    # Champs principaux
    name = fields.Char(string="Nom", compute='_compute_name', store=True)
    project_id = fields.Many2one(
        'government.project', 
        string="Projet", 
        required=True, 
        ondelete='cascade',
        tracking=True
    )
    
    title = fields.Char(
        string="Titre du Texte", 
        required=True, 
        tracking=True,
        help="Titre complet du texte juridique"
    )
    
    reference = fields.Char(
        string="Référence Officielle", 
        required=True, 
        tracking=True,
        help="Ex: Loi n° 2023-01, Décret n° 2023-456, etc."
    )
    
    text_type = fields.Selection([
        ('constitution', 'Constitution'),
        ('loi', 'Loi'),
        ('loi_organique', 'Loi Organique'),
        ('decret', 'Décret'),
        ('arrete', 'Arrêté'),
        ('circulaire', 'Circulaire'),
        ('instruction', 'Instruction'),
        ('reglement', 'Règlement'),
        ('ordonnance', 'Ordonnance'),
        ('convention_internationale', 'Convention Internationale'),
        ('traite', 'Traité'),
        ('accord_bilateral', 'Accord Bilatéral'),
        ('directive', 'Directive'),
        ('autre', 'Autre')
    ], string="Type de Texte", required=True, tracking=True)
    
    hierarchy_level = fields.Selection([
        ('1_constitutionnel', '1. Constitutionnel'),
        ('2_legislatif', '2. Législatif'),
        ('3_reglementaire', '3. Réglementaire'),
        ('4_administratif', '4. Administratif'),
        ('5_international', '5. International')
    ], string="Niveau Hiérarchique", required=True, tracking=True,
       help="Niveau dans la hiérarchie des normes juridiques")
    
    # Informations sur le texte
    publication_date = fields.Date(
        string="Date de Publication", 
        tracking=True,
        help="Date de publication au Journal Officiel"
    )
    effective_date = fields.Date(
        string="Date d'Entrée en Vigueur", 
        tracking=True
    )
    issuing_authority = fields.Char(
        string="Autorité Émettrice",
        help="Ex: Assemblée Nationale, Président de la République, Ministre, etc."
    )
    
    description = fields.Text(
        string="Description",
        help="Résumé du contenu et de l'objet du texte"
    )
    
    # Relation avec le projet
    relevance_type = fields.Selection([
        ('fondement_legal', 'Fondement Légal'),
        ('autorisation', 'Autorisation Requise'),
        ('contrainte', 'Contrainte/Obligation'),
        ('procedure', 'Procédure à Suivre'),
        ('norme_technique', 'Norme Technique'),
        ('environnemental', 'Exigence Environnementale'),
        ('social', 'Exigence Sociale'),
        ('financier', 'Cadre Financier'),
        ('marches_publics', 'Marchés Publics'),
        ('autre', 'Autre')
    ], string="Type de Pertinence", required=True, tracking=True,
       help="Comment ce texte se rapporte au projet")
    
    specific_provisions = fields.Text(
        string="Dispositions Spécifiques Applicables",
        help="Articles ou dispositions spécifiques qui s'appliquent au projet"
    )
    
    compliance_requirements = fields.Text(
        string="Exigences de Conformité",
        help="Exigences spécifiques de conformité découlant de ce texte"
    )
    
    # Statut de conformité
    compliance_status = fields.Selection([
        ('not_assessed', 'Non Évalué'),
        ('compliant', 'Conforme'),
        ('partially_compliant', 'Partiellement Conforme'),
        ('non_compliant', 'Non Conforme'),
        ('not_applicable', 'Non Applicable')
    ], string="Statut de Conformité", default='not_assessed', tracking=True)
    
    compliance_notes = fields.Text(
        string="Notes de Conformité",
        help="Détails sur l'évaluation de la conformité"
    )
    
    # Actions requises
    required_actions = fields.Text(
        string="Actions Requises",
        help="Actions spécifiques requises pour assurer la conformité"
    )
    responsible_person = fields.Many2one(
        'res.users', 
        string="Responsable de la Conformité",
        help="Personne responsable de s'assurer de la conformité"
    )
    compliance_deadline = fields.Date(
        string="Échéance de Conformité",
        help="Date limite pour assurer la conformité"
    )
    
    # Documents et références
    official_document = fields.Binary(
        string="Document Officiel",
        help="Fichier PDF du texte officiel"
    )
    official_document_name = fields.Char(string="Nom du Document")
    
    journal_officiel_reference = fields.Char(
        string="Référence Journal Officiel",
        help="Référence de publication au Journal Officiel"
    )
    
    related_texts_ids = fields.Many2many(
        'project.legal.text',
        'legal_text_relation',
        'text_id',
        'related_text_id',
        string="Textes Connexes",
        help="Autres textes juridiques liés"
    )
    
    # Suivi et historique
    last_review_date = fields.Date(
        string="Dernière Révision",
        help="Date de la dernière révision de la conformité"
    )
    next_review_date = fields.Date(
        string="Prochaine Révision",
        help="Date prévue pour la prochaine révision"
    )
    
    is_active = fields.Boolean(
        string="Texte Actif", 
        default=True,
        help="Indique si le texte est toujours en vigueur"
    )
    
    superseded_by_id = fields.Many2one(
        'project.legal.text',
        string="Remplacé par",
        help="Texte qui remplace celui-ci (si abrogé)"
    )
    
    # Méthodes de calcul
    @api.depends('title', 'reference')
    def _compute_name(self):
        """Génère le nom affiché de l'enregistrement"""
        for record in self:
            if record.reference and record.title:
                record.name = f"{record.reference} - {record.title[:50]}{'...' if len(record.title) > 50 else ''}"
            elif record.reference:
                record.name = record.reference
            elif record.title:
                record.name = record.title[:50] + ('...' if len(record.title) > 50 else '')
            else:
                record.name = "Nouveau Texte Juridique"
    
    # Contraintes de validation
    @api.constrains('publication_date', 'effective_date')
    def _check_dates(self):
        """Vérifie la cohérence des dates"""
        for record in self:
            if record.publication_date and record.effective_date:
                if record.effective_date < record.publication_date:
                    raise ValidationError("La date d'entrée en vigueur ne peut pas être antérieure à la date de publication.")
    
    @api.constrains('compliance_deadline')
    def _check_compliance_deadline(self):
        """Vérifie que l'échéance de conformité est dans le futur"""
        for record in self:
            if record.compliance_deadline and record.compliance_deadline < fields.Date.today():
                raise ValidationError("L'échéance de conformité doit être dans le futur.")
    
    @api.constrains('superseded_by_id')
    def _check_superseded_by(self):
        """Vérifie qu'un texte ne peut pas être remplacé par lui-même"""
        for record in self:
            if record.superseded_by_id and record.superseded_by_id.id == record.id:
                raise ValidationError("Un texte ne peut pas être remplacé par lui-même.")
    
    # Actions
    def action_mark_compliant(self):
        """Marque le texte comme conforme"""
        self.write({
            'compliance_status': 'compliant',
            'last_review_date': fields.Date.today()
        })
    
    def action_mark_non_compliant(self):
        """Marque le texte comme non conforme"""
        self.write({
            'compliance_status': 'non_compliant',
            'last_review_date': fields.Date.today()
        })
    
    def action_schedule_review(self):
        """Programme une révision de conformité"""
        # Calculer la prochaine date de révision (par défaut 6 mois)
        next_review = fields.Date.today()
        next_review = next_review.replace(month=next_review.month + 6 if next_review.month <= 6 else next_review.month - 6)
        if next_review.month <= 6:
            next_review = next_review.replace(year=next_review.year + 1)
        
        self.write({'next_review_date': next_review})
    
    def action_supersede_text(self):
        """Marque le texte comme abrogé"""
        self.write({'is_active': False})
    
    def action_create_compliance_task(self):
        """Crée une tâche pour assurer la conformité"""
        if not self.responsible_person:
            raise ValidationError("Veuillez désigner un responsable avant de créer une tâche.")
        
        task_vals = {
            'name': f"Conformité {self.reference} - {self.project_id.name}",
            'description': f"Assurer la conformité au texte: {self.title}\n\nActions requises:\n{self.required_actions or 'À définir'}",
            'user_ids': [(6, 0, [self.responsible_person.id])],
            'date_deadline': self.compliance_deadline,
            'project_id': self.project_id.odoo_project_id.id if self.project_id.odoo_project_id else False,
        }
        
        task = self.env['project.task'].create(task_vals)
        
        return {
            'type': 'ir.actions.act_window',
            'name': 'Tâche de Conformité',
            'res_model': 'project.task',
            'res_id': task.id,
            'view_mode': 'form',
            'target': 'current',
        }
    
    # Méthodes utilitaires
    def get_compliance_summary(self):
        """Retourne un résumé de l'état de conformité"""
        status_labels = dict(self._fields['compliance_status'].selection)
        return {
            'reference': self.reference,
            'title': self.title,
            'status': status_labels.get(self.compliance_status, 'Inconnu'),
            'required_actions': bool(self.required_actions),
            'has_deadline': bool(self.compliance_deadline),
            'overdue': self.compliance_deadline and self.compliance_deadline < fields.Date.today() if self.compliance_deadline else False
        }
