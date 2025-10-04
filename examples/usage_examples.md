# Example Usage Scripts

## Basic Examples

### Check DNS delegation
python dns_validator.py delegation example.com

### Check DNS propagation  
python dns_validator.py propagation example.com

### Check specific record type
python dns_validator.py propagation example.com --type MX

### Check with expected value
python dns_validator.py propagation example.com --expected "192.168.1.1"

### Check Cloudflare settings
python dns_validator.py cloudflare example.com

### Full comprehensive check
python dns_validator.py full example.com --verbose

## Advanced Examples

### Validate new A record deployment
python dns_validator.py propagation newserver.example.com --type A --expected "203.0.113.10" --verbose

### Check MX record propagation for email setup
python dns_validator.py propagation example.com --type MX --verbose

### Validate CNAME record
python dns_validator.py propagation www.example.com --type CNAME --expected "example.com."

### Complete domain migration check
python dns_validator.py full example.com --type A --expected "203.0.113.10" --api-token your_cloudflare_token

### Troubleshoot DNS issues with full logging
python dns_validator.py --verbose full problematic-domain.com

## Batch Processing Examples

### Windows Batch Script (check_domains.bat)
```batch
@echo off
echo Checking multiple domains...
python dns_validator.py delegation domain1.com
python dns_validator.py delegation domain2.com  
python dns_validator.py delegation domain3.com
pause
```

### Linux/macOS Shell Script (check_domains.sh)
```bash
#!/bin/bash
domains=("domain1.com" "domain2.com" "domain3.com")

for domain in "${domains[@]}"; do
    echo "Checking $domain..."
    python3 dns_validator.py full "$domain" --verbose
    echo "------------------------"
done
```

### PowerShell Script (check_domains.ps1)
```powershell
$domains = @("domain1.com", "domain2.com", "domain3.com")

foreach ($domain in $domains) {
    Write-Host "Checking $domain..." -ForegroundColor Green
    python dns_validator.py full $domain --verbose
    Write-Host "------------------------" -ForegroundColor Gray
}
```

## Common Use Cases

### 1. After DNS Record Changes
# Wait for propagation and validate
python dns_validator.py propagation example.com --expected "new.ip.address" --verbose

### 2. Domain Migration Validation
# Check all aspects before switching nameservers
python dns_validator.py full example.com --api-token your_token

### 3. Troubleshooting Email Delivery
# Check MX records across all servers
python dns_validator.py propagation example.com --type MX --verbose

### 4. SSL Certificate Validation Prep
# Ensure A records are propagated for domain validation
python dns_validator.py propagation secure.example.com --type A --verbose

### 5. CDN Configuration Check
# Validate CNAME records for CDN setup
python dns_validator.py propagation cdn.example.com --type CNAME --verbose