import os
from proxyscrape import create_collector
from colorama import Fore, Style, init

init(autoreset=True)

# --- CONFIGURATION ---
OUTPUT_FILE = "proxies.txt"
# Resource types to retrieve. SOCKS5 is recommended for Guns.lol.
# You can add 'http' or 'socks4' to the list if you need more volume.
RESOURCE_TYPES = ['socks5'] 
# ----------------------

def scrape_to_file():
    print(f"{Fore.CYAN}Starting proxy collection...")
    
    # Initialize the collector with a unique name and desired resource types
    collector = create_collector('guns-lol-scraper', RESOURCE_TYPES)
    
    # Force a refresh from public proxy sources
    print(f"{Fore.YELLOW}Fetching data from public providers (this may take a moment)...")
    try:
        collector.refresh_proxies(force=True)
        
        # Retrieve the list of proxy objects
        proxy_list = collector.get_proxies()
        
        if not proxy_list:
            print(f"{Fore.RED}No proxies were found. Try adding 'http' to RESOURCE_TYPES.")
            return

        # Save to the output file in host:port format
        with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
            for p in proxy_list:
                # Format: 1.2.3.4:8080
                f.write(f"{p.host}:{p.port}\n")
        
        print(f"{Fore.GREEN}SUCCESS! Saved {len(proxy_list)} proxies to {OUTPUT_FILE}")
        print(f"{Fore.WHITE}You can now run 'python main.py' to start the bot.")
        
    except Exception as e:
        print(f"{Fore.RED}An error occurred during scraping: {e}")

if __name__ == "__main__":
    scrape_to_file()