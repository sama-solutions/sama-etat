# -*- coding: utf-8 -*-
"""
OAuth Controllers for AI Providers
"""

import logging
import requests
import urllib.parse
from datetime import timedelta
from odoo import http, fields
from odoo.http import request

_logger = logging.getLogger(__name__)

class AIOAuthController(http.Controller):
    @http.route('/ai/oauth/dashboard', type='http', auth='user')
    def ai_oauth_dashboard(self, **kwargs):
        """Simple OAuth dashboard showing links to start provider OAuth flows."""
        base_url = request.env['ir.config_parameter'].sudo().get_param('web.base.url') or request.httprequest.url_root.rstrip('/')
        html = f"""
        <html>
          <head>
            <title>AI OAuth Dashboard</title>
            <style>
              body {{ font-family: Arial, sans-serif; background:#f7f7f9; margin:0; padding:24px; }}
              h1 {{ margin-bottom: 24px; }}
              .providers {{ display:flex; gap:16px; flex-wrap:wrap; }}
              .card {{ background:#fff; border:1px solid #e5e7eb; border-radius:10px; width:320px; padding:16px; box-shadow:0 1px 2px rgba(0,0,0,0.06); }}
              .card img {{ height:36px; }}
              .card h3 {{ margin:12px 0 8px; font-size:18px; }}
              .card p {{ margin:0 0 12px; color:#555; font-size:14px; }}
              .btn {{ display:inline-block; padding:10px 14px; border-radius:8px; text-decoration:none; font-weight:600; }}
              .btn-google {{ background:#1a73e8; color:#fff; }}
              .btn-ms {{ background:#2b2b2b; color:#fff; }}
              .btn-openai {{ background:#10a37f; color:#fff; }}
            </style>
          </head>
          <body>
            <h1>Connexion OAuth - Fournisseurs d'IA</h1>
            <div class='providers'>
              <div class='card'>
                <img alt='Google' src='https://www.google.com/images/branding/googlelogo/2x/googlelogo_color_74x24dp.png' />
                <h3>Google (Gemini)</h3>
                <p>Authentifiez-vous avec votre compte Google pour utiliser Gemini.</p>
                <a class='btn btn-google' href='{base_url}/ai/oauth/google/start'>Se connecter avec Google</a>
              </div>
              <div class='card'>
                <img alt='Microsoft' src='https://upload.wikimedia.org/wikipedia/commons/4/44/Microsoft_logo.svg' />
                <h3>Microsoft (Azure OpenAI)</h3>
                <p>Authentifiez-vous avec votre compte Microsoft pour Azure OpenAI.</p>
                <a class='btn btn-ms' href='{base_url}/ai/oauth/microsoft/start'>Se connecter avec Microsoft</a>
              </div>
              <div class='card'>
                <img alt='OpenAI' src='https://upload.wikimedia.org/wikipedia/commons/4/4d/OpenAI_Logo.svg' />
                <h3>OpenAI (ChatGPT)</h3>
                <p>Configurez votre fournisseur OpenAI dans "Fournisseurs d'IA" si OAuth n'est pas disponible.</p>
                <a class='btn btn-openai' href='{base_url}/web#model=ai.provider.config&view_type=list'>Ouvrir Fournisseurs d'IA</a>
              </div>
            </div>
          </body>
        </html>
        """
        return request.make_response(html, headers=[('Content-Type', 'text/html; charset=utf-8')])

    @http.route('/ai/oauth/google/start', type='http', auth='user')
    def google_oauth_start(self, **kwargs):
        """Initiate Google OAuth by redirecting to the consent screen."""
        ICP = request.env['ir.config_parameter'].sudo()
        client_id = ICP.get_param('ai.google.client_id')
        if not client_id:
            return request.make_response(
                "Google Client ID non configuré (ai.google.client_id).",
                headers=[('Content-Type', 'text/plain; charset=utf-8')],
                status=400,
            )
        redirect_uri = f"{ICP.get_param('web.base.url')}/ai/oauth/google/callback"
        scope = 'https://www.googleapis.com/auth/userinfo.email'
        params = {
            'response_type': 'code',
            'client_id': client_id,
            'redirect_uri': redirect_uri,
            'scope': scope,
            'access_type': 'offline',
            'prompt': 'consent',
        }
        url = 'https://accounts.google.com/o/oauth2/v2/auth?' + urllib.parse.urlencode(params)
        return request.make_response('', headers=[('Location', url)], status=302)

    @http.route('/ai/oauth/microsoft/start', type='http', auth='user')
    def microsoft_oauth_start(self, **kwargs):
        """Initiate Microsoft OAuth by redirecting to the consent screen."""
        ICP = request.env['ir.config_parameter'].sudo()
        client_id = ICP.get_param('ai.microsoft.client_id')
        if not client_id:
            return request.make_response(
                "Microsoft Client ID non configuré (ai.microsoft.client_id).",
                headers=[('Content-Type', 'text/plain; charset=utf-8')],
                status=400,
            )
        redirect_uri = f"{ICP.get_param('web.base.url')}/ai/oauth/microsoft/callback"
        scope = 'User.Read offline_access'
        params = {
            'client_id': client_id,
            'response_type': 'code',
            'redirect_uri': redirect_uri,
            'response_mode': 'query',
            'scope': scope,
        }
        url = 'https://login.microsoftonline.com/common/oauth2/v2.0/authorize?' + urllib.parse.urlencode(params)
        return request.make_response('', headers=[('Location', url)], status=302)
    
    @http.route('/ai/oauth/google/callback', type='http', auth='user')
    def google_oauth_callback(self, **kwargs):
        """Handle Google OAuth callback"""
        try:
            # Get authorization code
            auth_code = kwargs.get('code')
            if not auth_code:
                return request.make_response(
                    "OAuth authorization failed (missing code)",
                    headers=[('Content-Type', 'text/plain; charset=utf-8')],
                    status=400,
                )
            
            # Exchange code for token
            token_url = "https://oauth2.googleapis.com/token"
            client_id = request.env['ir.config_parameter'].sudo().get_param('ai.google.client_id')
            client_secret = request.env['ir.config_parameter'].sudo().get_param('ai.google.client_secret')
            redirect_uri = f"{request.env['ir.config_parameter'].sudo().get_param('web.base.url')}/ai/oauth/google/callback"
            
            data = {
                'code': auth_code,
                'client_id': client_id,
                'client_secret': client_secret,
                'redirect_uri': redirect_uri,
                'grant_type': 'authorization_code'
            }
            
            response = requests.post(token_url, data=data)
            token_info = response.json()
            
            if 'access_token' not in token_info:
                return request.make_response(
                    "Failed to obtain OAuth token",
                    headers=[('Content-Type', 'text/plain; charset=utf-8')],
                    status=400,
                )
            
            # Store token in user's AI provider config
            user = request.env.user
            provider_config = request.env['ai.provider.config'].search([
                ('provider_type', '=', 'google'),
                ('auth_method', '=', 'oauth')
            ], limit=1)
            
            if provider_config:
                provider_config.write({
                    'oauth_token': token_info['access_token'],
                    'oauth_refresh_token': token_info.get('refresh_token'),
                    'oauth_expires_at': fields.Datetime.now() + timedelta(seconds=token_info.get('expires_in', 3600))
                })
            
            return request.make_response(
                "Google OAuth connection successful!",
                headers=[('Content-Type', 'text/plain; charset=utf-8')],
                status=200,
            )
            
        except Exception as e:
            _logger.error(f"Google OAuth callback error: {e}")
            return request.make_response(
                "OAuth connection failed",
                headers=[('Content-Type', 'text/plain; charset=utf-8')],
                status=500,
            )
    
    @http.route('/ai/oauth/microsoft/callback', type='http', auth='user')
    def microsoft_oauth_callback(self, **kwargs):
        """Handle Microsoft OAuth callback"""
        try:
            # Get authorization code
            auth_code = kwargs.get('code')
            if not auth_code:
                return request.make_response(
                    "OAuth authorization failed (missing code)",
                    headers=[('Content-Type', 'text/plain; charset=utf-8')],
                    status=400,
                )
            
            # Exchange code for token
            token_url = "https://login.microsoftonline.com/common/oauth2/v2.0/token"
            client_id = request.env['ir.config_parameter'].sudo().get_param('ai.microsoft.client_id')
            client_secret = request.env['ir.config_parameter'].sudo().get_param('ai.microsoft.client_secret')
            redirect_uri = f"{request.env['ir.config_parameter'].sudo().get_param('web.base.url')}/ai/oauth/microsoft/callback"
            
            data = {
                'code': auth_code,
                'client_id': client_id,
                'client_secret': client_secret,
                'redirect_uri': redirect_uri,
                'grant_type': 'authorization_code'
            }
            
            response = requests.post(token_url, data=data)
            token_info = response.json()
            
            if 'access_token' not in token_info:
                return request.make_response(
                    "Failed to obtain OAuth token",
                    headers=[('Content-Type', 'text/plain; charset=utf-8')],
                    status=400,
                )
            
            # Store token in user's AI provider config
            user = request.env.user
            provider_config = request.env['ai.provider.config'].search([
                ('provider_type', '=', 'microsoft'),
                ('auth_method', '=', 'oauth')
            ], limit=1)
            
            if provider_config:
                provider_config.write({
                    'oauth_token': token_info['access_token'],
                    'oauth_refresh_token': token_info.get('refresh_token'),
                    'oauth_expires_at': fields.Datetime.now() + timedelta(seconds=token_info.get('expires_in', 3600))
                })
            
            return request.make_response(
                "Microsoft OAuth connection successful!",
                headers=[('Content-Type', 'text/plain; charset=utf-8')],
                status=200,
            )
            
        except Exception as e:
            _logger.error(f"Microsoft OAuth callback error: {e}")
            return request.make_response(
                "OAuth connection failed",
                headers=[('Content-Type', 'text/plain; charset=utf-8')],
                status=500,
            )
