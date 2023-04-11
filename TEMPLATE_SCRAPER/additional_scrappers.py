from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By


from .scraper_config import Links
from .scraper_config import DriverConf

def get_num_pages() -> int:
    """Function which scrapes information about amount of pages
    with offers, which have to be iteraed over, in order to get
    all offer links on specified site"""

    first_page_link = Links.MAIN_LINK
    
    # Running Selenium Driver, with configuration
    # from scrapper_config file
    options = Options()
    options.headless = DriverConf.HEADLESS
    driver = webdriver.Firefox(options=options)

    # Loading webpage
    driver.get(first_page_link)

    # TODO Add scraping logic to receive last page number in range to scrape
    last_page_num =  driver.find_element()
    driver.quit()

    return int(last_page_num)