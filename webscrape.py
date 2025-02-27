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

# returned rows are not text. Rows is a list of beautiful soup objects whose text can be access via .get_text() method. Its type is "<class 'bs4.element.Tag'>""
def parse_raw_html_into_rows(html_content):
    soup = BeautifulSoup(html_content, 'lxml')
    rows = soup.find_all('tr')[1:]
    return rows


def parse_rows_into_dictionary_entries(rows_of_html):
    ess_dict = {}
    for row in rows_of_html:
        row_text = row.get_text(strip=True)
        row_text = row_text.replace("wiki", "")
        modified_row = re.split(r'(\d+)', row_text, maxsplit=1)

        essence_name = modified_row[0]

        if row == None:
            break
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
    ess_dict = parse_rows_into_dictionary_entries(rows)
    save_dict_to_file(ess_dict)
    return


