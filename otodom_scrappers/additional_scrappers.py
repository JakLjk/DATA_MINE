from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By


from .otodom_config import Links
from config import DriverConf

def get_num_pages() -> int:
    """Used to get value of last page with offers that is being listed on webpage"""
    first_page_link = Links.MAIN_LINK

    options = Options()
    options.headless = DriverConf.HEADLESS
    driver = webdriver.Firefox(options=options)
    driver.get(first_page_link)
    last_page_num =  driver.find_element(By.XPATH, 
        "/html/body/div[1]/div[2]/main/div/div[2]/div[1]/div[4]/div/nav/button[5]").text
    driver.quit()
    return int(last_page_num)