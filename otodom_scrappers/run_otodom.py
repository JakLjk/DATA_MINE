from standard_scrape_handling import scrape_links, scrape_parcel_data
from SQL_DATABASE import Database
from config import DBConf
from logger import logger

from otodom_scrappers.additional_scrappers import get_num_pages
from otodom_scrappers.links_scapper import get_offer_links_from_page
from otodom_scrappers.offer_scrapper import get_offer_details
import otodom_scrappers.otodom_config as otodom_config

# Scraping links and inserting them to db


def run_scraping():
    logger.info(f"Scraping link in scraper init: {__name__}")
    db_con = Database(
                DBConf.config("MYSQL_HOSTNAME"),
                DBConf.config("username"),
                DBConf.config("password"),
                DBConf.config("MYSQL_DBNAME"))
    # run_links(db_con)
    run_offers(db_con)


def run_links(db_con):
    scrape_links(
        delete_old_links = False,
        append_domain_to_link = True,
        db_con = db_con,
        scraper_config = otodom_config,

        num_pages_function = get_num_pages,
        links_scrapper_function = get_offer_links_from_page,
    )


def run_offers(db_con):
    scrape_parcel_data(
        db_con = db_con,
        mine_links_scraped_in_past = None,
        scraper_config = otodom_config,

        get_offer_function = get_offer_details
    )