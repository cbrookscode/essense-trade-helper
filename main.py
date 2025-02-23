from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from bs4 import BeautifulSoup
import time
import re

# Set up Chrome options for headless mode
options = Options()
options.add_argument('--headless')  # Runs Chrome in headless mode (no UI)

chromedriver_path = "/usr/local/bin/chromedriver"

service = Service(chromedriver_path)
driver = webdriver.Chrome(service=service, options=options)
driver.get('https://poe.ninja/economy/phrecia/essences')
time.sleep(10)
html_content = driver.page_source
driver.quit()

soup = BeautifulSoup(html_content, 'lxml')
rows = soup.find_all('tr')[1:]

my_dict = {}

# Parse table data in html content and create dictionary with key equaling the essence and value equaling its chaos value
for row in rows:
    row_text = row.get_text(strip=True)
    row_text = row_text.replace("wiki", "") 
    modified_row = re.split(r'(\d+)', row_text, maxsplit=1)
    essence_name = modified_row[0]
    chaos_value = modified_row[1][:1]
    my_dict[essence_name] = chaos_value

# missing other essences cause it doesn't load full page without hitting load more.