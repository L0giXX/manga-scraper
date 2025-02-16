from base_scraper import BaseMangaScraper
from bs4 import BeautifulSoup as bs
from colorama import Fore

class LikeMangaScraper(BaseMangaScraper):
    def __init__(self):
        super().__init__("https://likemanga.in")
    
    def get_image_links(self, soup):
        reading_container = soup.find("div", class_="reading-content")
        if not reading_container:
            return []
        return [img.get("src") for img in reading_container.find_all("img")]
    
    def show_chapters(self, manga):
        url = self.base_url + "/manga/" + manga + "/ajax/chapters"
        print(Fore.CYAN + f"[*] Searching for {url}")
        req = self.scraper.post(url)
        if req.status_code != 200:
            print(Fore.RED + "[X] Failed to fetch the manga. Check the manga name.")
            return
        
        soup = bs(req.text, "html.parser")
        manga_container = soup.find("ul", class_="main version-chap no-volumn")
        if not manga_container:
            print(Fore.RED + "[X] Failed to find chapter container.")
            return
        
        chapter_containers = manga_container.find_all("li", class_="wp-manga-chapter")

        if not chapter_containers:
            print(Fore.RED + "[X] No chapters found.")
            return
        
        print(Fore.GREEN + "[✔] Chapters Found:")
        print(Fore.CYAN + "------------------------------------")
        for chapter_container in chapter_containers:
            chapter = chapter_container.find("a")
            print(Fore.GREEN + chapter.string.strip())