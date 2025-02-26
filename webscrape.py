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
from filemod import *


# Need to pip install selenium, beautifulsoup4, lxml
# need to wget install linux based chrome (https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb) and webdriver from https://googlechromelabs.github.io/chrome-for-testing/#stable. location of webdriver needs to be put in /usr/local/bin/



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

