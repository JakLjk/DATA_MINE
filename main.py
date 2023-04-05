
from standard_scrape_handling import scrape_links, scrape_parcel_data

from logger import logger



def main():
    # Start logging configuration

    logger.info("Logger -test-")

    # actions that are needed:

    # scrape_links()
    scrape_parcel_data()


    # configure:

    pass
    


if __name__ == '__main__':
    main()



# TODO Standardize scrape_links_to_dbmso it works iith multiple scrappers
# from standard_scrape_handling.scrape_links_to_db import scrape_links
# from otodom_scrappers import get_num_pages

# def main():
#     # actions that are needed:
#     # 

#     scrape_links(get_num_pages)


#     # configure:

#     pass
    