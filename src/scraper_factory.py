from likemanga_scraper import LikeMangaScraper

def get_scraper(site):
    scrapers = {
        "likemanga": LikeMangaScraper()
    }

    return scrapers.get(site.lower())