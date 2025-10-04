# Cloud Provider API Setup Guide

This file provides setup instructions for integrating with various cloud DNS providers.

## 🔐 Secure Credential Management (NEW!)

The DNS Validator now includes a secure credential management system that encrypts and stores your API keys locally. This is the **recommended way** to handle credentials.

### Quick Start
```bash
# Add credentials interactively (most secure)
dns-validator creds add Cloudflare production --interactive

# Add credentials via command line
dns-validator creds add AWS staging --access-key YOUR_KEY --secret-key YOUR_SECRET --region us-east-1

# List stored credentials
dns-validator creds list

# Use stored credentials
dns-validator provider example.com --provider cloudflare --cred-name production

# Test credentials
dns-validator creds test Cloudflare production example.com
```

### Security Features
- 🔒 **AES-256 Encryption**: All credentials encrypted before storage
- 📁 **Secure Storage**: Credentials stored in `~/.dns-validator/` with proper permissions
- 👥 **Multi-Environment**: Store multiple credential sets per provider (dev, staging, prod)
- 🔐 **Interactive Input**: Secure password-style input for sensitive data
- 📤 **Safe Export**: Backup credentials with optional secret masking

---

## Cloudflare

### Setup Steps:
1. Log in to the Cloudflare dashboard
2. Go to "My Profile" → "API Tokens"
3. Create a token with "Zone:Read" permissions
4. Store the token securely using credential management

### 🔐 Recommended Usage (Secure):
```bash
# Store credentials securely
dns-validator creds add Cloudflare production --api-token YOUR_CLOUDFLARE_TOKEN

# Or use interactive mode (most secure)
dns-validator creds add Cloudflare production --interactive

# Use stored credentials
dns-validator provider example.com --provider cloudflare --cred-name production

# Test credentials
dns-validator creds test Cloudflare production example.com
```

### Legacy Usage (Less Secure):
```bash
dns-validator provider example.com --api-token YOUR_CLOUDFLARE_TOKEN
```

## AWS Route 53

### Setup Steps:
1. Create an IAM user with Route53 permissions
2. Attach the `AmazonRoute53ReadOnlyAccess` policy
3. Generate access keys for the user

### Required Permissions:
- `route53:ListHostedZones`
- `route53:GetHostedZone`
- `route53:ListResourceRecordSets`

### 🔐 Recommended Usage (Secure):
```bash
# Store credentials securely
dns-validator creds add AWS production --access-key YOUR_ACCESS_KEY --secret-key YOUR_SECRET_KEY --region us-east-1

# Or use interactive mode (most secure)
dns-validator creds add AWS production --interactive

# Use stored credentials
dns-validator provider example.com --provider aws --cred-name production

# Test credentials
dns-validator creds test AWS production example.com
```

### Legacy Usage:
```bash
# Using access keys directly
dns-validator provider example.com --access-key YOUR_ACCESS_KEY --secret-key YOUR_SECRET_KEY

# Using default AWS credentials
dns-validator provider example.com
```

### Prerequisites:
```bash
pip install boto3
```

## Google Cloud DNS

### Setup Steps:
1. Create a service account in Google Cloud Console
2. Download the service account JSON file
3. Grant the service account "DNS Reader" role
4. Note your project ID

### Required Roles:
- `roles/dns.reader`

### 🔐 Recommended Usage (Secure):
```bash
# Store credentials securely with service account file
dns-validator creds add "Google Cloud" production --service-account /path/to/service-account.json --project-id YOUR_PROJECT

# Or use interactive mode (most secure)
dns-validator creds add "Google Cloud" production --interactive

# Use stored credentials
dns-validator provider example.com --provider "google cloud" --cred-name production

# Test credentials
dns-validator creds test "Google Cloud" production example.com
```

### Legacy Usage:
```bash
# Using service account file directly
dns-validator provider example.com --service-account /path/to/service-account.json --project-id YOUR_PROJECT

# Using service account JSON string
dns-validator provider example.com --service-account '{"type":"service_account",...}' --project-id YOUR_PROJECT
```

### Prerequisites:
```bash
pip install google-cloud-dns
```

## Azure DNS

### Setup Steps:
1. Create an App Registration in Azure AD
2. Generate a client secret
3. Grant "DNS Zone Contributor" or "Reader" role to the app
4. Note your subscription ID, tenant ID, client ID, and resource group

### Required Roles:
- `DNS Zone Contributor` (for full access)
- `Reader` (for read-only access)

### 🔐 Recommended Usage (Secure):
```bash
# Store credentials securely
dns-validator creds add Azure production --subscription-id SUB_ID --tenant-id TENANT_ID --client-id CLIENT_ID --client-secret CLIENT_SECRET --resource-group RG_NAME

# Or use interactive mode (most secure)
dns-validator creds add Azure production --interactive

# Use stored credentials
dns-validator provider example.com --provider azure --cred-name production

# Test credentials
dns-validator creds test Azure production example.com
```

### Legacy Usage:
```bash
# Using service principal directly
dns-validator provider example.com --subscription-id SUB_ID --tenant-id TENANT_ID --client-id CLIENT_ID --client-secret CLIENT_SECRET --resource-group RG_NAME

# Using default Azure credentials (Azure CLI, managed identity)
dns-validator provider example.com --subscription-id SUB_ID --resource-group RG_NAME
```

### Prerequisites:
```bash
pip install azure-mgmt-dns azure-identity
```

## DigitalOcean

### Setup Steps:
1. Go to DigitalOcean Control Panel → API
2. Generate a new Personal Access Token
3. Grant "Read" permissions (or "Write" for full access)

### 🔐 Recommended Usage (Secure):
```bash
# Store credentials securely
dns-validator creds add DigitalOcean production --api-token YOUR_DO_TOKEN

# Or use interactive mode (most secure)
dns-validator creds add DigitalOcean production --interactive

# Use stored credentials
dns-validator provider example.com --provider digitalocean --cred-name production

# Test credentials
dns-validator creds test DigitalOcean production example.com
```

### Legacy Usage:
```bash
dns-validator provider example.com --api-token YOUR_DO_TOKEN
```

## Environment Variables

You can also set credentials using environment variables:

### AWS Route 53
```bash
export AWS_ACCESS_KEY_ID=your_access_key
export AWS_SECRET_ACCESS_KEY=your_secret_key
export AWS_DEFAULT_REGION=us-east-1
```

### Google Cloud DNS
```bash
export GOOGLE_APPLICATION_CREDENTIALS=/path/to/service-account.json
```

### Azure DNS
```bash
export AZURE_CLIENT_ID=your_client_id
export AZURE_CLIENT_SECRET=your_client_secret
export AZURE_TENANT_ID=your_tenant_id
export AZURE_SUBSCRIPTION_ID=your_subscription_id
```

### Cloudflare
```bash
export CLOUDFLARE_API_TOKEN=your_token
```

### DigitalOcean
```bash
export DIGITALOCEAN_TOKEN=your_token
```

## 🔐 Advanced Credential Management

### Managing Multiple Environments
```bash
# Add credentials for different environments
dns-validator creds add Cloudflare staging --api-token STAGING_TOKEN
dns-validator creds add Cloudflare production --api-token PROD_TOKEN
dns-validator creds add AWS dev --access-key DEV_KEY --secret-key DEV_SECRET --region us-west-2
dns-validator creds add AWS prod --access-key PROD_KEY --secret-key PROD_SECRET --region us-east-1

# List all stored credentials
dns-validator creds list

# Use specific environment
dns-validator provider example.com --provider cloudflare --cred-name staging
dns-validator provider example.com --provider aws --cred-name prod
```

### Credential Operations
```bash
# Edit existing credentials
dns-validator creds edit Cloudflare production

# Test credentials with a domain
dns-validator creds test AWS production example.com

# Export credentials for backup (secrets masked)
dns-validator creds export backup.json

# Export with secrets (use with extreme caution)
dns-validator creds export full-backup.json --include-secrets

# Delete specific credentials
dns-validator creds delete Cloudflare staging

# Clear all credentials (with confirmation)
dns-validator creds clear
```

### Security Best Practices
1. **Use Interactive Mode**: `--interactive` flag for secure input
2. **Multiple Environments**: Separate credentials for dev/staging/prod
3. **Regular Testing**: Test credentials with `creds test` command
4. **Secure Backups**: Export without secrets for safe backups
5. **Principle of Least Privilege**: Use read-only permissions when possible
6. **Regular Rotation**: Update credentials periodically

### File Locations
- **Credential Storage**: `~/.dns-validator/credentials.enc` (encrypted)
- **Encryption Key**: `~/.dns-validator/key.enc` (machine-specific)
- **Configuration**: Permissions set to 600 (owner read/write only)

## Troubleshooting

### Common Issues:

1. **Import Errors**: Install the required SDK
   ```bash
   pip install boto3 google-cloud-dns azure-mgmt-dns azure-identity
   ```

2. **Permission Denied**: Ensure your credentials have the necessary permissions

3. **Resource Not Found**: Check that the domain exists in your DNS provider

4. **Network Timeouts**: Check your internet connection and API endpoints

### Credential Management Issues:

1. **Permission Denied on Credential Directory**: 
   ```bash
   # Fix permissions (Linux/macOS)
   chmod 700 ~/.dns-validator/
   chmod 600 ~/.dns-validator/*
   ```

2. **Credential Not Found**: 
   ```bash
   # List all stored credentials
   dns-validator creds list
   
   # Check exact provider and credential names
   dns-validator creds test ProviderName credential-name example.com
   ```

3. **Encryption/Decryption Errors**: 
   ```bash
   # Clear and re-add credentials if encryption key is corrupted
   dns-validator creds clear --confirm
   dns-validator creds add ProviderName new-name --interactive
   ```

### Debug Mode:
Use the `--verbose` flag to see detailed error messages:
```bash
# Debug credential issues
dns-validator --verbose creds test Cloudflare production example.com

# Debug provider integration
dns-validator --verbose provider example.com --provider cloudflare --cred-name production

# Debug direct API usage
dns-validator --verbose provider example.com --api-token YOUR_TOKEN
```