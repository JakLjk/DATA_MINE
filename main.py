from logger import logger

# from otodom_scrapers import run_scraping as otodom_scraping
from otomoto_scrapers import run_scraping as otomoto_scraping


def main():


    # otodom_scraping(run_scrape_links=True)

    otomoto_scraping(run_scrape_links=True)


if __name__ == '__main__':
    main()




