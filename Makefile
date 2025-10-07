# Makefile for DNS Validator

.PHONY: install test clean help run-tests lint format

# Default target
help:
	@echo "DNS Validator - Available targets:"
	@echo "  install     - Install dependencies"
	@echo "  test        - Run test suite"
	@echo "  lint        - Run code linting"
	@echo "  format      - Format code"
	@echo "  clean       - Clean temporary files"
	@echo "  help        - Show this help"

# Install dependencies
install:
	pip install -r requirements.txt
	chmod +x dns_validator_cli.py
	chmod +x dns-validator.sh

# Run tests
test:
	python3 tests/test_dns_validator.py

# Run tests with coverage (if coverage is installed)
test-coverage:
	coverage run tests/test_dns_validator.py
	coverage report
	coverage html

# Lint code (if pylint is installed)
lint:
	pylint dns_validator/ || true

# Format code (if black is installed)
format:
	black dns_validator/ tests/ || true

# Clean temporary files
clean:
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -delete
	rm -rf htmlcov/
	rm -f .coverage

# Development install with additional tools
dev-install: install
	pip install pylint black coverage

# Quick validation test
quick-test:
	python3 dns_validator_cli.py delegation google.com
	python3 dns_validator_cli.py propagation google.com