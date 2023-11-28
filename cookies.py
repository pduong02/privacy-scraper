import http.cookiejar
import urllib.request
import csv
import pandas as pd

def analyze_cookies(domain):
    try:
        cookies = http.cookiejar.CookieJar()

        #opener with cookie jar
        opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cookies))

        #send request to website
        response = opener.open(domain)

        third = 0
        first = 0
        #prepare/parse cookie data
        for cookie in cookies:
            #determines if first or third party cookie
            if cookie.domain != urllib.request.urlparse(domain).hostname:
                third = third+1
            else:
                first = first+1
        
        return [first, third]

    except:
        return ['NA','NA']

#websites = ['https://www.google.com']

#website data
csv_file = 'finalurls.csv'

cookie_data = {}

with open(csv_file, 'r', newline='', encoding='utf-8') as file:
    read = csv.reader(file)
    #skip column names (header row)
    next(read, None)
    for entry in read:
        domain = "https://" + entry[0]
        num_cookies = analyze_cookies(domain)
        cookie_data[domain[8:]] = num_cookies
