from logger import logger
from custom_errors import ScrapeFailure
from support_functions.std_function_retry import function_retry
from time import sleep
# Get number of links
# TODO implement delete_old_links_from_db = False 
def scrape_links(
        delete_old_links = False,
        append_domain_to_link = False,
        db_con = None,
        scraper_config = None,
        num_pages_function = None,
        links_scrapper_function = None,
        max_failed_link_pages_in_row = 3 ):
    
    Links = scraper_config.Links
    DriverConfig = scraper_config.DriverConf
    DBOfferLinks = scraper_config.DBOfferLinks

    if delete_old_links:
        db_con.clear_table(DBOfferLinks.table_name)
        db_con.reset_table_id(DBOfferLinks.table_name)
        logger.info(f"Links table {DBOfferLinks.table_name} was cleared")

    # Get number pages with parcel offers
    num_pages_to_parse = num_pages_function()
    domain_name = Links.MAIN_DOMAIN

    # generate dummy links of every page to parse
    page_links_generator = (Links.PARSED_MAIN_LINK.format(i)
                        for i in range(num_pages_to_parse, 0, -1))
    
    # TODO add threading support


    repeats = DriverConfig.THROTTLE_REPEATS_FOR_LINKS_SCRAPPER
    for i, page_link in enumerate(page_links_generator):
        logger.info(f"Getting links from page {i+1}/{num_pages_to_parse}")
        repeat = True
        link_page_failure = 0
        while repeat:
            try: 
                offer_links = links_scrapper_function(page_link)
                repeat = False
            except:
                logger.warning(f"Failed while getting links from page.")
                link_page_failure += 1
                if link_page_failure >= len(repeats):
                    repeat = False
                    raise ScrapeFailure("""Too many failures, while scraping first pages. 
                    Most probably index has moved and such pages do not exist anymore""")

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
