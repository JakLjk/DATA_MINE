class Links:
    MAIN_DOMAIN = "https://www.otodom.pl"
    MAIN_LINK  = "https://www.otodom.pl/pl/oferty/sprzedaz/mieszkanie/cala-polska?viewType=listing"
    PARSED_MAIN_LINK = "https://www.otodom.pl/pl/oferty/sprzedaz/mieszkanie/cala-polska?viewType=listing&page={}"

class ScrapeConfig:
    delete_old_links = True
    mine_links_scraped_in_past = False


class DBDetails:
    db_name = "houses_data"
class DBOfferLinks:
    table_name = "parcel_links"

    table_link_col = "link_string"
    table_structure = [""]


class DBOfferDetails:
    table_name = "parcel_data"

    table_runtype_col = "run_type"
    table_scrapdate_col = "scrap_date"
    table_scrapiter_col = "scrap_iter"
    table_link_col = "link_string"
    
    table_structure = [""]


class DriverConf:
    """Configuration for selenium driver
    Currently working only on firefox"""

    # TODO add support for multiple browsers
    HEADLESS = True
    WAIT_UNTIL_PAGE_LOADED = 0.6
    THROTTLE_REPEATS = [10,30,45]
    SITE_LOAD_SCROLL_PAUSETIME = 0.05
    SITE_LOAD_AFTER_SCROLL_PAUSETIME = 1.0


    