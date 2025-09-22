"""
OAuth 2.0 and OpenID Connect integration tests for SAMA ETAT
"""
import json
import unittest
from unittest.mock import patch, MagicMock
from datetime import datetime, timedelta

from odoo.tests import tagged, HttpCase, new_test_user
from odoo import fields
from odoo.exceptions import ValidationError, UserError

from ..utils.oauth_utils import OAuthUtils

@tagged('post_install', '-at_install', 'oauth')
class TestOAuthFlows(HttpCase):
    """Test OAuth 2.0 and OpenID Connect flows"""
    
    def setUp(self):
        super().setUp()
        
        # Create test user
        self.test_user = new_test_user(
            self.env, 
            login='test_oauth_user',
            groups='base.group_user',
            name='Test OAuth User',
            email='test_oauth@example.com',
        )
        
        # Create test provider config
        self.provider = self.env['ai.provider.config'].create({
            'name': 'Google OAuth Test',
            'provider_type': 'google',
            'auth_method': 'oauth',
            'is_default': True,
        })
        
        # Set test OAuth parameters
        self.env['ir.config_parameter'].sudo().set_param('ai_oauth.google.client_id', 'test_client_id')
        self.env['ir.config_parameter'].sudo().set_param('ai_oauth.google.client_secret', 'test_client_secret')
        
        # Test tokens
        self.test_access_token = 'test_access_token_123'
        self.test_refresh_token = 'test_refresh_token_456'
        self.test_id_token = (
            'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.'
            'eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IlRlc3QgVXNlciIsImlhdCI6MTUxNjIzOTAyMn0.'
            'dytDWJ4e3lheBGkyYk7UJyobIXa5qT0GvU9JynwVN7w'
        )
        
        # Mock responses
        self.mock_token_response = {
            'access_token': self.test_access_token,
            'refresh_token': self.test_refresh_token,
            'expires_in': 3600,
            'token_type': 'Bearer',
            'id_token': self.test_id_token,
        }
    
    def test_oauth_utils_pkce_generation(self):
        """Test PKCE code generation and verification"""
        oauth_utils = OAuthUtils()
        verifier, challenge = oauth_utils.generate_pkce_codes()
        
        self.assertIsNotNone(verifier)
        self.assertIsNotNone(challenge)
        self.assertGreaterEqual(len(verifier), 43)
        self.assertLessEqual(len(verifier), 128)
        self.assertEqual(len(challenge), 43)  # Base64 URL-safe without padding
    
    @patch('requests.post')
    def test_token_refresh(self, mock_post):
        """Test OAuth token refresh flow"""
        # Setup mock response
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            'access_token': 'new_access_token',
            'expires_in': 3600,
            'token_type': 'Bearer',
        }
        mock_post.return_value = mock_response
        
        # Test token refresh
        result = OAuthUtils().refresh_access_token('google', 'test_refresh_token')
        
        # Verify results
        self.assertIsNotNone(result)
        self.assertEqual(result['access_token'], 'new_access_token')
        self.assertIn('expires_at', result)
        
        # Verify request was made correctly
        mock_post.assert_called_once()
        _, kwargs = mock_post.call_args
        self.assertIn('data', kwargs)
        self.assertEqual(kwargs['data']['grant_type'], 'refresh_token')
        self.assertEqual(kwargs['data']['refresh_token'], 'test_refresh_token')
    
    def test_secure_token_storage(self):
        """Test secure token storage in ir.config_parameter"""
        # Store tokens
        self.provider.oauth_token = self.test_access_token
        self.provider.oauth_refresh_token = self.test_refresh_token
        
        # Verify tokens are stored securely (not in the database)
        self.assertFalse(self.provider.oauth_token)  # Should be computed
        self.assertFalse(self.provider.oauth_refresh_token)  # Should be computed
        
        # Verify tokens can be retrieved
        self.assertEqual(
            self.provider._get_secure_param('oauth_token'),
            self.test_access_token
        )
        self.assertEqual(
            self.provider._get_secure_param('oauth_refresh_token'),
            self.test_refresh_token
        )
    
    @patch('requests.post')
    def test_token_revocation(self, mock_post):
        """Test OAuth token revocation"""
        # Setup mock response
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_post.return_value = mock_response
        
        # Test token revocation
        result = OAuthUtils().revoke_tokens('google', 'test_token')
        
        # Verify results
        self.assertTrue(result)
        mock_post.assert_called_once()
    
    def test_oauth_status_computation(self):
        """Test OAuth status computation"""
        # Initial state - not configured
        self.assertEqual(self.provider.oauth_status, 'not_configured')
        
        # Set token with future expiration
        future = fields.Datetime.to_string(datetime.utcnow() + timedelta(hours=1))
        self.provider._set_secure_param('oauth_token', self.test_access_token)
        self.provider.oauth_expires_at = future
        self.provider.invalidate_recordset()
        
        # Should be connected
        self.assertEqual(self.provider.oauth_status, 'connected')
        
        # Set token with past expiration but with refresh token
        past = fields.Datetime.to_string(datetime.utcnow() - timedelta(hours=1))
        self.provider.oauth_expires_at = past
        self.provider._set_secure_param('oauth_refresh_token', self.test_refresh_token)
        self.provider.invalidate_recordset()
        
        # Should still be connected because we have a refresh token
        self.assertEqual(self.provider.oauth_status, 'connected')
        
        # Remove refresh token
        self.provider._set_secure_param('oauth_refresh_token', None)
        self.provider.invalidate_recordset()
        
        # Should be expired
        self.assertEqual(self.provider.oauth_status, 'expired')
    
    def test_disconnect_oauth(self):
        """Test OAuth disconnect functionality"""
        # Set up test tokens
        self.provider._set_secure_param('oauth_token', self.test_access_token)
        self.provider._set_secure_param('oauth_refresh_token', self.test_refresh_token)
        self.provider.oauth_expires_at = fields.Datetime.to_string(datetime.utcnow() + timedelta(hours=1))
        
        # Verify tokens are set
        self.assertTrue(self.provider._get_secure_param('oauth_token'))
        self.assertTrue(self.provider._get_secure_param('oauth_refresh_token'))
        
        # Disconnect
        self.provider.disconnect_oauth()
        
        # Verify tokens are cleared
        self.assertFalse(self.provider._get_secure_param('oauth_token'))
        self.assertFalse(self.provider._get_secure_param('oauth_refresh_token'))
        self.assertFalse(self.provider.oauth_expires_at)
    
    @patch('requests.post')
    def test_controller_oauth_flow(self, mock_post):
        """Test complete OAuth flow through the controller"""
        # Setup mock response for token endpoint
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = self.mock_token_response
        mock_post.return_value = mock_response
        
        # Start OAuth flow
        with self.subTest('Start OAuth flow'):
            response = self.url_open('/ai/oauth/google/start')
            self.assertEqual(response.status_code, 200)
            
            # Should redirect to Google's auth page
            self.assertIn('https://accounts.google.com/o/oauth2/v2/auth', response.url)
        
        # Simulate callback with code
        with self.subTest('OAuth callback'):
            # Get the session to set up test data
            session = self.authenticate('test_oauth_user', 'test_oauth_user')
            session['oauth_code_verifier'] = 'test_verifier'
            session['oauth_state'] = 'test_state'
            session['oauth_nonce'] = 'test_nonce'
            session.save_request()
            
            # Make callback request
            response = self.url_open(
                '/ai/oauth/google/callback?'
                'code=test_auth_code&state=test_state',
                timeout=30
            )
            
            # Should redirect to success page
            self.assertEqual(response.status_code, 200)
            self.assertIn('oauth/success', response.url)
            
            # Verify tokens were stored
            self.assertEqual(
                self.provider._get_secure_param('oauth_token'),
                self.test_access_token
            )
            self.assertEqual(
                self.provider._get_secure_param('oauth_refresh_token'),
                self.test_refresh_token
            )
    
    def test_secure_redirect_validation(self):
        """Test secure redirect URL validation"""
        oauth_utils = OAuthUtils()
        
        # Test valid URLs
        self.assertTrue(oauth_utils._is_safe_redirect_url('/dashboard'))
        self.assertTrue(oauth_utils._is_safe_redirect_url('https://example.com/relative/path'))
        
        # Test invalid URLs
        self.assertFalse(oauth_utils._is_safe_redirect_url('http://evil.com/steal-cookies'))
        self.assertFalse(oauth_utils._is_safe_redirect_url('javascript:alert(1)'))
        
        # Test with configured base URL
        self.env['ir.config_parameter'].sudo().set_param('web.base.url', 'https://example.com')
        self.assertTrue(oauth_utils._is_safe_redirect_url('https://example.com/valid-path'))
        self.assertFalse(oauth_utils._is_safe_redirect_url('https://evil.com/steal-cookies'))

    @patch('requests.post')
    def test_token_refresh_flow(self, mock_post):
        """Test automatic token refresh when token is expired"""
        # Set up expired token
        past = fields.Datetime.to_string(datetime.utcnow() - timedelta(hours=1))
        self.provider._set_secure_param('oauth_token', 'expired_token')
        self.provider._set_secure_param('oauth_refresh_token', 'test_refresh_token')
        self.provider.oauth_expires_at = past
        
        # Setup mock refresh response
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            'access_token': 'new_access_token',
            'expires_in': 3600,
            'token_type': 'Bearer',
        }
        mock_post.return_value = mock_response
        
        # Try to get authorization header (should trigger refresh)
        auth_header = self.provider.get_oauth_authorization()
        
        # Verify new token is used
        self.assertIsNotNone(auth_header)
        self.assertIn('new_access_token', auth_header.get('Authorization', ''))
        
        # Verify token was refreshed
        self.assertEqual(
            self.provider._get_secure_param('oauth_token'),
            'new_access_token'
        )
        self.assertIsNotNone(self.provider.oauth_expires_at)
