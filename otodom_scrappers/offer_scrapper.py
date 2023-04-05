from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from time import sleep

import bs4
import re

from config import DriverConf
from support_functions.selenium_support import driver_connection_retry
from logger import logger

def get_offer_details(link: str) -> dict:
        options = Options()
        options.headless = DriverConf.HEADLESS
        driver = webdriver.Firefox(options=options)
        driver_connection_retry(driver, link, DriverConf.THROTTLE_REPEATS)
        sleep(DriverConf.WAIT_UNTIL_PAGE_LOADED)
        
        # Scrolling necessary to load information about coordinates.
        # height = driver.execute_script("return document.body.scrollHeight") - alternative to 
        # setting fixed height, but struggles or some sites
        height = 2600
        scroll_amount_px = 150
        curren_scroll_px = 0
        while curren_scroll_px <= height:
                curren_scroll_px += scroll_amount_px
                driver.execute_script(f"window.scrollTo(0, {str(curren_scroll_px)})")
                sleep(DriverConf.SITE_LOAD_SCROLL_PAUSETIME)
        sleep(DriverConf.SITE_LOAD_AFTER_SCROLL_PAUSETIME)

        page_html = driver.page_source
        driver.quit()

        soup = bs4.BeautifulSoup(page_html, 'html.parser')
        full_offer_info = {}

        try:
                full_offer_info['link_string'] = link
                full_offer_info['offer_title'] = soup.find('h1', {'data-cy':'adPageAdTitle'}).get_text().strip()
                full_offer_info['offer_price'] = soup.find('strong', {'data-cy':'adPageHeaderPrice'}).get_text().strip()
                full_offer_info['offer_address'] = soup.find('a',{'aria-label':'Adres'}).get_text().strip()
        except AttributeError as ae:
                logger.error("Could not fetch data about parcel - Site was deleted or has not been poperly loaded.")
                logger.error(f"Error page link: {link}")
                logger.error(f"Exception: {ae}")
                raise ae
        
        try:
                coordinates_raw_1 = soup.find('div', {'class', 'gm-style'})
                coordinates_raw_2 = coordinates_raw_1.find_all('a', attrs={'href': re.compile("^https://")})
                coordinates_link = [link.get('href') for link in coordinates_raw_2][0]
                full_offer_info['coordinates'] = coordinates_link.split('ll=')[1].split('&')[0]
                full_offer_info['are_coords_exact'] = True if soup.find('div', {'class':'css-3te2t7 ej9jroc0'}) == None else False
        except AttributeError as ae:
                logger.error(f"There was a problem with finding |COORIDATES| - Try increasing |SITE_LOAD_SCROLL_PAUSETIME| ")
                logger.error(f"Exception: {ae}")
                full_offer_info['coordinates'] = None
                full_offer_info['are_coords_exact'] = None

        try:
                details_container = soup.find('div',{'class':'css-xr7ajr e10umaf20'})
                details_name_value = details_container.find_all('div',{'class':{'css-kkaknb enb64yk0'}})
        except AttributeError as ae:
                logger.error(f"Could not fetch main details container")
                logger.error(f"Most propably site was not loaded properly, or site structure changed ")
                logger.error(f"Error page link: {link}")
                logger.error(f"Exception: {ae}")
                raise ae
        for dnv in details_name_value:
                print("-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-")
                print(dnv)
                print("-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-")
                detail_name = dnv.find('div',{'class':'css-rqy0wg enb64yk2'}).get_text().strip()
                try:
                    detail_value = dnv.find('div',{'class':'css-1wi2w6s enb64yk4'}).get_text().strip()
                except AttributeError:
                    detail_value = dnv.find('button',{'class':'css-x0kl3j e1k3ukdh0'}).get_text().strip()
        
                full_offer_info[detail_name]=detail_value
                
                print(full_offer_info)

                # name_value_containers = dnv.find_all('div',{'class':'css-1qzszy5 estckra8'})
                # name_value_list = [nvc.get_text().strip() for nvc in name_value_containers]
                # if len(name_value_list) != 2: raise Exception(f"Problem with name_value length in |Details|: expected len(2), got {len(name_value_list)}")
                # full_offer_info[name_value_list[0]]=name_value_list[1]
                

        try:
                additional_info_container = soup.find('div',{'class':'css-1l1r91c emxfhao1'})
                additional_info_value = additional_info_container.find_all('div',{'class':'css-f45csg estckra9'})
                for aiv in additional_info_value:
                        name_value_containers = aiv.find_all('div',{'class':'css-1qzszy5 estckra8'})
                        name_value_list = [nvc.get_text().strip() for nvc in name_value_containers]
                        if name_value_list == []:
                                name_value_containers = aiv.find_all('div',{'class':'css-1sqc82x estckra8'})
                                name_value_list = [nvc.get_text().strip() for nvc in name_value_containers]
                        if len(name_value_list) != 2: raise Exception(f"Problem with name_value length in |Additional Info|: expected len(2), got {len(name_value_list)}")
                        full_offer_info[name_value_list[0]]=name_value_list[1]
        except AttributeError as ae:
                logger.error(f"There was problem with fetching additional information from link {link}")
                logger.error(f"Most probably such information is not available")
                logger.error(f"Exception {ae}")
                raise ae

        return(full_offer_info)