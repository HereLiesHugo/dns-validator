#!/usr/bin/env python3
"""
DNS Validator CLI - Backward compatibility wrapper

This script provides backward compatibility for users who run the tool directly
without installing it as a package.

Author: Matisse Urquhart
Contact: me@maturqu.com
License: GNU AGPL v3.0
"""

import sys
import os

# Add the dns_validator package to the path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Import and run the CLI
from dns_validator.dns_validator import cli

if __name__ == '__main__':
    cli()