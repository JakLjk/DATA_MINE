from logger import logger

from otodom_scrapers import run_scraping



def main():


    # Run function for otodom site    
    run_scraping(run_scrape_links=False)


if __name__ == '__main__':
    main()




