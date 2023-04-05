# TODO Change this too, all pages have to have their own links in their config,
# together with their db structure
from custom_errors import ScrapeFailure

from SQL_DATABASE import Database
from config import DBConf
# TODO get rid of those, when changing fucntion
from otodom_scrappers import get_num_pages, get_offer_links_from_page
from otodom_scrappers import get_offer_links_from_page
from otodom_scrappers.otodom_config import Links, DBOfferLinks

from logger import logger

# TODO - schema where  key:val is passed with name of scrapper and
#  table name, where it should be put in
# def scrape_links(get_num_pages, {'table_name':get_link_to_db}, threads):

# TODO Every page will have separate initialisation file, which will use functions
# found in module

db_con = Database(
            DBConf.config("MYSQL_HOSTNAME"),
            DBConf.config("username"),
            DBConf.config("password"),
            DBConf.config("MYSQL_DBNAME")
    )

append_domain_to_link = True


# Get number of links
def scrape_links():
    # Get number pages with parcel offers
    num_pages_to_parse = get_num_pages()
    domain_name = Links.MAIN_DOMAIN

# generate dummy links of every page to parse
    page_links_generator = (Links.PARSED_MAIN_LINK.format(i)
                        for i in range(num_pages_to_parse, 0, -1))

    # TODO add threading support
    for i, page_link in enumerate(page_links_generator):
        logger.info(f"Getting links from page {i+1}/{num_pages_to_parse}")
        try:
            offer_links = get_offer_links_from_page(page_link)
        except ScrapeFailure as sf: 
            # TODO add logging for error
            continue

        if append_domain_to_link:
            offer_links = [domain_name + link for link in offer_links]

        num_links = len(offer_links)
        logger.info(f"Inserting {num_links} links into Database")
        db_con.insert_multiple_into_table(table_name=DBOfferLinks.table_name,
                                          col_names=DBOfferLinks.table_link_col,
                                          data=offer_links)
        db_con.commit()

        num_links_db = db_con.count_rows(DBOfferLinks.table_name)
        logger.info(f"Inserted {num_links} links into Database")
        logger.info(f"Current number of links in Database: {num_links_db}")

# TODO go page after page and get links, which will be passed to database
