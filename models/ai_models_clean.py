# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import ValidationError, UserError
import requests
import json
import logging

_logger = logging.getLogger(__name__)

class AIModelConfig(models.Model):
    """Configuration des modèles IA pour la génération de contenu"""
    _name = 'ai.model.config'
    _description = 'Configuration des Modèles IA'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    
    name = fields.Char(string="Nom", required=True, tracking=True)
    model_type = fields.Selection([
        ('openai', 'OpenAI (GPT)'),
        ('google', 'Google (Gemini)'),
        ('microsoft', 'Microsoft (Azure OpenAI)'),
        ('ollama', 'Ollama (Local)')
    ], string="Type de Modèle", required=True, tracking=True)
    
    # Configuration API
    api_key = fields.Char(string="Clé API", help="Clé d'authentification API (laissez vide pour Ollama local)")
    api_url = fields.Char(string="URL API", help="URL de base de l'API")
    model_name = fields.Char(string="Nom du Modèle", help="Nom spécifique du modèle à utiliser")
    
    # Paramètres
    max_tokens = fields.Integer(string="Tokens Maximum", default=1000)
    temperature = fields.Float(string="Température", default=0.7, help="Créativité du modèle (0-1)")
    
    # Statut
    active = fields.Boolean(string="Actif", default=True, tracking=True)
    is_default = fields.Boolean(string="Par Défaut", tracking=True)
    
    @api.model
    def create(self, vals):
        # Ensure only one default model
        if vals.get('is_default'):
            self.search([('is_default', '=', True)]).write({'is_default': False})
        return super().create(vals)
    
    def write(self, vals):
        # Ensure only one default model
        if vals.get('is_default'):
            self.search([('is_default', '=', True), ('id', '!=', self.id)]).write({'is_default': False})
        return super().write(vals)
    
    def test_connection(self):
        """Test la connexion avec le modèle IA"""
        try:
            result = self.generate_content("Test de connexion", test_mode=True)
            if result:
                return {
                    'type': 'ir.actions.client',
                    'tag': 'display_notification',
                    'params': {
                        'title': 'Connexion réussie',
                        'message': 'La connexion avec le modèle IA fonctionne correctement.',
                        'type': 'success',
                    }
                }
        except Exception as e:
            return {
                'type': 'ir.actions.client',
                'tag': 'display_notification',
                'params': {
                    'title': 'Erreur de connexion',
                    'message': f'Impossible de se connecter au modèle IA: {str(e)}',
                    'type': 'danger',
                }
            }
    
    def generate_content(self, prompt, context=None, test_mode=False):
        """Génère du contenu avec le modèle IA configuré"""
        if not self.active:
            raise UserError("Ce modèle IA n'est pas actif.")
        
        try:
            if self.model_type == 'openai':
                return self._call_openai_api(prompt, context, test_mode)
            elif self.model_type == 'google':
                return self._call_google_api(prompt, context, test_mode)
            elif self.model_type == 'microsoft':
                return self._call_microsoft_api(prompt, context, test_mode)
            elif self.model_type == 'ollama':
                return self._call_ollama_api(prompt, context, test_mode)
            else:
                raise UserError(f"Type de modèle non supporté: {self.model_type}")
                
        except Exception as e:
            _logger.error(f"Erreur lors de la génération de contenu: {e}")
            if test_mode:
                raise
            return f"Erreur lors de la génération: {str(e)}"
    
    def _call_openai_api(self, prompt, context=None, test_mode=False):
        """Appel à l'API OpenAI"""
        if not self.api_key:
            raise ValidationError("Clé API OpenAI requise")
        
        url = self.api_url or "https://api.openai.com/v1/chat/completions"
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        data = {
            "model": self.model_name or "gpt-3.5-turbo",
            "messages": [{"role": "user", "content": prompt}],
            "max_tokens": self.max_tokens,
            "temperature": self.temperature
        }
        
        if test_mode:
            data["max_tokens"] = 10
            data["messages"] = [{"role": "user", "content": "Hello"}]
        
        response = requests.post(url, headers=headers, json=data, timeout=30)
        response.raise_for_status()
        
        result = response.json()
        return result['choices'][0]['message']['content']
    
    def _call_google_api(self, prompt, context=None, test_mode=False):
        """Appel à l'API Google Gemini"""
        if not self.api_key:
            raise ValidationError("Clé API Google requise")
        
        url = self.api_url or f"https://generativelanguage.googleapis.com/v1/models/{self.model_name or 'gemini-pro'}:generateContent"
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
        
        response = requests.post(f"{url}?key={self.api_key}", headers=headers, json=data, timeout=30)
        response.raise_for_status()
        
        result = response.json()
        return result['candidates'][0]['content']['parts'][0]['text']
    
    def _call_microsoft_api(self, prompt, context=None, test_mode=False):
        """Appel à l'API Microsoft Azure OpenAI"""
        if not self.api_key:
            raise ValidationError("Clé API Microsoft Azure requise")
        
        if not self.api_url:
            raise ValidationError("URL API Azure requise")
        
        headers = {
            "api-key": self.api_key,
            "Content-Type": "application/json"
        }
        
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
    def get_default_model(self):
        """Récupère le modèle par défaut"""
        default_model = self.search([('is_default', '=', True), ('active', '=', True)], limit=1)
        if not default_model:
            default_model = self.search([('active', '=', True)], limit=1)
        return default_model
