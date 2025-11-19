import random
import argparse
from typing import List
import os

class GSDInserter:
    def __init__(self):
        # GSD patterns based on common phishing tactics
        self.brands = ['paypal', 'microsoft', 'apple', 'google', 'amazon', 
                      'netflix', 'facebook', 'instagram', 'whatsapp', 'twitter',
                      'linkedin', 'ebay', 'wellsfargo', 'bankofamerica', 'chase']
        
        self.actions = ['login', 'verify', 'secure', 'update', 'confirm', 
                       'validate', 'authorize', 'authenticate', 'security', 'account']
        
        self.modifiers = ['support', 'help', 'service', 'billing', 'payment',
                         'recovery', 'access', 'identity', 'credentials', 'portal']
        
        self.tlds = ['.com', '.net', '.org', '.info', '.icu', '.top', '.xyz', 
                    '.online', '.site', '.club', '.work', '.shop']

    def generate_gsd_domain(self) -> str:
        """Generate a single GSD domain using linguistic patterns"""
        pattern_type = random.choice([
            'brand_action_random',
            'action_brand_random', 
            'brand_modifier_random',
            'modifier_brand_random'
        ])
        
        if pattern_type == 'brand_action_random':
            return f"{random.choice(self.brands)}{random.choice(self.actions)}{random.randint(100,9999)}{random.choice(self.tlds)}"
        
        elif pattern_type == 'action_brand_random':
            return f"{random.choice(self.actions)}{random.choice(self.brands)}{random.randint(10,999)}{random.choice(self.tlds)}"
        
        elif pattern_type == 'brand_modifier_random':
            return f"{random.choice(self.brands)}{random.choice(self.modifiers)}{random.randint(100,999)}{random.choice(self.tlds)}"
        
        else:  # modifier_brand_random
            return f"{random.choice(self.modifiers)}{random.choice(self.brands)}{random.randint(1000,9999)}{random.choice(self.tlds)}"

    def read_domains_from_file(self, filename: str) -> List[str]:
        """Read domains from input file"""
        domains = []
        try:
            with open(filename, 'r', encoding='utf-8') as file:
                for line in file:
                    domain = line.strip()
                    if domain:  # Skip empty lines
                        domains.append(domain)
            print(f"✓ Read {len(domains)} domains from {filename}")
            return domains
        except FileNotFoundError:
            print(f"✗ Error: File {filename} not found")
            return []
        except Exception as e:
            print(f"✗ Error reading file: {e}")
            return []

    def insert_gsd_domains(self, original_domains: List[str], num_gsd: int = 4500) -> List[str]:
        """Insert GSD domains randomly throughout the list"""
        if len(original_domains) == 0:
            print("✗ No domains to process")
            return []
        
        print(f"✓ Starting with {len(original_domains)} original domains")
        print(f"✓ Generating {num_gsd} GSD domains...")
        
        # Generate all GSD domains
        gsd_domains = [self.generate_gsd_domain() for _ in range(num_gsd)]
        print(f"✓ Generated {len(gsd_domains)} GSD domains")
        
        # Combine lists
        all_domains = original_domains + gsd_domains
        
        # Shuffle randomly
        random.shuffle(all_domains)
        print(f"✓ Shuffled {len(all_domains)} total domains")
        
        return all_domains

    def save_domains_to_file(self, domains: List[str], filename: str):
        """Save domains to output file"""
        try:
            with open(filename, 'w', encoding='utf-8') as file:
                for domain in domains:
                    file.write(domain + '\n')
            print(f"✓ Saved {len(domains)} domains to {filename}")
        except Exception as e:
            print(f"✗ Error saving file: {e}")

    def analyze_output(self, domains: List[str], original_count: int):
        """Analyze the final output"""
        gsd_count = len(domains) - original_count
        gsd_percentage = (gsd_count / len(domains)) * 100
        
        print("\n" + "="*50)
        print("OUTPUT ANALYSIS")
        print("="*50)
        print(f"Total domains: {len(domains):,}")
        print(f"Original domains: {original_count:,}")
        print(f"GSD domains inserted: {gsd_count:,}")
        print(f"GSD percentage: {gsd_percentage:.2f}%")
        
        # Show some sample GSD domains
        print(f"\nSample GSD domains generated:")
        gsd_samples = [d for d in domains if any(brand in d for brand in self.brands)]
        for i, sample in enumerate(gsd_samples[:10]):
            print(f"  {i+1}. {sample}")

def main():
    parser = argparse.ArgumentParser(description='Insert GSD domains into PhishTank list')
    parser.add_argument('input_file', help='Input file with PhishTank domains')
    parser.add_argument('-o', '--output', default='phishing_domains_with_gsd.txt', 
                       help='Output filename (default: phishing_domains_with_gsd.txt)')
    parser.add_argument('-n', '--num-gsd', type=int, default=4500,
                       help='Number of GSD domains to insert (default: 4500)')
    
    args = parser.parse_args()
    
    # Check if input file exists
    if not os.path.exists(args.input_file):
        print(f"✗ Error: Input file '{args.input_file}' not found")
        return
    
    # Initialize inserter
    inserter = GSDInserter()
    
    # Read original domains
    original_domains = inserter.read_domains_from_file(args.input_file)
    if not original_domains:
        return
    
    # Check if we have enough original domains
    if len(original_domains) < 25500:
        print(f"⚠ Warning: Expected 25,500 domains but found {len(original_domains)}")
        print("  Continuing anyway...")
    
    # Insert GSD domains
    final_domains = inserter.insert_gsd_domains(original_domains, args.num_gsd)
    
    if not final_domains:
        return
    
    # Save to file
    inserter.save_domains_to_file(final_domains, args.output)
    
    # Analyze results
    inserter.analyze_output(final_domains, len(original_domains))
    
    print(f"\n🎉 Successfully created enhanced phishing database!")
    print(f"   Input: {len(original_domains):,} domains from {args.input_file}")
    print(f"   Added: {args.num_gsd:,} GSD domains")
    print(f"   Output: {len(final_domains):,} domains in {args.output}")

if __name__ == "__main__":
    main()