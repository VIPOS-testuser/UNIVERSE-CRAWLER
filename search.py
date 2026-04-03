import requests
import time
import os

# Terminal ranglari
GREEN = '\033[92m'
CYAN = '\033[96m'
RED = '\033[91m'
YELLOW = '\033[93m'
RESET = '\033[0m'
BOLD = '\033[1m'

def print_banner():
    banner = f"""
{CYAN}{BOLD}
        ▗▖ ▗▖▗▖  ▗▖▗▄▄▄▖▗▖  ▗▖▗▄▄▄▖▗▄▄▖  ▗▄▄▖▗▄▄▄▖     ▗▄▄▖▗▄▄▖  ▗▄▖ ▗▖ ▗▖▗▖   ▗▄▄▄▖▗▄▄▖
        ▐▌ ▐▌▐▛▚▖▐▌  █  ▐▌  ▐▌▐▌   ▐▌ ▐▌▐▌   ▐▌       ▐▌   ▐▌ ▐▌▐▌ ▐▌▐▌ ▐▌▐▌   ▐▌   ▐▌ ▐▌
        ▐▌ ▐▌▐▌ ▝▜▌  █  ▐▌  ▐▌▐▛▀▀▘▐▛▀▚▖ ▝▀▚▖▐▛▀▀▘    ▐▌   ▐▛▀▚▖▐▛▀▜▌▐▌ ▐▌▐▌   ▐▛▀▀▘▐▛▀▚▖
        ▝▚▄▞▘▐▌  ▐▌▗▄█▄▖ ▝▚▞▘ ▐▙▄▄▖▐▌ ▐▌▗▄▄▞▘▐▙▄▄▖    ▝▚▄▄▖▐▌ ▐▌▐▌ ▐▌▐▙█▟▌▐▙▄▄▖▐▙▄▄▖▐▌ ▐▌

                                {YELLOW}Universe.exe OSINT Edition{CYAN}
                            {RED}--- Multi-Engine URL Extractor ---{RESET}
    """
    print(banner)

def ultra_search():
    print_banner()
    
    query = input(f"{BOLD}{YELLOW}Universe (Search) >>> {RESET}").strip()
    if not query: return

    url = "http://localhost:8080/search"
    headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36'}
    
    page = 1
    total = 0
    all_urls = [] # Faylga saqlash uchun ro'yxat

    print(f"\n{GREEN}[*] Barcha tizimlar bo'yicha qidirilmoqda...{RESET}")
    print(f"{RED}[!] To'xtatish uchun: Ctrl + C{RESET}\n")

    try:
        while True:
            params = {
                'q': query,
                'format': 'json',
                'pageno': page
            }

            try:
                response = requests.get(url, params=params, headers=headers, timeout=30)
                data = response.json()
                results = data.get('results', [])

                if not results:
                    print(f"\n{YELLOW}[+] Natijalar tugadi.{RESET}")
                    break

                for res in results:
                    total += 1
                    link = res.get('url')
                    all_urls.append(link)
                    # Faqat URLni terminalga chiqarish
                    print(f"{CYAN}[{total}]{RESET} {link}")

                page += 1
                time.sleep(0.5) 

            except Exception as e:
                print(f"\n{RED}[!] Aloqa xatosi: {e}{RESET}")
                break

    except KeyboardInterrupt:
        print(f"\n\n{RED}[!] Jarayon foydalanuvchi tomonidan to'xtatildi.{RESET}")

    # Faylga saqlash qismi
    if total > 0:
        print(f"\n{BOLD}{GREEN}[√] Jami {total} ta URL topildi.{RESET}")
        save_choice = input(f"\n{BOLD}{YELLOW}Natijalarni faylga saqlashni xohlaysizmi? (y/n): {RESET}").lower()
        
        if save_choice == 'y':
            filename = f"crawl_{query.replace(' ', '_')}_{int(time.time())}.txt"
            try:
                with open(filename, "w", encoding="utf-8") as f:
                    for url_link in all_urls:
                        f.write(url_link + "\n")
                print(f"{GREEN}[+] Muvaffaqiyatli saqlandi: {BOLD}{filename}{RESET}")
            except Exception as e:
                print(f"{RED}[!] Faylga yozishda xato: {e}{RESET}")
    else:
        print(f"\n{RED}[-] Hech qanday natija topilmadi.{RESET}")

if __name__ == "__main__":
    # Terminalni tozalash (ixtiyoriy)
    # os.system('clear') 
    ultra_search()
