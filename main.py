from logger import logger

from otodom_scrapers import run_scraping as otodom_scraping



def main():


    # Run function for otodom site    
    otodom_scraping(run_scrape_links=True)


if __name__ == '__main__':
    main()




