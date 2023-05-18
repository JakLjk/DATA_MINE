from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By

from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
from time import sleep

import bs4
import re

from .scraper_config import DriverConf
from support_functions.selenium_support import driver_connection_retry
from logger import logger
from custom_errors import ScrapeFailure

def get_offer_details(link: str) -> dict:
        # Running Selenium Driver, with configuration
        # from scrapper_config file
        options = Options()
        options.headless = DriverConf.HEADLESS
        driver = webdriver.Firefox(options=options)

        # In case of failed connection, driver will try to reload the site, 
        # based on time intervals specified in config.py
        driver_connection_retry(driver, link, DriverConf.THROTTLE_REPEATS)
        sleep(DriverConf.WAIT_UNTIL_PAGE_LOADED)

        # TODO assure that site is porperly loaded into |page_html|
        # It is often required to use functions like:
        # "driver.execute_script("window.scrollTo(0,3600)")"
        # in order to load the whole site properly
        try:    
                cookie_button = driver.find_element(By.ID,"onetrust-accept-btn-handler")
                cookie_button.click()
        except:
                logger.info("Cookie popup wasn't closed (It is possible that it has not shown)")
                logger.info(f"Link: {link}") 

        driver.execute_script("window.scrollTo(0,2800)")
        sleep(2)
        equipment_expand_xpath = "/html/body/div[4]/main/div[1]/div[1]/div[2]/div[1]/div[1]/div[5]/a/i"
        wait = WebDriverWait(driver, 2)
        try:
                wait.until(EC.visibility_of_element_located((By.XPATH, equipment_expand_xpath ))).click()
        except TimeoutException:
                logger.error(f"Unable to expand vehicle equipment (most probably it is non-expandable) LINK: {link} ")
        page_html = driver.page_source
        driver.quit()

        soup = bs4.BeautifulSoup(page_html, 'html.parser')

        # TODO Add scraping logic, which will return dictionary
        # whith keys being column names in corresponing sql database
        # and values, which will be put in specified columns
        full_offer_info = {}

        sleep(1)
        full_offer_info['link_oferty'] = link
        try:
                full_offer_info['tytul_oferty'] = soup.find('h1', {'class':'offer-title big-text'}).get_text().strip()
        except AttributeError as ae:
                logger.error(f"Unable to open offer - it might have been removed. LINK: {link}")
                return None
        full_offer_info['cena'] = soup.find('span', {'class':'offer-price__number'}).get_text().strip()

        # TODO make flexible Szczegóły
        details_2 = soup.find('div', {'id':'parameters'})
        details_2 = details_2.find_all('li', {'class':"offer-params__item"})
        for detail_container in details_2:
                detail_name = detail_container.find('span', {'class':'offer-params__label'}).get_text().strip()
                detail_value = detail_container.find('div',{'class':'offer-params__value'}).get_text().strip()
                full_offer_info[detail_name] = detail_value 

        # Koordynaty 
        coords_1 = soup.find('div', {'class', 'gm-style'})
        coords_1 = coords_1.find_all('a', attrs={'href': re.compile("^https://")})
        coords_1 = [link.get('href') for link in coords_1][0]
        full_offer_info['coordinates'] = coords_1.split('ll=')[1].split('&')[0]
        # TODO is "are coord exact necessary?"

        # Wyposazenie
        try:    
                details_3 = soup.find('div', {'id':'rmjs-1'})
                details_3 = details_3.find_all('li', {'class':"parameter-feature-item"})
                full_offer_info["Wyposazenie"] = "|".join([item.get_text().strip() for item in details_3])
        except AttributeError as ae:
                logger.error(f"Unable to find equipment element - most probably it does not exist. LINK: {link}") 

        # TODO Opis 
        return full_offer_info