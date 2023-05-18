from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from time import sleep

import bs4

from logger import logger

from .scraper_config import DriverConf
from custom_errors import ScrapeFailure
from support_functions.selenium_support import driver_connection_retry

from urllib.parse import urlparse

def get_offer_links_from_page(page_link:str) -> list:
        # Running Selenium Driver, with configuration
        # from scrapper_config file
        options = Options()
        options.headless = DriverConf.HEADLESS
        driver = webdriver.Firefox(options=options)

        # Retrying connection in case of failure, based on settings
        # Specified in config file
        driver_connection_retry(driver, page_link, DriverConf.THROTTLE_REPEATS)
        # Sleeping in order to prevent errors thrown by site not loading completely
        sleep(DriverConf.WAIT_UNTIL_PAGE_LOADED)

        # TODO assure that site is properly loaded into |page_html|
        # It is often required to use functions like:
        # "driver.execute_script("window.scrollTo(0,3600)")"
        # in order to load the whole site properly
        driver.execute_script("window.scrollTo(0,3600)")
        page_html = driver.page_source
        driver.quit()


        # TODO Add scraping logic using webpage info in |soup| variable
        # to receive last page number in range to scrape
        soup = bs4.BeautifulSoup(page_html, 'html.parser')
        
        main_frame = soup.find('main',{'class','ooa-1hab6wx er8sc6m9'})

        


        try:
                all_link_elements = main_frame.find_all(
                       'article', {'data-variant':'regular'})
        except AttributeError as ae:
            logger.critical("There was a problem parsing page:")
            logger.critical(page_link)
            logger.critical(f"Error: {ae}")
            raise ScrapeFailure("Unable to properly scrape this page")
        
        elements = [elem.find('a', href=True)['href'] for elem in all_link_elements]
        elems_to_return = []
        for elem in elements:
               if 'otomoto.pl' in elem:
                      elems_to_return.append(elem)
  
        return elems_to_return

