# DNS Validator

A comprehensive cross-platform CLI tool for DNS validation, security analysis, and provider management with advanced features for enterprise environments.

![Python](https://img.shields.io/badge/python-3.7+-blue.svg)
![Platform](https://img.shields.io/badge/platform-Windows%20%7C%20Linux%20%7C%20macOS-lightgrey.svg)
![License](https://img.shields.io/badge/license-GNU%20AGPLv3-blue.svg)
![PyPI](https://img.shields.io/badge/PyPI-dns--validator-blue.svg)

## 📋 Table of Contents

- [Installation](#-installation)
- [Quick Start](#-quick-start)
- [Features Overview](#-features-overview)
- [Command Reference](#-command-reference)
- [Bulk Processing](#-bulk-processing)
- [Security Features](#-security-features)
- [API Integration](#-api-integration)
- [Supported Providers](#-supported-providers)
- [Advanced Usage](#-advanced-usage)
- [Examples](#-examples)
- [Troubleshooting](#-troubleshooting)
- [Contributing](#-contributing)

## 🚀 Installation

### Method 1: pip install (Recommended)

```bash
# Install from PyPI
pip install dns-validator

# Verify installation
dns-validator --help
```

**Available commands after installation:**
```bash
dns-validator [command] [options]    # Primary command
dnsval [command] [options]           # Short alias
python -m dns_validator [command]    # Module execution
```

### Method 2: Clone Repository

```bash
# Clone the repository
git clone https://github.com/HereLiesHugo/dns-validator.git
cd dns-validator

# Install dependencies
pip install -r requirements.txt

# Run directly
python dns_validator_cli.py [command] [options]
```

### System Requirements

- **Python**: 3.7 or higher
- **Operating Systems**: Windows, Linux, macOS
- **Internet Connection**: Required for DNS queries and API calls

## ⚡ Quick Start

```bash
# Basic DNS validation
dns-validator delegation example.com

# Check DNS propagation across multiple servers
dns-validator propagation example.com

# Comprehensive security analysis
dns-validator security-analysis example.com

# Bulk processing multiple domains
dns-validator bulk domains.txt --output report.html

# Manage API credentials securely
dns-validator creds add Cloudflare production --interactive
```

## ✨ Features Overview

### 🔍 **Core DNS Validation**
- **DNS Delegation**: Verify authoritative nameservers and delegation chains
- **Propagation Testing**: Check DNS propagation across 8+ major public DNS servers
- **Provider Detection**: Automatically identify DNS providers from 50+ supported services
- **Multi-Record Support**: A, AAAA, CNAME, MX, NS, TXT, SOA record validation

### 🔐 **Security & DNSSEC**
- **DNSSEC Validation**: Complete DNSSEC chain analysis with DS, DNSKEY, RRSIG verification
- **Security Analysis**: Open resolver detection, amplification vulnerability assessment
- **Certificate Integration**: SSL/TLS analysis, Certificate Transparency monitoring, CAA validation
- **Reverse DNS**: PTR record validation with forward/reverse consistency checking
- **Security Scoring**: Comprehensive 0-100 security scoring system

### 🌍 **Advanced Analysis**
- **Geographic DNS**: Test resolution from 15+ global locations with GeoDNS detection
- **Load Balancer Health**: Multi-endpoint health validation and failover assessment  
- **IPv6 Readiness**: Dual-stack configuration analysis with 0-100 scoring
- **Cache Analysis**: TTL compliance and cache behavior optimization
- **Health Monitoring**: Real-time DNS monitoring with alerting capabilities

### 🚀 **Enterprise Features**
- **Bulk Processing**: Parallel processing of multiple domains with progress tracking
- **Secure Credentials**: AES-256 encrypted API key management for multiple providers
- **Multiple Output Formats**: JSON, HTML, CSV reporting for automation and analysis
- **API Integration**: Deep integration with 10+ DNS provider APIs
- **Cross-Platform**: Native support for Windows, Linux, and macOS

## 📚 Command Reference

### Global Options

```bash
--verbose, -v    # Enable detailed output and debugging information
--help, -h       # Show help message for any command
```

### Core DNS Commands

#### `delegation <domain>`
Verify DNS delegation and authoritative nameservers.

```bash
# Basic delegation check
dns-validator delegation example.com

# Verbose delegation analysis
dns-validator --verbose delegation example.com
```

**Features:**
- Validates authoritative nameservers
- Checks parent delegation consistency  
- Identifies delegation chain issues
- Reports nameserver response times

#### `propagation <domain>`
Test DNS propagation across multiple public DNS servers.

```bash
# Check A record propagation
dns-validator propagation example.com

# Check specific record type
dns-validator propagation example.com --type MX

# Validate against expected value
dns-validator propagation example.com --expected "192.168.1.1"
```

**Options:**
- `--type, -t`: Record type (A, AAAA, CNAME, MX, NS, TXT, SOA)
- `--expected, -e`: Expected value for validation

**Features:**
- Tests 8+ major public DNS servers (Google, Cloudflare, Quad9, etc.)
- Concurrent queries for fast results
- Consistency checking across servers
- Response time measurement

#### `providers <domain>`
Detect and analyze DNS providers for a domain.

```bash
# Detect DNS providers
dns-validator providers example.com

# List all supported providers  
dns-validator list-providers
```

**Features:**
- Identifies primary and secondary DNS providers
- Shows provider detection confidence
- Lists nameserver details and patterns

#### `full <domain>`
Run comprehensive DNS validation including all checks.

```bash
# Complete validation suite
dns-validator full example.com

# Full check with specific record type
dns-validator full example.com --type A --expected "1.2.3.4"
```

**Features:**
- Combines delegation, propagation, and provider checks
- Comprehensive validation report
- Summary of all issues found
- Recommended remediation actions

### Security Commands

#### `dnssec <domain>`
Comprehensive DNSSEC validation and security analysis.

```bash
# Basic DNSSEC validation
dns-validator dnssec example.com

# Detailed DNSSEC analysis
dns-validator --verbose dnssec cloudflare.com
```

**Features:**
- Complete DNSSEC chain validation
- DS record verification in parent zone
- DNSKEY and RRSIG signature analysis
- DNSSEC authentication chain verification
- Algorithm strength assessment

#### `security-analysis <domain>`
Comprehensive DNS security vulnerability assessment.

```bash
# Security analysis with scoring
dns-validator security-analysis example.com

# Detailed vulnerability breakdown
dns-validator --verbose security-analysis corporate.com
```

**Features:**
- Open resolver detection and testing
- DNS amplification vulnerability assessment
- Subdomain enumeration protection analysis
- Security scoring (0-100 points)
- Vulnerability classification and remediation guidance

#### `certificate-analysis <domain>`
SSL/TLS certificate and Certificate Authority validation.

```bash
# Certificate and CAA analysis
dns-validator certificate-analysis example.com

# Comprehensive certificate chain analysis
dns-validator --verbose certificate-analysis secure-site.com
```

**Features:**
- Certificate Transparency log monitoring
- CAA record validation and compliance
- SSL/TLS configuration grading (A-F scale)
- Certificate chain validation
- Expiration tracking and renewal alerts

#### `reverse-dns <ip_address>`
Reverse DNS validation and consistency checking.

```bash
# IPv4 reverse DNS check
dns-validator reverse-dns 8.8.8.8

# IPv6 reverse DNS validation
dns-validator reverse-dns 2001:4860:4860::8888
```

**Features:**
- PTR record validation for IPv4 and IPv6
- Forward/reverse consistency verification
- Comprehensive reverse lookup analysis
- Mail server validation support

### Advanced Analysis Commands

#### `geo-dns <domain>`
Test DNS resolution from multiple geographic locations.

```bash
# Global DNS resolution testing
dns-validator geo-dns example.com

# Detailed geographic analysis
dns-validator --verbose geo-dns microsoft.com
```

**Features:**
- Resolution testing from 15+ global locations
- GeoDNS routing detection and validation
- CDN endpoint identification
- Response time comparison across regions
- Geographic consistency analysis

#### `load-balancer <domain>`
Health validation for load-balanced DNS configurations.

```bash
# Load balancer health assessment
dns-validator load-balancer cloudflare.com

# Comprehensive endpoint analysis
dns-validator --verbose load-balancer aws.com
```

**Features:**
- Multiple A record endpoint health validation
- TCP connectivity testing (ports 80, 443, 22, 21, 25, 53)
- HTTP/HTTPS endpoint health verification
- Load balancing pattern analysis
- Failover capability assessment

#### `ipv6-check <domain>`
IPv6 readiness assessment and dual-stack validation.

```bash
# IPv6 readiness scoring
dns-validator ipv6-check example.com

# Complete IPv6 connectivity analysis
dns-validator --verbose ipv6-check github.com
```

**Features:**
- AAAA record validation and analysis
- IPv6-only DNS server testing
- Dual-stack configuration verification
- IPv6 connectivity testing (ping + TCP)
- Readiness scoring (0-100 points)

#### `cache-analysis <domain>`
DNS caching behavior analysis and optimization.

```bash
# TTL and caching analysis
dns-validator cache-analysis example.com

# Specific record type analysis
dns-validator cache-analysis mail.example.com --type MX
```

**Options:**
- `--type, -t`: DNS record type to analyze (default: A)

**Features:**
- TTL compliance checking across servers
- Cache behavior analysis and recommendations
- Cache poisoning detection indicators
- Performance optimization suggestions

#### `health-monitor <domain>`
Real-time DNS health monitoring with alerting.

```bash
# Basic health monitoring (60 minutes)
dns-validator health-monitor example.com

# Custom monitoring duration and intervals
dns-validator health-monitor critical-site.com --duration 1440 --interval 60
```

**Options:**
- `--duration, -d`: Monitoring duration in minutes (default: 60)
- `--interval, -i`: Check interval in seconds (default: 300)

**Features:**
- Real-time DNS health monitoring
- Automated alerting on failures
- Historical tracking and logging
- Exportable monitoring reports

### Provider API Integration

#### `provider <domain>`
Deep DNS provider analysis with API integration.

```bash
# Auto-detect provider and analyze
dns-validator provider example.com

# Use stored credentials
dns-validator provider example.com --provider cloudflare --cred-name production

# Direct API usage (less secure)
dns-validator provider example.com --api-token YOUR_TOKEN
```

**Options:**
- `--provider`: Specify provider (cloudflare, aws, azure, gcp, etc.)
- `--cred-name`: Use stored credential set
- `--api-token`: Direct API token (various providers)
- `--access-key`: AWS access key
- `--secret-key`: AWS secret key
- `--service-account`: Google Cloud service account file

**Features:**
- Automatic provider detection
- API integration for detailed settings
- DNS record retrieval and analysis
- Provider-specific configuration display

### Credential Management

#### `creds` - Secure API Credential Management

Store and manage API credentials with AES-256 encryption.

```bash
# Add credentials interactively (most secure)
dns-validator creds add Cloudflare production --interactive

# Add credentials via command line
dns-validator creds add AWS staging --access-key KEY --secret-key SECRET --region us-east-1

# List stored credentials (secrets masked)
dns-validator creds list

# Test credentials with a domain
dns-validator creds test Cloudflare production example.com

# Edit existing credentials
dns-validator creds edit AWS production

# Export credentials for backup (without secrets)
dns-validator creds export backup.json

# Delete specific credentials
dns-validator creds delete Cloudflare staging

# Clear all credentials
dns-validator creds clear
```

**Subcommands:**
- `add <provider> <name>`: Add new credential set
- `list`: Show all stored credentials (secrets masked)
- `edit <provider> <name>`: Edit existing credentials
- `delete <provider> <name>`: Remove credential set
- `test <provider> <name> <domain>`: Test credentials
- `export <file>`: Export credential structure
- `clear`: Remove all stored credentials

**Security Features:**
- 🔒 AES-256 encryption for all sensitive data
- 📁 Secure storage in `~/.dns-validator/` directory
- 👥 Multiple credential sets per provider
- 🔐 Interactive secure input mode
- 📤 Safe export/backup functionality

## 🚀 Bulk Processing

Process multiple domains efficiently with parallel processing and comprehensive reporting.

### `bulk <domains_file>`
Parallel bulk processing of multiple domains.

```bash
# Basic bulk processing
dns-validator bulk domains.txt

# Full security analysis with custom workers
dns-validator bulk domains.txt \
  --checks delegation \
  --checks propagation \
  --checks security \
  --checks dnssec \
  --workers 20 \
  --output security-report.html

# Generate JSON report for automation
dns-validator bulk domains.txt \
  --checks delegation \
  --checks propagation \
  --output results.json

# CSV export for spreadsheet analysis
dns-validator bulk domains.txt \
  --output report.csv \
  --format csv
```

**Options:**
- `--checks, -c`: Choose checks (delegation, propagation, provider, dnssec, security, certificate, ipv6, reverse-dns)
- `--workers, -w`: Parallel workers (default: 10, max: 50)
- `--output, -o`: Output file (.json, .html, .csv)
- `--format, -f`: Force output format

**Performance:**
- **Small scale** (1-10 domains): ~50 domains/second
- **Medium scale** (10-100 domains): ~20-30 domains/second
- **Large scale** (100+ domains): ~10-15 domains/second

### `create-bulk-file <output_file>`
Create domain files for bulk processing.

```bash
# Create from command line
dns-validator create-bulk-file domains.txt example.com google.com github.com

# Create from clipboard
dns-validator create-bulk-file domains.txt --from-clipboard
```

**Options:**
- `--from-clipboard`: Read domains from system clipboard

## 🔐 Security Features

### DNSSEC Validation
- Complete DNSSEC chain validation
- DS record verification in parent zones
- DNSKEY and RRSIG signature analysis
- Algorithm strength assessment
- Trust anchor validation

### Security Analysis
- Open resolver detection and testing
- DNS amplification vulnerability assessment
- Subdomain enumeration protection evaluation
- Security scoring (0-100 points)
- Vulnerability classification and remediation

### Certificate Integration
- Certificate Transparency log monitoring
- CAA record validation and compliance
- SSL/TLS configuration analysis and grading
- Certificate chain validation
- Expiration tracking and alerts

## 🌐 API Integration

### Supported Providers with Full API Integration

#### Cloud Providers
- **Cloudflare** - Full DNS zone management
- **AWS Route 53** - Complete DNS record analysis
- **Google Cloud DNS** - Zone and record management
- **Azure DNS** - Comprehensive DNS analysis
- **DigitalOcean** - DNS record and zone management

#### Domain Registrars
- **Namecheap** - Full DNS management with sandbox support
- **GoDaddy** - Complete DNS zone management
- **Name.com** - DNS record and domain management
- **Gandi** - LiveDNS zone management
- **OVH** - Multi-region DNS management

### Authentication Methods

#### Secure Credential Storage (Recommended)
```bash
# Store credentials with encryption
dns-validator creds add Cloudflare production --api-token YOUR_TOKEN

# Use stored credentials
dns-validator provider example.com --provider cloudflare --cred-name production
```

#### Direct API Usage
```bash
# Cloudflare
dns-validator provider example.com --api-token YOUR_CF_TOKEN

# AWS Route 53
dns-validator provider example.com --access-key KEY --secret-key SECRET

# Google Cloud DNS
dns-validator provider example.com --service-account /path/to/service-account.json --project-id PROJECT

# Azure DNS
dns-validator provider example.com --subscription-id SUB_ID --tenant-id TENANT_ID --client-id CLIENT_ID --client-secret SECRET
```

#### Environment Variables
```bash
# Cloudflare
export CLOUDFLARE_API_TOKEN=your_token

# AWS
export AWS_ACCESS_KEY_ID=your_access_key
export AWS_SECRET_ACCESS_KEY=your_secret_key

# Google Cloud
export GOOGLE_APPLICATION_CREDENTIALS=/path/to/service-account.json

# Azure
export AZURE_CLIENT_ID=your_client_id
export AZURE_CLIENT_SECRET=your_client_secret
export AZURE_TENANT_ID=your_tenant_id
export AZURE_SUBSCRIPTION_ID=your_subscription_id
```

## 📊 Supported Providers

### DNS Servers Tested
The propagation check queries these major public DNS servers:

| Provider | Primary | Secondary |
|----------|---------|-----------|
| Google | 8.8.8.8 | 8.8.4.4 |
| Cloudflare | 1.1.1.1 | 1.0.0.1 |
| Quad9 | 9.9.9.9 | 149.112.112.112 |
| OpenDNS | 208.67.222.222 | 208.67.220.220 |
| Verisign | 64.6.64.6 | 64.6.65.6 |
| Level3 | 4.2.2.1 | 4.2.2.2 |

### 50+ Detected DNS Providers

#### Major Cloud Providers (✅ API Support)
- **Cloudflare** - Global CDN and DNS
- **AWS Route 53** - Amazon's DNS service
- **Google Cloud DNS** - Google's managed DNS
- **Azure DNS** - Microsoft's DNS service
- **DigitalOcean** - Developer-focused DNS

#### Domain Registrars (✅ API Support)
- **Namecheap** - Popular domain registrar
- **GoDaddy** - Leading domain provider
- **Name.com** - Domain registration and DNS
- **Gandi** - European domain registrar
- **OVH** - European hosting and DNS

#### Enterprise DNS Services
- **DNS Made Easy** - Enterprise DNS platform
- **NS1** - Advanced DNS and traffic management
- **Constellix** - Multi-provider DNS
- **UltraDNS** - Neustar's enterprise DNS
- **Dyn** - Oracle's managed DNS

#### Free DNS Services
- **No-IP** - Dynamic DNS service
- **DuckDNS** - Free dynamic DNS
- **FreeDNS** - Afraid.org's free DNS
- **Hurricane Electric** - Free DNS hosting

*Use `dns-validator list-providers` to see the complete list with API status.*

## 🎯 Advanced Usage

### Enterprise Security Auditing
```bash
# Comprehensive security audit
dns-validator bulk company-domains.txt \
  --checks delegation \
  --checks dnssec \
  --checks security \
  --checks certificate \
  --workers 25 \
  --output security-audit-$(date +%Y%m%d).html
```

### DNS Migration Validation
```bash
# Validate DNS changes after migration
dns-validator bulk migrated-domains.txt \
  --checks delegation \
  --checks propagation \
  --output migration-validation.json

# Monitor DNS propagation
dns-validator health-monitor example.com \
  --duration 120 \
  --interval 30
```

### Performance Monitoring
```bash
# Geographic performance analysis
dns-validator geo-dns example.com

# Load balancer health monitoring
dns-validator load-balancer api.example.com

# IPv6 readiness assessment
dns-validator ipv6-check example.com
```

### Automation and CI/CD Integration
```bash
# JSON output for automated processing
dns-validator propagation example.com --type A | jq '.status'

# Bulk processing in CI/CD pipelines
dns-validator bulk domains.txt --output results.json
if [ $? -eq 0 ]; then echo "All checks passed"; fi
```

## 📋 Examples

### Basic Validation Workflow
```bash
# 1. Check DNS delegation
dns-validator delegation example.com

# 2. Verify propagation across DNS servers
dns-validator propagation example.com --type A

# 3. Detect DNS provider
dns-validator providers example.com

# 4. Run comprehensive check
dns-validator full example.com
```

### Security Assessment Workflow
```bash
# 1. DNSSEC validation
dns-validator dnssec example.com

# 2. Security vulnerability analysis
dns-validator security-analysis example.com

# 3. Certificate and SSL analysis
dns-validator certificate-analysis example.com

# 4. Reverse DNS validation
dns-validator reverse-dns $(dig +short example.com)
```

### Enterprise Bulk Processing
```bash
# 1. Create domain list
dns-validator create-bulk-file enterprise-domains.txt \
  app.company.com \
  api.company.com \
  www.company.com \
  mail.company.com

# 2. Comprehensive security analysis
dns-validator bulk enterprise-domains.txt \
  --checks delegation \
  --checks propagation \
  --checks dnssec \
  --checks security \
  --checks certificate \
  --workers 20 \
  --output enterprise-security-report.html
```

### API Integration Setup
```bash
# 1. Add Cloudflare credentials securely
dns-validator creds add Cloudflare production --interactive

# 2. Test credentials
dns-validator creds test Cloudflare production example.com

# 3. Analyze provider settings
dns-validator provider example.com --provider cloudflare --cred-name production

# 4. List all stored credentials
dns-validator creds list
```

## 🛠 Troubleshooting

### Common Issues

#### Installation Problems
```bash
# Update pip and try again
pip install --upgrade pip
pip install dns-validator

# Install from source if PyPI fails
git clone https://github.com/HereLiesHugo/dns-validator.git
cd dns-validator
pip install -e .
```

#### DNS Resolution Issues
```bash
# Use verbose mode for debugging
dns-validator --verbose propagation example.com

# Check specific DNS server
dig @8.8.8.8 example.com

# Verify internet connectivity
dns-validator propagation google.com
```

#### API Authentication Problems
```bash
# Test credentials
dns-validator creds test Cloudflare production example.com

# Verify API token permissions
curl -H "Authorization: Bearer YOUR_TOKEN" https://api.cloudflare.com/client/v4/user/tokens/verify
```

#### Performance Issues
```bash
# Reduce concurrent workers
dns-validator bulk domains.txt --workers 5

# Use smaller batch sizes
split -l 100 large-domains.txt batch_

# Monitor system resources
top -p $(pgrep -f dns-validator)
```

### Error Messages

| Error | Solution |
|-------|----------|
| `ModuleNotFoundError: No module named 'dns'` | `pip install dnspython` |
| `Cloudflare API error: Invalid token` | Check token permissions |
| `Timeout errors` | Normal for slow DNS servers |
| `Permission denied` | `chmod +x dns-validator` (Linux/macOS) |

### Debug Mode
```bash
# Enable maximum verbosity
dns-validator --verbose [command] [domain]

# Python debugging
python -v -m dns_validator [command] [domain]

# Network debugging
dns-validator propagation example.com --verbose 2>&1 | grep -i error
```

## 📦 Dependencies

### Required Dependencies (Auto-installed)
- `click>=8.0.0` - Command-line interface framework
- `dnspython>=2.3.0` - DNS toolkit for Python
- `requests>=2.28.0` - HTTP library for API calls
- `colorama>=0.4.6` - Cross-platform colored output
- `tabulate>=0.9.0` - Pretty-print tabular data
- `cryptography>=41.0.0` - Credential encryption
- `pyOpenSSL>=23.0.0` - SSL/TLS certificate handling

### Optional Cloud Provider SDKs
```bash
# AWS Route 53
pip install boto3

# Google Cloud DNS
pip install google-cloud-dns

# Azure DNS
pip install azure-mgmt-dns azure-identity
```

## 🤝 Contributing

We welcome contributions! Please see our [Contributing Guidelines](CONTRIBUTING.md).

### Development Setup
```bash
# Clone repository
git clone https://github.com/HereLiesHugo/dns-validator.git
cd dns-validator

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Linux/macOS
# venv\Scripts\activate     # Windows

# Install in development mode
pip install -e .

# Run tests
python -m pytest tests/
```

### Reporting Issues
- 🐛 **Bug Reports**: [GitHub Issues](https://github.com/HereLiesHugo/dns-validator/issues)
- 💡 **Feature Requests**: [GitHub Issues](https://github.com/HereLiesHugo/dns-validator/issues)
- 📖 **Documentation**: [GitHub Wiki](https://github.com/HereLiesHugo/dns-validator/wiki)

## 📄 License

This project is licensed under the **GNU Affero General Public License v3.0** - see the [LICENSE](LICENSE) file for details.

## 🏷️ Version Information

**Current Version**: 2.6.0  
**Release Date**: October 8, 2025  
**Python Support**: 3.7+  
**Platforms**: Windows, Linux, macOS  

### Recent Updates
- ✅ **v2.5.0**: Bulk domain processing with parallel execution
- ✅ **v2.4.0**: Extended DNS provider API integrations  
- ✅ **v2.3.0**: Security analysis and certificate features
- ✅ **v2.1.0**: DNSSEC validation and health monitoring
- ✅ **v2.0.0**: Secure credential management system

---

**Made with ❤️ by the DNS Validator team**

For detailed documentation, visit our [GitHub Repository](https://github.com/HereLiesHugo/dns-validator)