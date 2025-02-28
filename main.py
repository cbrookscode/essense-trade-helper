from webscrape import *
from options import *
from cli import *

# need check to see if dictionary already created or not. should only happen on
def main():
    if check_if_dict_exists():
        program_loop()
    else:
        ess_dict = get_new_poe_pricing()
        save_dict_to_file(ess_dict)
        program_loop()


if __name__ == '__main__':
    main()

