import asyncio
import os
import sys
import random
from datetime import datetime
from playwright.async_api import async_playwright
from colorama import Fore, Style, init

init(autoreset=True)

# --- CONFIGURATION ---
TARGET_URL = "https://guns.lol/fitzypopper"
PROXY_FILE = r"proxies.txt"  # Relative path for easier portability
MAX_CONCURRENT_BROWSERS = 25  # Optimized for 32GB RAM
TIMEOUT = 15000              # 15 seconds
# ----------------------

stats = {"success": 0, "failed": 0, "start_time": datetime.now()}

def print_status():
    elapsed = (datetime.now() - stats["start_time"]).total_seconds()
    rpm = (stats["success"] / elapsed * 60) if elapsed > 0 else 0
    # Clear console and print status
    sys.stdout.write("\033[H\033[J")
    print(f"{Fore.CYAN}=== GUNS.LOL PLAYWRIGHT STEALTH BOT ==={Style.RESET_ALL}")
    print(f"{Fore.GREEN}SUCCESS: {stats['success']} | {Fore.RED}FAILED: {stats['failed']}")
    print(f"{Fore.YELLOW}SPEED:   {rpm:.1f} views/min")
    print(f"{Fore.MAGENTA}{'-'*40}")

async def run_proxy(pw, proxy_str, sem):
    async with sem:
        p_addr = proxy_str if "://" in proxy_str else f"socks5://{proxy_str}"
        browser = None
        try:
            # 1. Launch with flags to hide automation status
            browser = await pw.chromium.launch(
                headless=True, 
                proxy={"server": p_addr},
                args=["--disable-blink-features=AutomationControlled"]
            )
            
            context = await browser.new_context(
                user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36",
                viewport={'width': 1920, 'height': 1080}
            )
            page = await context.new_page()
            
            # 2. Navigate to target
            await page.goto(TARGET_URL, wait_until="domcontentloaded", timeout=TIMEOUT)
            
            # 3. SIMULATE HUMAN BEHAVIOR
            # Move mouse to random locations
            for _ in range(3):
                x = random.randint(100, 700)
                y = random.randint(100, 700)
                await page.mouse.move(x, y, steps=10) # Smooth movement
                await asyncio.sleep(random.uniform(0.5, 1.5))

            # 4. Scroll up and down
            await page.mouse.wheel(0, random.randint(300, 600))
            await asyncio.sleep(1)
            await page.mouse.wheel(0, -200)

            # 5. Click background to verify activity
            await page.mouse.click(random.randint(10, 50), random.randint(10, 50))

            # 6. Wait for view event to register
            await asyncio.sleep(random.randint(10, 15)) 
            
            stats["success"] += 1
        except Exception:
            stats["failed"] += 1
        finally:
            if browser:
                await browser.close()
            print_status()

async def main():
    if not os.path.exists(PROXY_FILE):
        print(f"{Fore.RED}Could not find {PROXY_FILE}")
        return

    with open(PROXY_FILE, "r", encoding="utf-8", errors="ignore") as f:
        proxies = [line.strip() for line in f if line.strip()]

    print(f"{Fore.CYAN}Loaded {len(proxies)} proxies. Starting engines...")
    await asyncio.sleep(1)

    async with async_playwright() as pw:
        sem = asyncio.Semaphore(MAX_CONCURRENT_BROWSERS)
        tasks = []
        
        for p in proxies:
            tasks.append(run_proxy(pw, p, sem))
            
        await asyncio.gather(*tasks)

    print(f"\n{Fore.GREEN}FINISHED! All proxies processed.")

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print(f"\n{Fore.YELLOW}Aborted by user.")