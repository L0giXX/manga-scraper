import cloudscraper
import os
import time
from bs4 import BeautifulSoup as bs
from colorama import Fore, Style, init 

init(autoreset=True)

def create_folder(folder_name):
    try:
        os.makedirs(folder_name)
        print(Fore.GREEN + f"[✔] Created folder: {folder_name}")
    except:
        print(Fore.YELLOW + f"[!] Folder {folder_name} already exists")


def download_images(url, folder_name, chapter, scraper):
    print(Fore.CYAN + f"[*] Searching for {url}")
    req = scraper.get(url)
    if req.status_code != 200:
        print(Fore.RED + "[X] Failed to fetch the chapter. Check the manga name and chapter number.")
        return

    # ensure connection is established before downloading images
    time.sleep(2)
    soup = bs(req.text, features="html.parser")
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


def show_chapters(url, scraper):
    print(Fore.CYAN + f"[*] Searching for {url}")
    req = scraper.post(url)
    if req.status_code != 200:
        print(Fore.RED + "[X] Failed to fetch the manga. Check the manga name.")
        return
    
    soup = bs(req.text, features="html.parser")
    manga_container = soup.find("ul", class_="main version-chap no-volumn")
    
    if not manga_container:
        print(Fore.RED + "[X] Failed to find chapter container.")
        return
    
    chapter_containers = manga_container.find_all("li", class_="wp-manga-chapter")

    if len(chapter_containers) == 0:
        print(Fore.RED + "[X] No chapters found.")
        return
    
    print(Fore.GREEN + "[✔] Chapters Found:")
    print(Fore.CYAN + "------------------------------------")
    for chapter_container in chapter_containers:
        chapter = chapter_container.find("a")
        print(Fore.GREEN + chapter.string.strip())

def main():
    print(Fore.CYAN + Style.BRIGHT + """
    ┌──────────────────────────────────────┐
    │        Manga Image Downloader        │
    └──────────────────────────────────────┘
    """)

    scraper = cloudscraper.create_scraper(delay=10)
    BASE_URL = "https://likemanga.in/manga/"

    manga = input(Fore.YELLOW + "[?] Enter the manga name: ").strip().lower().replace(" ", "-")
    if not manga:
        print(Fore.RED + "[X] Manga name cannot be empty!")
        return
    
    chapter = input(Fore.YELLOW + "[?] Enter the chapter number: ").strip()
    if not chapter.isdigit():
        print(Fore.RED + "[X] Invalid chapter number!")
        return
    
    full_url = BASE_URL + manga + "/chapter-" + chapter
    chapter_url = BASE_URL + manga + "/ajax/chapters"
    create_folder(manga)
    show_chapters(chapter_url, scraper)
    download_images(full_url, manga, chapter, scraper)

    print(Fore.GREEN + "\n[✔] Download complete!")

main()