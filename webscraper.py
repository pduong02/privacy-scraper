import requests
from bs4 import BeautifulSoup
import pandas as pd

def count_third_party_requests(url):
    response = requests.get(url)

    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        tpscripts = soup.find_all('script', src = True)
        print(f"{len(tpscripts)}")
    else:
        print(f"Failed: {response.status_code}" + " " + url)

df = pd.read_csv('virginiauniversities.csv')
df['Domain Name'] = df['Domain Name'].apply(lambda x: 'https://' + x)
df['Domain Name'].apply(count_third_party_requests)

