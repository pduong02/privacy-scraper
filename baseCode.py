import requests
from bs4 import BeautifulSoup

def measure_intrusiveness(url):
    response = requests.get(url)
    
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')

        # Count ads (example: counting elements with class 'ad')
        ads_count = len(soup.find_all(class_='ad'))

        # Identify pop-ups (example: elements with onclick attribute)
        popups_count = len(soup.find_all(attrs={"onclick": True}))

        # Analyze tracking scripts (example: elements with 'script' tag)
        scripts_count = len(soup.find_all('script'))

        # Evaluate page load time
        page_load_time = response.elapsed.total_seconds()

        print(f"Ads count: {ads_count}")
        print(f"Pop-ups count: {popups_count}")
        print(f"Tracking scripts count: {scripts_count}")
        print(f"Page load time: {page_load_time} seconds")

    else:
        print(f"Failed to retrieve the webpage. Status code: {response.status_code}")

# Replace 'url' with the actual URL of the website you want to analyze
measure_intrusiveness('https://example.com')
