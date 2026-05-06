import os
import colorama
import tls_client
from datetime import datetime

# --- INITIALIZATION ---
colorama.init(autoreset=True)
RED = colorama.Fore.RED
GREEN = colorama.Fore.GREEN
PURPLE = colorama.Fore.MAGENTA
CYAN = colorama.Fore.CYAN
RESET = colorama.Fore.RESET

def get_time():
    return datetime.now().strftime("%H:%M:%S")

def log(text, color=RESET):
    print(f"{PURPLE}[{get_time()}] {color}{text}")

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

# --- LOGO ---
def draw_logo():
    logo = f"""
    {PURPLE}  ██████╗ ██╗  ██╗    ██████╗  ██████╗  ██████╗ ███████╗████████╗
    {PURPLE}  ██╔══██╗╚██╗██╔╝    ██╔══██╗██╔═══██╗██╔═══██╗██╔════╝╚══██╔══╝
    {PURPLE}  ██████╔╝ ╚███╔╝     ██████╔╝██║   ██║██║   ██║███████╗   ██║   
    {PURPLE}  ██╔══██╗ ██╔██╗     ██╔══██╗██║   ██║██║   ██║╚════██║   ██║   
    {PURPLE}  ██║  ██║██╔╝ ██╗    ██████╔╝╚██████╔╝╚██████╔╝███████║   ██║   
    {PURPLE}  ╚═╝  ╚═╝╚═╝  ╚═╝    ╚═════╝  ╚═════╝  ╚═════╝ ╚══════╝   ╚═╝   
    {CYAN}  ════════════════ RX BOOSTER TECHNOLOGY v1.1 ════════════════
    """
    print(logo)

# --- CORE LOGIC ---
class Nitro:
    def __init__(self, token: str):
        self.token = token
        self.headers = {
            "accept": "*/*",
            "authorization": token,
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) discord/1.0.9007 Chrome/91.0.4472.164 Electron/13.6.6 Safari/537.36",
            "x-super-properties": "eyJvcyI6IldpbmRvd3MiLCJicm93c2VyIjoiRGlzY29yZCBDbGllbnQiLCJyZWxlYXNlX2NoYW5uZWwiOiJzdGFibGUiLCJjbGllbnRfdmVyc2lvbiI6IjEuMC45MDA3Iiwib3NfdmVyc2lvbiI6IjEwLjAuMTkwNDMiLCJvc19hcmNoIjoieDY0Iiwic3lzdGVtX2xvY2FsZSI6ImVuLVVTIiwiY2xpZW50X2J1aWxkX251bWJlciI6MTYxODQyLCJjbGllbnRfZXZlbnRfc291cmNlIjpudWxsfQ=="
        }
        self.session = tls_client.Session(client_identifier="chrome_107") #
        self.sub_ids = []

    def check_nitro(self):
        try:
            res = self.session.get(
                "https://discord.com/api/v9/users/@me/guilds/premium/subscription-slots",
                headers=self.headers,
            ) #
            if res.status_code == 200:
                for sub in res.json():
                    self.sub_ids.append(sub["id"]) #
                if self.sub_ids:
                    log(f"SUCCESS: {self.token[:20]}... has {len(self.sub_ids)} slots.", GREEN)
                    return True
                log(f"NO NITRO: {self.token[:20]}...", RED)
            else:
                log(f"INVALID: {self.token[:20]}...", RED)
        except Exception as e:
            log(f"ERROR: Connection failed.", RED)
        return False

    def boost(self, guild_id):
        for i, slot_id in enumerate(self.sub_ids):
            self.headers["Content-Type"] = "application/json"
            r = self.session.put(
                url=f"https://discord.com/api/v9/guilds/{guild_id}/premium/subscriptions",
                headers=self.headers,
                json={"user_premium_guild_subscription_slot_ids": [slot_id]},
            ) #[cite: 1]
            if r.status_code == 201:
                log(f"BOOST SUCCESS: Slot {i+1} applied.", GREEN)
            elif r.status_code == 400:
                log(f"BOOST FAILED: Slot {i+1} already used.", RED)
            else:
                log(f"ERROR: {r.status_code}", RED)

# --- MAIN INTERFACE ---
def main():
    clear()
    draw_logo()
    
    print(f"{PURPLE}[1]{RESET} Check Tokens")
    print(f"{PURPLE}[2]{RESET} Start Boosting")
    print(f"{PURPLE}[3]{RESET} Exit")
    
    choice = input(f"\n{PURPLE}REAPER > {RESET}")

    if choice == "1":
        with open("tokens.txt", "r") as f:
            tokens = f.read().splitlines()
        log(f"Checking {len(tokens)} tokens...")
        for t in tokens:
            Nitro(t).check_nitro()
        input(f"\n{CYAN}Press Enter to return to menu...")
        main()

    elif choice == "2":
        guild_id = input(f"{CYAN}Enter Guild ID: {RESET}") #[cite: 1]
        with open("tokens.txt", "r") as f:
            tokens = f.read().splitlines()
        for t in tokens:
            bot = Nitro(t)
            if bot.check_nitro():
                bot.boost(guild_id) #[cite: 1]
        input(f"\n{CYAN}Boost completed. Press Enter...")
        main()

    elif choice == "3":
        exit()

if __name__ == "__main__":
    main()