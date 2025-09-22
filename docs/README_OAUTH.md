# SAMA ETAT - OAuth 2.0 Integration Guide

This document provides instructions for setting up and configuring OAuth 2.0 authentication with supported AI providers (Google, Microsoft) in the SAMA ETAT Odoo module.

## Prerequisites

- Odoo 16.0 or later
- Python dependencies:
  - `pyjwt` (for JWT token validation)
  - `cryptography` (for token encryption)

## Installation

1. Install the required Python packages:
   ```bash
   pip install pyjwt cryptography
   ```

2. Update the module in Odoo:
   - Go to Apps → Update Apps List
   - Search for "SAMA ETAT"
   - Click "Upgrade"

## Configuration

### 1. System Parameters

Set the following system parameters in Odoo (Settings → Technical → Parameters → System Parameters):

#### Google OAuth
- `ai_oauth.google.client_id` - Your Google OAuth Client ID
- `ai_oauth.google.client_secret` - Your Google OAuth Client Secret

#### Microsoft OAuth
- `ai_oauth.microsoft.client_id` - Your Microsoft App (client) ID
- `ai_oauth.microsoft.client_secret` - Your Microsoft Client Secret
- `ai_oauth.microsoft.tenant_id` - Your Microsoft Tenant ID (or use 'common' for multi-tenant)

### 2. OAuth Redirect URIs

Add the following redirect URIs to your OAuth provider's configuration:

#### Google Cloud Console
1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Navigate to APIs & Services → Credentials
3. Add authorized redirect URI:
   ```
   https://your-odoo-domain.com/ai/oauth/google/callback
   ```

#### Microsoft Azure Portal
1. Go to [Azure Portal](https://portal.azure.com/)
2. Navigate to Azure Active Directory → App registrations → Your app → Authentication
3. Add a new platform: Web
4. Add redirect URI:
   ```
   https://your-odoo-domain.com/ai/oauth/microsoft/callback
   ```

## Usage

### Connecting an AI Provider

1. Go to SAMA ETAT → AI Providers
2. Click "Connect" next to your desired provider (Google/Microsoft)
3. You'll be redirected to the provider's login page
4. After authenticating, you'll be redirected back to Odoo
5. The connection status will be updated automatically

### Disconnecting an AI Provider

1. Go to SAMA ETAT → AI Providers
2. Click "Disconnect" next to the connected provider
3. Confirm the disconnection

## Security Considerations

### Token Storage
- Access tokens and refresh tokens are stored encrypted in the database
- Encryption uses Odoo's database secret key
- Only system administrators can view or modify token data

### Session Security
- OAuth state and nonce values are validated to prevent CSRF attacks
- PKCE (Proof Key for Code Exchange) is used for public clients
- All OAuth endpoints require an authenticated session

### Rate Limiting
- Consider implementing rate limiting for OAuth endpoints
- Monitor for unusual authentication patterns

## Troubleshooting

### Common Issues

#### 1. "Invalid OAuth provider" error
- Verify the provider name is correct (google/microsoft)
- Check that the provider is enabled in the module configuration

#### 2. "Invalid state parameter" error
- Clear your browser cookies and try again
- Ensure your system time is synchronized (NTP recommended)

#### 3. Token refresh failures
- Verify the refresh token is still valid
- Check that the OAuth client configuration allows offline access

### Logs
Check Odoo server logs for detailed error messages:
```bash
tail -f /var/log/odoo/odoo-server.log | grep -i oauth
```

## Development

### Adding New OAuth Providers

1. Update the `_OAUTH_CONFIG` dictionary in `controllers/secure_oauth.py`
2. Add provider-specific token handling in `_exchange_code_for_tokens`
3. Update the UI templates if needed

### Testing

Run the test suite with:
```bash
./odoo-bin -d test_db -i sama_etat --test-enable --stop-after-init
```

## Support

For additional support, please contact the SAMA ETAT development team.
