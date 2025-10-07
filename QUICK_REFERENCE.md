# DNS Validator - Quick Reference

## Installation
```bash
python install.py
```

## Basic Usage
```bash
# Check DNS delegation
python dns_validator.py delegation example.com

# Check DNS propagation
python dns_validator.py propagation example.com

# Detect DNS providers
python dns_validator.py providers example.com

# List all supported providers
python dns_validator.py list-providers

# Check provider settings
python dns_validator.py provider example.com --api-token YOUR_TOKEN

# Run all checks
python dns_validator.py full example.com

# Enable verbose output
python dns_validator.py --verbose [command] [domain]
```

## Windows Shortcuts
```cmd
# Use batch file
dns-validator.bat delegation example.com

# Or PowerShell script
.\dns-validator.ps1 delegation example.com
```

## Advanced Options
```bash
# Check specific record type
python dns_validator.py propagation example.com --type MX

# Validate expected value
python dns_validator.py propagation example.com --expected "192.168.1.1"

# Use provider API integration
python dns_validator.py provider example.com --api-token YOUR_TOKEN

# Check specific provider
python dns_validator.py provider example.com --provider "AWS Route 53"

# Complete validation with all options
python dns_validator.py full example.com --type A --expected "1.2.3.4" --api-token YOUR_TOKEN
```

## Common Record Types
- A: IPv4 address
- AAAA: IPv6 address  
- CNAME: Canonical name
- MX: Mail exchange
- NS: Name server
- TXT: Text records
- SOA: Start of authority

## Exit Codes
- 0: Success
- 1: Error or validation failure

## Files
- `dns_validator/`: Main package directory
  - `dns_validator.py`: Core DNS validation functionality
  - `api_key_manager.py`: Secure credential management
  - `__init__.py`: Package initialization
  - `__main__.py`: Module entry point
- `dns_validator_cli.py`: Backward compatibility wrapper
- `requirements.txt`: Python dependencies
- `setup.py`: Package installation configuration
- `dns-validator.bat`: Windows batch launcher
- `dns-validator.ps1`: PowerShell launcher
- `dns-validator.sh`: Unix shell launcher
- `tests/`: Test suite
- `examples/`: Usage examples