from selenium import webdriver

options = webdriver.ChromeOptions()
options.add_argument("--headless")  # Run without UI
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")

# Initialize WebDriver
driver = webdriver.Chrome(options=options)
driver.get("https://www.google.com")

# Check if page title contains "Google"
print("Page title:", driver.title)

# Close the browser
driver.quit()
