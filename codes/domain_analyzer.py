#!/usr/bin/env python3
"""
Author: Mert SARICA
E-mail: mert [ . ] sarica [ @ ] gmail [ . ] com
URL: https://www.hack4career.com

Domain Typosquatting Analyzer
Analyzes CSV files containing domain paths to detect brand names and typosquatting attempts.
"""

import pandas as pd
import re
from urllib.parse import urlparse
from difflib import SequenceMatcher
from collections import defaultdict, Counter
import Levenshtein
import unicodedata
import string

class DomainAnalyzer:
    def __init__(self):
        self.brand_domains = {}
        self.typosquats = []
        self.legitimate_domains = []
        
    def normalize_text(self, text):
        """Normalize text for better comparison (remove accents, lowercase, etc.)"""
        # Remove accents and special characters
        text = unicodedata.normalize('NFD', text)
        text = ''.join(c for c in text if unicodedata.category(c) != 'Mn')
        # Convert to lowercase and remove spaces, hyphens, underscores
        return text.lower().replace(' ', '').replace('-', '').replace('_', '')
    
    def extract_domain_info(self, file_path):
        """Extract domain name and brand name from file path"""
        # Remove .png extension
        path = file_path.replace('.png', '')
        
        # Split path by '/' to get components
        parts = path.split('/')
        
        if len(parts) >= 3:
            # Expected format: Crypto/BrandName/domain.name
            category = parts[0]
            brand_folder = parts[1]
            domain = parts[2]
            
            return {
                'category': category,
                'brand_folder': brand_folder,
                'domain': domain,
                'full_path': file_path
            }
        
        return None
    
    def extract_main_domain(self, domain):
        """Extract main domain from URL or domain string"""
        if not domain.startswith('http'):
            domain = 'http://' + domain
        
        try:
            parsed = urlparse(domain)
            hostname = parsed.hostname or parsed.netloc
            
            # Remove www. prefix
            if hostname.startswith('www.'):
                hostname = hostname[4:]
                
            return hostname
        except:
            return domain
    
    def get_domain_parts(self, domain):
        """Get different parts of domain for analysis"""
        main_domain = self.extract_main_domain(domain)
        
        # Split by dots to get parts
        parts = main_domain.split('.')
        
        # Get the main domain name (usually the second-to-last part for .com, .org, etc.)
        if len(parts) >= 2:
            domain_name = parts[-2]  # e.g., 'btcturk' from 'btcturk.co.in'
            tld = '.'.join(parts[-1:])  # e.g., 'in' from 'btcturk.co.in'
            
            # Handle cases like .co.uk, .co.in etc.
            if len(parts) >= 3 and parts[-2] in ['co', 'com', 'net', 'org']:
                domain_name = parts[-3]
                tld = '.'.join(parts[-2:])
        else:
            domain_name = parts[0] if parts else main_domain
            tld = ''
            
        return {
            'full_domain': main_domain,
            'domain_name': domain_name,
            'tld': tld,
            'subdomains': parts[:-2] if len(parts) > 2 else []
        }
    
    def similarity_score(self, s1, s2):
        """Calculate similarity between two strings"""
        s1_norm = self.normalize_text(s1)
        s2_norm = self.normalize_text(s2)
        
        # Use multiple similarity metrics
        seq_match = SequenceMatcher(None, s1_norm, s2_norm).ratio()
        levenshtein_ratio = 1 - (Levenshtein.distance(s1_norm, s2_norm) / max(len(s1_norm), len(s2_norm)))
        
        return max(seq_match, levenshtein_ratio)
    
    def detect_typosquatting_patterns(self, domain_name, brand_name):
        """Detect various typosquatting patterns"""
        domain_norm = self.normalize_text(domain_name)
        brand_norm = self.normalize_text(brand_name)
        
        patterns = []
        
        # 1. Character omission (turkishairlins → turkishairlines, vakıfbank → vkfbnk)
        if len(domain_norm) < len(brand_norm):
            # Check if domain is a subsequence of brand
            if self.is_subsequence(domain_norm, brand_norm):
                patterns.append("character_omission")
        
        # 2. Single character omission (more sensitive detection)  
        if abs(len(domain_norm) - len(brand_norm)) == 1:
            longer = brand_norm if len(brand_norm) > len(domain_norm) else domain_norm
            shorter = domain_norm if len(domain_norm) < len(brand_norm) else brand_norm
            
            # Check if removing one character from longer string gives shorter string
            for i in range(len(longer)):
                if longer[:i] + longer[i+1:] == shorter:
                    patterns.append("single_char_omission")
                    break
        
        # 3. Character substitution/addition
        edit_distance = Levenshtein.distance(domain_norm, brand_norm)
        if 1 <= edit_distance <= 3 and len(domain_norm) >= len(brand_norm) - 2:
            patterns.append("character_substitution")
        
        # 4. Hyphenation/separation tricks
        brand_with_hyphens = brand_norm.replace('', '-')[1:-1]  # Add hyphens between chars
        if any(sep in domain_name.lower() for sep in ['-', '_']) and brand_norm in domain_norm.replace('-', '').replace('_', ''):
            patterns.append("hyphenation_trick")
        
        # 5. Prefix/suffix addition
        if brand_norm in domain_norm and brand_norm != domain_norm:
            patterns.append("prefix_suffix_addition")
        
        # 6. Homograph attack (similar looking characters)
        if self.has_homograph_chars(domain_name, brand_name):
            patterns.append("homograph_attack")
        
        # 7. Keyboard proximity typos
        if self.has_keyboard_typos(domain_norm, brand_norm):
            patterns.append("keyboard_typo")
            
        return patterns
    
    def is_subsequence(self, s, t):
        """Check if s is a subsequence of t"""
        i = 0
        for char in t:
            if i < len(s) and char == s[i]:
                i += 1
        return i == len(s)
    
    def has_homograph_chars(self, domain, brand):
        """Detect homograph characters (visually similar)"""
        # Common homograph pairs
        homographs = {
            'a': 'à á â ã ä å α а',
            'e': 'è é ê ë ε е',
            'i': 'ì í î ï ι і',
            'o': 'ò ó ô õ ö ø ο о',
            'u': 'ù ú û ü υ у',
            'c': 'ç ć č с',
            'n': 'ñ ń ň н',
            'r': 'ř р',
            's': 'š ś ş ѕ',
            'y': 'ý ÿ у',
            'p': 'р',
            'h': 'һ',
            'x': 'х',
        }
        
        domain_chars = set(domain.lower())
        brand_chars = set(brand.lower())
        
        for char in domain_chars:
            if char in string.ascii_lowercase:
                continue
            # Check if this non-ASCII char could be a homograph
            for ascii_char, variants in homographs.items():
                if char in variants and ascii_char in brand_chars:
                    return True
        
        return False
    
    def has_keyboard_typos(self, domain, brand):
        """Detect keyboard proximity typos"""
        keyboard_layout = {
            'q': 'wae', 'w': 'qerasd', 'e': 'wrdsfa', 'r': 'etfgd',
            't': 'rygfh', 'y': 'tugh', 'u': 'yijh', 'i': 'uojk',
            'o': 'ipkl', 'p': 'ol',
            'a': 'qwszx', 's': 'awedxz', 'd': 'serfcx', 'f': 'drtgvc',
            'g': 'ftyhbv', 'h': 'gyujnb', 'j': 'huikmn', 'k': 'jiolm',
            'l': 'kop',
            'z': 'asx', 'x': 'zsdc', 'c': 'xdfv', 'v': 'cfgb',
            'b': 'vghn', 'n': 'bhjm', 'm': 'njk'
        }
        
        if abs(len(domain) - len(brand)) != 1:
            return False
            
        # Check for single character keyboard typo
        for i in range(min(len(domain), len(brand))):
            if domain[i] != brand[i]:
                nearby_chars = keyboard_layout.get(brand[i], '')
                if domain[i] in nearby_chars:
                    return True
                break
                
        return False
    
    def get_brand_variations(self, brand_name):
        """Get various brand name variations including common translations"""
        variations = [brand_name]
        
        # Common brand translations and variations
        brand_translations = {
            'turk hava yolları': ['turkish airlines', 'turkishairlines', 'thy'],
            'turkish airlines': ['turk hava yolları', 'turkishairlines', 'thy'],
            'türk hava yolları': ['turkish airlines', 'turkishairlines', 'thy'],
            'vakıfbank': ['vakifbank', 'vakif bank'],
            'vakifbank': ['vakıfbank', 'vakif bank'],
            'garanti bbva': ['garanti', 'garantibbva', 'garanti bank'],
            'garanti': ['garanti bbva', 'garantibbva', 'garanti bank'],
            'yapı kredi': ['yapi kredi', 'yapikredi', 'ykb'],
            'yapi kredi': ['yapı kredi', 'yapikredi', 'ykb'],
            'türkiye iş bankası': ['is bank', 'isbank', 'turkiye is bankasi'],
            'is bank': ['türkiye iş bankası', 'isbank', 'turkiye is bankasi'],
            'hepsiburada': ['hepsi burada'],
            'hepsi burada': ['hepsiburada'],
            'n11': ['n11.com'],
            'trendyol': ['trendy ol'],
            'gittigidiyor': ['gitti gidiyor'],
            'gitti gidiyor': ['gittigidiyor'],
        }
        
        # Add direct translations if available
        brand_lower = brand_name.lower()
        if brand_lower in brand_translations:
            variations.extend(brand_translations[brand_lower])
        
        # Add variations without spaces, hyphens
        for var in variations.copy():
            variations.append(var.replace(' ', ''))
            variations.append(var.replace(' ', '').replace('-', ''))
        
        # Remove duplicates and return
        return list(set(variations))
    
    def is_typosquat_advanced(self, domain_name, brand_name, threshold=0.6):
        """Enhanced typosquat detection with brand variations"""
        brand_variations = self.get_brand_variations(brand_name)
        
        best_similarity = 0
        best_patterns = []
        is_typo = False
        
        # Test against all brand variations
        for brand_var in brand_variations:
            similarity = self.similarity_score(domain_name, brand_var)
            patterns = self.detect_typosquatting_patterns(domain_name, brand_var)
            
            # Update best match
            if similarity > best_similarity:
                best_similarity = similarity
                best_patterns = patterns
            
            # Check if this variation indicates typosquatting
            if similarity >= threshold and similarity < 0.95:
                is_typo = True
            elif patterns and similarity >= 0.3:
                is_typo = True
        
        return is_typo, best_patterns, best_similarity
    
    def analyze_csv(self, csv_file_path):
        """Main function to analyze the CSV file"""
        print(f"Loading CSV file: {csv_file_path}")
        
        try:
            df = pd.read_csv(csv_file_path)
        except Exception as e:
            print(f"Error reading CSV: {e}")
            return
        
        print(f"Found {len(df)} rows in CSV")
        
        # Determine which column contains the file paths
        path_column = None
        for col in df.columns:
            if df[col].dtype == 'object':
                # Check if column contains .png file paths
                has_png = df[col].astype(str).str.endswith('.png').any()
                if has_png:
                    path_column = col
                    break
        
        if not path_column:
            print("Could not find column with .png file paths")
            print("Available columns:", df.columns.tolist())
            return
        
        print(f"Using column '{path_column}' for file paths")
        
        # Extract domain information and deduplicate
        domain_data = []
        brand_domains = defaultdict(list)
        seen_domains = set()  # Track unique domain paths to avoid duplicates
        
        for idx, row in df.iterrows():
            file_path = row[path_column]
            if pd.isna(file_path):
                continue
            
            # Skip if we've already processed this domain path
            if file_path in seen_domains:
                continue
                
            seen_domains.add(file_path)
            domain_info = self.extract_domain_info(file_path)
            if domain_info:
                domain_parts = self.get_domain_parts(domain_info['domain'])
                
                analysis_data = {
                    **domain_info,
                    **domain_parts,
                    'row_index': idx
                }
                
                domain_data.append(analysis_data)
                brand_domains[domain_info['brand_folder']].append(analysis_data)
        
        print(f"Extracted {len(domain_data)} unique domains (deduplicated from {len(df)} total rows)")
        print(f"Found {len(brand_domains)} brands")
        
        # Analyze each brand's domains
        results = {
            'brand_analysis': {},
            'typosquats_detected': [],
            'legitimate_domains': [],
            'summary': {}
        }
        
        total_domains = 0
        total_typosquats = 0
        total_legitimate = 0
        
        for brand_folder, domains in brand_domains.items():
            print(f"\nAnalyzing brand: {brand_folder}")
            
            brand_legitimate = []
            brand_typosquats = []
            
            for domain_data in domains:
                domain_name = domain_data['domain_name']
                brand_name = brand_folder
                
                # Check if it's a typosquat using enhanced detection
                is_typo, patterns, similarity = self.is_typosquat_advanced(domain_name, brand_name)
                
                analysis_result = {
                    **domain_data,
                    'similarity_score': similarity,
                    'typosquat_patterns': patterns,
                    'is_typosquat': is_typo
                }
                
                if is_typo:
                    brand_typosquats.append(analysis_result)
                    results['typosquats_detected'].append(analysis_result)
                else:
                    brand_legitimate.append(analysis_result)
                    results['legitimate_domains'].append(analysis_result)
            
            total_domains += len(domains)
            total_typosquats += len(brand_typosquats)
            total_legitimate += len(brand_legitimate)
            
            results['brand_analysis'][brand_folder] = {
                'total_domains': len(domains),
                'legitimate_count': len(brand_legitimate),
                'typosquat_count': len(brand_typosquats),
                'typosquat_ratio': len(brand_typosquats) / len(domains) if domains else 0,
                'legitimate_domains': brand_legitimate,
                'typosquats': brand_typosquats
            }
            
            print(f"  Total domains: {len(domains)}")
            print(f"  Legitimate: {len(brand_legitimate)}")
            print(f"  Typosquats: {len(brand_typosquats)}")
            print(f"  Typosquat ratio: {len(brand_typosquats) / len(domains) * 100:.1f}%" if domains else "  Typosquat ratio: 0%")
        
        # Overall summary
        results['summary'] = {
            'total_domains': total_domains,
            'total_brands': len(brand_domains),
            'total_legitimate': total_legitimate,
            'total_typosquats': total_typosquats,
            'overall_typosquat_ratio': total_typosquats / total_domains if total_domains else 0
        }
        
        return results
    
    def print_detailed_results(self, results):
        """Print detailed analysis results"""
        print("\n" + "="*80)
        print("DOMAIN TYPOSQUATTING ANALYSIS RESULTS")
        print("="*80)
        
        summary = results['summary']
        print(f"\nOVERALL SUMMARY:")
        print(f"Total Domains Analyzed: {summary['total_domains']}")
        print(f"Total Brands: {summary['total_brands']}")
        print(f"Legitimate Domains: {summary['total_legitimate']}")
        print(f"Typosquatting Domains: {summary['total_typosquats']}")
        print(f"Overall Typosquat Ratio: {summary['overall_typosquat_ratio']*100:.1f}%")
        
        print(f"\nBRAND-BY-BRAND ANALYSIS:")
        print("-" * 50)
        
        for brand, analysis in results['brand_analysis'].items():
            print(f"\nBrand: {brand}")
            print(f"  Total Domains: {analysis['total_domains']}")
            print(f"  Legitimate: {analysis['legitimate_count']}")
            print(f"  Typosquats: {analysis['typosquat_count']}")
            print(f"  Typosquat Ratio: {analysis['typosquat_ratio']*100:.1f}%")
            
            if analysis['legitimate_domains']:
                print(f"  Legitimate Domains:")
                for domain in analysis['legitimate_domains'][:5]:  # Show first 5
                    print(f"    - {domain['full_domain']}")
                if len(analysis['legitimate_domains']) > 5:
                    print(f"    ... and {len(analysis['legitimate_domains']) - 5} more")
            
            if analysis['typosquats']:
                print(f"  Typosquat Domains:")
                for domain in analysis['typosquats'][:5]:  # Show first 5
                    patterns_str = ", ".join(domain['typosquat_patterns']) if domain['typosquat_patterns'] else "low_similarity"
                    print(f"    - {domain['full_domain']} (similarity: {domain['similarity_score']:.2f}, patterns: {patterns_str})")
                if len(analysis['typosquats']) > 5:
                    print(f"    ... and {len(analysis['typosquats']) - 5} more")
        
        print(f"\nTOP TYPOSQUATTING PATTERNS:")
        print("-" * 30)
        
        # Count pattern frequencies
        pattern_counter = Counter()
        for typo in results['typosquats_detected']:
            for pattern in typo['typosquat_patterns']:
                pattern_counter[pattern] += 1
        
        for pattern, count in pattern_counter.most_common():
            print(f"  {pattern}: {count} occurrences")
    
    def save_results_to_csv(self, results, output_file="domain_analysis_results.csv"):
        """Save results to CSV file"""
        all_results = []
        
        for brand, analysis in results['brand_analysis'].items():
            for domain in analysis['legitimate_domains'] + analysis['typosquats']:
                all_results.append({
                    'brand': brand,
                    'domain': domain['full_domain'],
                    'domain_name': domain['domain_name'],
                    'is_typosquat': domain['is_typosquat'],
                    'similarity_score': domain['similarity_score'],
                    'typosquat_patterns': '; '.join(domain['typosquat_patterns']),
                    'full_path': domain['full_path']
                })
        
        results_df = pd.DataFrame(all_results)
        results_df.to_csv(output_file, index=False)
        print(f"\nResults saved to: {output_file}")


def main():
    """Main function to run the analysis"""
    import sys
    
    if len(sys.argv) != 2:
        print("Usage: python domain_analyzer.py <csv_file_path>")
        print("Example: python domain_analyzer.py domains.csv")
        return
    
    csv_file = sys.argv[1]
    
    analyzer = DomainAnalyzer()
    results = analyzer.analyze_csv(csv_file)
    
    if results:
        analyzer.print_detailed_results(results)
        analyzer.save_results_to_csv(results)


if __name__ == "__main__":
    main()