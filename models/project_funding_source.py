from odoo import models, fields, api
from odoo.exceptions import ValidationError

class ProjectFundingSource(models.Model):
    _name = 'project.funding.source'
    _description = 'Sources de Financement - Conformité Légale Sénégal'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'sequence, source_name'

    # Champs principaux
    name = fields.Char(string="Nom", compute='_compute_name', store=True)
    project_id = fields.Many2one(
        'government.project', 
        string="Projet", 
        required=True, 
        ondelete='cascade',
        tracking=True
    )
    sequence = fields.Integer(string="Séquence", default=10)
    
    source_name = fields.Char(
        string="Nom de la Source", 
        required=True, 
        tracking=True,
        help="Ex: Budget National, Banque Mondiale, AFD, etc."
    )
    
    source_type = fields.Selection([
        ('budget_national', 'Budget National'),
        ('pret_multilateral', 'Prêt Multilatéral'),
        ('pret_bilateral', 'Prêt Bilatéral'),
        ('don_multilateral', 'Don Multilatéral'),
        ('don_bilateral', 'Don Bilatéral'),
        ('secteur_prive', 'Secteur Privé'),
        ('partenariat_ppp', 'Partenariat Public-Privé'),
        ('fonds_special', 'Fonds Spécial'),
        ('autre', 'Autre')
    ], string="Type de Source", required=True, tracking=True)
    
    funding_category = fields.Selection([
        ('investissement', 'Investissement'),
        ('fonctionnement', 'Fonctionnement'),
        ('urgence', 'Urgence'),
        ('contrepartie', 'Contrepartie Nationale')
    ], string="Catégorie de Financement", required=True, tracking=True)
    
    # Montants et pourcentages
    amount = fields.Monetary(
        string="Montant", 
        currency_field='currency_id', 
        required=True, 
        tracking=True
    )
    currency_id = fields.Many2one(
        'res.currency', 
        string='Devise', 
        default=lambda self: self._get_default_currency(),
        required=True
    )
    
    percentage = fields.Float(
        string="% du Financement Total", 
        compute='_compute_percentage', 
        store=True,
        help="Pourcentage par rapport au coût total du projet"
    )
    
    # Informations sur le bailleur/partenaire
    partner_id = fields.Many2one(
        'res.partner', 
        string="Partenaire/Bailleur",
        help="Organisation ou institution qui fournit le financement"
    )
    partner_country_id = fields.Many2one(
        'res.country', 
        string="Pays du Partenaire",
        related='partner_id.country_id',
        store=True
    )
    
    # Conditions et modalités
    financing_conditions = fields.Text(
        string="Conditions de Financement",
        help="Conditions spécifiques liées à ce financement (taux, garanties, etc.)"
    )
    repayment_terms = fields.Text(
        string="Modalités de Remboursement",
        help="Conditions de remboursement (pour les prêts)"
    )
    interest_rate = fields.Float(
        string="Taux d'Intérêt (%)",
        help="Taux d'intérêt applicable (pour les prêts)"
    )
    grace_period = fields.Integer(
        string="Période de Grâce (années)",
        help="Période de grâce avant remboursement"
    )
    maturity_period = fields.Integer(
        string="Période de Maturité (années)",
        help="Durée totale du prêt"
    )
    
    # Statut et suivi
    commitment_status = fields.Selection([
        ('proposed', 'Proposé'),
        ('under_negotiation', 'En Négociation'),
        ('committed', 'Engagé'),
        ('signed', 'Signé'),
        ('effective', 'Effectif'),
        ('disbursing', 'En Décaissement'),
        ('completed', 'Achevé'),
        ('cancelled', 'Annulé')
    ], string="Statut de l'Engagement", default='proposed', tracking=True)
    
    disbursed_amount = fields.Monetary(
        string="Montant Décaissé", 
        currency_field='currency_id',
        help="Montant effectivement décaissé à ce jour"
    )
    remaining_amount = fields.Monetary(
        string="Montant Restant", 
        compute='_compute_remaining_amount', 
        store=True,
        currency_field='currency_id'
    )
    disbursement_rate = fields.Float(
        string="Taux de Décaissement (%)", 
        compute='_compute_disbursement_rate', 
        store=True
    )
    
    # Dates importantes
    commitment_date = fields.Date(string="Date d'Engagement")
    signature_date = fields.Date(string="Date de Signature")
    effectiveness_date = fields.Date(string="Date d'Entrée en Vigueur")
    closing_date = fields.Date(string="Date de Clôture")
    
    # Documents et références
    agreement_reference = fields.Char(
        string="Référence de l'Accord",
        help="Numéro de référence de l'accord de financement"
    )
    legal_documents = fields.Text(
        string="Documents Juridiques",
        help="Liste des documents juridiques associés"
    )
    
    # Conformité et audit
    compliance_requirements = fields.Text(
        string="Exigences de Conformité",
        help="Exigences spécifiques de conformité du bailleur"
    )
    reporting_requirements = fields.Text(
        string="Obligations de Reporting",
        help="Obligations de rapport et de suivi"
    )
    audit_requirements = fields.Text(
        string="Exigences d'Audit",
        help="Exigences d'audit spécifiques"
    )
    
    # Méthodes de calcul
    @api.depends('source_name', 'amount')
    def _compute_name(self):
        """Génère le nom affiché de l'enregistrement"""
        for record in self:
            if record.source_name and record.amount:
                record.name = f"{record.source_name} - {record.amount:,.0f} {record.currency_id.symbol or 'XOF'}"
            else:
                record.name = record.source_name or "Nouvelle Source"
    
    @api.depends('amount', 'project_id.cout_total_projet')
    def _compute_percentage(self):
        """Calcule le pourcentage par rapport au coût total du projet"""
        for record in self:
            if record.project_id.cout_total_projet and record.amount:
                record.percentage = (record.amount / record.project_id.cout_total_projet) * 100
            else:
                record.percentage = 0.0
    
    @api.depends('amount', 'disbursed_amount')
    def _compute_remaining_amount(self):
        """Calcule le montant restant à décaisser"""
        for record in self:
            record.remaining_amount = record.amount - (record.disbursed_amount or 0)
    
    @api.depends('disbursed_amount', 'amount')
    def _compute_disbursement_rate(self):
        """Calcule le taux de décaissement"""
        for record in self:
            if record.amount and record.disbursed_amount:
                record.disbursement_rate = (record.disbursed_amount / record.amount) * 100
            else:
                record.disbursement_rate = 0.0
    
    def _get_default_currency(self):
        """Retourne la devise CFA (XOF) par défaut"""
        xof_currency = self.env['res.currency'].search([('name', '=', 'XOF')], limit=1)
        if xof_currency:
            return xof_currency.id
        return self.env.company.currency_id.id
    
    # Contraintes de validation
    @api.constrains('amount', 'disbursed_amount')
    def _check_positive_amounts(self):
        """Vérifie que les montants sont positifs"""
        for record in self:
            if record.amount <= 0:
                raise ValidationError("Le montant du financement doit être positif.")
            if record.disbursed_amount and record.disbursed_amount < 0:
                raise ValidationError("Le montant décaissé ne peut pas être négatif.")
            if record.disbursed_amount and record.disbursed_amount > record.amount:
                raise ValidationError("Le montant décaissé ne peut pas dépasser le montant total.")
    
    @api.constrains('interest_rate')
    def _check_interest_rate(self):
        """Vérifie que le taux d'intérêt est valide"""
        for record in self:
            if record.interest_rate and record.interest_rate < 0:
                raise ValidationError("Le taux d'intérêt ne peut pas être négatif.")
    
    @api.constrains('commitment_date', 'signature_date', 'effectiveness_date', 'closing_date')
    def _check_dates_sequence(self):
        """Vérifie la séquence logique des dates"""
        for record in self:
            dates = [
                (record.commitment_date, 'engagement'),
                (record.signature_date, 'signature'),
                (record.effectiveness_date, 'entrée en vigueur'),
                (record.closing_date, 'clôture')
            ]
            # Filtrer les dates non nulles et les trier
            valid_dates = [(date, name) for date, name in dates if date]
            valid_dates.sort(key=lambda x: x[0])
            
            # Vérifier que les dates sont dans l'ordre logique
            if len(valid_dates) > 1:
                for i in range(1, len(valid_dates)):
                    if valid_dates[i][0] < valid_dates[i-1][0]:
                        raise ValidationError(f"La date de {valid_dates[i][1]} doit être postérieure à la date de {valid_dates[i-1][1]}.")
    
    # Actions
    def action_commit_funding(self):
        """Marque le financement comme engagé"""
        self.write({
            'commitment_status': 'committed',
            'commitment_date': fields.Date.today()
        })
    
    def action_sign_agreement(self):
        """Marque l'accord comme signé"""
        self.write({
            'commitment_status': 'signed',
            'signature_date': fields.Date.today()
        })
    
    def action_make_effective(self):
        """Rend l'accord effectif"""
        self.write({
            'commitment_status': 'effective',
            'effectiveness_date': fields.Date.today()
        })
    
    def action_start_disbursement(self):
        """Démarre le processus de décaissement"""
        self.write({'commitment_status': 'disbursing'})
    
    def action_complete_funding(self):
        """Marque le financement comme achevé"""
        self.write({
            'commitment_status': 'completed',
            'disbursed_amount': self.amount
        })
    
    def action_cancel_funding(self):
        """Annule le financement"""
        self.write({'commitment_status': 'cancelled'})
