from webscrape import *
from filemod import *
import re

# should this be create price sheet and then store the information in a text f ile that can be viewed at will and then updated with another function?
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
        ess_dict[key][0] = new_values_dict[key][0]
    save_dict_to_file(ess_dict)
    return

def three_to_one():
    ess_dict = open_dict()
    if not ess_dict:
        return "essence dictionary not created yet"
    tracked = []
    exclude = ["Essence of Horror", "Essence of Delirium", "Essence of Insanity", "Essence of Hysteria", "Remnant of Corruption"]
    count = 0
    for key in ess_dict.keys():
        if key in exclude:
            continue
        split = re.split(r'(Essence.*)', key, maxsplit=1)
        base_essence_name = split[1]
        if base_essence_name not in tracked:
            screaming_key = "Screaming " + base_essence_name
            shrieking_key = "Shrieking " + base_essence_name
            deafening_key = "Deafening " + base_essence_name
            screaming_bulk_value = 0
            shrieking_bulk_value = 0
            deafening_bulk_value = 0
            if screaming_key in ess_dict.keys():
                screaming_bulk_value = float(ess_dict[screaming_key][0]) * ess_dict[screaming_key][1]
            if shrieking_key in ess_dict.keys():
                shrieking_bulk_value = float(ess_dict[shrieking_key][0]) * ess_dict[shrieking_key][1]
            if deafening_key in ess_dict.keys():
                deafening_bulk_value = float(ess_dict[deafening_key][0]) * ess_dict[deafening_key][1]
            if screaming_bulk_value < shrieking_bulk_value:
                count += 1
                print(f"upgrade {base_essence_name} to shrieking")
            if shrieking_bulk_value < deafening_bulk_value:
                count += 1
                print(f"upgrade {base_essence_name} to deafening")
            tracked.append(base_essence_name)
    if count == 0:
        print("No upgrades to suggest")
    return



'''
only need to check upgrading screaming > shrieking and shrieking > deafening

create empty tracked list
iterate over dictionary keys excluding special essences and remnants
filter out base essence name
if base essence name has been tracked then skip.
    create string name key to search for bulksale values of screaming, shrieking, deafening
    perform calcs to determine if should 3>1 at any stage in the above
    print(upgrad screamings or upgrade shriekings or both)
    move base essence name to tracked list
'''