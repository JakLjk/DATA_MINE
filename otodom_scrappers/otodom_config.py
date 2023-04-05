class Links:
    MAIN_DOMAIN = "https://www.otodom.pl"
    MAIN_LINK  = "https://www.otodom.pl/pl/oferty/sprzedaz/mieszkanie/slaskie?distanceRadius=0&market=ALL&locations=%5Bregions-12%5D&viewType=listing"
    PARSED_MAIN_LINK = "https://www.otodom.pl/pl/oferty/sprzedaz/mieszkanie/slaskie?distanceRadius=0&market=ALL&locations=%5Bregions-12%5D&viewType=listing&page={}"
    LINK_MAIN_PART  = "https://www.otodom.pl{}"



class DBOfferLinks:
    table_name = "parcel_links"

    table_link_col = "link_string"
    table_structure = [""]


class DBOfferDetails:
    table_name = "parcel_data"

    table_runtype_col = "run_type"
    table_scrapdate_col = "scrap_date"
    table_scrapiter_col = "scrap_iter"
    table_link_col = "link_string"
    table_structure = [		
"offer_title",	
"offer_price",	
"offer_address",	
"coordinates",	
"are_coords_exact",	
"Powierzchnia",	
"Forma własności",	
"Liczba pokoi",	
"Stan wykończenia",	
"Piętro",	
"Balkon / ogród / taras",	
"Czynsz",	
"Miejsce parkingowe",	
"Obsługa zdalna",	
"Ogrzewanie",	
"Rynek",	
"Typ ogłoszeniodawcy",	
"Dostępne od",	
"Rok budowy",	
"Rodzaj zabudowy",	
]