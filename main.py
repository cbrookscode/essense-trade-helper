from webscrape import *

# need check to see if dictionary already created or not. should only happen once.
create_essence_dictionary()

i = 1
while i == 1:
    program_loop()
    user_input = input("Which option would you like to select? ")
    check = implement_user_options(user_input)
    if check == 0:
        break


# create logical seperation of functions into different files.
# create unit tests
# Fix holes in existing logic
# Add last remaining function in options list
