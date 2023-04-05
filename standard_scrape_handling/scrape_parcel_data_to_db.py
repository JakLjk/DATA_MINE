
from otodom_scrappers import get_offer_details
from otodom_scrappers.otodom_config import DBOfferDetails, DBOfferLinks

from config import DBConf, DataMineConf
from SQL_DATABASE import Database

from logger import logger

def scrape_parcel_data():
    db_con = Database(
            DBConf.config("MYSQL_HOSTNAME"),
            DBConf.config("username"),
            DBConf.config("password"),
            DBConf.config("MYSQL_DBNAME")
    )

    # Used to get information about which iteration of this function was data gathered from
    data_interation_num = db_con.get_col_max_val(
                                    DBOfferDetails.table_name, 
                                    DBOfferDetails.table_scrapiter_col)
    
    if isinstance(data_interation_num, int): 
        data_interation_num += 1 
    else: 
        data_interation_num = 0
    
    # TODO get one row mechanics
    if DataMineConf.MINE_LINKS_SCRAPPED_IN_PAST:
        run_type = "FULL"  
        links_to_parse = db_con.get_distinct_col(DBOfferLinks.table_name,
                                DBOfferLinks.table_link_col)

    # TODO Check proper partial working, after first iteration
    else:
        run_type = "PARTIAL"
        links_to_parse = db_con.get_distinct_not_in_table2(DBOfferLinks.table_name, 
                                                           DBOfferDetails.table_name, 
                                                           DBOfferDetails.table_link_col)
        

    num_of_links = len(links_to_parse)
    for i, link in enumerate(links_to_parse):
        logger.info(f"Gathering data about parcel {i+1}/{num_of_links}")
        offer_details = get_offer_details(link)
        offer_details[DBOfferDetails.table_runtype_col] = run_type
        offer_details[DBOfferDetails.table_scrapdate_col] = db_con.get_sql_date()
        offer_details[DBOfferDetails.table_scrapiter_col] = data_interation_num
        offer_details[DBOfferDetails.table_link_col] = link

        logger.info(f"Inserting parcel data into Database")
        db_con.insert_into_table(DBOfferDetails.table_name,
                                 offer_details)
        logger.info(f"Parcel data successfully inserted")

