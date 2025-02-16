from colorama import Fore, Style, init 
from scraper_factory import get_scraper

init(autoreset=True)

def main():
    print(Fore.CYAN + Style.BRIGHT + """
    ┌──────────────────────────────────────┐
    │        Manga Image Downloader        │
    └──────────────────────────────────────┘
    """)

    site = input(Fore.YELLOW + "[?] Enter the manga site: ").strip().lower()
    scraper = get_scraper(site)

    if not scraper:
        print(Fore.RED + "[X] Invalid site selected!")
        return        

    manga = input(Fore.YELLOW + "[?] Enter the manga name: ").strip().lower().replace(" ", "-")
    if not manga:
        print(Fore.RED + "[X] Manga name cannot be empty!")
        return
    
    chapter = input(Fore.YELLOW + "[?] Enter the chapter number: ").strip()
    if not chapter.isdigit():
        print(Fore.RED + "[X] Invalid chapter number!")
        return
    
    scraper.create_folder(manga)
    scraper.show_chapters(manga)
    scraper.download_images(scraper.base_url + "/manga/" + manga + "/chapter-" + chapter, manga, chapter)
    
    print(Fore.GREEN + "\n[✔] Download complete!")


if __name__ == "__main__":
    main()