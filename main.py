from logger import logger
from otodom_scrappers import run_scraping

from config import DBConf
from setup_db import change_db_creds


def main(edit_db_creds = True):
    # TODO add database_config manual password input
        
    # Test function for otodom scrapper
    run_scraping()


if __name__ == '__main__':
    main()




