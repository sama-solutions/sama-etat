"""
OAuth2/OIDC utility functions for secure token management
"""
import logging
import json
import base64
import hashlib
import secrets
import time
from datetime import datetime, timedelta
from urllib.parse import urlencode, urlparse, parse_qs

import requests
import jwt
from odoo import _, fields, models, api
from odoo.exceptions import ValidationError, UserError
from odoo.http import request

_logger = logging.getLogger(__name__)

class OAuthUtils:
    """Utility class for OAuth2/OIDC operations"""
    
    @staticmethod
    def generate_pkce_codes():
        """Generate PKCE code verifier and challenge"""
        # Generate a random code verifier (43-128 characters)
        code_verifier = base64.urlsafe_b64encode(
            secrets.token_bytes(32)
        ).decode('utf-8').rstrip('=')
        
        # Generate code challenge (S256 method)
        code_challenge = base64.urlsafe_b64encode(
            hashlib.sha256(code_verifier.encode('utf-8')).digest()
        ).decode('utf-8').rstrip('=')
        
        return code_verifier, code_challenge
    
    @classmethod
    def get_oauth_config(cls, provider):
        """Get OAuth configuration for the specified provider"""
        icp = request.env['ir.config_parameter'].sudo()
        
        config = {
            'client_id': icp.get_param(f'ai_oauth.{provider}.client_id'),
            'client_secret': icp.get_param(f'ai_oauth.{provider}.client_secret'),
            'auth_uri': '',
            'token_uri': '',
            'userinfo_uri': '',
            'jwks_uri': '',
            'scope': 'openid email profile',
        }
        
        # Configure provider-specific endpoints
        if provider == 'google':
            config.update({
                'auth_uri': 'https://accounts.google.com/o/oauth2/v2/auth',
                'token_uri': 'https://oauth2.googleapis.com/token',
                'userinfo_uri': 'https://www.googleapis.com/oauth2/v3/userinfo',
                'jwks_uri': 'https://www.googleapis.com/oauth2/v3/certs',
                'scope': 'openid email profile https://www.googleapis.com/auth/cloud-platform',
            })
        elif provider == 'microsoft':
            config.update({
                'auth_uri': 'https://login.microsoftonline.com/common/oauth2/v2.0/authorize',
                'token_uri': 'https://login.microsoftonline.com/common/oauth2/v2.0/token',
                'userinfo_uri': 'https://graph.microsoft.com/oidc/userinfo',
                'jwks_uri': 'https://login.microsoftonline.com/common/discovery/v2.0/keys',
                'scope': 'openid email profile offline_access',
            })
            
        return config
    
    @classmethod
    def validate_id_token(cls, provider, id_token, nonce=None):
        """Validate ID token signature and claims"""
        try:
            config = cls.get_oauth_config(provider)
            
            # Get JWKS keys
            jwks_client = jwt.PyJWKClient(config['jwks_uri'])
            signing_key = jwks_client.get_signing_key_from_jwt(id_token)
            
            # Decode and verify token
            payload = jwt.decode(
                id_token,
                signing_key.key,
                algorithms=['RS256'],
                audience=config['client_id'],
                options={
                    'verify_iss': True,
                    'verify_aud': True,
                    'verify_iat': True,
                    'verify_exp': True,
                    'verify_nbf': True,
                },
                issuer={
                    'google': 'https://accounts.google.com',
                    'microsoft': 'https://login.microsoftonline.com/9188040d-6c67-4c5b-b112-36a304b66dad/v2.0'
                }.get(provider)
            )
            
            # Validate nonce if provided
            if nonce and payload.get('nonce') != nonce:
                _logger.error("Invalid nonce in ID token")
                return False
                
            return payload
            
        except Exception as e:
            _logger.error("ID token validation failed: %s", str(e), exc_info=True)
            return False
    
    @classmethod
    def refresh_access_token(cls, provider, refresh_token):
        """Refresh OAuth access token using refresh token"""
        try:
            config = cls.get_oauth_config(provider)
            
            params = {
                'client_id': config['client_id'],
                'client_secret': config['client_secret'],
                'refresh_token': refresh_token,
                'grant_type': 'refresh_token',
            }
            
            response = requests.post(
                config['token_uri'],
                data=params,
                timeout=30,
                headers={'Accept': 'application/json'}
            )
            response.raise_for_status()
            
            token_data = response.json()
            
            # Calculate expiration time
            expires_in = int(token_data.get('expires_in', 3600))
            expires_at = fields.Datetime.to_string(
                datetime.utcnow() + timedelta(seconds=expires_in - 60)  # 60s buffer
            )
            
            return {
                'access_token': token_data.get('access_token'),
                'refresh_token': token_data.get('refresh_token', refresh_token),  # Keep existing if not provided
                'expires_at': expires_at,
                'token_type': token_data.get('token_type', 'Bearer'),
                'scope': token_data.get('scope', ''),
            }
            
        except Exception as e:
            _logger.error("Failed to refresh %s token: %s", provider, str(e), exc_info=True)
            return None
    
    @classmethod
    def revoke_tokens(cls, provider, token, token_type_hint='access_token'):
        """Revoke OAuth tokens"""
        try:
            if provider == 'google':
                revoke_url = 'https://oauth2.googleapis.com/revoke'
            elif provider == 'microsoft':
                revoke_url = 'https://login.microsoftonline.com/common/oauth2/v2.0/logout'
            else:
                _logger.warning("Token revocation not supported for provider: %s", provider)
                return False
                
            params = {
                'token': token,
                'token_type_hint': token_type_hint,
            }
            
            response = requests.post(
                revoke_url,
                data=params,
                timeout=10,
                headers={'Content-Type': 'application/x-www-form-urlencoded'}
            )
            response.raise_for_status()
            return True
            
        except Exception as e:
            _logger.warning("Failed to revoke %s token: %s", provider, str(e))
            return False
