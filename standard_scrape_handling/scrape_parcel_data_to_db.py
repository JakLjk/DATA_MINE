from support_functions.std_function_retry import function_retry, RetryFailure
from logger import logger


def scrape_parcel_data(
        db_con = None,
        mine_links_scraped_in_past = False,
        scraper_config = None,
        
        get_offer_function = None,):
    
    DBOfferDetails = scraper_config.DBOfferDetails
    DBOfferLinks = scraper_config.DBOfferLinks

    # Get information about which iteration of this function was data gathered from
    data_interation_num = db_con.get_col_max_val(
                                    DBOfferDetails.table_name, 
                                    DBOfferDetails.table_scrapiter_col)
    
    if isinstance(data_interation_num, int): 
        data_interation_num += 1 
    else: 
        data_interation_num = 0
    
    if mine_links_scraped_in_past:
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
        try:
            # TODO add retry only on specific raise error
            # offer_details = function_retry(function = get_offer_function,
            #                             args = link,
            #                             retries=3,)
            offer_details = get_offer_function(link)
        except RetryFailure:
            # TODO delete row with bad link
            logger.info(f"Failed to get offer details, skipping...")
            logger.info(f"Offer link: {link}")
            continue

        if offer_details is None:
            db_con.detele_rows_containing(
                            table_name=DBOfferDetails.table_name, 
                            column_name=DBOfferDetails.table_link_col, 
                            value=link)
            logger.info(f"DELETED Faulty link from db: {link}")
            continue

        offer_details[DBOfferDetails.table_runtype_col] = run_type
        offer_details[DBOfferDetails.table_scrapdate_col] = db_con.get_sql_date()
        offer_details[DBOfferDetails.table_scrapiter_col] = data_interation_num
        offer_details[DBOfferDetails.table_link_col] = link

        logger.info(f"Inserting parcel data into Database")
        # TESTING --------------
        db_con.make_lacking_column_insert_into_table(DBOfferDetails.table_name,
                                                     offer_details)
        # Old way that did not allow for inserting new cols:
        # db_con.insert_into_table(DBOfferDetails.table_name,
        #                          offer_details)
        db_con.commit()
        logger.info(f"Parcel data successfully inserted into db")

