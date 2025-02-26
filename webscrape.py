from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
#  locate elements on a page (e.g., by tag name, class name, etc.).
from selenium.webdriver.common.by import By
# allows waiting until an element appears instead of using time.sleep()
from selenium.webdriver.support.ui import WebDriverWait
# provides pre-built conditions (like waiting for an element to be visible)
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import re
import time
import json
import os


# Need to pip install selenium, beautifulsoup4, lxml
# need to wget install linux based chrome (https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb) and webdriver from https://googlechromelabs.github.io/chrome-for-testing/#stable. location of webdriver needs to be put in /usr/local/bin/

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

def initiate_browser():
    options = Options()
    options.add_argument('--headless')  # Runs Chrome in headless mode (no UI)

    chromedriver_path = "/usr/local/bin/chromedriver"
    service = Service(chromedriver_path)
    driver = webdriver.Chrome(service=service, options=options)
    driver.get('https://poe.ninja/economy/phrecia/essences')

    #dynamically wait (max of 30 seconds) till body tagged html elements load.
    WebDriverWait(driver, 30).until(EC.presence_of_all_elements_located ((By.TAG_NAME, "tr")))

    button = driver.find_element(By.XPATH, '//button[text()="Show more"]')
    button.click()
    time.sleep(3)
    button.click()


    html_content = driver.page_source
    driver.quit()
    return html_content

# Parse table data in html content and create dictionary with key equaling the essence and value equaling its chaos value
def create_essence_dictionary():
    if check_if_dict_exists():
        return "Essence Dictionary already exists"
    html_content = initiate_browser()
    soup = BeautifulSoup(html_content, 'lxml')
    rows = soup.find_all('tr')[1:]
    ess_dict = {}
    for row in rows:
        row_text = row.get_text(strip=True)
        row_text = row_text.replace("wiki", "")
        modified_row = re.split(r'(\d+)', row_text, maxsplit=1)

        essence_name = modified_row[0]

        if len(modified_row) != 3:
            break
        else:
            delim = "Not enough data"
            if delim in "".join(modified_row[1:]):
                chaos_value = re.split(f"{delim}", "".join(modified_row[1:]), maxsplit=1)
                ess_dict[essence_name] = [chaos_value[0][1:], 3.0]

            elif "+" in "".join(modified_row[1:]):
                chaos_value = re.split(r"\+", "".join(modified_row[1:]), maxsplit=1)
                ess_dict[essence_name] = [chaos_value[0][1:], 3.0]

            else:
                if "-" in "".join(modified_row[1:]):
                    chaos_value = re.split(r"-", "".join(modified_row[1:]), maxsplit=1)
                    ess_dict[essence_name] = [chaos_value[0][1:], 3.0]

                else:
                    chaos_value = re.split(r'(?<=0)', "".join(modified_row[1:]), maxsplit=1)
                    ess_dict[essence_name] = [chaos_value[0][1:], 3.0]
    save_dict_to_file(ess_dict)
    return


def get_new_poe_pricing():
    html_content = initiate_browser()
    soup = BeautifulSoup(html_content, 'lxml')
    rows = soup.find_all('tr')[1:]
    ess_dict = {}
    for row in rows:
        row_text = row.get_text(strip=True)
        row_text = row_text.replace("wiki", "")
        modified_row = re.split(r'(\d+)', row_text, maxsplit=1)

        essence_name = modified_row[0]

        if len(modified_row) != 3:
            break
        else:
            delim = "Not enough data"
            if delim in "".join(modified_row[1:]):
                chaos_value = re.split(f"{delim}", "".join(modified_row[1:]), maxsplit=1)
                ess_dict[essence_name] = chaos_value[0][1:]

            elif "+" in "".join(modified_row[1:]):
                chaos_value = re.split(r"\+", "".join(modified_row[1:]), maxsplit=1)
                ess_dict[essence_name] = chaos_value[0][1:]
            else:
                if "-" in "".join(modified_row[1:]):
                    chaos_value = re.split(r"-", "".join(modified_row[1:]), maxsplit=1)
                    ess_dict[essence_name] = chaos_value[0][1:]

                else:
                    chaos_value = re.split(r'(?<=0)', "".join(modified_row[1:]), maxsplit=1)
                    ess_dict[essence_name] = chaos_value[0][1:]
    return ess_dict

def update_ess_dict_with_new_poeninja_pricing():
    ess_dict = open_dict()
    if not ess_dict:
        return "essence dictionary not created yet"
    
    new_values_dict = get_new_poe_pricing()
    for key in ess_dict.keys():
        ess_dict[key][0] = new_values_dict[key]
    # overwright existing file with new information
    save_dict_to_file(ess_dict)
    return

# ess_name: listing to paste into poe, bulkprice per essence
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
        # overwright existing file with new information
        save_dict_to_file(ess_dict)
        return f"{key}'s multiplier has been updated"
    else:
        return "Essence doesn't exist or was typed incorrectly"
    

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
    
def program_loop():
    print("Hello! Welcome to Essence Trade Manager! See below for the list of options to select. Use numbers 1-5 for your input selections.")
    print("Options Menu:")
    print("1. See price Sheet")
    print("2. Update essence price shee")
    print("3. Update database with new poe ninja price per essence")
    print("4. 3-1 suggestions (Out of Order, sorry!)")
    print("5. Exit")
    return