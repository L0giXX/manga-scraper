import cloudscraper
import os
import time
from bs4 import BeautifulSoup as bs
from colorama import Fore


class BaseMangaScraper:
    def __init__(self, base_url):
        self.base_url = base_url
        self.scraper = cloudscraper.create_scraper(delay=10)

    def create_folder(self, manga):
        try:
            os.makedirs(manga)
            print(Fore.GREEN + f"[✔] Created folder: {manga}")
        except:
            print(Fore.YELLOW + f"[!] Folder {manga} already exists")

    def download_images(self, url, manga, chapter):
        print(Fore.CYAN + f"[*] Searching for {url}")
        req = self.scraper.get(url)
        if req.status_code != 200:
            print(Fore.RED + "[X] Failed to fetch the chapter. Check the manga name and chapter number.")
            return
        
        time.sleep(2)
        soup = bs(req.text, "html.parser")
        images = self.get_image_links(soup)

        if not images:
            print(Fore.RED + "[X] No images found. The chapter may not exist.")
            return
        
        print(Fore.CYAN + f"[*] Total {len(images)} images found!")
        for i, image in enumerate(images):
            r = self.scraper.get(image).content
            try:
                r = str(r, "utf-8")
            except UnicodeDecodeError:
                with open(f"{manga}/{chapter}-{i}.jpg", "wb") as f:
                    f.write(r)
            except Exception as e:
                print(Fore.RED + f"\n[X] Failed to download {image}: {e}")  
    
    def get_image_links(self, soup):
        raise NotImplementedError("get_image_lionks() must be implemented by the child class")
    
    def show_chapters(self, manga):
        raise NotImplementedError("show_chapters() must be implemented by the child class")