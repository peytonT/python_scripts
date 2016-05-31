# Retrieve time of a specific location, user inputs an address or blank for current location

# sample use:
# python clock.py 'dallas, tx'
# ['Tuesday, 31 May 2016, 12:32:01']
# America/Chicago
# Central Daylight Time

import requests
import time
import re
import urllib
import argparse
import sys

if len(sys.argv) == 1:
    print(time.ctime())

else:
    # get coordinates from the address
    addr = sys.argv[1].replace(' ','+')
    url = 'https://maps.googleapis.com/maps/api/geocode/json?address={}' \
            '&key=AIzaSyAtRjOGCDF27C6Pr6NRK53ahNWs-5FBhPE'.format(addr)
    req = requests.get(url)
    json_string = req.json()

    geometry = [item['geometry']for item in json_string['results']]
    location = [item['location'] for item in geometry]  # if 'location' in item]

    # get timezone info form the coordinates
    UTC_timestamp = time.time()
    url1 = 'https://maps.googleapis.com/maps/api/timezone/json?location={},{}&timestamp={}' \
        '&key=AIzaSyB8ECTWZTmsF2F6Ji3YMvvzLRJdAWOg8Ss'.format(
            location[0]['lat'], location[0]['lng'], UTC_timestamp)

    req1 = requests.get(url1)
    json_string1 = req1.json()
    timezone = json_string1['timeZoneId']
    timezone_name = json_string1['timeZoneName']

    # retrieve time
    # further work: using timezonedb API to get the time
    url2 = 'https://timezonedb.com/time-zones/{}'.format(timezone)
    req = urllib.request.Request(url2)
    resp = urllib.request.urlopen(req)
    html_page = resp.read()

    cur_time = re.findall(r'<span id="clock">(.*?)</span>', str(html_page))
    print(cur_time)
    print(timezone)
    print(timezone_name)
