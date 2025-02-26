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
        return "nothing"
    elif user_input == "5":
        return 0

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
    while i == 1:
        menu_text()
        user_input = input("Which option would you like to select? ")
        check = implement_user_options(user_input)
        if check == 0:
            break