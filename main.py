from webscrape import *
from options import *
from cli import *

# need check to see if dictionary already created or not. should only happen on
def main():
    if check_if_dict_exists():
        program_loop()
    else:
        get_new_poe_pricing()
        program_loop()


if __name__ == '__main__':
    main()



# Add last remaining function in options list
# Sort data prior to storing in dictionary?
# store price sheet in text file? Store it in same fashion as essence tab for viewing?
