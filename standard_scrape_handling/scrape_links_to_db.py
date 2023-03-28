from config import Links

# TODO get rid of those, when changing fucntion
from otodom_scrappers import get_num_pages

# TODO - schema where  key:val is passed with name of scrapper and
#  table name, where it should be put in
# def scrape_links(get_num_pages, {'table_name':get_link_to_db}, threads):

# Get number of links
def scrape_links(get_num_pages):
    # Get number pages with parcel offers
    num_pages_to_parse = get_num_pages()
    print(num_pages_to_parse)

# generate dummy links of every page to parse
    page_links_generator = (Links.PARSED_MAIN_LINK.format(i)
                        for i in range(num_pages_to_parse, 0, -1))


    # TODO add threading support
    for page_link in page_links_generator:
        pass


# TODO go page after page and get links, which will be passed to database