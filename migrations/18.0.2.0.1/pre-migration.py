"""
Migration script to securely move OAuth tokens to ir.config_parameter
"""

def migrate(cr, version):
    if not version:
        return
        
    # Import inside function to avoid import errors during Odoo startup
    import logging
    from odoo import api, SUPERUSER_ID
    
    _logger = logging.getLogger(__name__)
    
    env = api.Environment(cr, SUPERUSER_ID, {})
    
    # Find all AI provider configs with OAuth tokens
    providers = env['ai.provider.config'].search([
        '|',
        ('oauth_token', '!=', False),
        ('oauth_refresh_token', '!=', False)
    ])
    
    migrated = 0
    for provider in providers:
        try:
            # Only migrate if we have tokens in the database
            if provider.oauth_token or provider.oauth_refresh_token:
                # Store tokens in secure parameters
                provider._set_secure_param('oauth_token', provider.oauth_token)
                provider._set_secure_param('oauth_refresh_token', provider.oauth_refresh_token)
                
                # Clear the plaintext tokens
                cr.execute("""
                    UPDATE ai_provider_config 
                    SET oauth_token = NULL, 
                        oauth_refresh_token = NULL
                    WHERE id = %s
                """, (provider.id,))
                migrated += 1
                
        except Exception as e:
            _logger.error("Failed to migrate tokens for provider %s: %s", provider.id, str(e))
            continue
    
    _logger.info("Successfully migrated %d OAuth tokens to secure storage", migrated)
