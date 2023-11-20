import requests
from bs4 import BeautifulSoup

def count_third_party_requests(url):
    response = requests.get(url)

    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        tpscripts = soup.find_all('script', src = True)
        print(f"Number of third-party requests: {len(tpscripts)}")
        #for resource in tpscripts:
         #   print(resource['src'] if 'src' in resource.attrs else resource['href'])
    else:
        print(f"Failed: {response.status_code}")

url = 'https://nba.com'
count_third_party_requests(url)