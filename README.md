# DNS Validator

A comprehensive cross-platform CLI tool for DNS validation, featuring delegation checks, propagation testing, and DNS provider settings analysis.

![Python](https://img.shields.io/badge/python-3.7+-blue.svg)
![Platform](https://img.shields.io/badge/platform-Windows%20%7C%20Linux%20%7C%20macOS-lightgrey.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)

## Features

- **DNS Delegation Check**: Verify DNS delegation and authoritative name servers
- **Propagation Check**: Test DNS propagation across multiple public DNS servers
- **Multi-Provider DNS Settings**: Detect and analyze DNS settings from 50+ providers including Cloudflare, AWS Route 53, Google Cloud DNS, Azure DNS, and more
- **Verbose CLI Output**: Detailed logging and colored output for better debugging
- **Cross-platform Compatibility**: Works on Windows, Linux, and macOS
- **Concurrent Processing**: Fast parallel DNS queries for efficient testing

## Installation

### Method 1: Direct Installation (Recommended)

```bash
# Clone the repository
git clone https://github.com/HereLiesHugo/dns-validator.git
cd dns-validator

# Install dependencies
pip install -r requirements.txt

# Make the script executable (Linux/macOS)
chmod +x dns_validator.py
```

### Method 2: Package Installation

```bash
# Install as a Python package
pip install -e .

# Now you can use the commands globally
dns-validator --help
dnsval --help
```

## Usage

### Basic Commands

```bash
# Check DNS delegation
python dns_validator.py delegation example.com

# Check DNS propagation (A record)
python dns_validator.py propagation example.com

# Check propagation for specific record type
python dns_validator.py propagation example.com --type MX

# Check propagation with expected value validation
python dns_validator.py propagation example.com --expected "192.168.1.1"

# Detect DNS providers
python dns_validator.py providers example.com

# List all supported providers
python dns_validator.py list-providers

# Check provider settings (with API integration)
python dns_validator.py provider example.com --api-token your_token

# Check Cloudflare settings (legacy command)
python dns_validator.py cloudflare example.com --api-token your_cf_token

# Run all checks at once
python dns_validator.py full example.com

# Enable verbose output for any command
python dns_validator.py --verbose delegation example.com
```

### Advanced Usage Examples

```bash
# Comprehensive check with all options
python dns_validator.py full example.com \
  --type A \
  --expected "192.168.1.1" \
  --api-token your_cloudflare_token

# Check MX record propagation
python dns_validator.py propagation example.com --type MX --verbose

# Validate CNAME record
python dns_validator.py propagation subdomain.example.com --type CNAME
```

## Command Reference

### Global Options

- `--verbose, -v`: Enable verbose output with detailed logging

### Commands

#### `delegation <domain>`
Check DNS delegation for a domain.

**Features:**
- Validates authoritative name servers
- Checks parent delegation
- Identifies delegation issues

#### `propagation <domain>`
Check DNS propagation across multiple DNS servers.

**Options:**
- `--type, -t`: DNS record type (default: A)
- `--expected, -e`: Expected value to validate against

**Features:**
- Tests 8 major public DNS servers (Google, Cloudflare, Quad9, etc.)
- Concurrent queries for fast results
- Consistency checking across servers
- Response time measurement

#### `providers <domain>`
Detect DNS providers for a domain.

**Features:**
- Identifies primary and secondary DNS providers
- Shows all detected providers
- Lists nameserver details

#### `list-providers`
List all supported DNS providers.

**Features:**
- Shows 50+ supported DNS providers organized by category
- Indicates API integration status
- Displays detection patterns

#### `provider <domain>`
Check DNS provider settings with API integration.

**Options:**
- `--provider`: Specify provider to check
- `--api-token`: API token for provider integration
- `--api-secret`: API secret for providers that require it
- `--access-key`: Access key for AWS Route 53
- `--secret-key`: Secret key for AWS Route 53
- `--service-account`: Service account file for Google Cloud DNS

**Features:**
- Auto-detects DNS provider
- API integration for detailed settings
- DNS record retrieval and analysis
- Provider-specific configuration display

#### `cloudflare <domain>`
Check Cloudflare DNS settings (legacy command).

**Options:**
- `--api-token`: Cloudflare API token for detailed information

**Features:**
- Detects Cloudflare nameserver usage
- Retrieves zone settings (with API token)
- Lists all DNS records with proxy status
- Shows security and performance settings

#### `full <domain>`
Perform all DNS checks in sequence.

**Options:**
- `--type, -t`: DNS record type for propagation check
- `--expected, -e`: Expected value for validation
- `--api-token`: Cloudflare API token

**Features:**
- Comprehensive validation report
- Summary of all issues found
- Recommended actions

## DNS Servers Tested

The propagation check queries the following public DNS servers:

| Provider | Primary | Secondary |
|----------|---------|-----------|
| Google | 8.8.8.8 | 8.8.4.4 |
| Cloudflare | 1.1.1.1 | 1.0.0.1 |
| Quad9 | 9.9.9.9 | - |
| OpenDNS | 208.67.222.222 | - |
| Verisign | 64.6.64.6 | - |
| Level3 | 4.2.2.1 | - |

## Supported DNS Providers

The tool supports detection and analysis of 50+ DNS providers:

### 🌐 Major Cloud Providers
- **Cloudflare** (✅ Full API Support)
- **AWS Route 53** (🔧 API Planned)
- **Google Cloud DNS** (🔧 API Planned)
- **Azure DNS** (🔧 API Planned)

### 🚀 VPS/Cloud Hosting
- DigitalOcean, Linode, Vultr, OVH, Hetzner, Scaleway

### 🏢 Domain Registrars
- Namecheap, GoDaddy, Name.com, Domain.com, Gandi, Hover, Dynadot

### 🔒 Security/Privacy DNS
- Quad9, OpenDNS

### ⚡ Performance DNS
- DNS Made Easy, NS1, Constellix, UltraDNS

### 🆓 Free DNS Services
- No-IP, DuckDNS, FreeDNS, Hurricane Electric

And many more! Use `python dns_validator.py list-providers` to see the complete list.

## API Integration

### Cloudflare
To use Cloudflare API features:
1. Log in to the Cloudflare dashboard
2. Go to "My Profile" → "API Tokens"
3. Create a token with "Zone:Read" permissions
4. Use with `--api-token YOUR_TOKEN`

### Other Providers
API integration for AWS Route 53, Google Cloud DNS, Azure DNS, and DigitalOcean is planned for future releases.

## Examples

### Check if DNS changes have propagated

```bash
# After updating A record to point to new server
python dns_validator.py propagation example.com --expected "192.168.1.100"
```

### Troubleshoot DNS delegation issues

```bash
# Check if nameservers are properly configured
python dns_validator.py delegation example.com --verbose
```

### Detect and validate DNS provider

```bash
# Detect DNS provider
python dns_validator.py providers example.com

# Check provider settings with API
python dns_validator.py provider example.com --api-token your_token

# Legacy Cloudflare check
python dns_validator.py cloudflare example.com --api-token your_token
```

### Complete domain validation

```bash
# Run all checks with verbose output
python dns_validator.py --verbose full example.com --api-token your_token
```

## Output Colors

The tool uses colored output for better readability:

- 🟢 **Green**: Success, valid configurations
- 🔴 **Red**: Errors, failed validations
- 🟡 **Yellow**: Warnings, inconsistencies
- 🔵 **Blue**: Information, processing status
- 🟣 **Magenta**: Headers, summaries

## Troubleshooting

### Common Issues

1. **"No module named 'dns'"**: Install dnspython
   ```bash
   pip install dnspython
   ```

2. **Cloudflare API errors**: Check your API token permissions

3. **Timeout errors**: Some DNS servers may be slow; this is normal

4. **Permission denied (Linux/macOS)**: Make the script executable
   ```bash
   chmod +x dns_validator.py
   ```

### Windows PowerShell

If you encounter execution policy issues on Windows:

```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

## Requirements

- Python 3.7 or higher
- Internet connection for DNS queries
- Optional: Cloudflare API token for enhanced features

## Dependencies

- `click`: Command-line interface framework
- `dnspython`: DNS toolkit for Python
- `requests`: HTTP library for API calls
- `colorama`: Cross-platform colored terminal text
- `tabulate`: Pretty-print tabular data
- `pycryptodome`: Cryptographic library

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Support

- 🐛 **Bug Reports**: [GitHub Issues](https://github.com/HereLiesHugo/dns-validator/issues)
- 💡 **Feature Requests**: [GitHub Issues](https://github.com/HereLiesHugo/dns-validator/issues)
- 📖 **Documentation**: [README](https://github.com/HereLiesHugo/dns-validator#readme)

## Changelog

### v1.0.0
- Initial release
- DNS delegation checking
- DNS propagation testing across 8 public servers
- Cloudflare integration with API support
- Cross-platform compatibility
- Verbose logging and colored output
- Concurrent DNS queries for performance
