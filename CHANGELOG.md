# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [2.0.1] - 2025-10-07

### Fixed
- **Package Structure for pip Installation**: Fixed `ModuleNotFoundError` when installing via pip
  - Created proper Python package structure with `dns_validator/` directory
  - Added `__init__.py` and `__main__.py` files for proper package entry points
  - Updated import statements to use relative imports within the package
  - Created backward compatibility wrapper `dns_validator_cli.py` for direct script execution
  - Updated setup.py console_scripts entry points to reference correct module paths
  - Fixed all shell scripts, batch files, and documentation references

### Changed
- Moved `dns_validator.py` and `api_key_manager.py` into `dns_validator/` package directory
- Updated version number to 2.0.1 in setup.py
- Updated all scripts and documentation to use new file structure

### Added
- `dns_validator/__init__.py`: Package initialization with version and exports
- `dns_validator/__main__.py`: Entry point for `python -m dns_validator` execution
- `dns_validator_cli.py`: Backward compatibility wrapper for direct script execution

## [2.0.0] - 2025-10-04

### Added
- 🔐 **Secure Credential Management System**
  - AES-256 encrypted storage of API keys and tokens
  - Multi-provider credential support (Cloudflare, AWS, Google Cloud, Azure, DigitalOcean)
  - Multiple credential sets per provider (staging, production, etc.)
  - Interactive secure input for sensitive data
  - Credential testing, export, and backup functionality
- 🌐 **Enhanced API Integration**
  - Full API support for AWS Route 53, Google Cloud DNS, Azure DNS, DigitalOcean
  - Improved error handling and debugging
  - Better provider detection (52+ providers supported)
- 🛡️ **Security Improvements**
  - Credentials never stored in plain text
  - Secure credential directory (~/.dns-validator/)
  - Safe export options (with/without secrets)
- 🚀 **Performance & UX**
  - Faster concurrent DNS queries
  - Better error messages and help text
  - Improved cross-platform compatibility

### Commands Added
- `creds add <provider> <name>`: Add new credentials with secure encryption
- `creds list`: Display all stored credentials (secrets masked)
- `creds edit <provider> <name>`: Interactively edit existing credentials
- `creds delete <provider> <name>`: Remove stored credentials
- `creds test <provider> <name> <domain>`: Test credentials with API call
- `creds export <file>`: Export credential structure (optional --include-secrets)
- `creds clear`: Remove all stored credentials

## [1.0.0] - 2025-10-01

### Added
- Initial release
- DNS delegation checking
- DNS propagation testing across 8 public servers
- Cloudflare integration with API support
- Cross-platform compatibility (Windows, Linux, macOS)
- Verbose logging and colored output
- Concurrent DNS queries for performance
- Support for multiple DNS record types (A, AAAA, CNAME, MX, NS, TXT, SOA)
- Provider detection for 50+ DNS providers
- CLI commands: delegation, propagation, cloudflare, full, providers, list-providers
- Installation scripts and cross-platform launchers