#!/usr/bin/env python3
import requests
import time
from pathlib import Path

URL = "https://crt.sh/?q={domain}&output=json"
POPULAR_DOMAINS = [
    "google.com", "facebook.com", "youtube.com", "amazon.com", "twitter.com",
    "instagram.com", "linkedin.com", "microsoft.com", "apple.com", "netflix.com",
    "github.com", "stackoverflow.com", "reddit.com", "wikipedia.org", "cloudflare.com"
]
OUTPUT_FILE = "domains.txt"

def fetch_certificates(domain):
    """Fetch certificates for a domain from crt.sh."""
    for attempt in range(3):
        try:
            r = requests.get(
                URL.format(domain=domain),
                timeout=30,  # Increased timeout
                headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"},
                verify=False
            )
            if r.status_code == 200:
                return r.json()
            elif r.status_code == 429:  # Rate limited
                print(f"[!] Rate limited, waiting 10 seconds...")
                time.sleep(10)
                continue
            else:
                print(f"[!] HTTP {r.status_code} for {domain}")
                time.sleep(2)
        except requests.exceptions.Timeout:
            print(f"[!] Timeout fetching {domain} (attempt {attempt + 1})")
            time.sleep(5)
        except Exception as e:
            print(f"[!] Error fetching {domain}: {e}")
            time.sleep(2)
    return None

def extract_domains(entry):
    """Extract CN + SAN domains from a crt.sh JSON entry."""
    if not entry:
        return set()  # Return empty set instead of list

    domains = set()
    for item in entry:
        cn = item.get("common_name", "")
        if cn:
            domains.add(cn.lower())

        name_value = item.get("name_value", "")
        for d in name_value.split("\n"):
            d = d.strip().lower()
            if d:
                domains.add(d)

    return domains

def main():
    all_domains = set()

    print(f"[*] Collecting CT domains from popular sites…")

    for domain in POPULAR_DOMAINS:
        print(f"[+] Querying {domain}...")
        data = fetch_certificates(domain)
        domains = extract_domains(data)
        all_domains |= domains  # Now both are sets
        
        print(f"[+] {domain} → {len(domains)} domains → total: {len(all_domains)}")
        time.sleep(2)  # Be respectful to the server

    print(f"[✔] Finished: {len(all_domains)} domains collected.")

    with open(OUTPUT_FILE, "w") as f:
        for d in sorted(all_domains):
            f.write(d + "\n")

    print(f"[✔] Saved to {OUTPUT_FILE}")

if __name__ == "__main__":
    main()
