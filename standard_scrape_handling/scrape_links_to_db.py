# TODO Change this too, all pages have to have their own links in their config,
# together with their db structure
from custom_errors import ScrapeFailure

from SQL_DATABASE import Database
from config import DBConf
# TODO get rid of those, when changing fucntion
from otodom_scrappers import get_num_pages
from otodom_scrappers import get_offer_links_from_page
from otodom_scrappers import Links
from otodom_scrappers import links_table_name, links_table_structure

# TODO - schema where  key:val is passed with name of scrapper and
#  table name, where it should be put in
# def scrape_links(get_num_pages, {'table_name':get_link_to_db}, threads):

# TODO Every page will have separate initialisation file, which will use functions
# found in module


# Get number of links
def scrape_links():
    # Get number pages with parcel offers
    num_pages_to_parse = get_num_pages()
    print(num_pages_to_parse)

# generate dummy links of every page to parse
    page_links_generator = (Links.PARSED_MAIN_LINK.format(i)
                        for i in range(num_pages_to_parse, 0, -1))
    

    db_con = Database(
            DBConf.config("MYSQL_HOSTNAME"),
            DBConf.config("username"),
            DBConf.config("password"),
            DBConf.config("MYSQL_DBNAME")
    )

    # TODO add threading support
    for page_link in page_links_generator:
        try:
            offer_links = get_offer_links_from_page(page_link)
        except ScrapeFailure as sf:
            # TODO add logging for error
            continue
        # TODO add this functionality 
        db_con.insert_multiple_into_table(links_table_name, 
                                          headers=links_table_structure, 
                                          values=offer_links)

# TODO go page after page and get links, which will be passed to database