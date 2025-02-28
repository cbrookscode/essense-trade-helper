from options import *

def implement_user_options(user_input):
    if user_input == "1":
        print_price_sheet()
        return
    elif user_input == "2":
        update_multiplier()
        return
    elif user_input == "3":
        update_ess_dict_with_new_poeninja_pricing()
        return
    elif user_input == "4":
        return three_to_one()
    elif user_input == "5":
        return 0
    
def check_if_valid_user_input(user_input):
    valid = ["1", "2", "3", "4", "5"]
    if user_input not in valid:
        return False
    return True

def menu_text():
    print("Hello! Welcome to Essence Trade Manager! See below for the list of options to select. Use numbers 1-5 for your input selections.")
    print("Options Menu:")
    print("1. See price Sheet")
    print("2. Update essence price sheet")
    print("3. Update database with new poe ninja price per essence")
    print("4. 3-1 suggestions (Out of Order, sorry!)")
    print("5. Exit")
    return

def program_loop():
    i = 1
    seperator = "=============================================================================="
    while i == 1:
        menu_text()
        user_input = input("Which option would you like to select? ")
        if check_if_valid_user_input(user_input):
            print(seperator)
            check = implement_user_options(user_input)
            print(seperator)
            if check == 0:
                break
        else:
            print(seperator)
            print("ERROR: Not a valid option. Enter a number 1-5")
            print(seperator)