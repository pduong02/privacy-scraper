from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

chrome_driver_path = ChromeDriverManager().install()
chrome_service = Service(chrome_driver_path)
options = webdriver.ChromeOptions()
options.add_argument('--ignore-certificate-errors')
driver = webdriver.Chrome(options=options, service=chrome_service)

def get_ad_count(url):
    try:
        driver.get(url)
        ads = driver.find_elements(By.XPATH, '//*[contains(text(), "ad")]')
        print(f"Ad count on {url}: {len(ads)}")

    finally:
        pass  # No need to quit the driver here, as it will be done outside the function

with open('sketchystreamingsites.txt', 'r') as file:
    for line in file:
        line = "https://" + line.strip('\n')  # Remove newline characters
        get_ad_count(line)

# Quit the driver after processing all URLs
driver.quit()
