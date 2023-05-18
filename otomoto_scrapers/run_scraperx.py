from getpass import getpass

from standard_scrape_handling import scrape_links, scrape_parcel_data
from logger import logger

from SQL_DATABASE import Database
from SQL_DATABASE.standard_db_config import DBConf

# TODO import proper functions from local folder (delete TEMPLATE_SCRAPER)
from otomoto_scrapers.additional_scrappers import get_num_pages
from otomoto_scrapers.links_scaper import get_offer_links_from_page
from otomoto_scrapers.offer_scraper import get_offer_details
import otomoto_scrapers.scraper_config as template_config
from otomoto_scrapers.scraper_config import ScrapeConfig


def run_scraping(edit_db_creds = True,
                 run_scrape_links= True,
                run_scrape_parcel_data=True):
    
    logger.info(f"Scraping in scraper init: {__name__}")

    if edit_db_creds:
        db_cred = DBConf
        db_cred.set("username",
                    input("Database username: "))
        db_cred.set("password",
                    getpass("Database password: "))
        db_cred.set("database_name",
                    input("Database name: "))
    else:
        raise DBConf.CredentialsError
    
    # Connecting to db, based on specified credentials
    db_con = Database(
                DBConf.config("SQL_HOSTNAME"),
                DBConf.config("username"),
                DBConf.config("password"),
                DBConf.config("database_name"))

    if run_scrape_links:
        # TODO configure standard scrape fucntions, by specifying
        # proper function names, and proper argument configuration
        # Given that refratoring will work properly, and function names
        # will stay the same as in TEMPLATE, no changes are necessary
        # in order for the code to work.
        scrape_links(
            delete_old_links = ScrapeConfig.delete_old_links,
            append_domain_to_link = False,
            db_con = db_con,
            scraper_config = template_config,

            num_pages_function = get_num_pages,
            links_scrapper_function = get_offer_links_from_page,)
        
    if run_scrape_parcel_data:
        scrape_parcel_data(
            mine_links_scraped_in_past = ScrapeConfig.mine_links_scraped_in_past,
            scraper_config = template_config,
            db_con = db_con,    

            get_offer_function = get_offer_details)
        