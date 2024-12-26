#!/usr/bin/env python3
import requests
from bs4 import BeautifulSoup
import re
import time
from colorama import Fore, Style, init
import argparse
from datetime import datetime
import urllib3
import random

# SSL uyarılarını kapat
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

init(autoreset=True)

LAOTH_BANNER = f"""{Fore.RED}
██╗      █████╗  ██████╗ ████████╗██╗  ██╗
██║     ██╔══██╗██╔═══██╗╚══██╔══╝██║  ██║
██║     ███████║██║   ██║   ██║   ███████║
██║     ██╔══██║██║   ██║   ██║   ██╔══██║
███████╗██║  ██║╚██████╔╝   ██║   ██║  ██║
╚══════╝╚═╝  ╚═╝ ╚═════╝    ╚═╝   ╚═╝  ╚═╝{Fore.CYAN}
                    ⚔️  GANG EDITION ⚔️ 
         ╔═══════════════════════════╗
         ║    Pastebin Leak Scanner  ║
         ║      By LAOTH - v1.0      ║
         ╚═══════════════════════════╝{Style.RESET_ALL}
"""

class PastebinScanner:
    def __init__(self):
        self.base_url = "https://pastebin.com"
        self.headers = {
            'User-Agent': random.choice([
                'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
                'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Edge/91.0.864.59 Safari/537.36',
                'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.1 Safari/605.1.15'
            ])
        }
        self.results = []
        self.patterns = [
            r'[\w\.-]+@[\w\.-]+\s*[:|\|]\s*\S+',  # email:password veya email|password
            r'[\w\.-]+\s*[:|\|]\s*\S+',           # username:password veya username|password
            r'[\w\.-]+\s*=\s*\S+',                # username=password
            r'[\w\.-]+/\s*\S+',                   # username/password
            r'[\w\.-]+\s+\S+@\S+\.\w+',          # username email@domain.com
            r'(?:password|pass|pwd)[\s:]+\S+',    # password: xxxx
            r'(?:username|user|login)[\s:]+\S+',  # username: xxxx
            r'\b[\w\.-]+@[\w\.-]+\.\w+\b'        # sadece email
        ]
        self.common_keywords = [
            'combo', 'combo list', 'combolist', 'leak', 'leaked', 'database', 'breach',
            'account', 'accounts', 'cracked', 'hacked', 'dump', 'email', 'login', 'password'
        ]

    def is_valid_credential(self, text, service):
        # Bazı genel kontroller
        if len(text) < 5:  # Çok kısa stringler geçersiz
            return False
        if text.count(' ') > 3:  # Çok fazla boşluk varsa muhtemelen geçersiz
            return False
        if not any(c.isalnum() for c in text):  # En az bir alfanumerik karakter olmalı
            return False
            
        # Servis adına özel kontroller
        service = service.lower()
        if service == "spotify":
            return bool(re.search(r'@|\w+[:|\|]\w+', text))
        elif service == "steam":
            return bool(re.search(r'@|\w+[:|\|]\w+', text))
        elif service == "netflix":
            return bool(re.search(r'@|\w+[:|\|]\w+', text))
        elif service == "riot":
            return bool(re.search(r'@|\w+[:|\|]\w+', text))
        
        return True

    def search_paste(self, paste_url, service):
        try:
            response = requests.get(paste_url, headers=self.headers, verify=False)
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')
                raw_text = soup.find('textarea').text if soup.find('textarea') else ""
                
                # Paste içeriğinde servis adı veya yaygın anahtar kelimeler var mı kontrol et
                content_lower = raw_text.lower()
                if not any(keyword in content_lower for keyword in [service.lower()] + self.common_keywords):
                    return []
                
                found_credentials = []
                lines = raw_text.split('\n')
                
                for line in lines:
                    line = line.strip()
                    if not line:
                        continue
                        
                    # Her satır için tüm desenleri kontrol et
                    for pattern in self.patterns:
                        matches = re.finditer(pattern, line, re.IGNORECASE)
                        for match in matches:
                            credential = match.group(0).strip()
                            if self.is_valid_credential(credential, service):
                                found_credentials.append(credential)
                
                # Tekrar eden sonuçları temizle
                found_credentials = list(dict.fromkeys(found_credentials))
                return found_credentials
            return []
        except Exception as e:
            print(f"{Fore.RED}[HATA] Paste erişiminde hata: {str(e)}{Style.RESET_ALL}")
            return []

    def search_service(self, service, max_pages=5):
        try:
            total_pastes = 0
            search_terms = [
                service,
                f"{service} account",
                f"{service} combo",
                f"{service} leak",
                f"{service} database",
                f"{service} login"
            ]
            
            for search_term in search_terms:
                print(f"\n{Fore.CYAN}[ARAMA] '{search_term}' için arama yapılıyor...{Style.RESET_ALL}")
                
                for page in range(1, max_pages + 1):
                    print(f"{Fore.CYAN}[BİLGİ] Sayfa {page} taranıyor...{Style.RESET_ALL}")
                    
                    # Pastebin arama URL'si
                    search_url = f"{self.base_url}/search?q={search_term}"
                    if page > 1:
                        search_url += f"&page={page}"
                    
                    response = requests.get(search_url, headers=self.headers, verify=False)
                    if response.status_code == 200:
                        soup = BeautifulSoup(response.text, 'html.parser')
                        paste_links = soup.find_all('a', href=re.compile(r'/[a-zA-Z0-9]{8}'))
                        
                        if not paste_links:
                            print(f"{Fore.YELLOW}[BİLGİ] Sayfa {page}'de paste bulunamadı.{Style.RESET_ALL}")
                            break
                        
                        for link in paste_links:
                            paste_url = f"{self.base_url}{link['href']}"
                            title = link.text.strip()
                            
                            print(f"{Fore.CYAN}[TARAMA] Paste kontrol ediliyor: {paste_url}{Style.RESET_ALL}")
                            if title:
                                print(f"{Fore.CYAN}[BAŞLIK] {title}{Style.RESET_ALL}")
                            
                            credentials = self.search_paste(paste_url, service)
                            if credentials:
                                self.results.append({
                                    'url': paste_url,
                                    'title': title,
                                    'service': service,
                                    'credentials': credentials,
                                    'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                                })
                                print(f"{Fore.GREEN}[BULUNDU] {len(credentials)} adet kimlik bilgisi bulundu: {paste_url}{Style.RESET_ALL}")
                                for cred in credentials:
                                    print(f"{Fore.YELLOW}[KİMLİK] {cred}{Style.RESET_ALL}")
                            
                            total_pastes += 1
                            time.sleep(random.uniform(1.0, 2.0))  # Rastgele bekleme süresi
                    
                    time.sleep(random.uniform(2.0, 3.0))  # Sayfalar arası rastgele bekleme
                
            print(f"\n{Fore.GREEN}[BİLGİ] Toplam {total_pastes} paste kontrol edildi.{Style.RESET_ALL}")
            print(f"{Fore.GREEN}[BİLGİ] Toplam {sum(len(r['credentials']) for r in self.results)} adet kimlik bilgisi bulundu.{Style.RESET_ALL}")
                    
        except Exception as e:
            print(f"{Fore.RED}[HATA] Tarama sırasında hata: {str(e)}{Style.RESET_ALL}")

    def save_results(self, filename="sonuclar.txt"):
        if self.results:
            with open(filename, 'w', encoding='utf-8') as f:
                f.write("=== Pastebin Tarama Sonuçları ===\n\n")
                total_credentials = 0
                for result in self.results:
                    f.write(f"URL: {result['url']}\n")
                    f.write(f"Başlık: {result['title']}\n")
                    f.write(f"Servis: {result['service']}\n")
                    f.write(f"Tarih: {result['timestamp']}\n")
                    f.write("Bulunan Kimlik Bilgileri:\n")
                    for cred in result['credentials']:
                        f.write(f"- {cred}\n")
                        total_credentials += 1
                    f.write("-" * 50 + "\n")
                f.write(f"\nToplam bulunan kimlik bilgisi sayısı: {total_credentials}\n")
            print(f"{Fore.GREEN}[BİLGİ] Sonuçlar {filename} dosyasına kaydedildi.{Style.RESET_ALL}")
        else:
            print(f"{Fore.YELLOW}[BİLGİ] Hiç sonuç bulunamadı.{Style.RESET_ALL}")

def main():
    print(f"{Fore.CYAN}{LAOTH_BANNER}{Style.RESET_ALL}")

    parser = argparse.ArgumentParser(description='Pastebin Leak Scanner')
    parser.add_argument('-find', type=str, required=True,
                        help='Aranacak servis adı (örn: spotify, riot)')
    parser.add_argument('-p', '--pages', type=int, default=5,
                        help='Taranacak maksimum sayfa sayısı (varsayılan: 5)')
    parser.add_argument('-o', '--output', default='sonuclar.txt',
                        help='Sonuçların kaydedileceği dosya (varsayılan: sonuclar.txt)')

    args = parser.parse_args()

    print(f"{Fore.YELLOW}[BAŞLANGIÇ] Pastebin taraması başlatılıyor...{Style.RESET_ALL}")
    print(f"{Fore.YELLOW}[BİLGİ] Aranan servis: {args.find}{Style.RESET_ALL}")
    print(f"{Fore.YELLOW}[BİLGİ] Taranacak sayfa sayısı: {args.pages}{Style.RESET_ALL}")

    scanner = PastebinScanner()
    scanner.search_service(args.find, args.pages)
    scanner.save_results(args.output)

if __name__ == "__main__":
    main() 