# -*- coding: utf-8 -*-

from odoo import http
from odoo.http import request


class SyndicatWebsiteController(http.Controller):
    """Contrôleur pour les pages publiques du syndicat"""
    
    @http.route('/syndicat/test', type='http', auth='public')
    def syndicat_test(self, **kwargs):
        """Page de test simple"""
        return "<h1>SAMA SYNDICAT - Test OK!</h1><p>Le contrôleur fonctionne.</p>"

    @http.route(['/syndicat', '/syndicat/home'], type='http', auth='public', website=True)
    def syndicat_home(self, **kwargs):
        """Page d'accueil publique du syndicat"""
        try:
            # Récupérer les statistiques publiques
            dashboard = request.env['syndicat.dashboard'].sudo().search([], limit=1)
            
            # Récupérer les dernières actualités
            communications = request.env['syndicat.communication'].sudo().search([
                ('statut', '=', 'publiee'),
                ('type_communication', '=', 'actualite')
            ], limit=5, order='date_creation desc')
            
            # Récupérer les prochaines assemblées publiques
            assemblees = request.env['syndicat.assemblee'].sudo().search([
                ('statut', 'in', ['planifiee', 'confirmee']),
                ('type_assemblee', '=', 'generale')
            ], limit=3, order='date_assemblee asc')
            
            # Récupérer les formations ouvertes
            formations = request.env['syndicat.formation'].sudo().search([
                ('statut', '=', 'inscriptions_ouvertes')
            ], limit=3, order='date_debut asc')
            
            values = {
                'dashboard': dashboard,
                'communications': communications,
                'assemblees': assemblees,
                'formations': formations,
            }
            
            return request.render('sama_syndicat.website_home', values)
        except Exception as e:
            # En cas d'erreur, retourner une page simple
            return request.make_response(f"""
            <html>
                <head><title>SAMA SYNDICAT</title></head>
                <body>
                    <h1>Bienvenue au Syndicat SAMA</h1>
                    <p>Le site web est en cours de configuration.</p>
                    <p>Erreur: {str(e)}</p>
                    <a href="/web">Accéder à l'interface d'administration</a>
                </body>
            </html>
            """)

    @http.route('/syndicat/about', type='http', auth='public', website=True)
    def syndicat_about(self, **kwargs):
        """Page à propos du syndicat"""
        return request.render('sama_syndicat.website_about')

    @http.route('/syndicat/adhesion', type='http', auth='public', website=True)
    def syndicat_adhesion(self, **kwargs):
        """Page d'adhésion en ligne"""
        return request.render('sama_syndicat.website_adhesion')

    @http.route('/syndicat/adhesion/submit', type='http', auth='public', website=True, methods=['POST'], csrf=False)
    def syndicat_adhesion_submit(self, **post):
        """Traitement du formulaire d'adhésion"""
        try:
            # Créer un nouveau contact
            partner = request.env['res.partner'].sudo().create({
                'name': post.get('name'),
                'email': post.get('email'),
                'phone': post.get('phone'),
                'street': post.get('address'),
                'is_company': False,
                'customer_rank': 1,
                'supplier_rank': 0,
            })
            
            # Créer une demande d'adhésion
            adherent = request.env['syndicat.adherent'].sudo().create({
                'partner_id': partner.id,
                'profession': post.get('profession'),
                'statut_adhesion': 'candidat',
                'date_adhesion': request.env.context.get('today', ''),
                'notes': f"Demande d'adhésion via le site web le {request.env.context.get('today', '')}",
            })
            
            return request.render('sama_syndicat.website_adhesion_success', {
                'adherent': adherent
            })
            
        except Exception as e:
            return request.render('sama_syndicat.website_adhesion_error', {
                'error': str(e)
            })

    @http.route('/syndicat/actualites', type='http', auth='public', website=True)
    def syndicat_actualites(self, **kwargs):
        """Page des actualités publiques"""
        communications = request.env['syndicat.communication'].sudo().search([
            ('statut', '=', 'publiee'),
            ('type_communication', '=', 'actualite')
        ], order='date_creation desc')
        
        return request.render('sama_syndicat.website_actualites', {
            'communications': communications
        })

    @http.route('/syndicat/actualites/<int:communication_id>', type='http', auth='public', website=True)
    def syndicat_actualite_detail(self, communication_id, **kwargs):
        """Détail d'une actualité"""
        communication = request.env['syndicat.communication'].sudo().browse(communication_id)
        
        if not communication.exists() or communication.statut != 'publiee':
            return request.not_found()
            
        # Incrémenter le compteur de lectures
        communication.sudo().action_incrementer_lectures()
        
        return request.render('sama_syndicat.website_actualite_detail', {
            'communication': communication
        })

    @http.route('/syndicat/contact', type='http', auth='public', website=True)
    def syndicat_contact(self, **kwargs):
        """Page de contact"""
        return request.render('sama_syndicat.website_contact')

    @http.route('/syndicat/contact/submit', type='http', auth='public', website=True, methods=['POST'], csrf=False)
    def syndicat_contact_submit(self, **post):
        """Traitement du formulaire de contact"""
        try:
            # Créer un message de contact
            message = request.env['mail.message'].sudo().create({
                'subject': f"Contact site web: {post.get('subject', 'Sans objet')}",
                'body': f"""
                <p><strong>Nom:</strong> {post.get('name', '')}</p>
                <p><strong>Email:</strong> {post.get('email', '')}</p>
                <p><strong>Téléphone:</strong> {post.get('phone', '')}</p>
                <p><strong>Sujet:</strong> {post.get('subject', '')}</p>
                <p><strong>Message:</strong></p>
                <p>{post.get('message', '')}</p>
                """,
                'message_type': 'comment',
                'author_id': request.env.ref('base.public_user').partner_id.id,
            })
            
            return request.render('sama_syndicat.website_contact_success')
            
        except Exception as e:
            return request.render('sama_syndicat.website_contact_error', {
                'error': str(e)
            })

    @http.route('/syndicat/revendications', type='http', auth='public', website=True)
    def syndicat_revendications(self, **kwargs):
        """Page des revendications publiques"""
        try:
            revendications = request.env['syndicat.revendication'].sudo().search([
                ('statut', 'in', ['soumise', 'en_negociation', 'acceptee'])
            ], order='date_creation desc')
            
            return request.render('sama_syndicat.website_revendications', {
                'revendications': revendications
            })
        except Exception as e:
            # En cas d'erreur, retourner une page simple
            return request.make_response(f"""
            <html>
                <head><title>SAMA SYNDICAT - Revendications</title></head>
                <body>
                    <h1>Revendications du Syndicat SAMA</h1>
                    <p>La page des revendications est en cours de configuration.</p>
                    <p>Erreur: {str(e)}</p>
                    <a href="/syndicat">Retour à l'accueil</a>
                </body>
            </html>
            """)

    @http.route('/syndicat/formations', type='http', auth='public')
    def syndicat_formations(self, **kwargs):
        """Page des formations ouvertes"""
        try:
            formations = request.env['syndicat.formation'].sudo().search([], limit=5)
            
            html = "<h1>SAMA SYNDICAT - Formations</h1>"
            html += f"<p>Nombre de formations trouvées: {len(formations)}</p>"
            
            for formation in formations:
                html += f"<p>- {formation.titre}</p>"
                
            html += '<a href="/syndicat">Retour à l\'accueil</a>'
            
            return request.make_response(html)
        except Exception as e:
            # En cas d'erreur, retourner une page simple
            return request.make_response(f"""
            <html>
                <head><title>SAMA SYNDICAT - Formations</title></head>
                <body>
                    <h1>Formations du Syndicat SAMA</h1>
                    <p>La page des formations est en cours de configuration.</p>
                    <p>Erreur: {str(e)}</p>
                    <a href="/syndicat">Retour à l'accueil</a>
                </body>
            </html>
            """)

    @http.route('/syndicat/formations/<int:formation_id>/inscription', type='http', auth='public', website=True)
    def syndicat_formation_inscription(self, formation_id, **kwargs):
        """Page d'inscription à une formation"""
        formation = request.env['syndicat.formation'].sudo().browse(formation_id)
        
        if not formation.exists() or formation.statut != 'inscriptions_ouvertes':
            return request.not_found()
            
        return request.render('sama_syndicat.website_formation_inscription', {
            'formation': formation
        })

    @http.route('/syndicat/formations/<int:formation_id>/inscription/submit', type='http', auth='public', website=True, methods=['POST'], csrf=False)
    def syndicat_formation_inscription_submit(self, formation_id, **post):
        """Traitement de l'inscription à une formation"""
        try:
            formation = request.env['syndicat.formation'].sudo().browse(formation_id)
            
            if not formation.exists() or formation.statut != 'inscriptions_ouvertes':
                return request.not_found()
            
            # Créer ou trouver le contact
            partner = request.env['res.partner'].sudo().search([
                ('email', '=', post.get('email'))
            ], limit=1)
            
            if not partner:
                partner = request.env['res.partner'].sudo().create({
                    'name': post.get('name'),
                    'email': post.get('email'),
                    'phone': post.get('phone'),
                    'is_company': False,
                })
            
            # Vérifier si la personne est adhérente
            adherent = request.env['syndicat.adherent'].sudo().search([
                ('partner_id', '=', partner.id)
            ], limit=1)
            
            if adherent:
                # Inscrire l'adhérent à la formation
                formation.sudo().action_inscrire_adherent(adherent.id)
                
                return request.render('sama_syndicat.website_formation_inscription_success', {
                    'formation': formation,
                    'adherent': adherent
                })
            else:
                return request.render('sama_syndicat.website_formation_inscription_error', {
                    'error': 'Vous devez être adhérent pour vous inscrire à cette formation.'
                })
                
        except Exception as e:
            return request.render('sama_syndicat.website_formation_inscription_error', {
                'error': str(e)
            })