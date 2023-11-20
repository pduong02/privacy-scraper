import requests
from bs4 import BeautifulSoup
import pandas as pd

def count_tracking_pixels_and_trackers(url):
    try:
        # Send an HTTP GET request to the URL
        response = requests.get(url)
        response.raise_for_status()

        # Parse the HTML content using BeautifulSoup
        soup = BeautifulSoup(response.content, 'html.parser')

        # Count the number of tracking pixels (1x1 images)
        tracking_pixels = soup.find_all('img', {'src': True, 'width': ['0', '1'], 'height': ['0', '1']})
        num_tracking_pixels = len(tracking_pixels)

        # Identify potential ad trackers based on script URLs
        ad_trackers = soup.find_all('script', src=True)
        ad_trackers_filtered = [script for script in ad_trackers if is_ad_tracker(script['src'])]
        num_ad_trackers = len(ad_trackers_filtered)

        # Detect fingerprinting indicators
        fingerprint_indicators = detect_fingerprinting(url)

        return num_tracking_pixels, num_ad_trackers, fingerprint_indicators

    except Exception as e:
        print(f"Error: {e}")
        return None, None, None

def is_ad_tracker(script_url):
    # Add conditions here to filter out non-ad tracker scripts
    ad_keywords = ['ad', 'doubleclick', 'google-analytics', 'analytics.js']

    # Check if any of the keywords are present in the script URL
    return any(keyword in script_url.lower() for keyword in ad_keywords)

def detect_fingerprinting(url):
    try:
        # Send an HTTP GET request to the URL
        response = requests.get(url)
        response.raise_for_status()

        # Parse the HTML content using BeautifulSoup
        soup = BeautifulSoup(response.content, 'html.parser')

        # Check for potential fingerprinting indicators in the HTML
        fingerprint_indicators = []

        # Check for the presence of browser properties that can contribute to fingerprinting
        user_agent_meta = soup.find('meta', {'name': 'useragent'})
        if user_agent_meta:
            fingerprint_indicators.append('User Agent Meta Tag')

        # You may need to add more checks based on specific fingerprinting methods

        return fingerprint_indicators

    except Exception as e:
        print(f"Error: {e}")
        return None

def analyze_websites_from_csv(csv_path):
    # Read the CSV into a DataFrame
    df = pd.read_csv(csv_path)

    # Create columns to store the results
    df['Tracking Pixels'] = None
    df['Ad Trackers'] = None
    df['Fingerprint Indicators'] = None

    # Iterate through the DataFrame and analyze each website
    for index, row in df.iterrows():
        url = row['Domain Name']
        tracking_pixels, ad_trackers, fingerprint_indicators = count_tracking_pixels_and_trackers(url)
        df.at[index, 'Tracking Pixels'] = tracking_pixels
        df.at[index, 'Ad Trackers'] = ad_trackers
        df.at[index, 'Fingerprint Indicators'] = fingerprint_indicators

    return df

# Example usage with a CSV file containing a 'Domain Name' column
csv_file_path = 'df_1_copy.csv'
result_df = analyze_websites_from_csv(csv_file_path)

# Display the resulting DataFrame
print(result_df)
