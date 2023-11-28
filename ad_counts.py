from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import pandas as pd

chrome_driver_path = ChromeDriverManager().install()
chrome_service = Service(chrome_driver_path)
options = webdriver.ChromeOptions()
driver = webdriver.Chrome(options=options, service=chrome_service)

ad_counts = []
def get_ad_count(url):
    try:
        driver.get(url)
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[contains(text(), "ad")]')))
        ads = driver.find_elements(By.XPATH, '//*[contains(text(), "ad")]')
        print(f"Ad count on {url}: {len(ads)}")
        ad_counts.append(len(ads))
    except TimeoutException as e:
        ad_counts.append(0)
    except NoSuchElementException as e:
        ad_counts.append(0)

df = pd.read_csv('finalurls.csv')
websites = df['Domain Name']
for website in websites:
    website = "https://" + website
    get_ad_count(website)

df['Ad Counts'] = ad_counts
df.to_csv('finalurls.csv', index = False)

driver.quit()
