#!/usr/bin/env python3
"""
DNS Validator CLI - A comprehensive DNS validation tool
"""

import click
import dns.resolver
import dns.zone  
import dns.query
import dns.message
import requests
import sys
import time
import socket
from typing import List, Dict, Optional, Tuple
from colorama import init, Fore, Style
from tabulate import tabulate
import concurrent.futures
import threading
from datetime import datetime

# Initialize colorama for cross-platform colored output
init(autoreset=True)

class DNSValidator:
    """Main DNS validation class"""
    
    def __init__(self, verbose: bool = False):
        self.verbose = verbose
        self.lock = threading.Lock()
        
    def log(self, message: str, color: str = Fore.WHITE, level: str = "INFO"):
        """Thread-safe logging with color support"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        with self.lock:
            if self.verbose or level in ["ERROR", "WARNING"]:
                print(f"{color}[{timestamp}] {level}: {message}{Style.RESET_ALL}")
    
    def check_delegation(self, domain: str) -> Dict:
        """Check DNS delegation for a domain"""
        self.log(f"Checking DNS delegation for {domain}", Fore.CYAN)
        
        result = {
            "domain": domain,
            "authoritative_servers": [],
            "parent_servers": [],
            "delegation_valid": False,
            "errors": []
        }
        
        try:
            # Get authoritative name servers from the domain's zone
            ns_records = dns.resolver.resolve(domain, 'NS')
            result["authoritative_servers"] = [str(ns) for ns in ns_records]
            self.log(f"Found {len(result['authoritative_servers'])} authoritative servers", Fore.GREEN)
            
            # Check parent delegation
            parent_domain = '.'.join(domain.split('.')[1:])
            if parent_domain:
                try:
                    parent_ns = dns.resolver.resolve(parent_domain, 'NS')
                    result["parent_servers"] = [str(ns) for ns in parent_ns]
                    self.log(f"Found {len(result['parent_servers'])} parent servers", Fore.GREEN)
                except Exception as e:
                    self.log(f"Could not resolve parent NS records: {e}", Fore.YELLOW, "WARNING")
            
            # Verify delegation consistency
            if result["authoritative_servers"]:
                result["delegation_valid"] = True
                self.log("DNS delegation appears valid", Fore.GREEN)
            else:
                result["errors"].append("No authoritative servers found")
                self.log("No authoritative servers found", Fore.RED, "ERROR")
                
        except dns.resolver.NXDOMAIN:
            error_msg = f"Domain {domain} does not exist"
            result["errors"].append(error_msg)
            self.log(error_msg, Fore.RED, "ERROR")
        except Exception as e:
            error_msg = f"Error checking delegation: {str(e)}"
            result["errors"].append(error_msg)
            self.log(error_msg, Fore.RED, "ERROR")
        
        return result
    
    def check_propagation(self, domain: str, record_type: str = 'A', expected_value: str = None) -> Dict:
        """Check DNS propagation across multiple public DNS servers"""
        self.log(f"Checking DNS propagation for {domain} ({record_type} record)", Fore.CYAN)
        
        # Popular public DNS servers
        dns_servers = [
            ("Google Primary", "8.8.8.8"),
            ("Google Secondary", "8.8.4.4"),
            ("Cloudflare Primary", "1.1.1.1"),
            ("Cloudflare Secondary", "1.0.0.1"),
            ("Quad9", "9.9.9.9"),
            ("OpenDNS", "208.67.222.222"),
            ("Verisign", "64.6.64.6"),
            ("Level3", "4.2.2.1")
        ]
        
        result = {
            "domain": domain,
            "record_type": record_type,
            "expected_value": expected_value,
            "servers": {},
            "propagated": True,
            "consistency": True
        }
        
        def check_server(server_info):
            name, ip = server_info
            try:
                resolver = dns.resolver.Resolver()
                resolver.nameservers = [ip]
                resolver.timeout = 5
                resolver.lifetime = 10
                
                response = resolver.resolve(domain, record_type)
                values = [str(record) for record in response]
                
                self.log(f"{name} ({ip}): {', '.join(values)}", Fore.GREEN)
                
                return name, {
                    "ip": ip,
                    "values": values,
                    "response_time": response.response.time * 1000,  # Convert to ms
                    "status": "success"
                }
            except dns.resolver.NXDOMAIN:
                self.log(f"{name} ({ip}): NXDOMAIN", Fore.RED)
                return name, {"ip": ip, "values": [], "status": "nxdomain"}
            except Exception as e:
                self.log(f"{name} ({ip}): Error - {str(e)}", Fore.YELLOW)
                return name, {"ip": ip, "values": [], "status": "error", "error": str(e)}
        
        # Check all servers concurrently
        with concurrent.futures.ThreadPoolExecutor(max_workers=8) as executor:
            futures = {executor.submit(check_server, server): server for server in dns_servers}
            
            for future in concurrent.futures.as_completed(futures):
                name, server_result = future.result()
                result["servers"][name] = server_result
        
        # Analyze results
        successful_responses = [s for s in result["servers"].values() if s["status"] == "success"]
        
        if not successful_responses:
            result["propagated"] = False
            self.log("DNS record not found on any server", Fore.RED, "ERROR")
        else:
            # Check consistency across servers
            all_values = [set(s["values"]) for s in successful_responses]
            if len(set(frozenset(values) for values in all_values)) > 1:
                result["consistency"] = False
                self.log("Inconsistent DNS responses detected across servers", Fore.YELLOW, "WARNING")
            
            # Check against expected value if provided
            if expected_value:
                matches = any(expected_value in s["values"] for s in successful_responses)
                if not matches:
                    result["propagated"] = False
                    self.log(f"Expected value '{expected_value}' not found", Fore.RED, "ERROR")
        
        return result
    
    def check_cloudflare_settings(self, domain: str, api_token: str = None) -> Dict:
        """Check Cloudflare DNS settings if API token is provided"""
        self.log(f"Checking Cloudflare settings for {domain}", Fore.CYAN)
        
        result = {
            "domain": domain,
            "cloudflare_detected": False,
            "records": [],
            "settings": {},
            "errors": []
        }
        
        # First, check if domain is using Cloudflare nameservers
        try:
            ns_records = dns.resolver.resolve(domain, 'NS')
            nameservers = [str(ns).lower() for ns in ns_records]
            
            cloudflare_ns_patterns = ['cloudflare.com', 'ns.cloudflare.com']
            is_cloudflare = any(any(pattern in ns for pattern in cloudflare_ns_patterns) for ns in nameservers)
            
            result["cloudflare_detected"] = is_cloudflare
            
            if is_cloudflare:
                self.log("Cloudflare nameservers detected", Fore.GREEN)
            else:
                self.log("Cloudflare nameservers not detected", Fore.YELLOW, "WARNING")
                
        except Exception as e:
            result["errors"].append(f"Could not check nameservers: {str(e)}")
        
        # If API token provided, get detailed settings
        if api_token and result["cloudflare_detected"]:
            try:
                headers = {
                    'Authorization': f'Bearer {api_token}',
                    'Content-Type': 'application/json'
                }
                
                # Get zone ID
                zones_response = requests.get(
                    f'https://api.cloudflare.com/client/v4/zones?name={domain}',
                    headers=headers,
                    timeout=10
                )
                
                if zones_response.status_code == 200:
                    zones_data = zones_response.json()
                    if zones_data['success'] and zones_data['result']:
                        zone_id = zones_data['result'][0]['id']
                        zone_info = zones_data['result'][0]
                        
                        result["settings"] = {
                            "status": zone_info.get('status', 'unknown'),
                            "plan": zone_info.get('plan', {}).get('name', 'unknown'),
                            "development_mode": zone_info.get('development_mode', False),
                            "security_level": zone_info.get('security_level', 'unknown')
                        }
                        
                        # Get DNS records
                        records_response = requests.get(
                            f'https://api.cloudflare.com/client/v4/zones/{zone_id}/dns_records',
                            headers=headers,
                            timeout=10
                        )
                        
                        if records_response.status_code == 200:
                            records_data = records_response.json()
                            if records_data['success']:
                                result["records"] = records_data['result']
                                self.log(f"Retrieved {len(result['records'])} DNS records from Cloudflare", Fore.GREEN)
                
                else:
                    result["errors"].append(f"Cloudflare API error: {zones_response.status_code}")
                    
            except Exception as e:
                result["errors"].append(f"Error accessing Cloudflare API: {str(e)}")
        
        return result


@click.group()
@click.option('--verbose', '-v', is_flag=True, help='Enable verbose output')
@click.pass_context
def cli(ctx, verbose):
    """DNS Validator - A comprehensive DNS validation tool"""
    ctx.ensure_object(dict)
    ctx.obj['validator'] = DNSValidator(verbose=verbose)


@cli.command()
@click.argument('domain')
@click.pass_context
def delegation(ctx, domain):
    """Check DNS delegation for a domain"""
    validator = ctx.obj['validator']
    result = validator.check_delegation(domain)
    
    print(f"\n{Fore.CYAN}DNS Delegation Check for {domain}{Style.RESET_ALL}")
    print("=" * 50)
    
    if result["delegation_valid"]:
        print(f"{Fore.GREEN}✓ Delegation Status: VALID{Style.RESET_ALL}")
    else:
        print(f"{Fore.RED}✗ Delegation Status: INVALID{Style.RESET_ALL}")
    
    if result["authoritative_servers"]:
        print(f"\n{Fore.YELLOW}Authoritative Name Servers:{Style.RESET_ALL}")
        for i, server in enumerate(result["authoritative_servers"], 1):
            print(f"  {i}. {server}")
    
    if result["parent_servers"]:
        print(f"\n{Fore.YELLOW}Parent Name Servers:{Style.RESET_ALL}")
        for i, server in enumerate(result["parent_servers"], 1):
            print(f"  {i}. {server}")
    
    if result["errors"]:
        print(f"\n{Fore.RED}Errors:{Style.RESET_ALL}")
        for error in result["errors"]:
            print(f"  • {error}")
    
    print()


@cli.command()
@click.argument('domain')
@click.option('--type', '-t', default='A', help='DNS record type to check (default: A)')
@click.option('--expected', '-e', help='Expected value to validate against')
@click.pass_context
def propagation(ctx, domain, type, expected):
    """Check DNS propagation across multiple DNS servers"""
    validator = ctx.obj['validator']
    result = validator.check_propagation(domain, type.upper(), expected)
    
    print(f"\n{Fore.CYAN}DNS Propagation Check for {domain} ({type.upper()} record){Style.RESET_ALL}")
    print("=" * 60)
    
    if result["propagated"]:
        print(f"{Fore.GREEN}✓ Propagation Status: COMPLETE{Style.RESET_ALL}")
    else:
        print(f"{Fore.RED}✗ Propagation Status: INCOMPLETE{Style.RESET_ALL}")
    
    if not result["consistency"]:
        print(f"{Fore.YELLOW}⚠ Warning: Inconsistent responses detected{Style.RESET_ALL}")
    
    # Create table for results
    table_data = []
    for server_name, server_data in result["servers"].items():
        status_color = Fore.GREEN if server_data["status"] == "success" else Fore.RED
        values_str = ", ".join(server_data.get("values", [])) or "No response"
        response_time = f"{server_data.get('response_time', 0):.1f}ms" if server_data.get('response_time') else "N/A"
        
        table_data.append([
            server_name,
            server_data["ip"],
            f"{status_color}{server_data['status'].upper()}{Style.RESET_ALL}",
            values_str,
            response_time
        ])
    
    print(f"\n{Fore.YELLOW}Server Results:{Style.RESET_ALL}")
    print(tabulate(
        table_data,
        headers=["DNS Server", "IP Address", "Status", "Values", "Response Time"],
        tablefmt="grid"
    ))
    
    if expected:
        print(f"\n{Fore.YELLOW}Expected Value:{Style.RESET_ALL} {expected}")
    
    print()


@cli.command()
@click.argument('domain')
@click.option('--api-token', help='Cloudflare API token for detailed settings')
@click.pass_context
def cloudflare(ctx, domain, api_token):
    """Check Cloudflare DNS settings"""
    validator = ctx.obj['validator']
    result = validator.check_cloudflare_settings(domain, api_token)
    
    print(f"\n{Fore.CYAN}Cloudflare Settings Check for {domain}{Style.RESET_ALL}")
    print("=" * 50)
    
    if result["cloudflare_detected"]:
        print(f"{Fore.GREEN}✓ Cloudflare nameservers detected{Style.RESET_ALL}")
        
        if result["settings"]:
            print(f"\n{Fore.YELLOW}Zone Settings:{Style.RESET_ALL}")
            for key, value in result["settings"].items():
                print(f"  {key.replace('_', ' ').title()}: {value}")
        
        if result["records"]:
            print(f"\n{Fore.YELLOW}DNS Records ({len(result['records'])} total):{Style.RESET_ALL}")
            
            # Group records by type
            records_by_type = {}
            for record in result["records"]:
                record_type = record.get("type", "UNKNOWN")
                if record_type not in records_by_type:
                    records_by_type[record_type] = []
                records_by_type[record_type].append(record)
            
            for record_type, records in records_by_type.items():
                print(f"\n  {record_type} Records:")
                for record in records:
                    name = record.get("name", "N/A")
                    content = record.get("content", "N/A")
                    ttl = record.get("ttl", "N/A")
                    proxied = record.get("proxied", False)
                    proxy_status = "🟠 Proxied" if proxied else "⚪ DNS Only"
                    print(f"    {name} → {content} (TTL: {ttl}) {proxy_status}")
    
    else:
        print(f"{Fore.YELLOW}⚠ Cloudflare nameservers not detected{Style.RESET_ALL}")
        
        if not api_token:
            print(f"{Fore.CYAN}💡 Tip: Use --api-token to get detailed Cloudflare settings{Style.RESET_ALL}")
    
    if result["errors"]:
        print(f"\n{Fore.RED}Errors:{Style.RESET_ALL}")
        for error in result["errors"]:
            print(f"  • {error}")
    
    print()


@cli.command()
@click.argument('domain')
@click.option('--type', '-t', default='A', help='DNS record type to check')
@click.option('--expected', '-e', help='Expected value to validate against')
@click.option('--api-token', help='Cloudflare API token')
@click.pass_context
def full(ctx, domain, type, expected, api_token):
    """Perform all DNS checks (delegation, propagation, and Cloudflare settings)"""
    validator = ctx.obj['validator']
    
    print(f"\n{Fore.MAGENTA}{'='*60}")
    print(f"COMPREHENSIVE DNS VALIDATION for {domain}")
    print(f"{'='*60}{Style.RESET_ALL}")
    
    # 1. Delegation Check
    print(f"\n{Fore.CYAN}1. DELEGATION CHECK{Style.RESET_ALL}")
    delegation_result = validator.check_delegation(domain)
    
    if delegation_result["delegation_valid"]:
        print(f"{Fore.GREEN}✓ DNS delegation is valid{Style.RESET_ALL}")
    else:
        print(f"{Fore.RED}✗ DNS delegation issues detected{Style.RESET_ALL}")
        for error in delegation_result["errors"]:
            print(f"  • {error}")
    
    # 2. Propagation Check
    print(f"\n{Fore.CYAN}2. PROPAGATION CHECK{Style.RESET_ALL}")
    propagation_result = validator.check_propagation(domain, type.upper(), expected)
    
    if propagation_result["propagated"]:
        print(f"{Fore.GREEN}✓ DNS propagation is complete{Style.RESET_ALL}")
    else:
        print(f"{Fore.RED}✗ DNS propagation issues detected{Style.RESET_ALL}")
    
    if not propagation_result["consistency"]:
        print(f"{Fore.YELLOW}⚠ Inconsistent responses across DNS servers{Style.RESET_ALL}")
    
    # 3. Cloudflare Check
    print(f"\n{Fore.CYAN}3. CLOUDFLARE SETTINGS CHECK{Style.RESET_ALL}")
    cloudflare_result = validator.check_cloudflare_settings(domain, api_token)
    
    if cloudflare_result["cloudflare_detected"]:
        print(f"{Fore.GREEN}✓ Cloudflare nameservers detected{Style.RESET_ALL}")
        if cloudflare_result["records"]:
            print(f"  📋 {len(cloudflare_result['records'])} DNS records found")
    else:
        print(f"{Fore.YELLOW}⚠ Not using Cloudflare nameservers{Style.RESET_ALL}")
    
    # Summary
    print(f"\n{Fore.MAGENTA}SUMMARY{Style.RESET_ALL}")
    print("=" * 20)
    
    issues = []
    if not delegation_result["delegation_valid"]:
        issues.append("DNS delegation issues")
    if not propagation_result["propagated"]:
        issues.append("DNS propagation incomplete")
    if not propagation_result["consistency"]:
        issues.append("Inconsistent DNS responses")
    if cloudflare_result["errors"]:
        issues.append("Cloudflare API errors")
    
    if not issues:
        print(f"{Fore.GREEN}🎉 All DNS checks passed successfully!{Style.RESET_ALL}")
    else:
        print(f"{Fore.YELLOW}⚠ Issues found:{Style.RESET_ALL}")
        for issue in issues:
            print(f"  • {issue}")
    
    print(f"\n{Fore.MAGENTA}{'='*60}{Style.RESET_ALL}\n")


if __name__ == '__main__':
    try:
        cli()
    except KeyboardInterrupt:
        print(f"\n{Fore.YELLOW}Operation cancelled by user{Style.RESET_ALL}")
        sys.exit(1)
    except Exception as e:
        print(f"\n{Fore.RED}Unexpected error: {str(e)}{Style.RESET_ALL}")
        sys.exit(1)