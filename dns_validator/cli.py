"""
DNS Validator - CLI Module

Command line interface for the DNS validator tool.

Author: Matisse Urquhart
License: GNU AGPL v3.0
"""

import sys
import json
import click
from pathlib import Path
from typing import Dict, List

from colorama import Fore, Style
from tabulate import tabulate

from .dns_validator import DNSValidator
from .analytics import DNSQueryAnalytics, DNSAnalyticsReporter
from .bulk import BulkDomainProcessor, create_bulk_domains_file, load_domains_from_file


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
@click.argument('domains_file')
@click.option('--checks', '-c', default='delegation,propagation', 
              help='Comma-separated list of checks to perform')
@click.option('--output', '-o', help='Output file for results')
@click.option('--workers', '-w', default=10, type=int, help='Number of parallel workers')
@click.option('--format', '-f', type=click.Choice(['csv', 'json', 'html']), 
              default='csv', help='Output format')
@click.pass_context
def bulk(ctx, domains_file, checks, output, workers, format):
    """Process multiple domains in bulk"""
    validator = ctx.obj['validator']
    
    # Load domains from file
    domains = load_domains_from_file(domains_file)
    if not domains:
        print(f"{Fore.RED}❌ No valid domains found in file{Style.RESET_ALL}")
        return
    
    # Parse checks
    check_list = [check.strip() for check in checks.split(',')]
    
    # Set output file if not specified
    if not output:
        output = f"bulk_results_{Path(domains_file).stem}.{format}"
    
    # Initialize bulk processor
    processor = BulkDomainProcessor(validator, max_workers=workers)
    
    try:
        # Process domains
        summary = processor.process_domains(domains, check_list, output)
        
        print(f"\n{Fore.GREEN}✅ Bulk processing completed successfully!{Style.RESET_ALL}")
        
    except KeyboardInterrupt:
        print(f"\n{Fore.YELLOW}⚠️  Bulk processing interrupted{Style.RESET_ALL}")
    except Exception as e:
        print(f"\n{Fore.RED}❌ Bulk processing failed: {str(e)}{Style.RESET_ALL}")


@cli.command('create-bulk-file')
@click.argument('output_file')
@click.argument('domains', nargs=-1)
@click.option('--from-clipboard', is_flag=True, 
              help='Read domains from clipboard instead of arguments')
@click.pass_context
def create_bulk_file(ctx, output_file, domains, from_clipboard):
    """Create a domains file for bulk processing"""
    if from_clipboard:
        success = create_bulk_domains_file(output_file, from_clipboard=True)
    elif domains:
        success = create_bulk_domains_file(output_file, list(domains))
    else:
        print(f"{Fore.RED}❌ No domains provided. Use --from-clipboard or provide domain arguments{Style.RESET_ALL}")
        return
    
    if success:
        print(f"{Fore.GREEN}✅ Domains file created successfully{Style.RESET_ALL}")
    else:
        print(f"{Fore.RED}❌ Failed to create domains file{Style.RESET_ALL}")


@cli.command('query-analytics')
@click.argument('domain')
@click.option('--duration', '-d', default=5, type=int, help='Collection duration in minutes')
@click.option('--interval', '-i', default=5, type=int, help='Query interval in seconds')
@click.option('--query-types', '-t', default='A,AAAA,MX,NS,TXT', 
              help='Comma-separated query types')
@click.option('--output', '-o', help='Output file for analytics data (JSON format)')
@click.option('--geographic', is_flag=True, help='Enable geographic analysis')
@click.option('--performance', is_flag=True, help='Include performance metrics')
@click.pass_context
def query_analytics(ctx, domain, duration, interval, query_types, output, geographic, performance):
    """Advanced DNS query analytics with comprehensive data collection"""
    validator = ctx.obj['validator']
    
    # Parse query types
    qtypes = [qt.strip().upper() for qt in query_types.split(',')]
    
    # Initialize analytics
    analytics = DNSQueryAnalytics(validator)
    
    try:
        # Run analytics
        result = analytics.analyze_domain_queries(
            domain, 
            query_types=qtypes,
            duration_minutes=duration,
            interval_seconds=interval
        )
        
        # Save results if output file specified
        if output:
            with open(output, 'w', encoding='utf-8') as f:
                json.dump(result, f, indent=2, default=str)
            print(f"\n💾 Analytics data saved to: {output}")
        
        # Display summary
        summary = result.get("summary", {})
        print(f"\n{Fore.CYAN}📊 Analytics Summary{Style.RESET_ALL}")
        print("=" * 40)
        
        query_summary = summary.get("query_type_summary", {})
        for qtype, data in query_summary.items():
            success_rate = data.get("success_rate", 0)
            avg_time = data.get("average_response_time_ms", 0)
            print(f"{qtype}: {success_rate:.1f}% success, {avg_time:.1f}ms avg")
        
        print(f"\n{Fore.GREEN}✅ Query analytics completed!{Style.RESET_ALL}")
        
    except KeyboardInterrupt:
        print(f"\n{Fore.YELLOW}⚠️  Analytics collection interrupted{Style.RESET_ALL}")
    except Exception as e:
        print(f"\n{Fore.RED}❌ Analytics collection failed: {str(e)}{Style.RESET_ALL}")


@cli.command('analytics-report')
@click.argument('data_file')
@click.option('--format', '-f', type=click.Choice(['executive', 'technical', 'geographic', 'performance']),
              default='executive', help='Report format')
@click.option('--output', '-o', help='Output file path')
@click.pass_context
def analytics_report(ctx, data_file, format, output):
    """Generate comprehensive analytics reports from collected data"""
    try:
        # Load analytics data
        with open(data_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # Generate report
        reporter = DNSAnalyticsReporter()
        report_content = reporter.generate_report(data, format, output)
        
        if output:
            print(f"{Fore.GREEN}✅ {format.title()} report saved to: {output}{Style.RESET_ALL}")
        else:
            print(report_content)
        
    except FileNotFoundError:
        print(f"{Fore.RED}❌ Analytics data file not found: {data_file}{Style.RESET_ALL}")
    except Exception as e:
        print(f"{Fore.RED}❌ Report generation failed: {str(e)}{Style.RESET_ALL}")


@cli.command('dns-insights')
@click.argument('domain')
@click.option('--quick', '-q', is_flag=True, help='Quick insight generation (1 minute)')
@click.option('--comprehensive', '-c', is_flag=True, help='Comprehensive analysis (15 minutes)')
@click.option('--baseline', '-b', is_flag=True, help='Establish performance baseline')
@click.pass_context
def dns_insights(ctx, domain, quick, comprehensive, baseline):
    """Advanced DNS insights combining real-time analytics with patterns"""
    validator = ctx.obj['validator']
    
    # Determine duration based on options
    if quick:
        duration = 1
        print(f"{Fore.CYAN}🚀 Quick DNS insights for {domain} (1 minute){Style.RESET_ALL}")
    elif comprehensive:
        duration = 15
        print(f"{Fore.CYAN}🔍 Comprehensive DNS insights for {domain} (15 minutes){Style.RESET_ALL}")
    else:
        duration = 5
        print(f"{Fore.CYAN}📊 Standard DNS insights for {domain} (5 minutes){Style.RESET_ALL}")
    
    # Initialize analytics
    analytics = DNSQueryAnalytics(validator)
    
    try:
        # Run insights collection
        result = analytics.analyze_domain_queries(
            domain,
            duration_minutes=duration,
            interval_seconds=10 if quick else 30
        )
        
        # Display insights
        summary = result.get("summary", {})
        
        print(f"\n{Fore.CYAN}🎯 DNS Insights for {domain}{Style.RESET_ALL}")
        print("=" * 50)
        
        # Performance insights
        query_summary = summary.get("query_type_summary", {})
        if query_summary:
            print(f"\n{Fore.YELLOW}⚡ Performance Insights{Style.RESET_ALL}")
            for qtype, data in query_summary.items():
                success_rate = data.get("success_rate", 0)
                avg_time = data.get("average_response_time_ms", 0)
                
                if success_rate >= 95:
                    status_icon = "✅"
                elif success_rate >= 90:
                    status_icon = "⚠️ "
                else:
                    status_icon = "❌"
                
                print(f"{status_icon} {qtype}: {success_rate:.1f}% success, {avg_time:.1f}ms response")
        
        # Geographic insights
        geo_summary = summary.get("geographic_summary", {})
        if geo_summary:
            location_count = len(geo_summary.get("locations", []))
            anycast_count = geo_summary.get("anycast_servers", 0)
            
            print(f"\n{Fore.YELLOW}🌍 Geographic Distribution{Style.RESET_ALL}")
            if location_count >= 3:
                print(f"🌍 {Fore.GREEN}Good geographic distribution ({location_count} regions){Style.RESET_ALL}")
            else:
                print(f"🌍 {Fore.RED}Limited geographic distribution ({location_count} region){Style.RESET_ALL}")
            
            if anycast_count > 0:
                print(f"🚀 {Fore.GREEN}Anycast services detected ({anycast_count} servers){Style.RESET_ALL}")
        
        # Display recommendations prominently
        recommendations = summary.get("recommendations", [])
        if recommendations:
            print(f"\n{Fore.CYAN}💡 Actionable Recommendations{Style.RESET_ALL}")
            print("=" * 40)
            for i, rec in enumerate(recommendations, 1):
                print(f"{i}. {rec}")
        
        # Quick performance score
        success_rates = [data.get("success_rate", 0) for data in query_summary.values()]
        if success_rates:
            avg_success = sum(success_rates) / len(success_rates)
            if avg_success >= 95:
                score_color = Fore.GREEN
                score_text = "Excellent"
            elif avg_success >= 90:
                score_color = Fore.YELLOW  
                score_text = "Good"
            else:
                score_color = Fore.RED
                score_text = "Needs Attention"
            
            print(f"\n{Fore.CYAN}📊 Overall DNS Health Score{Style.RESET_ALL}")
            print(f"Score: {score_color}{avg_success:.1f}% ({score_text}){Style.RESET_ALL}")
        
        print(f"\n{Fore.GREEN}✅ DNS insights analysis completed!{Style.RESET_ALL}")
        
    except KeyboardInterrupt:
        print(f"\n{Fore.YELLOW}⚠️  Insights analysis interrupted{Style.RESET_ALL}")
    except Exception as e:
        print(f"\n{Fore.RED}❌ Insights analysis failed: {str(e)}{Style.RESET_ALL}")


def main():
    """Main entry point for the CLI"""
    try:
        cli()
    except KeyboardInterrupt:
        print(f"\n{Fore.YELLOW}Operation cancelled by user{Style.RESET_ALL}")
        sys.exit(1)
    except Exception as e:
        print(f"\n{Fore.RED}Unexpected error: {str(e)}{Style.RESET_ALL}")
        sys.exit(1)


if __name__ == '__main__':
    main()