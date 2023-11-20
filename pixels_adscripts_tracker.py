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
        tracking_pixels = soup.find_all('img', {'width': '1', 'height': '1'})
        num_tracking_pixels = len(tracking_pixels)

        # Identify potential ad trackers based on script URLs
        ad_trackers = soup.find_all('script', src=True)
        ad_trackers_filtered = [script for script in ad_trackers if is_ad_tracker(script['src'])]
        num_ad_trackers = len(ad_trackers_filtered)

        return num_tracking_pixels, num_ad_trackers

    except Exception as e:
        print(f"Error: {e}")
        return None, None

def is_ad_tracker(script_url):
    # Add conditions here to filter out non-ad tracker scripts
    ad_keywords = ['ad', 'doubleclick', 'google-analytics', 'analytics.js']
    
    # Check if any of the keywords are present in the script URL
    return any(keyword in script_url.lower() for keyword in ad_keywords)

def analyze_websites_from_csv(csv_path):
    # Read the CSV into a DataFrame
    df = pd.read_csv(csv_path)

    # Create columns to store the results
    df['Tracking Pixels'] = None
    df['Ad Trackers'] = None

    # Iterate through the DataFrame and analyze each website
    for index, row in df.iterrows():
        url = row['Domain Name']
        tracking_pixels, ad_trackers = count_tracking_pixels_and_trackers(url)
        df.at[index, 'Tracking Pixels'] = tracking_pixels
        df.at[index, 'Ad Trackers'] = ad_trackers

    return df

csv_file_path = 'df_1_copy.csv'
result_df = analyze_websites_from_csv(csv_file_path)

# Display the resulting DataFrame
print(result_df)
