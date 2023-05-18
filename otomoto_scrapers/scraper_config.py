class Links:
    MAIN_DOMAIN = "https://otomoto.pl"
    # Link from which links scrapping action will start, 
    # Should be first page of offers listing i.e. page 1/125
    MAIN_LINK  = "https://www.otomoto.pl/osobowe/slaskie?page=1&search%5Badvanced_search_expanded%5D=true"
    # "https://www.otomoto.pl/osobowe?page=1"
    # Similar to |MAIN_LINK|, but has empty format place in string - {}, for link page number
    # Which will be parsed in next iteration of link gathering script
    PARSED_MAIN_LINK = "https://www.otomoto.pl/osobowe/slaskie?page={}&search%5Badvanced_search_expanded%5D=true"
    # "https://www.otomoto.pl/osobowe?page={}"

class ScrapeConfig:
    # Specifies if new links gathering script initalisation should delete
    # old links that are in database, which has the benefit, that main offer 
    # mining script won't iterate over old/dead links which are no longer available
    delete_old_links = False
    # If False, links that have been scraped in the past, won't be scraped
    # once more, reducting amount of offers which have to be parsed
    # at the cost of loosing data, that shows changes in offer price
    # over time
    mine_links_scraped_in_past = False

class DBOfferLinks:
    # Name of the table, where scraped offer links are to be stored
    table_name = "vehicle_links"

    # Mandatory column in which links are to be stored
    table_link_col = "link_string"
    # Not utilized in actual code, |table_structure| can be used,
    # in order to keep information about other columns in link table,
    # for information purposes
    table_structure = [""]


class DBOfferDetails:
    # Name of the offer details table
    table_name = "vehicle_data"

    # Mandatory columns, used by the script

    # Tells, if offer scrape was "FULL" i.e. 
    # All offers, even the ones scraped earlier, were scraped again
    # or if it was "PARTIAL", where only new links, were scraped
    table_runtype_col = "run_type"
    # Auto column, with date when scraping has occured
    table_scrapdate_col = "scrap_date"
    # Made in order to distinguish from which script iteration
    # data was received. If script will be relaunched
    # this column will have value will be +1, in comparison to
    # the last scrape
    table_scrapiter_col = "scrap_iter"
    # Column in which offer link is stored
    table_link_col = "link_string"
    # Not utilized in actual code, |table_structure| can be used,
    # in order to keep information about other columns in link table,
    # for information purposes
    table_structure = [""]


class DriverConf:
    """Configuration for selenium driver
    Currently working only on firefox"""

    # Configuration of driver behavior,
    HEADLESS = True

    # Time, just after loading page, which assures that the whole site has loaded properly 
    WAIT_UNTIL_PAGE_LOADED = 0.6

    # How many times, and how many seconds should script try to refresh site, if it
    # doesn't respond properly.
    # It is implemented in support function |driver_connection_retry|
    THROTTLE_REPEATS = [10,30,45]

    THROTTLE_REPEATS_FOR_LINKS_SCRAPPER = [5,10,10]

    # TODO add additional config variables if necessary 
