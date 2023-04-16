from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from time import sleep

import bs4
import re

from .otodom_config import DriverConf
from support_functions.selenium_support import driver_connection_retry
from logger import logger
from custom_errors import ScrapeFailure

def get_offer_details(link: str) -> dict:
        options = Options()
        options.headless = DriverConf.HEADLESS
        driver = webdriver.Firefox(options=options)
        # In case of failed connection, driver will try to reload the site, 
        # based on time intervals specified in config.py
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
        
        # Seller details is an popup that can show, after pressing button that reveals phone number
        seller_details = None

        # Hiding cookie popup
        try:
                cookie_button = driver.find_element(By.ID,"onetrust-accept-btn-handler")
                cookie_button.click()
        except:
                logger.info("Cookie popup wasn't closed (It is possible that it has not shown)")
                logger.info(f"Link: {link}")

        # Uncovering phone number:
        try:
                phone_button = driver.find_element(By.CSS_SELECTOR,"div.css-1pyh82i:nth-child(1) > div:nth-child(1) > div:nth-child(4) > div:nth-child(1) > button:nth-child(2)")
                phone_button.click()

                # If popup with additional info pops up:
                try:
                        # Get additional seller details for analysis
                        seller_details = driver.find_element(By.XPATH, "//div[@class='css-1kqtaqd e1bxdpug0']").get_attribute('innerHTML')  
                        seller_details = bs4.BeautifulSoup(seller_details, 'html.parser')                 
                        pup_up_close = driver.find_element(By.CSS_SELECTOR, ".css-1ex6smy")
                        pup_up_close.click()
                except Exception as e:
                        logger.info("Additional seller_details popup wasn't closed (It is possible that it has not shown)")
                        logger.info(f"Link: {link}")
                        
        except Exception as e:
                logger.info("Phone button wasn't clicked (It may not be available)")
                logger.info(f"Link: {link}")

        page_html = driver.page_source
        driver.quit()

        soup = bs4.BeautifulSoup(page_html, 'html.parser')
        full_offer_info = {}


        # Scrape main offer info
        try:
                
                full_offer_info['link_string'] = link
                full_offer_info['offer_title'] = soup.find('h1', {'data-cy':'adPageAdTitle'}).get_text().strip()
                full_offer_info['offer_price'] = soup.find('strong', {'data-cy':'adPageHeaderPrice'}).get_text().strip()
                full_offer_info['offer_address'] = soup.find('a',{'aria-label':'Adres'}).get_text().strip()
        except AttributeError as ae:
                logger.error("Could not fetch data about parcel - Site was deleted or hasn't been properly loaded.")
                logger.error(f"Error page link: {link}")
                raise ae

        # Scrape contact info
        try:
                contact_name = soup.find('span', {'class':'css-1yijy9r es5t28b4'}).get_text()
                # Type of business that is offering this parcel
                offer_type = soup.find('div', {'class':'css-ubt094 es5t28b7'}).get_text()

                full_offer_info['selling_agent_name'] = contact_name
                full_offer_info['selling_firm_type'] = offer_type
        except AttributeError as ea:
                logger.error("Could not fetch contact information")
                raise ae
        
        try:
                phone_number = soup.find('a', {'class':'css-1g26sdq'}).get_text()
                full_offer_info['seller_phone_num'] = phone_number
        except AttributeError as ae:
                logger.error("Could not fetch phone number (may not be available)")
                logger.error(f"Link: {link}")

        if seller_details:
                try:
                        company_name = seller_details.find('strong',{'class':'css-1475nf7 e1bxdpug7'}).get_text()
                except Exception as ae:
                        logger.error(ae)   
                        logger.error("Could not fetch company_namer (may not be available)")
                        logger.error(f"Link: {link}")
                        company_name = None
                try:
                        company_site_link = soup.find('img', {'class':'css-1ga2hw8 e10zojt31'})['src']
                except Exception as ae:
                        logger.error(ae)   
                        logger.error("Could not fetch company_site_link (may not be available)")
                        logger.error(f"Link: {link}")                     
                        company_site_link = None
                try: 
                        company_address = seller_details.find('span', {'class':'css-mzpff5 e1bxdpug10'}).get_text()

                except Exception as ae:
                        logger.error(ae)   
                        logger.error("Could not fetch company_address (may not be available)")
                        logger.error(f"Link: {link}")                        
                        company_address = None
                full_offer_info['selling_firm_name'] = company_name
                full_offer_info['selling_firm_site'] = company_site_link
                full_offer_info['selling_firm_addr'] = company_address

        try:
                # get coordinates from google maps embedded widged
                coordinates_raw_1 = soup.find('div', {'class', 'gm-style'})
                coordinates_raw_2 = coordinates_raw_1.find_all('a', attrs={'href': re.compile("^https://")})
                coordinates_link = [link.get('href') for link in coordinates_raw_2][0]
                full_offer_info['coordinates'] = coordinates_link.split('ll=')[1].split('&')[0]
                full_offer_info['are_coords_exact'] = True if soup.find('div', {'class':'css-3te2t7 ej9jroc0'}) == None else False
        except AttributeError as ae:
                logger.error(f"There was a problem with finding |COORIDATES| - Try increasing |SITE_LOAD_SCROLL_PAUSETIME| ")
                full_offer_info['coordinates'] = None
                full_offer_info['are_coords_exact'] = None
                raise ae

        try:
                details_container = soup.find('div',{'class':'css-xr7ajr e10umaf20'})
                details_name_value = details_container.find_all('div',{'class':{'css-kkaknb enb64yk0'}})
        except AttributeError as ae:
                logger.error(f"Could not fetch main details container")
                logger.error(f"Most probably site was not loaded properly, or site structure changed ")
                logger.error(f"Error page link: {link}")
                raise ae
        
        for dnv in details_name_value:
                detail_name = dnv.find('div',{'class':'css-rqy0wg enb64yk2'}).get_text().strip()
                try:
                    detail_value = dnv.find('div',{'class':'css-1wi2w6s enb64yk4'}).get_text().strip()
                except AttributeError:
                    detail_value = dnv.find('button',{'class':'css-x0kl3j e1k3ukdh0'}).get_text().strip()
        
                full_offer_info[detail_name]=detail_value
                
        try:
                additional_info_container = soup.find('div',{'css-1utkgzv e10umaf20'})
                additional_info_value = additional_info_container.find_all('div',{'class':'css-1k2qr23 enb64yk0'})
                for aiv in additional_info_value:
                        name_value_containers = aiv.find_all('div',{'class':'css-1qzszy5 enb64yk1'})
                        name_value_list = [nvc.get_text().strip() for nvc in name_value_containers]
                        if name_value_list == []:
                                name_value_containers = aiv.find_all('div',{'class':'css-1sqc82x enb64yk1'})
                                name_value_list = [nvc.get_text().strip() for nvc in name_value_containers]
                        if len(name_value_list) != 2: raise ScrapeFailure(f"Problem with name_value length in |Additional Info|: expected len(2), got {len(name_value_list)}")
                        full_offer_info[name_value_list[0]]=name_value_list[1]
        except AttributeError as ae:
                logger.error(f"There was problem with fetching additional information from link {link}")
                logger.error(f"Most probably such information is not available")
                logger.error(f"Exception {ae}")
        
        try:
                added_when_info = soup.find('div', {'class':'css-1soi3e7 e16xl7024'}).get_text()
                last_offer_update_when = soup.find('div', {'class':'css-9dilgw e16xl7025'}).get_text()
                full_offer_info['added_when'] = added_when_info
                full_offer_info['last_offer_update'] = last_offer_update_when
        except AttributeError as ae:
                logger.error(f"There was problem with fetching offer add/update information {link}")
                logger.error(f"Exception {ae}")
        return full_offer_info