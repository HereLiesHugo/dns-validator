"""
DNS Validator - Analytics Module

DNS Query Analytics and Reporting functionality for comprehensive DNS analysis.

Author: Matisse Urquhart
License: GNU AGPL v3.0
"""

import time
import threading
import ipaddress
from datetime import datetime, timedelta
from typing import List, Dict, Optional, Tuple, TYPE_CHECKING

import dns.resolver
from colorama import Fore, Style

if TYPE_CHECKING:
    from .dns_validator import DNSValidator


class DNSQueryAnalytics:
    """DNS Query Analytics with geographic and temporal analysis"""
    
    def __init__(self, validator: 'DNSValidator'):
        self.validator = validator
        self.analytics_data = {
            "query_log": [],
            "query_types": {},
            "geographic_data": {},
            "temporal_patterns": {},
            "performance_metrics": {},
            "error_patterns": {}
        }
        self.start_time = datetime.now()
        self.lock = threading.Lock()
    
    def analyze_domain_queries(self, domain: str, query_types: List[str] = None, 
                              duration_minutes: int = 60, interval_seconds: int = 60) -> Dict:
        """Comprehensive DNS query analytics for a domain"""
        
        if query_types is None:
            query_types = ['A', 'AAAA', 'CNAME', 'MX', 'TXT', 'NS', 'SOA']
        
        print(f"\n{Fore.CYAN}🔍 DNS Query Analytics for {domain}{Style.RESET_ALL}")
        print(f"📊 Monitoring duration: {duration_minutes} minutes")
        print(f"⏱️  Sampling interval: {interval_seconds} seconds")
        print(f"🔍 Query types: {', '.join(query_types)}")
        print("=" * 60)
        
        analytics_result = {
            "domain": domain,
            "start_time": datetime.now().isoformat(),
            "duration_minutes": duration_minutes,
            "query_distribution": {},
            "geographic_analysis": {},
            "temporal_patterns": {},
            "performance_analysis": {},
            "nameserver_analysis": {},
            "summary": {}
        }
        
        end_time = datetime.now() + timedelta(minutes=duration_minutes)
        sample_count = 0
        
        while datetime.now() < end_time:
            sample_count += 1
            timestamp = datetime.now()
            
            print(f"\r🔄 Sample {sample_count} - {timestamp.strftime('%H:%M:%S')} ", end="", flush=True)
            
            # Collect query data for this sample
            sample_data = self._collect_query_sample(domain, query_types, timestamp)
            analytics_result["query_distribution"] = self._update_query_distribution(
                analytics_result["query_distribution"], sample_data
            )
            
            # Geographic analysis
            geo_data = self._analyze_geographic_distribution(domain, timestamp)
            analytics_result["geographic_analysis"] = self._update_geographic_analysis(
                analytics_result["geographic_analysis"], geo_data
            )
            
            # Performance metrics
            perf_data = self._measure_query_performance(domain, query_types)
            analytics_result["performance_analysis"] = self._update_performance_analysis(
                analytics_result["performance_analysis"], perf_data, timestamp
            )
            
            # Nameserver analysis
            ns_data = self._analyze_nameserver_responses(domain)
            analytics_result["nameserver_analysis"] = self._update_nameserver_analysis(
                analytics_result["nameserver_analysis"], ns_data
            )
            
            time.sleep(interval_seconds)
        
        # Generate temporal patterns and summary
        analytics_result["temporal_patterns"] = self._analyze_temporal_patterns(analytics_result)
        analytics_result["summary"] = self._generate_analytics_summary(analytics_result, sample_count)
        
        print(f"\n\n{Fore.GREEN}✅ Analytics collection completed!{Style.RESET_ALL}")
        return analytics_result
    
    def _collect_query_sample(self, domain: str, query_types: List[str], timestamp: datetime) -> Dict:
        """Collect DNS query sample data"""
        sample = {
            "timestamp": timestamp.isoformat(),
            "queries": {},
            "response_times": {},
            "status": {}
        }
        
        for qtype in query_types:
            try:
                start = time.time()
                answers = self.validator.resolver.resolve(domain, qtype)
                response_time = (time.time() - start) * 1000  # Convert to milliseconds
                
                sample["queries"][qtype] = len(answers) if answers else 0
                sample["response_times"][qtype] = response_time
                sample["status"][qtype] = "success"
                
            except Exception as e:
                sample["queries"][qtype] = 0
                sample["response_times"][qtype] = None
                sample["status"][qtype] = str(type(e).__name__)
        
        return sample
    
    def _analyze_geographic_distribution(self, domain: str, timestamp: datetime) -> Dict:
        """Analyze geographic distribution of DNS responses"""
        geo_data = {
            "timestamp": timestamp.isoformat(),
            "nameservers": {},
            "geographic_locations": {},
            "anycast_detection": {}
        }
        
        try:
            # Get nameservers for the domain
            ns_records = self.validator.resolver.resolve(domain, 'NS')
            
            for ns in ns_records:
                ns_name = str(ns).rstrip('.')
                ns_info = self._geolocate_nameserver(ns_name)
                geo_data["nameservers"][ns_name] = ns_info
                
                # Track geographic locations
                if ns_info.get("country"):
                    country = ns_info["country"]
                    if country not in geo_data["geographic_locations"]:
                        geo_data["geographic_locations"][country] = []
                    geo_data["geographic_locations"][country].append(ns_name)
        
        except Exception as e:
            geo_data["error"] = str(e)
        
        return geo_data
    
    def _geolocate_nameserver(self, nameserver: str) -> Dict:
        """Get geographic information for a nameserver"""
        try:
            # Resolve nameserver to IP
            ip_result = self.validator.resolver.resolve(nameserver, 'A')
            if not ip_result:
                return {"error": "No A record"}
            
            ip_address = str(ip_result[0])
            
            # Basic geolocation based on IP patterns and known ranges
            geo_info = {
                "ip": ip_address,
                "country": self._guess_country_from_ip(ip_address),
                "provider": self._guess_provider_from_ip(ip_address),
                "anycast_likely": self._detect_anycast_patterns(nameserver, ip_address)
            }
            
            return geo_info
            
        except Exception as e:
            return {"error": str(e)}
    
    def _guess_country_from_ip(self, ip: str) -> str:
        """Basic country guessing based on IP ranges and patterns"""
        # This is a simplified version - in production, use a proper GeoIP database
        try:
            ip_obj = ipaddress.ip_address(ip)
            
            # Common cloud provider ranges (simplified)
            if ip_obj in ipaddress.ip_network('8.8.0.0/16'):  # Google Public DNS
                return "US (Google)"
            elif ip_obj in ipaddress.ip_network('1.1.0.0/16'):  # Cloudflare
                return "Global (Cloudflare)"
            elif ip_obj in ipaddress.ip_network('208.67.0.0/16'):  # OpenDNS
                return "US (OpenDNS)"
            elif str(ip).startswith('185.'):
                return "EU"
            elif str(ip).startswith('103.'):
                return "APAC"
            else:
                return "Unknown"
        except ValueError:
            return "Invalid IP"
    
    def _guess_provider_from_ip(self, ip: str) -> str:
        """Guess DNS provider from IP address patterns"""
        ip_str = str(ip)
        
        # Common provider patterns
        if ip_str.startswith('8.8.'):
            return "Google"
        elif ip_str.startswith('1.1.'):
            return "Cloudflare"
        elif ip_str.startswith('208.67.'):
            return "OpenDNS"
        elif ip_str.startswith('9.9.'):
            return "Quad9"
        else:
            return "Unknown"
    
    def _detect_anycast_patterns(self, nameserver: str, ip: str) -> bool:
        """Detect if nameserver likely uses anycast"""
        # Simplified anycast detection
        anycast_indicators = [
            'cloudflare' in nameserver.lower(),
            'google' in nameserver.lower(),
            'quad9' in nameserver.lower(),
            ip.startswith('1.1.'),
            ip.startswith('8.8.'),
            ip.startswith('9.9.')
        ]
        return any(anycast_indicators)
    
    def _measure_query_performance(self, domain: str, query_types: List[str]) -> Dict:
        """Measure DNS query performance metrics"""
        performance = {
            "response_times": {},
            "cache_status": {},
            "tcp_fallback": {},
            "edns_support": {}
        }
        
        for qtype in query_types:
            try:
                # Measure response time
                start = time.time()
                result = self.validator.resolver.resolve(domain, qtype)
                response_time = (time.time() - start) * 1000
                
                performance["response_times"][qtype] = {
                    "time_ms": response_time,
                    "status": "success",
                    "record_count": len(result) if result else 0
                }
                
                # Simple cache status detection (simplified)
                performance["cache_status"][qtype] = "unknown"
                
            except Exception as e:
                performance["response_times"][qtype] = {
                    "time_ms": None,
                    "status": "failed",
                    "error": str(e)
                }
        
        return performance
    
    def _analyze_nameserver_responses(self, domain: str) -> Dict:
        """Analyze nameserver response patterns"""
        ns_analysis = {
            "nameservers": {},
            "consistency": {},
            "response_variations": {}
        }
        
        try:
            # Get nameservers
            ns_records = self.validator.resolver.resolve(domain, 'NS')
            
            for ns in ns_records:
                ns_name = str(ns).rstrip('.')
                ns_data = self._query_specific_nameserver(domain, ns_name)
                ns_analysis["nameservers"][ns_name] = ns_data
        
        except Exception as e:
            ns_analysis["error"] = str(e)
        
        return ns_analysis
    
    def _query_specific_nameserver(self, domain: str, nameserver: str) -> Dict:
        """Query a specific nameserver directly"""
        try:
            # Create resolver for specific nameserver
            specific_resolver = dns.resolver.Resolver()
            
            # Get nameserver IP
            ns_ip_result = self.validator.resolver.resolve(nameserver, 'A')
            if not ns_ip_result:
                return {"error": "Cannot resolve nameserver IP"}
            
            specific_resolver.nameservers = [str(ns_ip_result[0])]
            
            # Test A record query
            start = time.time()
            result = specific_resolver.resolve(domain, 'A')
            response_time = (time.time() - start) * 1000
            
            return {
                "ip": str(ns_ip_result[0]),
                "response_time_ms": response_time,
                "record_count": len(result) if result else 0,
                "status": "success"
            }
            
        except Exception as e:
            return {"error": str(e), "status": "failed"}
    
    def _update_query_distribution(self, current_dist: Dict, sample_data: Dict) -> Dict:
        """Update query type distribution statistics"""
        if not current_dist:
            current_dist = {
                "total_samples": 0,
                "query_counts": {},
                "success_rates": {},
                "average_response_times": {}
            }
        
        current_dist["total_samples"] += 1
        
        for qtype, count in sample_data["queries"].items():
            # Update counts
            if qtype not in current_dist["query_counts"]:
                current_dist["query_counts"][qtype] = {"total": 0, "samples": 0}
            
            current_dist["query_counts"][qtype]["total"] += count
            current_dist["query_counts"][qtype]["samples"] += 1
            
            # Update success rates
            if qtype not in current_dist["success_rates"]:
                current_dist["success_rates"][qtype] = {"success": 0, "total": 0}
            
            current_dist["success_rates"][qtype]["total"] += 1
            if sample_data["status"][qtype] == "success":
                current_dist["success_rates"][qtype]["success"] += 1
            
            # Update response times
            if qtype not in current_dist["average_response_times"]:
                current_dist["average_response_times"][qtype] = {"total_time": 0, "count": 0}
            
            if sample_data["response_times"][qtype] is not None:
                current_dist["average_response_times"][qtype]["total_time"] += sample_data["response_times"][qtype]
                current_dist["average_response_times"][qtype]["count"] += 1
        
        return current_dist
    
    def _update_geographic_analysis(self, current_geo: Dict, geo_data: Dict) -> Dict:
        """Update geographic analysis data"""
        if not current_geo:
            current_geo = {
                "location_frequency": {},
                "provider_distribution": {},
                "anycast_servers": set()
            }
        
        # Update location frequency
        for country, servers in geo_data.get("geographic_locations", {}).items():
            if country not in current_geo["location_frequency"]:
                current_geo["location_frequency"][country] = 0
            current_geo["location_frequency"][country] += len(servers)
        
        # Update provider distribution
        for ns_name, ns_info in geo_data.get("nameservers", {}).items():
            provider = ns_info.get("provider", "Unknown")
            if provider not in current_geo["provider_distribution"]:
                current_geo["provider_distribution"][provider] = 0
            current_geo["provider_distribution"][provider] += 1
            
            # Track anycast servers
            if ns_info.get("anycast_likely"):
                current_geo["anycast_servers"].add(ns_name)
        
        return current_geo
    
    def _update_performance_analysis(self, current_perf: Dict, perf_data: Dict, timestamp: datetime) -> Dict:
        """Update performance analysis with temporal tracking"""
        if not current_perf:
            current_perf = {
                "response_time_history": {},
                "performance_trends": {},
                "peak_times": [],
                "slowest_queries": {}
            }
        
        # Update response time history
        time_key = timestamp.strftime('%H:%M')
        if time_key not in current_perf["response_time_history"]:
            current_perf["response_time_history"][time_key] = {}
        
        for qtype, perf_info in perf_data["response_times"].items():
            if qtype not in current_perf["response_time_history"][time_key]:
                current_perf["response_time_history"][time_key][qtype] = []
            
            if perf_info["time_ms"] is not None:
                current_perf["response_time_history"][time_key][qtype].append(perf_info["time_ms"])
                
                # Track slowest queries
                if qtype not in current_perf["slowest_queries"]:
                    current_perf["slowest_queries"][qtype] = {"max_time": 0, "timestamp": None}
                
                if perf_info["time_ms"] > current_perf["slowest_queries"][qtype]["max_time"]:
                    current_perf["slowest_queries"][qtype] = {
                        "max_time": perf_info["time_ms"],
                        "timestamp": timestamp.isoformat()
                    }
        
        return current_perf
    
    def _update_nameserver_analysis(self, current_ns: Dict, ns_data: Dict) -> Dict:
        """Update nameserver analysis data"""
        if not current_ns:
            current_ns = {
                "server_performance": {},
                "consistency_scores": {},
                "availability_tracking": {}
            }
        
        for ns_name, ns_info in ns_data.get("nameservers", {}).items():
            if ns_name not in current_ns["server_performance"]:
                current_ns["server_performance"][ns_name] = {
                    "response_times": [],
                    "success_count": 0,
                    "total_queries": 0
                }
            
            current_ns["server_performance"][ns_name]["total_queries"] += 1
            
            if ns_info.get("status") == "success":
                current_ns["server_performance"][ns_name]["success_count"] += 1
                if ns_info.get("response_time_ms"):
                    current_ns["server_performance"][ns_name]["response_times"].append(
                        ns_info["response_time_ms"]
                    )
        
        return current_ns
    
    def _analyze_temporal_patterns(self, analytics_result: Dict) -> Dict:
        """Analyze temporal patterns in the data"""
        temporal = {
            "peak_usage_times": [],
            "response_time_trends": {},
            "query_pattern_changes": {},
            "performance_degradation": []
        }
        
        # Analyze response time history for peaks
        perf_history = analytics_result.get("performance_analysis", {}).get("response_time_history", {})
        
        for time_key, time_data in perf_history.items():
            total_avg_time = 0
            total_queries = 0
            
            for qtype, times in time_data.items():
                if times:
                    avg_time = sum(times) / len(times)
                    total_avg_time += avg_time
                    total_queries += len(times)
            
            if total_queries > 0:
                overall_avg = total_avg_time / len(time_data)
                temporal["response_time_trends"][time_key] = {
                    "average_response_time": overall_avg,
                    "query_count": total_queries
                }
        
        # Identify peak times (simplified)
        if temporal["response_time_trends"]:
            avg_response_times = [data["average_response_time"] for data in temporal["response_time_trends"].values()]
            if avg_response_times:
                max_time = max(avg_response_times)
                for time_key, data in temporal["response_time_trends"].items():
                    if data["average_response_time"] == max_time:
                        temporal["peak_usage_times"].append(time_key)
        
        return temporal
    
    def _generate_analytics_summary(self, analytics_result: Dict, sample_count: int) -> Dict:
        """Generate comprehensive analytics summary"""
        summary = {
            "total_samples": sample_count,
            "query_type_summary": {},
            "geographic_summary": {},
            "performance_summary": {},
            "recommendations": []
        }
        
        # Query type summary
        query_dist = analytics_result.get("query_distribution", {})
        if query_dist.get("query_counts"):
            for qtype, data in query_dist["query_counts"].items():
                avg_count = data["total"] / data["samples"] if data["samples"] > 0 else 0
                success_rate = 0
                if qtype in query_dist.get("success_rates", {}):
                    sr_data = query_dist["success_rates"][qtype]
                    success_rate = (sr_data["success"] / sr_data["total"] * 100) if sr_data["total"] > 0 else 0
                
                avg_response_time = 0
                if qtype in query_dist.get("average_response_times", {}):
                    rt_data = query_dist["average_response_times"][qtype]
                    avg_response_time = rt_data["total_time"] / rt_data["count"] if rt_data["count"] > 0 else 0
                
                summary["query_type_summary"][qtype] = {
                    "average_records": round(avg_count, 2),
                    "success_rate": round(success_rate, 2),
                    "average_response_time_ms": round(avg_response_time, 2)
                }
        
        # Geographic summary
        geo_analysis = analytics_result.get("geographic_analysis", {})
        summary["geographic_summary"] = {
            "locations": list(geo_analysis.get("location_frequency", {}).keys()),
            "providers": list(geo_analysis.get("provider_distribution", {}).keys()),
            "anycast_servers": len(geo_analysis.get("anycast_servers", set()))
        }
        
        # Performance summary
        perf_analysis = analytics_result.get("performance_analysis", {})
        slowest_queries = perf_analysis.get("slowest_queries", {})
        if slowest_queries:
            max_time = max(q["max_time"] for q in slowest_queries.values() if q.get("max_time"))
            summary["performance_summary"] = {
                "max_response_time_ms": max_time,
                "total_time_periods": len(perf_analysis.get("response_time_history", {}))
            }
        
        # Generate recommendations
        self._add_analytics_recommendations(summary, analytics_result)
        
        return summary
    
    def _add_analytics_recommendations(self, summary: Dict, analytics_result: Dict):
        """Add recommendations based on analytics data"""
        recommendations = []
        
        # Performance recommendations
        perf_summary = summary.get("performance_summary", {})
        if perf_summary.get("max_response_time_ms", 0) > 1000:
            recommendations.append("⚠️ High response times detected (>1000ms). Consider optimizing DNS configuration.")
        
        # Geographic recommendations
        geo_summary = summary.get("geographic_summary", {})
        if len(geo_summary.get("locations", [])) < 2:
            recommendations.append("🌍 Consider using geographically distributed DNS servers for better performance.")
        
        if geo_summary.get("anycast_servers", 0) == 0:
            recommendations.append("🚀 Consider using anycast DNS services for improved global performance.")
        
        # Query type recommendations
        query_summary = summary.get("query_type_summary", {})
        low_success_types = [qtype for qtype, data in query_summary.items() 
                           if data.get("success_rate", 0) < 95]
        if low_success_types:
            recommendations.append(f"❌ Low success rates for query types: {', '.join(low_success_types)}")
        
        if not recommendations:
            recommendations.append("✅ DNS configuration appears to be performing well!")
        
        summary["recommendations"] = recommendations


class DNSAnalyticsReporter:
    """Generate comprehensive reports from DNS analytics data"""
    
    def __init__(self):
        self.report_templates = {
            "executive": self._generate_executive_report,
            "technical": self._generate_technical_report,
            "geographic": self._generate_geographic_report,
            "performance": self._generate_performance_report
        }
    
    def generate_report(self, analytics_data: Dict, report_type: str = "technical", 
                       output_file: str = None) -> str:
        """Generate analytics report in specified format"""
        
        if report_type not in self.report_templates:
            raise ValueError(f"Unknown report type: {report_type}")
        
        report_content = self.report_templates[report_type](analytics_data)
        
        if output_file:
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(report_content)
            return f"Report saved to: {output_file}"
        
        return report_content
    
    def _generate_executive_report(self, data: Dict) -> str:
        """Generate executive summary report"""
        summary = data.get("summary", {})
        domain = data.get("domain", "Unknown")
        
        report = f"""
# DNS Analytics Executive Summary
## Domain: {domain}
## Analysis Period: {data.get('start_time', 'Unknown')} ({data.get('duration_minutes', 'N/A')} minutes)

### Key Findings

**Overall Performance:**
- Total monitoring samples: {summary.get('total_samples', 'N/A')}
- Geographic presence: {len(summary.get('geographic_summary', {}).get('locations', []))} regions
- DNS providers detected: {len(summary.get('geographic_summary', {}).get('providers', []))}

**Performance Metrics:**
"""
        
        query_summary = summary.get("query_type_summary", {})
        for qtype, data in query_summary.items():
            success_rate = data.get("success_rate", 0)
            response_time = data.get("average_response_time_ms", 0)
            report += f"- {qtype} records: {success_rate:.1f}% success rate, {response_time:.1f}ms average response\n"
        
        report += "\n**Recommendations:**\n"
        for rec in summary.get("recommendations", []):
            report += f"- {rec}\n"
        
        return report
    
    def _generate_technical_report(self, data: Dict) -> str:
        """Generate detailed technical report"""
        report = f"""
# DNS Analytics Technical Report
## Domain: {data.get('domain', 'Unknown')}
## Analysis Period: {data.get('start_time', 'Unknown')} - {data.get('duration_minutes', 'N/A')} minutes

### Query Distribution Analysis
"""
        
        query_dist = data.get("query_distribution", {})
        if query_dist.get("query_counts"):
            report += "| Query Type | Total Records | Avg Records/Sample | Success Rate | Avg Response Time |\n"
            report += "|------------|---------------|-------------------|--------------|-------------------|\n"
            
            summary = data.get("summary", {}).get("query_type_summary", {})
            for qtype, qdata in summary.items():
                avg_records = qdata.get("average_records", 0)
                success_rate = qdata.get("success_rate", 0)
                response_time = qdata.get("average_response_time_ms", 0)
                
                total_records = query_dist["query_counts"].get(qtype, {}).get("total", 0)
                report += f"| {qtype} | {total_records} | {avg_records:.2f} | {success_rate:.1f}% | {response_time:.2f}ms |\n"
        
        # Geographic Analysis
        report += "\n### Geographic Distribution\n"
        geo_analysis = data.get("geographic_analysis", {})
        if geo_analysis.get("location_frequency"):
            report += "**Regional Distribution:**\n"
            for location, count in geo_analysis["location_frequency"].items():
                report += f"- {location}: {count} nameservers\n"
        
        if geo_analysis.get("provider_distribution"):
            report += "\n**Provider Distribution:**\n"
            for provider, count in geo_analysis["provider_distribution"].items():
                report += f"- {provider}: {count} servers\n"
        
        # Temporal Patterns
        temporal = data.get("temporal_patterns", {})
        if temporal.get("peak_usage_times"):
            report += f"\n### Peak Usage Times\n"
            report += f"Identified peak periods: {', '.join(temporal['peak_usage_times'])}\n"
        
        return report
    
    def _generate_geographic_report(self, data: Dict) -> str:
        """Generate geographic-focused report"""
        report = f"""
# DNS Geographic Analysis Report
## Domain: {data.get('domain', 'Unknown')}

### Geographic Distribution Summary
"""
        
        geo_analysis = data.get("geographic_analysis", {})
        
        if geo_analysis.get("location_frequency"):
            total_locations = len(geo_analysis["location_frequency"])
            total_servers = sum(geo_analysis["location_frequency"].values())
            
            report += f"- **Total geographic regions:** {total_locations}\n"
            report += f"- **Total nameservers analyzed:** {total_servers}\n"
            report += f"- **Anycast servers detected:** {len(geo_analysis.get('anycast_servers', set()))}\n\n"
            
            report += "### Regional Breakdown\n"
            for location, count in sorted(geo_analysis["location_frequency"].items()):
                percentage = (count / total_servers) * 100 if total_servers > 0 else 0
                report += f"- **{location}**: {count} servers ({percentage:.1f}%)\n"
        
        return report
    
    def _generate_performance_report(self, data: Dict) -> str:
        """Generate performance-focused report"""
        report = f"""
# DNS Performance Analysis Report  
## Domain: {data.get('domain', 'Unknown')}

### Response Time Analysis
"""
        
        perf_analysis = data.get("performance_analysis", {})
        
        if perf_analysis.get("slowest_queries"):
            report += "**Slowest Query Types:**\n"
            for qtype, perf_data in perf_analysis["slowest_queries"].items():
                max_time = perf_data.get("max_time", 0)
                timestamp = perf_data.get("timestamp", "Unknown")
                report += f"- {qtype}: {max_time:.2f}ms (at {timestamp})\n"
        
        # Temporal performance trends
        if perf_analysis.get("response_time_history"):
            report += "\n### Temporal Performance Trends\n"
            report += "| Time | Average Response Time | Query Volume |\n"
            report += "|------|----------------------|-------------|\n"
            
            temporal_trends = data.get("temporal_patterns", {}).get("response_time_trends", {})
            for time_key in sorted(temporal_trends.keys()):
                trend_data = temporal_trends[time_key]
                avg_time = trend_data.get("average_response_time", 0)
                query_count = trend_data.get("query_count", 0)
                report += f"| {time_key} | {avg_time:.2f}ms | {query_count} queries |\n"
        
        return report