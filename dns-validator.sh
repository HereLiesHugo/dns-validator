#!/bin/bash
# DNS Validator - Unix Shell Script
# Easy launcher for Linux/macOS users

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
python3 "$SCRIPT_DIR/dns_validator.py" "$@"