import random
import argparse
from typing import List

class GSDGenerator:
    def __init__(self):
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

def main():
    parser = argparse.ArgumentParser(description='Add GSD domains to legitimate domains list')
    parser.add_argument('input_file', help='Input file with legitimate domains')
    parser.add_argument('-o', '--output', default='new_domains_with_gsd.txt', 
                       help='Output filename (default: new_domains_with_gsd.txt)')
    parser.add_argument('-n', '--num-gsd', type=int, default=522,
                       help='Number of GSD domains to add (default: 522)')
    
    args = parser.parse_args()
    
    # Read legitimate domains
    try:
        with open(args.input_file, 'r') as f:
            legitimate_domains = [line.strip() for line in f if line.strip()]
        print(f"✓ Read {len(legitimate_domains)} legitimate domains from {args.input_file}")
    except FileNotFoundError:
        print(f"✗ Error: File {args.input_file} not found")
        return
    except Exception as e:
        print(f"✗ Error reading file: {e}")
        return
    
    # Initialize GSD generator
    generator = GSDGenerator()
    
    # Generate GSD domains
    print(f"✓ Generating {args.num_gsd} GSD domains...")
    gsd_domains = [generator.generate_gsd_domain() for _ in range(args.num_gsd)]
    
    # Combine lists
    all_domains = legitimate_domains + gsd_domains
    
    # Shuffle randomly
    random.shuffle(all_domains)
    
    # Save to file
    try:
        with open(args.output, 'w') as f:
            for domain in all_domains:
                f.write(domain + '\n')
        print(f"✓ Saved {len(all_domains)} domains to {args.output}")
    except Exception as e:
        print(f"✗ Error saving file: {e}")
        return
    
    # Print summary
    print("\n" + "="*50)
    print("SUMMARY")
    print("="*50)
    print(f"Legitimate domains: {len(legitimate_domains):,}")
    print(f"GSD domains added: {len(gsd_domains):,}")
    print(f"Total domains: {len(all_domains):,}")
    print(f"GSD percentage: {(len(gsd_domains)/len(all_domains))*100:.2f}%")
    
    # Show some samples
    print(f"\nSample GSD domains generated:")
    for i, gsd in enumerate(gsd_domains[:10]):
        print(f"  {i+1}. {gsd}")
    
    print(f"\n✅ Success! Created new domains file with {args.num_gsd} GSDs randomly inserted")

if __name__ == "__main__":
    main()