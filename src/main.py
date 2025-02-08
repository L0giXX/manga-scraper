import cloudscraper
import os
import time
from bs4 import BeautifulSoup
from colorama import Fore, Style, init 

init(autoreset=True)

def create_folder(folder_name):
    try:
        os.makedirs(folder_name)
        print(Fore.GREEN + f"[✔] Created folder: {folder_name}")
    except:
        print(Fore.YELLOW + f"[!] Folder {folder_name} already exists")


def download_images(req, folder_name, chapter, scraper):
    soup = BeautifulSoup(req.text, features="html.parser")
    reading_container = soup.find("div", class_="reading-content")
    images = reading_container.find_all("img")

    if len(images) == 0:
        print(Fore.RED + "[X] No images found. The chapter may not exist.")
        return
    
    print(Fore.CYAN + f"[*] Total {len(images)} images found!")
    for i, image in enumerate(images):
        link = image.get("src")
        r = scraper.get(link).content
        try:
            r = str(r, "utf-8")
        except UnicodeDecodeError:
            with open(f"{folder_name}/{chapter}-{i}.jpg", "wb") as f:
                f.write(r)
        except Exception as e:
            print(Fore.RED + f"\n[X] Failed to download {link}: {e}")

def main():
    print(Fore.CYAN + Style.BRIGHT + """
    ┌──────────────────────────────────────┐
    │        Manga Image Downloader        │
    └──────────────────────────────────────┘
    """)

    scraper = cloudscraper.create_scraper()
    BASE_URL = "https://likemanga.in/manga/"

    manga = input(Fore.YELLOW + "[?] Enter the manga name: ").strip().lower().replace(" ", "-")
    if not manga:
        print(Fore.RED + "[X] Manga name cannot be empty!")
        return
    
    chapter = input(Fore.YELLOW + "[?] Enter the chapter number: ").strip()
    if not chapter.isdigit():
        print(Fore.RED + "[X] Invalid chapter number!")
        return
    
    url = BASE_URL + manga + "/chapter-" + chapter + "/"
    print(Fore.CYAN + f"[*] Searching for {url}")

    print(Fore.CYAN + "[*] Establishing connection to bypass Cloudflare...")

    req = scraper.get(url)
    if req.status_code != 200:
        print(Fore.RED + "[X] Failed to fetch the chapter. Check the manga name and chapter number.")
        return
    
    time.sleep(2)

    create_folder(manga)
    download_images(req, manga, chapter, scraper)

    print(Fore.GREEN + "\n[✔] Download complete!")

main()