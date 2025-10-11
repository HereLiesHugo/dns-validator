#!/usr/bin/env python3
"""
DNS Validator - Module Usage Examples

This script demonstrates how to use individual DNS validator modules
in your own Python projects.

Author: Matisse Urquhart
License: GNU AGPL v3.0
"""

import sys
from pathlib import Path

# Add the parent directory to the Python path for importing
sys.path.insert(0, str(Path(__file__).parent))

from dns_validator import DNSValidator, utils, analytics, bulk, APIKeyManager


def example_basic_validation():
    """Example: Basic DNS validation"""
    print("=" * 60)
    print("🔍 Basic DNS Validation Example")
    print("=" * 60)
    
    # Initialize validator
    validator = DNSValidator(verbose=False)
    
    # Check delegation
    domain = "example.com"
    result = validator.check_delegation(domain)
    
    print(f"Domain: {domain}")
    print(f"Delegation Valid: {result['delegation_valid']}")
    print(f"Authoritative Servers: {result['authoritative_servers']}")
    print()


def example_utils_module():
    """Example: Using utility functions"""
    print("=" * 60)
    print("🛠️  Utility Functions Example")
    print("=" * 60)
    
    # Validate domains
    test_domains = ["example.com", "invalid..domain", "google.com", "not-a-domain"]
    valid_domains = utils.clean_domain_list(test_domains)
    
    print(f"Original domains: {test_domains}")
    print(f"Valid domains: {valid_domains}")
    
    # Check IP addresses
    test_ips = ["8.8.8.8", "2001:4860:4860::8888", "invalid-ip", "192.168.1.1"]
    for ip in test_ips:
        is_valid = utils.is_valid_ip(ip)
        ip_type = "IPv6" if utils.is_ipv6(ip) else "IPv4" if utils.is_ipv4(ip) else "Invalid"
        print(f"IP: {ip:<20} Valid: {is_valid:<5} Type: {ip_type}")
    
    # Format utilities
    print(f"\nFormatted duration: {utils.format_duration(3665.5)}")
    print(f"Formatted bytes: {utils.format_bytes(1536000)}")
    print()


def example_bulk_processing():
    """Example: Bulk domain processing"""
    print("=" * 60)
    print("🚀 Bulk Processing Example")
    print("=" * 60)
    
    # Initialize components
    validator = DNSValidator(verbose=False)
    processor = bulk.BulkDomainProcessor(validator, max_workers=3)
    
    # Sample domains
    test_domains = ["example.com", "google.com", "github.com"]
    checks = ["delegation", "propagation"]
    
    print(f"Processing {len(test_domains)} domains with checks: {checks}")
    
    # Process domains (this will take a few seconds)
    try:
        summary = processor.process_domains(test_domains, checks)
        
        # Display summary
        processing_info = summary["processing_info"]
        print(f"\nResults:")
        print(f"  Success Rate: {processing_info['success_rate']:.1f}%")
        print(f"  Processing Speed: {processing_info['domains_per_second']:.2f} domains/sec")
        
    except KeyboardInterrupt:
        print("Processing interrupted by user")
    
    print()


def example_analytics_module():
    """Example: DNS analytics (quick demo)"""
    print("=" * 60)
    print("📊 DNS Analytics Example")
    print("=" * 60)
    
    # Initialize components
    validator = DNSValidator(verbose=False)
    analytics_engine = analytics.DNSQueryAnalytics(validator)
    
    domain = "example.com"
    print(f"Running quick analytics for {domain} (30 seconds)...")
    
    try:
        # Run quick analytics (30 seconds)
        result = analytics_engine.analyze_domain_queries(
            domain,
            query_types=['A', 'MX', 'NS'],
            duration_minutes=0.5,  # 30 seconds
            interval_seconds=5
        )
        
        # Display results
        summary = result.get("summary", {})
        query_summary = summary.get("query_type_summary", {})
        
        print(f"\nAnalytics Results for {domain}:")
        for qtype, data in query_summary.items():
            success_rate = data.get("success_rate", 0)
            avg_time = data.get("average_response_time_ms", 0)
            print(f"  {qtype}: {success_rate:.1f}% success, {avg_time:.1f}ms avg response")
        
        # Generate report
        reporter = analytics.DNSAnalyticsReporter()
        report = reporter.generate_report(result, "executive")
        print(f"\n--- Executive Report ---")
        print(report[:300] + "..." if len(report) > 300 else report)
        
    except KeyboardInterrupt:
        print("Analytics interrupted by user")
    
    print()


def example_api_credentials():
    """Example: API credential management"""
    print("=" * 60)
    print("🔐 API Credential Management Example")
    print("=" * 60)
    
    # Initialize API key manager
    api_manager = APIKeyManager()
    
    print("API Key Manager initialized")
    print(f"Supported providers: {', '.join(api_manager.supported_providers)}")
    
    # List existing credentials (will be empty on first run)
    credentials = api_manager.list_credentials()
    print(f"Existing credential sets: {len(credentials)}")
    
    print("\n💡 To add credentials, use the CLI command:")
    print("   dns-validator creds add Cloudflare production --api-token YOUR_TOKEN")
    print()


def main():
    """Run all examples"""
    print("🔍 DNS Validator - Module Usage Examples")
    print("This demonstrates how to use DNS validator modules in your Python projects.\n")
    
    try:
        # Run examples
        example_basic_validation()
        example_utils_module()
        
        # Ask user if they want to run time-consuming examples
        response = input("Run bulk processing and analytics examples? (y/N): ").lower().strip()
        if response in ('y', 'yes'):
            example_bulk_processing()
            example_analytics_module()
        else:
            print("Skipping time-consuming examples...")
        
        example_api_credentials()
        
        print("=" * 60)
        print("✅ All examples completed!")
        print("\n💡 You can now use these modules in your own projects:")
        print("   from dns_validator import DNSValidator, utils, analytics, bulk")
        print("=" * 60)
        
    except KeyboardInterrupt:
        print("\n⚠️  Examples interrupted by user")
    except Exception as e:
        print(f"\n❌ Error running examples: {str(e)}")


if __name__ == "__main__":
    main()