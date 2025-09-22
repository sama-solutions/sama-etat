# -*- coding: utf-8 -*-
"""
Secure OAuth 2.0 with PKCE and OpenID Connect implementation for SAMA ETAT
"""
import logging
import logging
from odoo import http, _
from odoo.http import request

from ..utils.oauth_utils import OAuthUtils

_logger = logging.getLogger(__name__)

# Try to import PyJWT for ID token validation
try:
    import jwt
    from jwt import PyJWKClient
    JWT_AVAILABLE = True
except ImportError:
    _logger.warning("PyJWT not installed. ID token validation will be limited.")
    JWT_AVAILABLE = False


class SecureOAuthController(http.Controller):
    """Secure OAuth 2.0 Controller with PKCE and OpenID Connect support"""
    
    def _get_oauth_config(self, provider):
        """Get OAuth configuration for the specified provider"""
        return self._get_oauth_utils().get_oauth_config(provider)
    
    def _get_oauth_params(self, provider):
        """Safely retrieve OAuth parameters from system parameters"""
        config = self._get_oauth_config(provider)
        params = {}
        icp = request.env['ir.config_parameter'].sudo()
        
        for key in config['config_keys']:
            param_name = f"ai_oauth.{provider}.{key}"
            value = icp.get_param(param_name)
            if not value:
                raise UserError(_("Missing required OAuth parameter: %s") % param_name)
            params[key] = value
            
        return params
    
    def _get_redirect_uri(self, provider):
        """Generate the OAuth redirect URI for callbacks"""
        base_url = request.env['ir.config_parameter'].sudo().get_param('web.base.url')
        if not base_url:
            raise UserError(_("Base URL is not configured (web.base.url)"))
        return request.env['ir.config_parameter'].sudo().get_param('web.base.url') + f"/ai/oauth/{provider}/callback"
    
    def _generate_code_verifier(self, length=64):
        """Generate a secure random code verifier for PKCE"""
        return secrets.token_urlsafe(length)[:128]  # Max length for code verifier
    
    def _generate_code_challenge(self, code_verifier):
        """Generate S256 code challenge from verifier"""
        digest = hashlib.sha256(code_verifier.encode('ascii')).digest()
        return base64.urlsafe_b64encode(digest).rstrip(b'=').decode('ascii')
    
    def _generate_state_token(self):
        """Generate a secure random state token"""
        return secrets.token_urlsafe(32)
    
    def _generate_nonce(self):
        """Generate a secure random nonce for OIDC"""
        return secrets.token_urlsafe(16)

    # -------------------------
    # OAuth Flow Methods
    # -------------------------
    
    @http.route('/ai/oauth/dashboard', type='http', auth='user', website=True)
    def oauth_dashboard(self, **kw):
        """Display OAuth configuration dashboard"""
        providers = []
        for provider in self._get_oauth_utils().get_supported_providers():
            providers.append({
                'name': provider,
                'connected': self._is_provider_connected(provider),
                'display_name': provider.capitalize(),
            })
        return request.render('sama_etat.oauth_dashboard_page', {'providers': providers})
    
    @http.route('/ai/oauth/<string:provider>/start', type='http', auth='user', website=True, csrf=False)
    def oauth_start(self, provider, **kwargs):
        """Initiate OAuth flow with PKCE"""
        try:
            # Generate PKCE code verifier and challenge
            code_verifier = self._generate_code_verifier()
            code_challenge = self._generate_code_challenge(code_verifier)
            
            # Generate state and nonce for OAuth 2.0 and OIDC
            state = self._generate_state_token()
            nonce = self._generate_nonce()
            
            # Store in session (do not store sensitive data)
            request.session['oauth_state'] = state
            request.session['oauth_nonce'] = nonce
            request.session['oauth_code_verifier'] = code_verifier
            request.session['oauth_provider'] = provider
            
            # Safe redirect handling with validation
            ref = request.httprequest.referrer or '/'
            request.session['oauth_redirect'] = ref if self._is_safe_redirect_url(ref) else '/'
            
            # Build authorization URL
            auth_url = self._get_oauth_utils().get_authorization_url(provider, code_challenge, state, nonce)
            return request.redirect(auth_url)
            
        except Exception as e:
            _logger.exception("OAuth start error")
            return self._handle_oauth_error(provider, _("Failed to start OAuth flow"))
    
    def _is_safe_redirect_url(self, url):
        """Validate that the redirect URL is safe (relative or same origin)"""
        if not url:
            return False
            
        # Allow relative URLs
        if url.startswith('/'):
            return True
            
        # Check same origin for absolute URLs
        try:
            from urllib.parse import urlparse
            from odoo.tools import config
            
            base_url = config.get('web.base.url', '')
            if not base_url:
                return False
                
            base_domain = urlparse(base_url).netloc.lower()
            redirect_domain = urlparse(url).netloc.lower()
            
            # Allow same domain and subdomains of the base URL
            return redirect_domain == base_domain or redirect_domain.endswith('.' + base_domain)
            
        except Exception as e:
            _logger.error("Error validating redirect URL: %s", str(e))
            return False

    @http.route('/ai/oauth/<string:provider>/callback', type='http', auth='user', website=True, csrf=False)
    def oauth_callback(self, provider, **kwargs):
        """Handle OAuth callback with PKCE validation"""
        try:
            # Verify state token
            state = kwargs.get('state')
            if not state or state != request.session.pop('oauth_state', None):
                _logger.warning("Invalid state token in OAuth callback")
                return self._handle_oauth_error(provider, _("Invalid request"))
            
            # Verify provider matches
            session_provider = request.session.pop('oauth_provider', None)
            if provider != session_provider:
                _logger.warning("Provider mismatch in OAuth callback")
                return self._handle_oauth_error(provider, _("Invalid provider"))
            
            # Get authorization code
            code = kwargs.get('code')
            if not code:
                _logger.warning("Missing authorization code in callback")
                return self._handle_oauth_error(provider, _("Authorization code missing"))
            
            # Exchange code for tokens
            code_verifier = request.session.pop('oauth_code_verifier', None)
            token_data = self._exchange_code_for_token(provider, code, code_verifier, self._get_redirect_uri(provider))
            if not token_data:
                return self._handle_oauth_error(provider, _("Failed to obtain tokens"))
            
            # Validate ID token if present (OIDC)
            id_token = token_data.get('id_token')
            nonce = request.session.pop('oauth_nonce', None)
            if id_token:
                try:
                    self._validate_id_token(provider, id_token, nonce)
                except Exception as e:
                    _logger.exception("ID token validation failed")
                    return self._handle_oauth_error(provider, _("ID token validation failed"))
            
            # Store tokens securely
            if not self._store_oauth_tokens(provider, token_data):
                return self._handle_oauth_error(provider, _("Failed to store tokens"))
            
            # Get and validate redirect URL
            redirect_url = request.session.pop('oauth_redirect', '/ai/oauth/success')
            if not self._is_safe_redirect_url(redirect_url):
                redirect_url = '/ai/oauth/success'
                _logger.warning("Invalid redirect URL, defaulting to success page")
                
            return request.redirect(redirect_url)
            
        except Exception as e:
            _logger.exception("OAuth callback error")
            return self._handle_oauth_error(provider, _("Authentication failed"))
    
    def _exchange_code_for_token(self, provider, code, code_verifier, redirect_uri):
        """Exchange authorization code for tokens"""
        return self._get_oauth_utils().exchange_code_for_token(provider, code, code_verifier, redirect_uri)
    
    def _validate_id_token(self, provider, id_token, nonce=None):
        """Validate ID token signature and claims"""
        return self._get_oauth_utils().validate_id_token(provider, id_token, nonce)
    
    def _store_oauth_tokens(self, provider, token_data):
        """Securely store OAuth tokens in the database"""
        try:
            ProviderConfig = request.env['ai.provider.config'].sudo()
            
            # Find or create provider config
            provider_config = ProviderConfig.search([
                ('provider_type', '=', provider),
                ('auth_method', '=', 'oauth')
            ], limit=1)
            
            if not provider_config:
                provider_config = ProviderConfig.create({
                    'name': f"{provider.capitalize()} (OAuth)",
                    'provider_type': provider,
                    'auth_method': 'oauth',
                })
            
            # Calculate expiration time
            expires_in = int(token_data.get('expires_in', 3600))
            expires_at = fields.Datetime.to_string(
                datetime.utcnow() + timedelta(seconds=expires_in)
            )
            
            # Update provider config with tokens
            update_vals = {
                'oauth_token': token_data.get('access_token'),
                'oauth_refresh_token': token_data.get('refresh_token'),
                'oauth_expires_at': expires_at,
                'active': True
            }
            
            provider_config.write(update_vals)
            _logger.info("OAuth tokens stored for provider %s", provider)
            return True
            
        except Exception as e:
            _logger.exception("Failed to store OAuth tokens")
            return False
    
    def _is_provider_connected(self, provider):
        """Check if provider is already connected"""
        try:
            provider_config = request.env['ai.provider.config'].sudo().search([
                ('provider_type', '=', provider),
                ('auth_method', '=', 'oauth'),
                ('active', '=', True)
            ], limit=1)
            
            if not provider_config or not provider_config.oauth_token:
                return False
                
            # Check if token is expired
            if provider_config.oauth_expires_at and \
               fields.Datetime.from_string(provider_config.oauth_expires_at) < datetime.utcnow():
                return False
                
            return True
            
        except Exception:
            return False
    
    def _handle_oauth_error(self, provider, message=None):
        """Handle OAuth errors gracefully"""
        _logger.error("OAuth error for %s: %s", provider, message or "Unknown error")
        return request.render('sama_etat.oauth_error_page', {
            'error_message': message or _("An error occurred during authentication.")
        })
    
    @http.route('/ai/oauth/success', type='http', auth='user', website=True)
    def oauth_success(self, **kwargs):
        """Display success page after OAuth flow"""
        provider = request.session.pop('oauth_provider', None)
        return request.render('sama_etat.oauth_success_page', {
            'provider_name': provider.capitalize() if provider else ''
        })
    
    @http.route('/ai/oauth/<string:provider>/disconnect', type='http', auth='user', website=True)
    def oauth_disconnect(self, provider, **kwargs):
        """Disconnect OAuth provider and revoke tokens"""
        try:
            # Revoke tokens if possible
            self._revoke_oauth_tokens(provider)
            
            # Clear tokens from database
            provider_config = request.env['ai.provider.config'].sudo().search([
                ('provider_type', '=', provider),
                ('auth_method', '=', 'oauth')
            ], limit=1)
            
            if provider_config:
                provider_config.write({
                    'oauth_token': False,
                    'oauth_refresh_token': False,
                    'oauth_expires_at': False,
                    'active': False
                })
            
            # Redirect to dashboard with success message
            request.session['oauth_message'] = {
                'type': 'success',
                'message': _("Successfully disconnected from %s") % provider.capitalize()
            }
            
        except Exception as e:
            _logger.exception("Error disconnecting OAuth provider")
            request.session['oauth_message'] = {
                'type': 'danger',
                'message': _("Error disconnecting from %s") % provider.capitalize()
            }
        
        return request.redirect('/ai/oauth/dashboard')
    
    def _revoke_oauth_tokens(self, provider):
        """Attempt to revoke OAuth tokens at the provider"""
        try:
            config = self._get_oauth_config(provider)
            provider_config = request.env['ai.provider.config'].sudo().search([
                ('provider_type', '=', provider),
                ('auth_method', '=', 'oauth')
            ], limit=1)
            
            if not provider_config or not provider_config.oauth_token:
                return False
                
            # Get OAuth parameters
            params = self._get_oauth_params(provider)
            
            # Provider-specific revocation endpoints
            revoke_url = None
            revoke_data = None
            
            if provider == 'google':
                revoke_url = 'https://oauth2.googleapis.com/revoke'
                revoke_data = {
                    'token': provider_config.oauth_token,
                    'client_id': params.get('client_id'),
                    'client_secret': params.get('client_secret')
                }
            elif provider == 'microsoft':
                revoke_url = 'https://login.microsoftonline.com/common/oauth2/v2.0/logout'
                revoke_data = {
                    'client_id': params.get('client_id'),
                    'client_secret': params.get('client_secret'),
                    'token': provider_config.oauth_token
                }
            
            if revoke_url:
                response = requests.post(
                    revoke_url,
                    data=revoke_data,
                    timeout=10,
                    headers={'Content-Type': 'application/x-www-form-urlencoded'}
                )
                response.raise_for_status()
                return True
                
        except Exception as e:
            _logger.warning("Failed to revoke OAuth tokens for %s: %s", provider, str(e))
            
        return False
