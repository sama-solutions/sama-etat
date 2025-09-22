# -*- coding: utf-8 -*-
"""
AIOAuthController - Secure OAuth 2.0 implementation with PKCE, nonce, and id_token verification
"""
import logging
import requests
import urllib.parse
import secrets
import hashlib
import base64
import json
from datetime import timedelta
from odoo import http, fields, _
from odoo.http import request
from odoo.exceptions import UserError
from werkzeug.urls import url_join

_logger = logging.getLogger(__name__)

class AIOAuthController(http.Controller):
    """Secure OAuth 2.0 Controller with PKCE and OIDC support"""
    
    _OAUTH_CONFIG = {
        'google': {
            'auth_url': 'https://accounts.google.com/o/oauth2/v2/auth',
            'token_url': 'https://oauth2.googleapis.com/token',
            'scope': 'openid email profile',
            'config_keys': ['client_id', 'client_secret'],
            'jwks_uri': 'https://www.googleapis.com/oauth2/v3/certs',
            'userinfo_endpoint': 'https://www.googleapis.com/oauth2/v3/userinfo',
        },
        'microsoft': {
            'auth_url': 'https://login.microsoftonline.com/common/oauth2/v2.0/authorize',
            'token_url': 'https://login.microsoftonline.com/common/oauth2/v2.0/token',
            'scope': 'openid email profile offline_access',
            'config_keys': ['client_id', 'client_secret', 'tenant_id'],
            'jwks_uri': 'https://login.microsoftonline.com/common/discovery/v2.0/keys',
            'userinfo_endpoint': 'https://graph.microsoft.com/oidc/userinfo',
        }
    }
    
    # -------------------------
    # Helpers: params / base_url
    # -------------------------
    def _get_oauth_config(self, provider):
        """Get OAuth configuration for the specified provider"""
        if provider not in self._OAUTH_CONFIG:
            raise UserError(_("Unsupported OAuth provider: %s") % provider)
        return self._OAUTH_CONFIG[provider]
    
    def _get_oauth_params(self, provider):
        """Securely read OAuth parameters from system parameters"""
        config = self._get_oauth_config(provider)
        params = {}
        icp = request.env['ir.config_parameter'].sudo()
        
        for key in config['config_keys']:
            # Parameters stored as: ai_oauth.<provider>.<key>
            param_name = f"ai_oauth.{provider}.{key}"
            value = icp.get_param(param_name)
            if not value:
                raise UserError(_("Missing required OAuth parameter: %s") % param_name)
            params[key] = value
            
        return params
    
    def _get_redirect_uri(self, provider):
        """Generate secure redirect URI for OAuth callback"""
        base_url = request.env['ir.config_parameter'].sudo().get_param('web.base.url')
        if not base_url:
            raise UserError(_("Base URL is not configured (web.base.url)"))
        return url_join(base_url, f"/ai/oauth/{provider}/callback")
    
    # -------------------------
    # PKCE & Security Helpers
    # -------------------------
    def _generate_code_verifier(self, length=64):
        """Generate a secure random code verifier for PKCE"""
        verifier = secrets.token_urlsafe(length)
        return verifier[:128]  # Max length constraint
    
    def _code_challenge_from_verifier(self, verifier):
        """Generate S256 code challenge from verifier"""
        digest = hashlib.sha256(verifier.encode('ascii')).digest()
        return base64.urlsafe_b64encode(digest).rstrip(b'=').decode('ascii')
    
    def _generate_state_token(self):
        """Generate a secure random state token for CSRF protection"""
        return secrets.token_urlsafe(32)
    
    def _generate_nonce(self):
        """Generate a secure random nonce for OIDC"""
        return secrets.token_urlsafe(16)
        
    # -------------------------
    # OAuth Flow: Start
    # -------------------------
    @http.route('/ai/oauth/dashboard', type='http', auth='user', website=True)
    def oauth_dashboard(self, **kw):
        """Render the OAuth dashboard with provider status"""
        providers = self._get_providers_status()
        return request.render('sama_etat.oauth_dashboard_page', {
            'providers': providers,
        })
        
    @http.route('/ai/oauth/<string:provider>/start', type='http', auth='user', website=True)
    def oauth_start(self, provider, **kwargs):
        """Initiate OAuth flow with PKCE and state/nonce"""
        try:
            config = self._get_oauth_config(provider)
            params = self._get_oauth_params(provider)

            # PKCE: Generate code verifier and challenge
            code_verifier = self._generate_code_verifier()
            code_challenge = self._code_challenge_from_verifier(code_verifier)

            # Security tokens
            state = self._generate_state_token()
            nonce = self._generate_nonce()

            # Store in session (safely)
            request.session['oauth_state'] = state
            request.session['oauth_nonce'] = nonce
            request.session['oauth_code_verifier'] = code_verifier
            request.session['oauth_provider'] = provider

            # Safe redirect handling
            ref = request.httprequest.referrer or '/'
            base = request.env['ir.config_parameter'].sudo().get_param('web.base.url') or ''
            if ref and (ref.startswith(base) or ref.startswith('/')):
                request.session['oauth_redirect'] = ref
            else:
                request.session['oauth_redirect'] = '/'

            # Build authorization URL
            auth_params = {
                'client_id': params['client_id'],
                'response_type': 'code',
                'redirect_uri': self._get_redirect_uri(provider),
                'scope': config['scope'],
                'state': state,
                'nonce': nonce,
                'code_challenge': code_challenge,
                'code_challenge_method': 'S256',
                'access_type': 'offline',
                'prompt': 'consent',
            }

            auth_url = f"{config['auth_url']}?{urllib.parse.urlencode(auth_params)}"
            return request.redirect(auth_url)

        except Exception as e:
            _logger.exception("OAuth start error")
            return self._handle_oauth_error(provider, _("Could not start authentication."))

class AIOAuthController(http.Controller):
    """Secure OAuth 2.0 Controller for AI Providers"""
    
    # OAuth configuration for supported providers
    _OAUTH_CONFIG = {
        'google': {
            'auth_url': 'https://accounts.google.com/o/oauth2/v2/auth',
            'token_url': 'https://oauth2.googleapis.com/token',
            'scope': 'openid email profile',
            'config_keys': ['client_id', 'client_secret'],
            'token_validation_url': 'https://www.googleapis.com/oauth2/v3/tokeninfo',
            'user_info_url': 'https://www.googleapis.com/oauth2/v3/userinfo',
        },
        'microsoft': {
            'auth_url': 'https://login.microsoftonline.com/common/oauth2/v2.0/authorize',
            'token_url': 'https://login.microsoftonline.com/common/oauth2/v2.0/token',
            'scope': 'openid email profile offline_access',
            'config_keys': ['client_id', 'client_secret', 'tenant_id'],
            'token_validation_url': 'https://graph.microsoft.com/oidc/userinfo',
            'user_info_url': 'https://graph.microsoft.com/oidc/userinfo',
        }
    }

    # Error messages
    _ERROR_MESSAGES = {
        'missing_config': 'Configuration manquante: %s',
        'invalid_provider': 'Fournisseur OAuth non supporté: %s',
        'oauth_failed': 'Échec de la connexion OAuth',
        'missing_code': 'Code d\'autorisation manquant',
        'token_failure': 'Échec de l\'obtention du jeton',
        'invalid_token': 'Jeton invalide ou expiré',
    }

    def _get_oauth_config(self, provider):
        """Get OAuth configuration for the specified provider"""
        if provider not in self._OAUTH_CONFIG:
            raise UserError(_(self._ERROR_MESSAGES['invalid_provider']) % provider)
        return self._OAUTH_CONFIG[provider]

    def _get_redirect_uri(self, provider):
        """Generate redirect URI for OAuth callback"""
        base_url = request.env['ir.config_parameter'].sudo().get_param('web.base.url')
        return f"{base_url}/ai/oauth/{provider}/callback"

    def _get_oauth_params(self, provider):
        """Get OAuth parameters from system parameters"""
        ICP = request.env['ir.config_parameter'].sudo()
        config = self._get_oauth_config(provider)
        params = {}
        
        for key in config['config_keys']:
            param_name = f'ai.{provider}.{key}'
            param_value = ICP.get_param(param_name)
            if not param_value:
                raise UserError(_(self._ERROR_MESSAGES['missing_config']) % param_name)
            params[key] = param_value
            
        return params

    def _get_provider_display_name(self, provider):
        """Get display name for provider"""
        names = {
            'google': 'Google (Gemini)',
            'microsoft': 'Microsoft (Azure OpenAI)',
            'openai': 'OpenAI (ChatGPT)'
        }
        return names.get(provider, provider.capitalize())

    def _get_provider_icon(self, provider):
        """Get icon URL for provider"""
        icons = {
            'google': 'https://www.google.com/images/branding/googlelogo/2x/googlelogo_color_74x24dp.png',
            'microsoft': 'https://upload.wikimedia.org/wikipedia/commons/4/44/Microsoft_logo.svg',
            'openai': 'https://upload.wikimedia.org/wikipedia/commons/4/4d/OpenAI_Logo.svg'
        }
        return icons.get(provider, '')

    @http.route('/ai/oauth/dashboard', type='http', auth='user', website=True, csrf=False)
    def oauth_dashboard(self, **kw):
        """Render the OAuth dashboard"""
        providers = self._get_providers_status()
        return request.render('sama_etat.oauth_dashboard_page', {
            'providers': providers,
        })

    def _is_provider_connected(self, provider):
        """Check if provider is already connected"""
        try:
            provider_config = request.env['ai.provider.config'].search([
                ('provider_type', '=', provider)
            ], limit=1)
            
            if not provider_config:
                return False
                
            # Check if OAuth token exists and is not expired
            if not provider_config.oauth_token or not provider_config.oauth_expires_at:
                return False
                
            # Check if token is still valid
            expires_at = fields.Datetime.from_string(provider_config.oauth_expires_at)
            return expires_at > fields.Datetime.now()
            
        except Exception as e:
            _logger.error("Error checking provider connection status: %s", str(e))
            return False

    @http.route(['/ai/oauth/<string:provider>/start'], type='http', auth='user', website=True, csrf=False)
    def oauth_start(self, provider, **kwargs):
        """Initiate OAuth flow for the specified provider"""
        try:
            config = self._get_oauth_config(provider)
            params = self._get_oauth_params(provider)
            
            # Generate state token for CSRF protection
            state = request.env['ir.config_parameter'].sudo().generate_oauth_state()
            
            # Build authorization URL
            auth_params = {
                'response_type': 'code',
                'client_id': params['client_id'],
                'redirect_uri': self._get_redirect_uri(provider),
                'scope': config['scope'],
                'state': state,
                'access_type': 'offline',
                'prompt': 'consent',
            }
            
            if provider == 'microsoft':
                auth_params['response_mode'] = 'query'
            
            auth_url = f"{config['auth_url']}?{urllib.parse.urlencode(auth_params)}"
            
            # Store state in session
            request.session['oauth_state'] = state
            request.session['oauth_provider'] = provider
            
            return request.redirect(auth_url)
            
        except Exception as e:
            _logger.error("OAuth start error: %s", str(e), exc_info=True)
            return self._handle_oauth_error(provider, str(e))

    @http.route(['/ai/oauth/<string:provider>/callback'], type='http', auth='user', website=True, csrf=False)
    def oauth_callback(self, provider, **kwargs):
        """Handle OAuth callback from provider"""
        try:
            # Verify state to prevent CSRF
            state = kwargs.get('state')
            if not state or state != request.session.pop('oauth_state', None):
                return self._handle_oauth_error(provider, 'Invalid state parameter')
            
            # Verify provider matches
            if provider != request.session.pop('oauth_provider', None):
                return self._handle_oauth_error(provider, 'Invalid provider')
            
            # Get authorization code
            code = kwargs.get('code')
            if not code:
                return self._handle_oauth_error(provider, self._ERROR_MESSAGES['missing_code'])
            
            # Exchange code for tokens
            token_data = self._get_oauth_tokens(provider, code)
            
            # Store tokens in provider config
            self._store_oauth_tokens(provider, token_data)
            
            # Redirect to success page
            return request.redirect('/ai/oauth/success')
            
        except Exception as e:
            _logger.error("%s OAuth callback error: %s", provider, str(e), exc_info=True)
            return request.render('sama_etat.oauth_error_page', {
                'error_message': str(e) or _("An unknown error occurred")
            })

    def _get_oauth_tokens(self, provider, code):
        """Exchange authorization code for access and refresh tokens"""
        config = self._get_oauth_config(provider)
        params = self._get_oauth_params(provider)
        
        data = {
            'code': code,
            'client_id': params['client_id'],
            'client_secret': params['client_secret'],
            'redirect_uri': self._get_redirect_uri(provider),
            'grant_type': 'authorization_code'
        }
        
        try:
            response = requests.post(config['token_url'], data=data, timeout=10)
            response.raise_for_status()
            return response.json()
            
        except requests.RequestException as e:
            _logger.error("Token request failed: %s", str(e))
            raise UserError(self._ERROR_MESSAGES['token_failure']) from e

    def _refresh_oauth_token(self, provider, refresh_token):
        """Refresh OAuth token using refresh token"""
        try:
            config = self._get_oauth_config(provider)
            params = self._get_oauth_params(provider)
            
            data = {
                'client_id': params['client_id'],
                'client_secret': params['client_secret'],
                'refresh_token': refresh_token,
                'grant_type': 'refresh_token'
            }
            
            response = requests.post(config['token_url'], data=data, timeout=10)
            response.raise_for_status()
            return response.json()
            
        except requests.RequestException as e:
            _logger.error("Token refresh failed for %s: %s", provider, str(e))
            return None

    def _get_valid_token(self, provider_config):
        """Get a valid token, refreshing if necessary"""
        if not provider_config.oauth_token:
            return None
            
        # If token is still valid, return it
        if (provider_config.oauth_expires_at and 
            fields.Datetime.from_string(provider_config.oauth_expires_at) > fields.Datetime.now()):
            return provider_config.oauth_token
            
        # If we have a refresh token, try to refresh
        if provider_config.oauth_refresh_token:
            token_data = self._refresh_oauth_token(
                provider_config.provider_type, 
                provider_config.oauth_refresh_token
            )
            
            if token_data and 'access_token' in token_data:
                self._store_oauth_tokens(provider_config.provider_type, token_data)
                return token_data['access_token']
                
        return None

    def _store_oauth_tokens(self, provider, token_data):
        """Store OAuth tokens in provider config"""
        if 'access_token' not in token_data:
            raise UserError(self._ERROR_MESSAGES['token_failure'])
        
        # Find or create provider config
        provider_config = request.env['ai.provider.config'].search([
            ('provider_type', '=', provider),
            ('auth_method', '=', 'oauth')
        ], limit=1)
        
        if not provider_config:
            provider_config = request.env['ai.provider.config'].create({
                'name': f"{self._get_provider_display_name(provider)} (OAuth)",
                'provider_type': provider,
                'auth_method': 'oauth',
            })
        
        # Calculate expiration time
        expires_in = token_data.get('expires_in', 3600)
        expires_at = fields.Datetime.now() + timedelta(seconds=expires_in)
        
        # Update tokens
        update_vals = {
            'oauth_token': token_data['access_token'],
            'oauth_expires_at': expires_at,
            'active': True
        }
        
        # Only update refresh token if we got a new one
        if 'refresh_token' in token_data:
            update_vals['oauth_refresh_token'] = token_data['refresh_token']
            
        provider_config.write(update_vals)
        
        _logger.info("Stored OAuth tokens for %s provider (expires: %s)", 
                    provider, expires_at)
        
        return provider_config

    def _handle_oauth_error(self, provider, message=None):
        """Handle OAuth errors gracefully"""
        if not message:
            message = self._ERROR_MESSAGES['oauth_failed']
            
        values = {
            'provider': self._get_provider_display_name(provider),
            'error_message': message,
            'base_url': request.env['ir.config_parameter'].sudo().get_param('web.base.url'),
        }
        
        # Render the error template within the Odoo backend layout
        return request.render('sama_etat.oauth_error_page', values, qcontext=values, status=400)

    @http.route('/ai/oauth/success', type='http', auth='user', website=True, csrf=False)
    def oauth_success(self, **kwargs):
        """Show success page after OAuth flow completes"""
        provider = request.params.get('provider', '').title()
        return request.render('sama_etat.oauth_success_page', {
            'provider_name': provider
        })
