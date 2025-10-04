# Cloud Provider API Setup Guide

This file provides setup instructions for integrating with various cloud DNS providers.

## Cloudflare

### Setup Steps:
1. Log in to the Cloudflare dashboard
2. Go to "My Profile" → "API Tokens"
3. Create a token with "Zone:Read" permissions
4. Use the token with `--api-token YOUR_TOKEN`

### Usage:
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

### Usage:
```bash
# Using access keys
dns-validator provider example.com --access-key YOUR_ACCESS_KEY --secret-key YOUR_SECRET_KEY

# Using default AWS credentials (recommended)
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

### Usage:
```bash
# Using service account file
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

### Usage:
```bash
# Using service principal
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

### Usage:
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

## Troubleshooting

### Common Issues:

1. **Import Errors**: Install the required SDK
   ```bash
   pip install boto3 google-cloud-dns azure-mgmt-dns azure-identity
   ```

2. **Permission Denied**: Ensure your credentials have the necessary permissions

3. **Resource Not Found**: Check that the domain exists in your DNS provider

4. **Network Timeouts**: Check your internet connection and API endpoints

### Debug Mode:
Use the `--verbose` flag to see detailed error messages:
```bash
dns-validator --verbose provider example.com --api-token YOUR_TOKEN
```