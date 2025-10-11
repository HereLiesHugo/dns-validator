"""
DNS Validator - Bulk Processing Module

Bulk domain processing functionality with parallel execution and comprehensive reporting.

Author: Matisse Urquhart
License: GNU AGPL v3.0
"""

import csv
import json
import threading
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Optional, Callable, TYPE_CHECKING
import concurrent.futures

from colorama import Fore, Style

if TYPE_CHECKING:
    from .dns_validator import DNSValidator


class BulkDomainProcessor:
    """Bulk domain processing with parallel execution and progress tracking"""
    
    def __init__(self, validator: 'DNSValidator', max_workers: int = 10):
        self.validator = validator
        self.max_workers = max_workers
        self.results = []
        self.progress = {"total": 0, "completed": 0, "failed": 0, "start_time": None}
        self.progress_lock = threading.Lock()
    
    def process_domains(self, domains: List[str], checks: List[str], output_file: str = None,
                       progress_callback: Optional[Callable] = None) -> Dict:
        """Process multiple domains with specified checks in parallel"""
        self.results = []
        self.progress = {
            "total": len(domains),
            "completed": 0,
            "failed": 0,
            "start_time": datetime.now(),
            "current_domain": "",
            "errors": []
        }
        
        print(f"\n{Fore.CYAN}🚀 Starting bulk processing of {len(domains)} domains{Style.RESET_ALL}")
        print(f"📊 Checks: {', '.join(checks)}")
        print(f"🔧 Workers: {self.max_workers}")
        print("=" * 60)
        
        with concurrent.futures.ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            # Submit all tasks
            future_to_domain = {
                executor.submit(self._process_single_domain, domain, checks): domain 
                for domain in domains
            }
            
            # Process completed tasks
            for future in concurrent.futures.as_completed(future_to_domain):
                domain = future_to_domain[future]
                try:
                    result = future.result()
                    with self.progress_lock:
                        self.results.append(result)
                        self.progress["completed"] += 1
                        self.progress["current_domain"] = domain
                        
                    if progress_callback:
                        progress_callback(self.progress)
                    else:
                        self._print_progress(domain, result.get("status", "completed"))
                        
                except Exception as e:
                    with self.progress_lock:
                        self.progress["failed"] += 1
                        self.progress["errors"].append({"domain": domain, "error": str(e)})
                        
                    self._print_progress(domain, "failed", str(e))
        
        # Generate final report
        elapsed_time = datetime.now() - self.progress["start_time"]
        summary = self._generate_summary(elapsed_time)
        
        if output_file:
            self._save_batch_report(output_file, summary)
            print(f"\n📄 Detailed report saved to: {output_file}")
        
        return summary
    
    def _process_single_domain(self, domain: str, checks: List[str]) -> Dict:
        """Process a single domain with specified checks"""
        result = {
            "domain": domain,
            "timestamp": datetime.now().isoformat(),
            "status": "success",
            "checks": {},
            "errors": []
        }
        
        try:
            for check in checks:
                if check == "delegation":
                    result["checks"]["delegation"] = self.validator.check_delegation(domain)
                elif check == "propagation":
                    result["checks"]["propagation"] = self.validator.check_propagation(domain)
                elif check == "provider":
                    result["checks"]["provider"] = self.validator.check_provider_settings(domain)
                elif check == "dnssec":
                    result["checks"]["dnssec"] = self.validator.check_dnssec(domain)
                elif check == "security":
                    result["checks"]["security"] = self.validator.analyze_dns_security(domain)
                elif check == "certificate":
                    result["checks"]["certificate"] = self.validator.analyze_certificate_integration(domain)
                elif check == "ipv6":
                    result["checks"]["ipv6"] = self.validator.check_ipv6_support(domain)
                elif check == "reverse-dns":
                    # Get A record first for reverse lookup
                    try:
                        a_records = self.validator.resolver.resolve(domain, 'A')
                        if a_records:
                            result["checks"]["reverse-dns"] = self.validator.check_reverse_dns(str(a_records[0]))
                    except Exception:
                        result["checks"]["reverse-dns"] = {"error": "No A records found"}
                else:
                    result["errors"].append(f"Unknown check type: {check}")
                    
        except Exception as e:
            result["status"] = "failed"
            result["errors"].append(str(e))
            
        return result
    
    def _print_progress(self, domain: str, status: str, error: str = None):
        """Print progress update"""
        with self.progress_lock:
            completed = self.progress["completed"]
            failed = self.progress["failed"]
            total = self.progress["total"]
            percentage = ((completed + failed) / total) * 100
            
            if status == "completed" or status == "success":
                print(f"✅ [{completed + failed:3d}/{total}] ({percentage:5.1f}%) {domain:<40} {Fore.GREEN}SUCCESS{Style.RESET_ALL}")
            else:
                error_msg = f" - {error}" if error else ""
                print(f"❌ [{completed + failed:3d}/{total}] ({percentage:5.1f}%) {domain:<40} {Fore.RED}FAILED{Style.RESET_ALL}{error_msg}")
    
    def _generate_summary(self, elapsed_time) -> Dict:
        """Generate processing summary"""
        total = self.progress["total"]
        completed = self.progress["completed"]
        failed = self.progress["failed"]
        
        summary = {
            "processing_info": {
                "total_domains": total,
                "successful": completed,
                "failed": failed,
                "success_rate": (completed / total * 100) if total > 0 else 0,
                "elapsed_time": str(elapsed_time),
                "domains_per_second": total / elapsed_time.total_seconds() if elapsed_time.total_seconds() > 0 else 0
            },
            "results": self.results,
            "errors": self.progress["errors"]
        }
        
        print(f"\n{Fore.CYAN}📊 Processing Summary{Style.RESET_ALL}")
        print("=" * 40)
        print(f"📈 Total domains: {Fore.YELLOW}{total}{Style.RESET_ALL}")
        print(f"✅ Successful: {Fore.GREEN}{completed}{Style.RESET_ALL}")
        print(f"❌ Failed: {Fore.RED}{failed}{Style.RESET_ALL}")
        print(f"📊 Success rate: {Fore.CYAN}{summary['processing_info']['success_rate']:.1f}%{Style.RESET_ALL}")
        print(f"⏱️  Total time: {Fore.MAGENTA}{elapsed_time}{Style.RESET_ALL}")
        print(f"🚀 Speed: {Fore.BLUE}{summary['processing_info']['domains_per_second']:.2f} domains/second{Style.RESET_ALL}")
        
        return summary
    
    def _save_batch_report(self, output_file: str, summary: Dict):
        """Save detailed batch report to file"""
        try:
            # Determine format based on file extension
            file_path = Path(output_file)
            
            if file_path.suffix.lower() == '.json':
                with open(output_file, 'w', encoding='utf-8') as f:
                    json.dump(summary, f, indent=2, default=str)
            elif file_path.suffix.lower() in ['.html', '.htm']:
                self._save_html_report(output_file, summary)
            else:
                # Default to CSV format
                self._save_csv_report(output_file, summary)
                
        except Exception as e:
            print(f"{Fore.RED}Error saving report: {str(e)}{Style.RESET_ALL}")
    
    def _save_csv_report(self, output_file: str, summary: Dict):
        """Save report in CSV format"""
        with open(output_file, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            
            # Header
            writer.writerow(['Domain', 'Status', 'Timestamp', 'Check Types', 'Errors'])
            
            # Data rows
            for result in summary['results']:
                check_types = ', '.join(result['checks'].keys())
                errors = '; '.join(result['errors']) if result['errors'] else ''
                writer.writerow([
                    result['domain'],
                    result['status'],
                    result['timestamp'],
                    check_types,
                    errors
                ])
    
    def _save_html_report(self, output_file: str, summary: Dict):
        """Save report in HTML format"""
        html_content = f"""
<!DOCTYPE html>
<html>
<head>
    <title>DNS Validator Bulk Report</title>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 20px; }}
        .header {{ background: #f0f0f0; padding: 20px; border-radius: 5px; }}
        .summary {{ margin: 20px 0; }}
        .success {{ color: green; }}
        .failed {{ color: red; }}
        table {{ border-collapse: collapse; width: 100%; }}
        th, td {{ border: 1px solid #ddd; padding: 8px; text-align: left; }}
        th {{ background-color: #f2f2f2; }}
        .status-success {{ background-color: #d4edda; }}
        .status-failed {{ background-color: #f8d7da; }}
    </style>
</head>
<body>
    <div class="header">
        <h1>🔍 DNS Validator Bulk Processing Report</h1>
        <p>Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
    </div>
    
    <div class="summary">
        <h2>📊 Summary</h2>
        <p><strong>Total domains:</strong> {summary['processing_info']['total_domains']}</p>
        <p><strong>Successful:</strong> <span class="success">{summary['processing_info']['successful']}</span></p>
        <p><strong>Failed:</strong> <span class="failed">{summary['processing_info']['failed']}</span></p>
        <p><strong>Success rate:</strong> {summary['processing_info']['success_rate']:.1f}%</p>
        <p><strong>Processing time:</strong> {summary['processing_info']['elapsed_time']}</p>
        <p><strong>Speed:</strong> {summary['processing_info']['domains_per_second']:.2f} domains/second</p>
    </div>
    
    <div>
        <h2>📋 Detailed Results</h2>
        <table>
            <thead>
                <tr>
                    <th>Domain</th>
                    <th>Status</th>
                    <th>Timestamp</th>
                    <th>Checks Performed</th>
                    <th>Errors</th>
                </tr>
            </thead>
            <tbody>
"""
        
        for result in summary['results']:
            status_class = 'status-success' if result['status'] == 'success' else 'status-failed'
            check_types = ', '.join(result['checks'].keys())
            errors = '<br>'.join(result['errors']) if result['errors'] else 'None'
            
            html_content += f"""
                <tr class="{status_class}">
                    <td>{result['domain']}</td>
                    <td>{result['status'].upper()}</td>
                    <td>{result['timestamp']}</td>
                    <td>{check_types}</td>
                    <td>{errors}</td>
                </tr>
"""
        
        html_content += """
            </tbody>
        </table>
    </div>
</body>
</html>
"""
        
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(html_content)


def create_bulk_domains_file(output_file: str, domains: List[str] = None, 
                           from_clipboard: bool = False) -> bool:
    """
    Create a domains file for bulk processing.
    
    Args:
        output_file: Path to output file
        domains: List of domains to include
        from_clipboard: Read domains from clipboard
        
    Returns:
        bool: True if successful, False otherwise
    """
    domain_list = []
    
    if from_clipboard:
        try:
            import pyperclip
            clipboard_content = pyperclip.paste()
            # Parse clipboard content
            domain_list = _parse_domains_from_text(clipboard_content)
            print(f"{Fore.GREEN}✅ Read {len(domain_list)} domains from clipboard{Style.RESET_ALL}")
        except ImportError:
            print(f"{Fore.RED}❌ pyperclip not installed. Install with: pip install pyperclip{Style.RESET_ALL}")
            return False
        except Exception as e:
            print(f"{Fore.RED}❌ Error reading from clipboard: {str(e)}{Style.RESET_ALL}")
            return False
    elif domains:
        domain_list = domains
    else:
        print(f"{Fore.RED}❌ No domains provided{Style.RESET_ALL}")
        return False
    
    try:
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write("# DNS Validator Bulk Domains File\n")
            f.write(f"# Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"# Total domains: {len(domain_list)}\n\n")
            
            for domain in domain_list:
                f.write(f"{domain}\n")
        
        print(f"{Fore.GREEN}✅ Created domains file: {output_file} ({len(domain_list)} domains){Style.RESET_ALL}")
        return True
        
    except Exception as e:
        print(f"{Fore.RED}❌ Error creating domains file: {str(e)}{Style.RESET_ALL}")
        return False


def _parse_domains_from_text(text: str) -> List[str]:
    """Parse domains from text content"""
    from .utils import clean_domain_list
    
    # Split by common separators
    lines = text.replace(',', '\n').replace(';', '\n').replace('\t', '\n').split('\n')
    
    # Clean and filter domains
    domains = []
    for line in lines:
        line = line.strip()
        if line and not line.startswith('#'):
            # Split multiple domains on same line
            line_domains = line.split()
            domains.extend(line_domains)
    
    return clean_domain_list(domains)


def load_domains_from_file(file_path: str) -> List[str]:
    """
    Load domains from a text file.
    
    Args:
        file_path: Path to domains file
        
    Returns:
        List of domain names
    """
    from .utils import clean_domain_list
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        domains = _parse_domains_from_text(content)
        print(f"{Fore.GREEN}✅ Loaded {len(domains)} domains from {file_path}{Style.RESET_ALL}")
        return domains
        
    except Exception as e:
        print(f"{Fore.RED}❌ Error loading domains file: {str(e)}{Style.RESET_ALL}")
        return []