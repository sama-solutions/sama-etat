import base64
import io
import qrcode
from odoo import http, fields
from odoo.http import request
from odoo.exceptions import AccessError, MissingError


class PublicSenegalGovController(http.Controller):
    """Contrôleur pour les pages publiques du Plan Sénégal 2050"""

    def _generate_qr_code(self, url):
        """Génère un QR code pour l'URL donnée"""
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(url)
        qr.make(fit=True)
        
        img = qr.make_image(fill_color="black", back_color="white")
        buffer = io.BytesIO()
        img.save(buffer, format='PNG')
        qr_code_data = base64.b64encode(buffer.getvalue()).decode()
        return qr_code_data

    @http.route(['/senegal2050/project/<int:project_id>'], type='http', auth="public", website=True)
    def public_project_page(self, project_id, **kwargs):
        """Page publique pour un projet gouvernemental"""
        try:
            project = request.env['government.project'].sudo().browse(project_id)
            if not project.exists():
                return request.render('http_routing.404')
            
            # Générer l'URL complète pour le QR code
            base_url = request.env['ir.config_parameter'].sudo().get_param('web.base.url')
            project_url = f"{base_url}/senegal2050/project/{project_id}"
            qr_code = self._generate_qr_code(project_url)
            
            values = {
                'project': project,
                'qr_code': qr_code,
                'project_url': project_url,
            }
            return request.render('senegal_gov_project_management.public_project_page', values)
        except (AccessError, MissingError):
            return request.render('http_routing.404')

    @http.route(['/senegal2050/ministry/<int:ministry_id>'], type='http', auth="public", website=True)
    def public_ministry_page(self, ministry_id, **kwargs):
        """Page publique pour un ministère"""
        try:
            ministry = request.env['government.ministry'].sudo().browse(ministry_id)
            if not ministry.exists():
                return request.render('http_routing.404')
            
            base_url = request.env['ir.config_parameter'].sudo().get_param('web.base.url')
            ministry_url = f"{base_url}/senegal2050/ministry/{ministry_id}"
            qr_code = self._generate_qr_code(ministry_url)
            
            # Récupérer les projets publics du ministère
            projects = ministry.project_ids.filtered(lambda p: p.status in ['validated', 'in_progress', 'completed'])
            
            values = {
                'ministry': ministry,
                'projects': projects,
                'qr_code': qr_code,
                'ministry_url': ministry_url,
            }
            return request.render('senegal_gov_project_management.public_ministry_page', values)
        except (AccessError, MissingError):
            return request.render('http_routing.404')

    @http.route(['/senegal2050/decision/<int:decision_id>'], type='http', auth="public", website=True)
    def public_decision_page(self, decision_id, **kwargs):
        """Page publique pour une décision officielle"""
        try:
            decision = request.env['government.decision'].sudo().browse(decision_id)
            if not decision.exists() or not decision.is_public:
                return request.render('http_routing.404')
            
            base_url = request.env['ir.config_parameter'].sudo().get_param('web.base.url')
            decision_url = f"{base_url}/senegal2050/decision/{decision_id}"
            qr_code = self._generate_qr_code(decision_url)
            
            values = {
                'decision': decision,
                'qr_code': qr_code,
                'decision_url': decision_url,
            }
            return request.render('senegal_gov_project_management.public_decision_page', values)
        except (AccessError, MissingError):
            return request.render('http_routing.404')

    @http.route(['/senegal2050/event/<int:event_id>'], type='http', auth="public", website=True)
    def public_event_page(self, event_id, **kwargs):
        """Page publique pour un événement"""
        try:
            event = request.env['government.event'].sudo().browse(event_id)
            if not event.exists():
                return request.render('http_routing.404')
            
            base_url = request.env['ir.config_parameter'].sudo().get_param('web.base.url')
            event_url = f"{base_url}/senegal2050/event/{event_id}"
            qr_code = self._generate_qr_code(event_url)
            
            values = {
                'event': event,
                'qr_code': qr_code,
                'event_url': event_url,
            }
            return request.render('senegal_gov_project_management.public_event_page', values)
        except (AccessError, MissingError):
            return request.render('http_routing.404')

    @http.route(['/senegal2050/budget/<int:budget_id>'], type='http', auth="public", website=True)
    def public_budget_page(self, budget_id, **kwargs):
        """Page publique pour un budget"""
        try:
            budget = request.env['government.budget'].sudo().browse(budget_id)
            if not budget.exists() or budget.status != 'active':
                return request.render('http_routing.404')
            
            base_url = request.env['ir.config_parameter'].sudo().get_param('web.base.url')
            budget_url = f"{base_url}/senegal2050/budget/{budget_id}"
            qr_code = self._generate_qr_code(budget_url)
            
            values = {
                'budget': budget,
                'qr_code': qr_code,
                'budget_url': budget_url,
            }
            return request.render('senegal_gov_project_management.public_budget_page', values)
        except (AccessError, MissingError):
            return request.render('http_routing.404')

    @http.route(['/senegal2050/objective/<int:objective_id>'], type='http', auth="public", website=True)
    def public_objective_page(self, objective_id, **kwargs):
        """Page publique pour un objectif stratégique"""
        try:
            objective = request.env['strategic.objective'].sudo().browse(objective_id)
            if not objective.exists():
                return request.render('http_routing.404')
            
            base_url = request.env['ir.config_parameter'].sudo().get_param('web.base.url')
            objective_url = f"{base_url}/senegal2050/objective/{objective_id}"
            qr_code = self._generate_qr_code(objective_url)
            
            # Récupérer les projets liés
            projects = objective.linked_projects.filtered(lambda p: p.status in ['validated', 'in_progress', 'completed'])
            
            values = {
                'objective': objective,
                'projects': projects,
                'qr_code': qr_code,
                'objective_url': objective_url,
            }
            return request.render('senegal_gov_project_management.public_objective_page', values)
        except (AccessError, MissingError):
            return request.render('http_routing.404')

    @http.route(['/senegal2050/dashboard'], type='http', auth="public", website=True)
    def public_dashboard(self, **kwargs):
        """Tableau de bord public du Plan Sénégal 2050"""
        try:
            # Statistiques publiques
            projects = request.env['government.project'].sudo().search([])
            ministries = request.env['government.ministry'].sudo().search([])
            decisions = request.env['government.decision'].sudo().search([('is_public', '=', True)])
            events = request.env['government.event'].sudo().search([])
            
            base_url = request.env['ir.config_parameter'].sudo().get_param('web.base.url')
            dashboard_url = f"{base_url}/senegal2050/dashboard"
            qr_code = self._generate_qr_code(dashboard_url)
            
            values = {
                'total_projects': len(projects),
                'active_projects': len(projects.filtered(lambda p: p.status in ['validated', 'in_progress'])),
                'completed_projects': len(projects.filtered(lambda p: p.status == 'completed')),
                'total_ministries': len(ministries),
                'public_decisions': len(decisions),
                'upcoming_events': len(events.filtered(lambda e: e.event_date and e.event_date >= fields.Date.today())),
                'qr_code': qr_code,
                'dashboard_url': dashboard_url,
            }
            return request.render('senegal_gov_project_management.public_dashboard_page', values)
        except Exception as e:
            return request.render('http_routing.404')

    @http.route(['/senegal2050/qr/<string:model>/<int:record_id>'], type='http', auth="public")
    def generate_qr_code_image(self, model, record_id, **kwargs):
        """Génère et retourne l'image QR code pour un enregistrement"""
        try:
            # Mapping des modèles vers les routes
            model_routes = {
                'government.project': 'project',
                'government.ministry': 'ministry',
                'government.decision': 'decision',
                'government.event': 'event',
                'government.budget': 'budget',
                'strategic.objective': 'objective',
            }
            
            if model not in model_routes:
                return request.not_found()
            
            base_url = request.env['ir.config_parameter'].sudo().get_param('web.base.url')
            record_url = f"{base_url}/senegal2050/{model_routes[model]}/{record_id}"
            
            # Générer le QR code
            qr = qrcode.QRCode(
                version=1,
                error_correction=qrcode.constants.ERROR_CORRECT_L,
                box_size=10,
                border=4,
            )
            qr.add_data(record_url)
            qr.make(fit=True)
            
            img = qr.make_image(fill_color="black", back_color="white")
            buffer = io.BytesIO()
            img.save(buffer, format='PNG')
            
            return request.make_response(
                buffer.getvalue(),
                headers=[
                    ('Content-Type', 'image/png'),
                    ('Cache-Control', 'public, max-age=3600'),
                ]
            )
        except Exception:
            return request.not_found()
