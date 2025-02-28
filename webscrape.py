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

    # Wait for the "Show more" button to be clickable
    button = WebDriverWait(driver, 30).until(
        EC.element_to_be_clickable((By.XPATH, '//button[text()="Show more"]'))
    )
    button.click()

    # Wait again for the button to be clickable before clicking again
    button = WebDriverWait(driver, 30).until(
        EC.element_to_be_clickable((By.XPATH, '//button[text()="Show more"]'))
    )
    button.click()


    html_content = driver.page_source
    driver.quit()
    return html_content

def filter_out_essences(sorted_rows_html):
    new_sorted_list = []
    prefixes_to_avoid = ["Wailing", "Weeping", "Whispering", "Muttering"]
    for row in sorted_rows_html:
        tracker = False
        if row == None:
            continue

        for prefix in prefixes_to_avoid:
            if prefix in row:
                tracker = True
                continue
        if tracker:
            continue
        new_sorted_list.append(row)
    return new_sorted_list



def parse_raw_html_into_rows(html_content):
    soup = BeautifulSoup(html_content, 'lxml')
    rows = soup.find_all('tr')[1:]
    rows_text = []
    for row in rows:
        row_text = row.get_text(strip=True)
        rows_text.append(row_text)
    sorted_rows_text = sorted(rows_text)
    return sorted_rows_text


def parse_rows_into_dictionary_entries(sorted_rows_html):
    ess_dict = {}
    for row in sorted_rows_html:
        row_text = row.replace("wiki", "")
        modified_row = re.split(r'(\d+)', row_text, maxsplit=1)

        essence_name = modified_row[0]

        if row == None:
            continue
        else:
            # need to fix this logic to just check if there is only one digit ahead of decimal, if so then dont slice the result.
            if essence_name == "Remnant of Corruption":
                match = re.search(r'\d+\.\d', "".join(modified_row[1:]))
                result = match.group()
                chaos_value = result
                ess_dict[essence_name] = [chaos_value, 3.0]
            else:
                match = re.search(r'\d+\.\d', "".join(modified_row[1:]))
                result = match.group()
                chaos_value = result[1:]
                ess_dict[essence_name] = [chaos_value, 3.0]
    return ess_dict

# Parse table data in html content and create dictionary with key equaling the essence and value equaling its chaos value
def get_new_poe_pricing():
    html_content = initiate_browser()
    rows = parse_raw_html_into_rows(html_content)
    filtered_ess_rows = filter_out_essences(rows)
    ess_dict = parse_rows_into_dictionary_entries(filtered_ess_rows)
    return ess_dict


