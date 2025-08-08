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
    
    # OAuth fields
    oauth_token = fields.Char(string="Token OAuth", readonly=True, help="Token d'accès OAuth obtenu après authentification")
    oauth_refresh_token = fields.Char(string="Refresh Token", readonly=True, help="Token de rafraîchissement OAuth")
    oauth_expires_at = fields.Datetime(string="Expiration du Token", readonly=True)
    is_oauth_connected = fields.Boolean(string="OAuth Connecté", compute="_compute_oauth_status", store=False)
    
    # Paramètres
    max_tokens = fields.Integer(string="Tokens Maximum", default=1000)
    temperature = fields.Float(string="Température", default=0.7, help="Créativité du modèle (0-1)")
    
    # Statut
    active = fields.Boolean(string="Actif", default=True, tracking=True)
    is_default = fields.Boolean(string="Configuration par Défaut", tracking=True)
    
    @api.depends('oauth_token', 'oauth_expires_at')
    def _compute_oauth_status(self):
        """Calcule le statut de connexion OAuth"""
        for record in self:
            if record.oauth_token and record.oauth_expires_at:
                record.is_oauth_connected = record.oauth_expires_at > fields.Datetime.now()
            else:
                record.is_oauth_connected = False
    
    def oauth_login(self):
        """Initie le processus de connexion OAuth"""
        if self.provider_type == 'google':
            return self._oauth_login_google()
        elif self.provider_type == 'microsoft':
            return self._oauth_login_microsoft()
        elif self.provider_type == 'openai':
            return self._oauth_login_openai()
        else:
            raise UserError(f"OAuth non supporté pour {self.provider_type}")
    
    def _oauth_login_google(self):
        """Connexion OAuth Google"""
        # URL de redirection OAuth Google
        google_oauth_url = "https://accounts.google.com/o/oauth2/auth"
        client_id = "your-google-client-id"  # À configurer
        redirect_uri = f"{self.env['ir.config_parameter'].sudo().get_param('web.base.url')}/ai/oauth/google/callback"
        scope = "openid email profile"
        
        auth_url = f"{google_oauth_url}?client_id={client_id}&redirect_uri={redirect_uri}&scope={scope}&response_type=code&access_type=offline"
        
        return {
            'type': 'ir.actions.act_url',
            'url': auth_url,
            'target': 'new',
        }
    
    def _oauth_login_microsoft(self):
        """Connexion OAuth Microsoft"""
        # URL de redirection OAuth Microsoft
        microsoft_oauth_url = "https://login.microsoftonline.com/common/oauth2/v2.0/authorize"
        client_id = "your-microsoft-client-id"  # À configurer
        redirect_uri = f"{self.env['ir.config_parameter'].sudo().get_param('web.base.url')}/ai/oauth/microsoft/callback"
        scope = "openid email profile"
        
        auth_url = f"{microsoft_oauth_url}?client_id={client_id}&redirect_uri={redirect_uri}&scope={scope}&response_type=code"
        
        return {
            'type': 'ir.actions.act_url',
            'url': auth_url,
            'target': 'new',
        }
    
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
    def create(self, vals):
        # Ensure only one default configuration
        if vals.get('is_default'):
            self.search([('is_default', '=', True)]).write({'is_default': False})
        return super().create(vals)
    
    def write(self, vals):
        # Ensure only one default configuration
        if vals.get('is_default'):
            self.search([('is_default', '=', True), ('id', '!=', self.id)]).write({'is_default': False})
        return super().write(vals)
    
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
