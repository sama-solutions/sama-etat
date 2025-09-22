# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import ValidationError, UserError
import requests
import json
import logging

_logger = logging.getLogger(__name__)

class AIProviderConfig(models.Model):
    """Configuration des Fournisseurs IA - Nouvelle implémentation propre"""
    _name = 'ai.provider.config'
    _description = 'Configuration des Fournisseurs IA'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    
    name = fields.Char(string="Nom de la Configuration", required=True, tracking=True)
    provider_type = fields.Selection([
        ('openai', 'OpenAI (ChatGPT)'),
        ('google', 'Google (Gemini)'),
        ('microsoft', 'Microsoft (Azure OpenAI)'),
        ('ollama', 'Ollama (Local)')
    ], string="Fournisseur IA", required=True, tracking=True)
    
    # Configuration API et OAuth
    auth_method = fields.Selection([
        ('api_key', 'Clé API'),
        ('oauth', 'Authentification OAuth')
    ], string="Méthode d'authentification", default='oauth', required=True)
    
    api_key = fields.Char(string="Clé API", help="Clé d'authentification API (pour méthode API key uniquement)")
    api_url = fields.Char(string="URL API", help="URL de base de l'API")
    model_name = fields.Char(string="Nom du Modèle", help="Nom spécifique du modèle à utiliser")
    
    # OAuth fields - Managed by the OAuth controller
    # Tokens are stored securely in ir.config_parameter
    oauth_token = fields.Char(
        string="Token OAuth",
        compute='_compute_oauth_token',
        inverse='_inverse_oauth_token',
        help="Token d'accès OAuth obtenu après authentification (stocké de manière sécurisée)",
        groups="base.group_system"
    )
    oauth_refresh_token = fields.Char(
        string="Refresh Token",
        compute='_compute_oauth_refresh_token',
        inverse='_inverse_oauth_refresh_token',
        help="Token de rafraîchissement OAuth (stocké de manière sécurisée)",
        groups="base.group_system"
    )
    
    def _get_secure_param_name(self, field_name):
        """Generate a secure parameter name for storing sensitive data"""
        self.ensure_one()
        return f'ai_oauth.secure.{self.id}.{field_name}'
    
    def _get_secure_param(self, field_name, default=None):
        """Get a secure parameter value"""
        self.ensure_one()
        param_name = self._get_secure_param_name(field_name)
        return self.env['ir.config_parameter'].sudo().get_param(param_name, default=default)
    
    def _set_secure_param(self, field_name, value):
        """Set a secure parameter value"""
        self.ensure_one()
        param_name = self._get_secure_param_name(field_name)
        if value is None:
            self.env['ir.config_parameter'].sudo().set_param(param_name, False)
        else:
            self.env['ir.config_parameter'].sudo().set_param(param_name, value)
    oauth_expires_at = fields.Datetime(
        string="Expiration du Token", 
        help="Date et heure d'expiration du jeton d'accès actuel"
    )
    oauth_token_initialized = fields.Boolean(
        string="OAuth Initialized",
        default=False,
        help="Indicates if OAuth tokens have been properly initialized"
    )
    oauth_last_sync = fields.Datetime(
        string="Dernière synchronisation",
        help="Date et heure de la dernière synchronisation OAuth réussie"
    )
    oauth_status = fields.Selection([
        ('not_configured', 'Non configuré'),
        ('connected', 'Connecté'),
        ('expired', 'Expiré'),
        ('error', 'Erreur')
    ], string="État OAuth", compute='_compute_oauth_status', store=True)
    
    @api.depends('oauth_expires_at', 'oauth_refresh_token')
    def _compute_oauth_status(self):
        """Compute the OAuth status based on token presence and expiration"""
        for config in self:
            oauth_token = config._get_secure_param('oauth_token')
            oauth_refresh_token = config._get_secure_param('oauth_refresh_token')
            
            if not oauth_token:
                config.oauth_status = 'not_configured'
            elif config.oauth_expires_at and fields.Datetime.from_string(config.oauth_expires_at) < fields.Datetime.now():
                config.oauth_status = 'expired' if not oauth_refresh_token else 'connected'
            else:
                config.oauth_status = 'connected'
    
    @api.model
    def _get_encryption_key(self):
        """Get the encryption key from system parameters"""
        icp = self.env['ir.config_parameter'].sudo()
        key = icp.get_param('database.secret')
        if not key:
            raise UserError(_("Encryption key not found. Please set 'database.secret' in system parameters."))
        return key.encode()
    
    def _refresh_oauth_token(self):
        """Refresh the OAuth access token using the refresh token"""
        self.ensure_one()
        refresh_token = self._get_secure_param('oauth_refresh_token')
        if not refresh_token:
            return False
            
        try:
            token_url = None
            params = {}
            
            if self.provider_type == 'google':
                token_url = 'https://oauth2.googleapis.com/token'
                params = {
                    'client_id': self.env['ir.config_parameter'].sudo().get_param(f'ai_oauth.{self.provider_type}.client_id'),
                    'client_secret': self.env['ir.config_parameter'].sudo().get_param(f'ai_oauth.{self.provider_type}.client_secret'),
                    'refresh_token': refresh_token,
                    'grant_type': 'refresh_token'
                }
            elif self.provider_type == 'microsoft':
                token_url = 'https://login.microsoftonline.com/common/oauth2/v2.0/token'
                params = {
                    'client_id': self.env['ir.config_parameter'].sudo().get_param(f'ai_oauth.{self.provider_type}.client_id'),
                    'client_secret': self.env['ir.config_parameter'].sudo().get_param(f'ai_oauth.{self.provider_type}.client_secret'),
                    'refresh_token': refresh_token,
                    'grant_type': 'refresh_token'
                }
            
            if token_url:
                response = requests.post(
                    token_url,
                    data=params,
                    timeout=30,
                    headers={'Accept': 'application/json'}
                )
                response.raise_for_status()
                token_data = response.json()
                
                # Update tokens using write to trigger secure storage
                vals = {
                    'oauth_expires_at': fields.Datetime.to_string(
                        fields.Datetime.now() + timedelta(seconds=int(token_data.get('expires_in', 3600)))
                    ),
                    'oauth_last_sync': fields.Datetime.now(),
                }
                self.write(vals)
                
                # Store tokens in secure parameters
                self._set_secure_param('oauth_token', token_data.get('access_token'))
                
                # Update refresh token if a new one was provided
                if token_data.get('refresh_token'):
                    self._set_secure_param('oauth_refresh_token', token_data.get('refresh_token'))
                
                return True
                
        except Exception as e:
            _logger.error("Failed to refresh OAuth token: %s", str(e), exc_info=True)
            
        return False
    is_oauth_connected = fields.Boolean(
        string="OAuth Connecté", 
        compute="_compute_oauth_status", 
        store=False,
        help="Indique si le fournisseur est actuellement connecté via OAuth"
    )
    
    # Paramètres
    max_tokens = fields.Integer(string="Tokens Maximum", default=1000)
    temperature = fields.Float(string="Température", default=0.7, help="Créativité du modèle (0-1)")
    
    # Statut
    active = fields.Boolean(string="Actif", default=True, tracking=True)
    is_default = fields.Boolean(string="Configuration par Défaut", tracking=True)
    
    @api.depends('oauth_expires_at')
    def _compute_oauth_status(self):
        """Calcule le statut de connexion OAuth"""
        now = fields.Datetime.now()
        for record in self:
            # Check if we have a token stored in secure parameters
            has_token = bool(record._get_secure_param('oauth_token'))
            if has_token and record.oauth_expires_at:
                expires_at = fields.Datetime.from_string(record.oauth_expires_at)
                record.is_oauth_connected = expires_at > now
            else:
                record.is_oauth_connected = False
    
    def get_oauth_authorization(self):
        """
        Returns the OAuth authorization header if the token is valid
        Returns False if token is invalid or expired
        """
        self.ensure_one()
        oauth_token = self._get_secure_param('oauth_token')
        if not oauth_token or not self.oauth_expires_at:
            return False
            
        # Get token from secure storage
        oauth_token = self._get_secure_param('oauth_token')
        
        # Check if token is expired
        expires_at = fields.Datetime.from_string(self.oauth_expires_at)
        if expires_at <= fields.Datetime.now():
            # Try to refresh token if we have a refresh token
            if not self.oauth_refresh_token or not self._refresh_oauth_token():
                return False
                
        return {'Authorization': f'Bearer {self.oauth_token}'}
        
    def _compute_oauth_token(self):
        """Compute method for oauth_token field"""
        for record in self:
            record.oauth_token = record._get_secure_param('oauth_token')
    
    def _inverse_oauth_token(self):
        """Inverse method for oauth_token field"""
        for record in self:
            record._set_secure_param('oauth_token', record.oauth_token or False)
    
    def _compute_oauth_refresh_token(self):
        """Compute method for oauth_refresh_token field"""
        for record in self:
            record.oauth_refresh_token = record._get_secure_param('oauth_refresh_token')
    
    def _inverse_oauth_refresh_token(self):
        """Inverse method for oauth_refresh_token field"""
        for record in self:
            record._set_secure_param('oauth_refresh_token', record.oauth_refresh_token or False)
    
    def _refresh_oauth_token(self):
        """
        Attempts to refresh the OAuth token using the refresh token
        Returns True if successful, False otherwise
        """
        self.ensure_one()
        refresh_token = self._get_secure_param('oauth_refresh_token')
        if not refresh_token:
            _logger.warning("No refresh token available for %s", self.provider_type)
            return False
            
        try:
            # This should be handled by the OAuth controller
            _logger.warning("Token refresh should be handled by the OAuth controller")
            return False
            
        except Exception as e:
            _logger.error("Failed to refresh OAuth token: %s", str(e), exc_info=True)
            return False
    
    def disconnect_oauth(self):
        """Disconnect OAuth by clearing tokens"""
        # Clear secure parameters
        self._set_secure_param('oauth_token', None)
        self._set_secure_param('oauth_refresh_token', None)
        
        # Clear regular fields
        self.write({
            'oauth_expires_at': False,
            'oauth_token_initialized': False,
        })
    
    def _oauth_login_openai(self):
        """Connexion OAuth OpenAI (ChatGPT)"""
        # Note: OpenAI ne supporte pas OAuth standard, utiliser API key
        return {
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'params': {
                'title': 'Information',
                'message': 'OpenAI utilise des clés API. Veuillez configurer votre clé API dans les paramètres.',
                'type': 'info',
            }
        }
    
    @api.model
    def write(self, vals):
        # Secure token handling
        if 'oauth_token' in vals:
            self._set_secure_param('oauth_token', vals.pop('oauth_token'))
        if 'oauth_refresh_token' in vals:
            self._set_secure_param('oauth_refresh_token', vals.pop('oauth_refresh_token'))
            
        # Ensure only one default configuration per provider type
        if 'is_default' in vals and vals.get('is_default'):
            # Find other default configs of the same provider type
            other_defaults = self.search([
                ('provider_type', '=', self.provider_type),
                ('is_default', '=', True),
                ('id', '!=', self.id)
            ])
            if other_defaults:
                other_defaults.write({'is_default': False})
                
        return super(AIProviderConfig, self).write(vals)
    
    def test_connection(self):
        """Test la connexion avec le fournisseur IA"""
        try:
            result = self.generate_content("Test de connexion", test_mode=True)
            if result:
                return {
                    'type': 'ir.actions.client',
                    'tag': 'display_notification',
                    'params': {
                        'title': 'Connexion réussie',
                        'message': f'La connexion avec {self.provider_type} fonctionne correctement.',
                        'type': 'success',
                    }
                }
        except Exception as e:
            return {
                'type': 'ir.actions.client',
                'tag': 'display_notification',
                'params': {
                    'title': 'Erreur de connexion',
                    'message': f'Impossible de se connecter: {str(e)}',
                    'type': 'danger',
                }
            }
    
    def generate_content(self, prompt, context=None, test_mode=False):
        """Génère du contenu avec le fournisseur IA configuré"""
        if not self.active:
            raise UserError("Cette configuration n'est pas active.")
        
        try:
            if self.provider_type == 'openai':
                return self._call_openai_api(prompt, context, test_mode)
            elif self.provider_type == 'google':
                return self._call_google_api(prompt, context, test_mode)
            elif self.provider_type == 'microsoft':
                return self._call_microsoft_api(prompt, context, test_mode)
            elif self.provider_type == 'ollama':
                return self._call_ollama_api(prompt, context, test_mode)
            else:
                raise UserError(f"Fournisseur non supporté: {self.provider_type}")
                
        except Exception as e:
            _logger.error(f"Erreur lors de la génération de contenu: {e}")
            if test_mode:
                raise
            return f"Erreur lors de la génération: {str(e)}"
    
    def _call_openai_api(self, prompt, context=None, test_mode=False):
        """Appel à l'API OpenAI (ChatGPT)"""
        headers = {
            "Content-Type": "application/json"
        }
        
        # Use OAuth token if OAuth method selected, otherwise use API key
        if self.auth_method == 'oauth':
            if not self.oauth_token:
                raise ValidationError("OAuth non connecté pour OpenAI")
            headers["Authorization"] = f"Bearer {self.oauth_token}"
        else:
            if not self.api_key:
                raise ValidationError("Clé API OpenAI requise")
            headers["Authorization"] = f"Bearer {self.api_key}"
        
        url = self.api_url or "https://api.openai.com/v1/chat/completions"
        data = {
            "model": self.model_name or "gpt-3.5-turbo",
            "messages": [{"role": "user", "content": prompt}],
            "max_tokens": 10 if test_mode else self.max_tokens,
            "temperature": self.temperature
        }
        
        if test_mode:
            data["messages"] = [{"role": "user", "content": "Hello"}]
        
        response = requests.post(url, headers=headers, json=data, timeout=30)
        response.raise_for_status()
        
        result = response.json()
        return result['choices'][0]['message']['content']
    
    def _call_google_api(self, prompt, context=None, test_mode=False):
        """Appel à l'API Google Gemini"""
        headers = {
            "Content-Type": "application/json"
        }
        
        data = {
            "contents": [{"parts": [{"text": prompt if not test_mode else "Hello"}]}],
            "generationConfig": {
                "maxOutputTokens": 10 if test_mode else self.max_tokens,
                "temperature": self.temperature
            }
        }
        
        # Use OAuth token if OAuth method selected, otherwise use API key
        if self.auth_method == 'oauth':
            if not self.oauth_token:
                raise ValidationError("OAuth non connecté pour Google")
            # For Google OAuth, we would typically use the token in the Authorization header
            headers["Authorization"] = f"Bearer {self.oauth_token}"
            url = self.api_url or f"https://generativelanguage.googleapis.com/v1/models/{self.model_name or 'gemini-pro'}:generateContent"
            # Google OAuth typically requires a different approach - this is a simplified version
            response = requests.post(f"{url}?key={self.oauth_token}", headers=headers, json=data, timeout=30)
        else:
            if not self.api_key:
                raise ValidationError("Clé API Google requise")
            url = self.api_url or f"https://generativelanguage.googleapis.com/v1/models/{self.model_name or 'gemini-pro'}:generateContent"
            response = requests.post(f"{url}?key={self.api_key}", headers=headers, json=data, timeout=30)
        
        response.raise_for_status()
        
        result = response.json()
        return result['candidates'][0]['content']['parts'][0]['text']
    
    def _call_microsoft_api(self, prompt, context=None, test_mode=False):
        """Appel à l'API Microsoft Azure OpenAI"""
        headers = {
            "Content-Type": "application/json"
        }
        
        # Use OAuth token if OAuth method selected, otherwise use API key
        if self.auth_method == 'oauth':
            if not self.oauth_token:
                raise ValidationError("OAuth non connecté pour Microsoft")
            # For Microsoft OAuth, we would typically use the token in the Authorization header
            headers["Authorization"] = f"Bearer {self.oauth_token}"
        else:
            if not self.api_key:
                raise ValidationError("Clé API Microsoft Azure requise")
            headers["api-key"] = self.api_key
        
        if not self.api_url:
            raise ValidationError("URL API Azure requise")
        
        data = {
            "messages": [{"role": "user", "content": prompt if not test_mode else "Hello"}],
            "max_tokens": 10 if test_mode else self.max_tokens,
            "temperature": self.temperature
        }
        
        response = requests.post(self.api_url, headers=headers, json=data, timeout=30)
        response.raise_for_status()
        
        result = response.json()
        return result['choices'][0]['message']['content']
    
    def _call_ollama_api(self, prompt, context=None, test_mode=False):
        """Appel à l'API Ollama locale"""
        url = self.api_url or "http://localhost:11434/api/generate"
        
        data = {
            "model": self.model_name or "llama2",
            "prompt": prompt if not test_mode else "Hello",
            "stream": False,
            "options": {
                "num_predict": 10 if test_mode else self.max_tokens,
                "temperature": self.temperature
            }
        }
        
        response = requests.post(url, json=data, timeout=60)
        response.raise_for_status()
        
        result = response.json()
        return result.get('response', '')

    @api.model
    def get_default_config(self):
        """Récupère la configuration par défaut"""
        default_config = self.search([('is_default', '=', True), ('active', '=', True)], limit=1)
        if not default_config:
            default_config = self.search([('active', '=', True)], limit=1)
        return default_config
