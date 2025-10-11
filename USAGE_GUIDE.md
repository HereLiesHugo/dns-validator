# DNS Validator Usage Guide

## ❌ Common Error: Relative Import Issues

If you see this error:
```
ImportError: attempted relative import with no known parent package
```

This happens when trying to run the module file directly like:
```bash
python dns_validator/dns_validator.py propagation example.com  # ❌ Don't do this
```

## ✅ Correct Usage Methods

### Method 1: Use the CLI wrapper script (Recommended)
```bash
# Linux/Mac
python dns_validator_cli.py propagation example.com

# Windows PowerShell
python dns_validator_cli.py propagation example.com

# Windows Batch File
dns-validator.bat propagation example.com
```

### Method 2: Run as a Python module
```bash
python -m dns_validator propagation example.com
```

### Method 3: Install as a package
```bash
# Install the package
pip install -e .

# Then use the command directly
dns-validator propagation example.com
```

## Quick Examples

```bash
# Check DNS propagation
python dns_validator_cli.py propagation example.com

# Check DNS delegation
python dns_validator_cli.py delegation example.com

# Full DNS analysis
python dns_validator_cli.py full example.com

# List all available providers
python dns_validator_cli.py list-providers

# DNS query analytics (from new modular architecture)
python dns_validator_cli.py query-analytics example.com --duration 30

# Bulk domain processing
python dns_validator_cli.py bulk domains.txt --output report.html
```

## Module-based Usage

You can also import individual modules from the new modular architecture:

```python
# Import specific functionality
from dns_validator.dns_validator import DNSValidator
from dns_validator.analytics import DNSQueryAnalytics
from dns_validator.bulk import BulkDomainProcessor

# Use the classes directly in your code
validator = DNSValidator()
result = validator.check_propagation("example.com")
```

The modular architecture allows for cleaner imports and better code organization!