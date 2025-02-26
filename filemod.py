import json
import os

def save_dict_to_file(ess_dict):
    with open('essenceinfo.txt', 'w') as file:
        json.dump(ess_dict, file, indent=4)
    return

def check_if_dict_exists():
    if os.path.exists('./essenceinfo.txt'):
        return True
    return False
def open_dict():
    ess_dict = {}
    if check_if_dict_exists:
        with open('essenceinfo.txt', 'r') as file:
            ess_dict = json.load(file)
    return ess_dict