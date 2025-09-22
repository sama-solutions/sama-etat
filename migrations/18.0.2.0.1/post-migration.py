"""
Post-migration script to verify and finalize OAuth security updates
"""

def migrate(cr, version):
    if not version:
        return
        
    # Import inside function to avoid import errors during Odoo startup
    import logging
    from odoo import api, SUPERUSER_ID
    
    _logger = logging.getLogger(__name__)
    
    env = api.Environment(cr, SUPERUSER_ID, {})
    
    # Verify all tokens were migrated successfully
    providers = env['ai.provider.config'].search([])
    migrated_count = 0
    error_count = 0
    
    for provider in providers:
        try:
            # Check if we have any plaintext tokens that need migration
            cr.execute("""
                SELECT oauth_token, oauth_refresh_token 
                FROM ai_provider_config 
                WHERE id = %s 
                AND (oauth_token IS NOT NULL OR oauth_refresh_token IS NOT NULL)
                LIMIT 1
            """, (provider.id,))
            
            result = cr.dictfetchone()
            if not result:
                continue
                
            # Log warning about plaintext tokens (should have been migrated in pre-migration)
            _logger.warning(
                "Found plaintext tokens for provider %s that weren't migrated properly. "
                "This might indicate a migration issue.", provider.id
            )
            
            # Attempt to migrate again
            if result.get('oauth_token'):
                provider._set_secure_param('oauth_token', result['oauth_token'])
                
            if result.get('oauth_refresh_token'):
                provider._set_secure_param('oauth_refresh_token', result['oauth_refresh_token'])
                
            # Clear plaintext tokens
            cr.execute("""
                UPDATE ai_provider_config 
                SET oauth_token = NULL, 
                    oauth_refresh_token = NULL
                WHERE id = %s
            """, (provider.id,))
            
            migrated_count += 1
            
        except Exception as e:
            _logger.error("Error during post-migration for provider %s: %s", provider.id, str(e))
            error_count += 1
    
    # Log migration summary
    _logger.info(
        "OAuth security migration completed. Providers processed: %d, Errors: %d",
        migrated_count, error_count
    )
    
    # Verify all sensitive parameters are properly secured
    sensitive_params = env['ir.config_parameter'].search([
        ('key', 'like', 'ai_oauth.secure.%')
    ])
    
    _logger.info("Found %d securely stored OAuth tokens", len(sensitive_params))
