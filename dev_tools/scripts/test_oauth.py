#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test script for OAuth AI provider functionality
"""

from odoo import fields
from datetime import datetime, timedelta

def test_oauth_config():
    """Test OAuth configuration for AI providers"""
    print("Testing OAuth AI provider configuration...")
    
    # Create a test Google OAuth configuration
    google_config = {
        'name': 'Google OAuth Test',
        'provider_type': 'google',
        'auth_method': 'oauth',
        'oauth_token': 'test_google_token',
        'oauth_expires_at': fields.Datetime.now() + timedelta(hours=1),
        'model_name': 'gemini-pro',
    }
    
    # Create a test Microsoft OAuth configuration
    microsoft_config = {
        'name': 'Microsoft OAuth Test',
        'provider_type': 'microsoft',
        'auth_method': 'oauth',
        'oauth_token': 'test_microsoft_token',
        'oauth_expires_at': fields.Datetime.now() + timedelta(hours=1),
        'model_name': 'gpt-35-turbo',
    }
    
    # Create a test OpenAI configuration (API key method)
    openai_config = {
        'name': 'OpenAI API Key Test',
        'provider_type': 'openai',
        'auth_method': 'api_key',
        'api_key': 'test_openai_key',
        'model_name': 'gpt-3.5-turbo',
    }
    
    print("OAuth configurations created successfully:")
    print(f"Google: {google_config}")
    print(f"Microsoft: {microsoft_config}")
    print(f"OpenAI: {openai_config}")
    
    return [google_config, microsoft_config, openai_config]

if __name__ == "__main__":
    test_oauth_config()
