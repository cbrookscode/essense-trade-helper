from webscrape import get_new_poe_pricing
from filemod import *

def print_price_sheet():
    ess_dict = open_dict()
    if not ess_dict:
        return "essence dictionary not created yet"
    
    for key in ess_dict.keys():
        poeninjaprice = float(ess_dict[key][0])
        multiplier = ess_dict[key][1]

        bulkprice = int(poeninjaprice * multiplier)
        listing = f"{bulkprice * 27}/27" 

        print(f"{key}: {listing}, {bulkprice}")
    return


def search_essence_name(search_value):
    ess_dict = open_dict()
    if not ess_dict:
        return "essence dictionary not created yet"
    
    for key in ess_dict.keys():
        if key.lower() == search_value.lower():
            return key
    return "not found"

def update_multiplier():
    ess_dict = open_dict()
    if not ess_dict:
        return "essence dictionary not created yet"
    
    user_input_ess_name = input("Enter essence name you want to update: ")
    user_input_last_sale_price = input("Enter listing price (ex. 65/5): ")

    parsed_input = user_input_last_sale_price.split('/', 1)
    num_sold = float(parsed_input[0])
    total_chaos = float(parsed_input[1])
    bulk_price_per_essence = num_sold/total_chaos

    key = search_essence_name(user_input_ess_name)
    if key != "not found":
        ess_dict[key][1] = bulk_price_per_essence/float(ess_dict[key][0])
        save_dict_to_file(ess_dict)
        return f"{key}'s multiplier has been updated"
    else:
        return "Essence doesn't exist or was typed incorrectly"

def update_ess_dict_with_new_poeninja_pricing():
    ess_dict = open_dict()
    if not ess_dict:
        return "essence dictionary not created yet"
    
    new_values_dict = get_new_poe_pricing()
    for key in ess_dict.keys():
        ess_dict[key][0] = new_values_dict[key]
    save_dict_to_file(ess_dict)
    return
