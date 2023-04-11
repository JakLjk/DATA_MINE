from getpass import getpass

from standard_scrape_handling import scrape_links, scrape_parcel_data
from SQL_DATABASE import Database
from SQL_DATABASE.standard_db_config import DBConf
from logger import logger

from otodom_scrapers.additional_scrappers import get_num_pages
from otodom_scrapers.links_scaper import get_offer_links_from_page
from otodom_scrapers.offer_scraper import get_offer_details
import otodom_scrapers.otodom_config as otodom_config
from otodom_scrapers.otodom_config import ScrapeConfig

# Scraping links and inserting them to db
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
        raise DBConf.CredentialsError("Credentials have to be specified manually")

    db_con = Database(
                db_cred.config("SQL_HOSTNAME"),
                db_cred.config("username"),
                db_cred.config("password"),
                db_cred.config("database_name"))

    if run_scrape_links:
        scrape_links(
            delete_old_links = ScrapeConfig.delete_old_links,
            append_domain_to_link = True,
            db_con = db_con,
            scraper_config = otodom_config,

            num_pages_function = get_num_pages,
            links_scrapper_function = get_offer_links_from_page,)
        
    if run_scrape_parcel_data:
        scrape_parcel_data(
            mine_links_scraped_in_past = ScrapeConfig.mine_links_scraped_in_past,
            scraper_config = otodom_config,
            db_con = db_con,    

            get_offer_function = get_offer_details)
        