#!/usr/bin/env python3
"""
Author: Mert SARICA
E-mail: mert [ . ] sarica [ @ ] gmail [ . ] com
URL: https://www.hack4career.com

Domain Extension Analyzer
Analyzes domain extensions from CSV file and creates pie chart visualization
"""

import pandas as pd
import matplotlib.pyplot as plt
from collections import Counter
import argparse
import sys
from urllib.parse import urlparse
import re

class DomainExtensionAnalyzer:
    def __init__(self):
        self.domain_data = []
        self.extension_counts = Counter()
        
    def extract_extension(self, domain):
        """Extract the top-level domain (extension) from a domain name"""
        if not domain or pd.isna(domain):
            return 'unknown'
        
        # Clean the domain name
        domain = str(domain).lower().strip()
        
        # Remove protocol if present
        if domain.startswith(('http://', 'https://')):
            domain = urlparse(domain).netloc or urlparse(domain).path
        
        # Remove www. prefix
        if domain.startswith('www.'):
            domain = domain[4:]
        
        # Remove any path, query parameters, or fragments
        domain = domain.split('/')[0].split('?')[0].split('#')[0]
        
        # Handle edge cases
        if not domain or '.' not in domain:
            return 'no_extension'
        
        # Split by dots and get the extension
        parts = domain.split('.')
        
        # Handle complex TLDs like .co.uk, .com.tr, .co.in
        if len(parts) >= 3:
            # Check for common country code TLDs with subdomains
            last_two = f".{parts[-2]}.{parts[-1]}"
            common_complex_tlds = [
                '.co.uk', '.co.in', '.com.tr', '.net.tr', '.org.tr', '.co.za',
                '.com.au', '.co.jp', '.co.kr', '.com.mx', '.com.br', '.co.nz',
                '.ru.com', '.sa.com', '.uk.com', '.us.com', '.br.com'
            ]
            
            if last_two in common_complex_tlds:
                return last_two
        
        # Get the last part as extension
        extension = '.' + parts[-1]
        
        # Handle some special cases
        if extension == '.localhost' or extension == '.local':
            return '.local'
        
        return extension
    
    def load_and_analyze(self, csv_file):
        """Load CSV file and analyze domain extensions"""
        try:
            print(f"Loading CSV file: {csv_file}")
            df = pd.read_csv(csv_file)
            print(f"Loaded {len(df)} rows")
            
            # Try to find the domain column
            domain_column = None
            possible_columns = ['domain', 'Domain', 'DOMAIN', 'domains', 'full_domain']
            
            for col in possible_columns:
                if col in df.columns:
                    domain_column = col
                    break
            
            if not domain_column:
                # If no obvious column found, use the first column
                domain_column = df.columns[0]
                print(f"No 'domain' column found, using '{domain_column}'")
            else:
                print(f"Using column '{domain_column}' for domain analysis")
            
            # Extract extensions
            extensions = []
            for idx, row in df.iterrows():
                domain = row[domain_column]
                extension = self.extract_extension(domain)
                extensions.append(extension)
                
                # Store for detailed analysis
                self.domain_data.append({
                    'domain': domain,
                    'extension': extension,
                    'row_index': idx
                })
            
            # Count extensions
            self.extension_counts = Counter(extensions)
            
            print(f"Found {len(self.extension_counts)} unique extensions")
            return True
            
        except FileNotFoundError:
            print(f"Error: File '{csv_file}' not found!")
            return False
        except Exception as e:
            print(f"Error reading CSV file: {e}")
            return False
    
    def print_statistics(self):
        """Print detailed statistics about domain extensions"""
        if not self.extension_counts:
            print("No data to analyze!")
            return
        
        total_domains = sum(self.extension_counts.values())
        
        print("\n" + "="*60)
        print("DOMAIN EXTENSION ANALYSIS")
        print("="*60)
        
        print(f"Total Domains Analyzed: {total_domains:,}")
        print(f"Unique Extensions Found: {len(self.extension_counts)}")
        
        print(f"\nTop 20 Most Common Extensions:")
        print("-" * 40)
        
        for i, (ext, count) in enumerate(self.extension_counts.most_common(20), 1):
            percentage = (count / total_domains) * 100
            print(f"{i:2d}. {ext:<15} {count:>6,} domains ({percentage:5.1f}%)")
        
        if len(self.extension_counts) > 20:
            remaining = len(self.extension_counts) - 20
            print(f"    ... and {remaining} more extensions")
        
        # Category analysis
        print(f"\nExtension Categories:")
        print("-" * 25)
        
        categories = self.categorize_extensions()
        for category, extensions in categories.items():
            total_in_category = sum(self.extension_counts[ext] for ext in extensions)
            percentage = (total_in_category / total_domains) * 100
            print(f"{category:<20} {total_in_category:>6,} domains ({percentage:5.1f}%)")
    
    def categorize_extensions(self):
        """Categorize extensions by type"""
        categories = {
            'Generic (.com, .org, .net)': [],
            'Country Code (.tr, .uk, .de)': [],
            'New gTLD (.shop, .online, .site)': [],
            'Dynamic DNS (.ddns, .dyn)': [],
            'Suspicious/Unusual': [],
            'Local/Development': []
        }
        
        generic_tlds = {'.com', '.org', '.net', '.edu', '.gov', '.mil', '.int'}
        country_codes = {
            '.tr', '.uk', '.de', '.fr', '.jp', '.cn', '.ru', '.br', '.au', '.ca',
            '.in', '.mx', '.za', '.kr', '.it', '.es', '.nl', '.se', '.no', '.dk',
            '.com.tr', '.net.tr', '.org.tr', '.co.uk', '.co.in', '.com.au'
        }
        new_gtlds = {
            '.shop', '.online', '.site', '.store', '.tech', '.app', '.dev',
            '.web', '.blog', '.news', '.click', '.link', '.top', '.xyz'
        }
        dynamic_dns = {
            '.ddns', '.dyn', '.dynuddns', '.ddnsguru', '.duckdns', '.ddnsgeek'
        }
        local_dev = {'.local', '.localhost', '.test', '.dev', '.example'}
        
        for ext in self.extension_counts:
            if ext in generic_tlds:
                categories['Generic (.com, .org, .net)'].append(ext)
            elif ext in country_codes:
                categories['Country Code (.tr, .uk, .de)'].append(ext)
            elif ext in new_gtlds:
                categories['New gTLD (.shop, .online, .site)'].append(ext)
            elif any(dyn in ext for dyn in dynamic_dns):
                categories['Dynamic DNS (.ddns, .dyn)'].append(ext)
            elif ext in local_dev:
                categories['Local/Development'].append(ext)
            else:
                categories['Suspicious/Unusual'].append(ext)
        
        # Remove empty categories
        return {k: v for k, v in categories.items() if v}
    
    def create_pie_chart(self, output_file='domain_extensions_chart.png', top_n=15):
        """Create and save pie chart of domain extensions"""
        if not self.extension_counts:
            print("No data to visualize!")
            return False
        
        # Get top N extensions
        top_extensions = dict(self.extension_counts.most_common(top_n))
        
        # Group remaining into "Others"
        total_domains = sum(self.extension_counts.values())
        top_total = sum(top_extensions.values())
        
        if len(self.extension_counts) > top_n:
            others_count = total_domains - top_total
            top_extensions['Others'] = others_count
        
        # Prepare data for plotting
        labels = list(top_extensions.keys())
        sizes = list(top_extensions.values())
        
        # Create better color palette (avoiding light yellows and pale colors)
        vibrant_colors = [
            '#1f77b4',  # Blue
            '#ff7f0e',  # Orange
            '#2ca02c',  # Green
            '#d62728',  # Red
            '#9467bd',  # Purple
            '#8c564b',  # Brown
            '#e377c2',  # Pink
            '#7f7f7f',  # Gray
            '#17becf',  # Cyan
            '#bcbd22',  # Olive (darker than yellow)
            '#ff9999',  # Light Red
            '#66b3ff',  # Light Blue
            '#99ff99',  # Light Green
            '#ffcc99',  # Light Orange
            '#c2c2f0',  # Light Purple
            '#ffb3e6',  # Light Pink
            '#c4e17f',  # Light Olive
            '#76d7c4',  # Turquoise
            '#f7dc6f',  # Gold (better than pale yellow)
            '#bb8fce',  # Lavender
        ]
        
        # Extend colors if we have more segments than colors
        while len(vibrant_colors) < len(labels):
            vibrant_colors.extend(vibrant_colors)
        
        colors = vibrant_colors[:len(labels)]
        
        # Create figure and axis
        fig, ax = plt.subplots(figsize=(12, 8))
        
        # Create pie chart
        wedges, texts, autotexts = ax.pie(
            sizes, 
            labels=labels, 
            colors=colors,
            autopct=lambda pct: f'{pct:.1f}%\n({int(pct/100*total_domains):,})',
            startangle=90,
            textprops={'fontsize': 9}
        )
        
        # Customize the chart
        ax.set_title(f'Domain Extensions Distribution\n(Total: {total_domains:,} domains)', 
                    fontsize=16, fontweight='bold', pad=20)
        
        # Make percentage text bold
        for autotext in autotexts:
            autotext.set_weight('bold')
            autotext.set_color('white')
        
        # Add legend
        ax.legend(wedges, [f"{label}: {count:,} domains" for label, count in top_extensions.items()],
                 title="Extensions",
                 loc="center left",
                 bbox_to_anchor=(1, 0, 0.5, 1))
        
        plt.tight_layout()
        
        # Save the chart
        plt.savefig(output_file, dpi=300, bbox_inches='tight')
        print(f"\n📊 Pie chart saved as: {output_file}")
        
        # Show the chart
        plt.show()
        
        return True
    
    def save_detailed_report(self, output_file='domain_extension_report.csv'):
        """Save detailed report to CSV"""
        if not self.domain_data:
            return False
        
        # Create DataFrame with all data
        df = pd.DataFrame(self.domain_data)
        
        # Add extension statistics
        df['extension_count'] = df['extension'].map(self.extension_counts)
        df['extension_percentage'] = (df['extension_count'] / len(df)) * 100
        
        # Sort by extension frequency, then by domain name
        df = df.sort_values(['extension_count', 'domain'], ascending=[False, True])
        
        # Save to CSV
        df.to_csv(output_file, index=False)
        print(f"📄 Detailed report saved as: {output_file}")
        
        return True


def main():
    """Main function"""
    parser = argparse.ArgumentParser(description='Analyze domain extensions and create pie chart')
    parser.add_argument('csv_file', nargs='?', default='extracted_domains.csv',
                       help='CSV file containing domains (default: extracted_domains.csv)')
    parser.add_argument('-o', '--output', default='domain_extensions_chart.png',
                       help='Output image file for pie chart')
    parser.add_argument('-n', '--top', type=int, default=15,
                       help='Number of top extensions to show in chart (default: 15)')
    parser.add_argument('--report', action='store_true',
                       help='Generate detailed CSV report')
    parser.add_argument('--no-chart', action='store_true',
                       help='Skip creating pie chart (only show statistics)')
    
    args = parser.parse_args()
    
    # Create analyzer
    analyzer = DomainExtensionAnalyzer()
    
    # Load and analyze data
    print("🔍 Starting domain extension analysis...")
    success = analyzer.load_and_analyze(args.csv_file)
    
    if not success:
        sys.exit(1)
    
    # Print statistics
    analyzer.print_statistics()
    
    # Create pie chart unless disabled
    if not args.no_chart:
        print(f"\n📊 Creating pie chart...")
        analyzer.create_pie_chart(args.output, args.top)
    
    # Generate detailed report if requested
    if args.report:
        report_file = args.csv_file.replace('.csv', '_extension_report.csv')
        print(f"\n📄 Generating detailed report...")
        analyzer.save_detailed_report(report_file)
    
    print(f"\n✅ Domain extension analysis completed!")


def quick_analysis(csv_file='extracted_domains.csv'):
    """Quick function for basic usage"""
    analyzer = DomainExtensionAnalyzer()
    
    if analyzer.load_and_analyze(csv_file):
        analyzer.print_statistics()
        analyzer.create_pie_chart()
        return True
    
    return False


if __name__ == "__main__":
    # If no arguments provided, show usage
    if len(sys.argv) == 1:
        print("Domain Extension Analyzer")
        print("========================")
        print("\nUsage examples:")
        print("  python domain_extension_analyzer.py")
        print("  python domain_extension_analyzer.py my_domains.csv")
        print("  python domain_extension_analyzer.py extracted_domains.csv -o chart.png")
        print("  python domain_extension_analyzer.py domains.csv --top 20 --report")
        print("\nOptions:")
        print("  -o, --output    Output image file for pie chart")
        print("  -n, --top       Number of top extensions to show (default: 15)")
        print("  --report        Generate detailed CSV report")
        print("  --no-chart      Skip creating pie chart")
        print("\nFor simple usage:")
        print("  from domain_extension_analyzer import quick_analysis")
        print("  quick_analysis('my_domains.csv')")
    else:
        main()