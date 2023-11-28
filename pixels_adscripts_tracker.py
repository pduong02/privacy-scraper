import requests
from bs4 import BeautifulSoup
import pandas as pd
from concurrent.futures import ThreadPoolExecutor

def count_tracking_pixels_and_trackers(url):
    try:
        with requests.get(url) as response:
            response.raise_for_status()
            soup = BeautifulSoup(response.content, 'html.parser')

            # Count the number of tracking pixels (1x1 images)
            tracking_pixels = soup.find_all('img', {'src': True, 'width': ['0', '1'], 'height': ['0', '1']})
            num_tracking_pixels = len(tracking_pixels)

            # Identify potential ad trackers based on script URLs
            ad_trackers = soup.find_all('script', src=True)
            ad_trackers_filtered = [script for script in ad_trackers if is_ad_tracker(script['src'])]
            num_ad_trackers = len(ad_trackers_filtered)

            # Detect fingerprinting indicators
            fingerprint_indicators = detect_fingerprinting(soup)

            return num_tracking_pixels, num_ad_trackers, fingerprint_indicators

    except Exception as e:
        print(f"Error: {e}")
        return None, None, None

def is_ad_tracker(script_url):
    # Add conditions here to filter out non-ad tracker scripts
    ad_keywords = ['ad', 'doubleclick', 'google-analytics', 'analytics.js']
    return any(keyword in script_url.lower() for keyword in ad_keywords)

def detect_fingerprinting(soup):
    fingerprint_indicators = []

    # Check for the presence of browser properties that can contribute to fingerprinting
    user_agent_meta = soup.find('meta', {'name': 'useragent'})
    if user_agent_meta:
        fingerprint_indicators.append('User Agent Meta Tag')

    # Check for canvas fingerprinting
    canvas_element = soup.find('canvas')
    if canvas_element:
        fingerprint_indicators.append('Canvas Fingerprinting')

    # Check for WebGL fingerprinting
    webgl_element = soup.find('script', {'type': 'application/javascript'}, text=lambda t: 'WEBGL_debug_renderer_info' in t)
    if webgl_element:
        fingerprint_indicators.append('WebGL Fingerprinting')

    # Check for font fingerprinting
    font_element = soup.find('style', {'type': 'text/css'}, text=lambda t: '@font-face' in t)
    if font_element:
        fingerprint_indicators.append('Font Fingerprinting')

    # You may need to add more checks based on specific fingerprinting methods

    return fingerprint_indicators

def analyze_website(url):
    tracking_pixels, ad_trackers, fingerprint_indicators = count_tracking_pixels_and_trackers(url)
    return {'Tracking Pixels': tracking_pixels, 'Ad Trackers': ad_trackers, 'Fingerprint Indicators': fingerprint_indicators}

def analyze_websites_from_csv(csv_path):
    # Read the CSV into a DataFrame
    df = pd.read_excel(csv_path)

    # Prepend 'https://' to the 'Domain Name' column
    df['URL'] = 'https://' + df['Domain Name']

    # Use ThreadPoolExecutor for parallelization
    with ThreadPoolExecutor(max_workers=5) as executor:
        results = list(executor.map(analyze_website, df['URL']))

    # Merge the results back into the DataFrame
    result_df = pd.concat([df, pd.DataFrame(results)], axis=1)

    return result_df

# Example usage with a CSV file containing a 'Domain Name' column
csv_file_path = 'thirdpartyrequests.xlsx'
result_df = analyze_websites_from_csv(csv_file_path)

# Display the resulting DataFrame
print(result_df)

result_df.to_csv('thirdpartyrequests2.csv', index=False)

