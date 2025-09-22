# -*- coding: utf-8 -*-

import logging
import unittest
from unittest.mock import patch, MagicMock
from datetime import datetime, timedelta

from odoo.tests import common, tagged
from odoo import fields
from odoo.exceptions import UserError, ValidationError

_logger = logging.getLogger(__name__)

@tagged('post_install', '-at_install')
class TestOAuthFlow(common.TransactionCase):
    """Test OAuth 2.0 flow and token management"""
    
    def setUp(self):
        super(TestOAuthFlow, self).setUp()
        
        # Create test users
        self.user_admin = self.env.ref('base.user_admin')
        self.user_demo = self.env.ref('base.user_demo')
        
        # Create test provider config
        self.provider_google = self.env['ai.provider.config'].create({
            'name': 'Google OAuth Test',
            'provider_type': 'google',
            'auth_method': 'oauth',
        })
        
        # Set test OAuth parameters
        ICP = self.env['ir.config_parameter'].sudo()
        ICP.set_param('ai_oauth.google.client_id', 'test-client-id')
        ICP.set_param('ai_oauth.google.client_secret', 'test-client-secret')
        
        # Test controller
        self.controller = self.env['ir.http'].sudo()._serve_db()
        
    def test_01_oauth_start_flow(self):
        """Test starting OAuth flow"""
        with self.subTest('Test valid provider'):
            with patch('odoo.http.redirect') as mock_redirect:
                mock_redirect.return_value = 'redirect_response'
                result = self.controller.oauth_start('google')
                self.assertEqual(result, 'redirect_response')
                
        with self.subTest('Test invalid provider'):
            with self.assertRaises(UserError):
                self.controller.oauth_start('invalid_provider')
                
    def test_02_oauth_callback(self):
        """Test OAuth callback handling"""
        # Setup test data
        test_state = 'test_state_123'
        test_code = 'test_auth_code_456'
        test_token_data = {
            'access_token': 'test_access_token',
            'refresh_token': 'test_refresh_token',
            'expires_in': 3600,
            'id_token': 'test.id.token',
        }
        
        # Mock session data
        self.controller.request.session = {
            'oauth_state': test_state,
            'oauth_provider': 'google',
            'oauth_code_verifier': 'test_verifier',
            'oauth_nonce': 'test_nonce',
            'oauth_redirect': '/web'
        }
        
        with patch('requests.post') as mock_post:
            # Mock token response
            mock_response = MagicMock()
            mock_response.json.return_value = test_token_data
            mock_response.raise_for_status.return_value = None
            mock_post.return_value = mock_response
            
            # Test successful callback
            with patch('jwt.decode', return_value={'nonce': 'test_nonce'}):
                result = self.controller.oauth_callback(
                    'google', 
                    state=test_state,
                    code=test_code
                )
                self.assertEqual(result.status_code, 303)  # Redirect
                
            # Verify tokens were stored
            self.assertEqual(self.provider_google.oauth_token, 'test_access_token')
            self.assertEqual(self.provider_google.oauth_refresh_token, 'test_refresh_token')
            self.assertTrue(self.provider_google.oauth_expires_at)
            
    def test_03_token_refresh(self):
        """Test token refresh functionality"""
        # Set up expired token
        self.provider_google.write({
            'oauth_token': 'expired_token',
            'oauth_refresh_token': 'valid_refresh_token',
            'oauth_expires_at': fields.Datetime.to_string(datetime.now() - timedelta(hours=1))
        })
        
        test_token_data = {
            'access_token': 'new_access_token',
            'expires_in': 3600,
            'refresh_token': 'new_refresh_token',
        }
        
        with patch('requests.post') as mock_post:
            # Mock refresh response
            mock_response = MagicMock()
            mock_response.json.return_value = test_token_data
            mock_response.raise_for_status.return_value = None
            mock_post.return_value = mock_response
            
            # Trigger refresh
            result = self.provider_google._refresh_oauth_token()
            self.assertTrue(result)
            
            # Verify tokens were updated
            self.assertEqual(self.provider_google.oauth_token, 'new_access_token')
            self.assertEqual(self.provider_google.oauth_refresh_token, 'new_refresh_token')
            self.assertTrue(self.provider_google.oauth_expires_at > fields.Datetime.now())
            
    def test_04_disconnect_provider(self):
        """Test disconnecting OAuth provider"""
        # Set up connected provider
        self.provider_google.write({
            'oauth_token': 'test_token',
            'oauth_refresh_token': 'test_refresh',
            'oauth_expires_at': fields.Datetime.to_string(datetime.now() + timedelta(hours=1))
        })
        
        with patch('requests.post') as mock_post:
            # Mock revoke response
            mock_response = MagicMock()
            mock_response.raise_for_status.return_value = None
            mock_post.return_value = mock_response
            
            # Test disconnect
            result = self.controller.oauth_disconnect('google')
            self.assertEqual(result.status_code, 303)  # Redirect
            
            # Verify tokens were cleared
            self.assertFalse(self.provider_google.oauth_token)
            self.assertFalse(self.provider_google.oauth_refresh_token)
            self.assertFalse(self.provider_google.oauth_expires_at)
            
    def test_05_security_rules(self):
        """Test security rules and access controls"""
        # Test admin can create/read/write/delete
        self.assertTrue(
            self.env['ai.provider.config'].with_user(self.user_admin).check_access_rights('create', raise_exception=False)
        )
        
        # Test regular user can read but not create/write/delete
        with self.assertRaises(AccessError):
            self.env['ai.provider.config'].with_user(self.user_demo).check_access_rights('create', raise_exception=True)
            
        # Test OAuth user can read/write their own records
        self.provider_google.with_user(self.user_demo).read(['name'])
        with self.assertRises(AccessError):
            self.provider_google.with_user(self.user_demo).write({'name': 'Updated'})
            
    def test_06_encrypted_fields(self):
        """Test that sensitive fields are properly encrypted"""
        # Set test data
        test_token = 'sensitive_access_token_123'
        self.provider_google.oauth_token = test_token
        
        # Verify the stored value is encrypted
        db_value = self.env.cr.execute(
            "SELECT oauth_token FROM ai_provider_config WHERE id = %s", 
            (self.provider_google.id,)
        )
        db_token = self.env.cr.fetchone()[0]
        self.assertNotEqual(db_token, test_token)  # Should be encrypted
        
        # Verify decryption works
        self.assertEqual(self.provider_google.oauth_token, test_token)
