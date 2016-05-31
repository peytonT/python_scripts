# get location from ip address
# using database from maxmind
# return details about the location & option to open Google Maps
# command: python location.py <ip_adress>

import requests
import sys
import webbrowser

url = 'http://freegeoip.net/json/'
host = sys.argv[1]      # 23.14.146.151
res = requests.get('{}{}'.format(url, host))
json_string = res.json()

for key, val in json_string.items():
    print('{}: {}'.format(key, val))

google_maps_link = 'https://www.google.com/maps/place/{},{}'.format(json_string['latitude'], json_string['longitude'])

# open google maps link of the location on a new tab on the default browser
open_link = input('\nOpen google maps? (y/n): ')
if open_link == 'y':
    webbrowser.open_new_tab(google_maps_link)
elif open_link == 'n':
    pass
else:
    print('Invalid input!')

# sample output:
# zip_code: 02142
# metro_code: 506
# time_zone: America/New_York
# longitude: -71.0843
# country_name: United States
# ip: 23.14.146.151
# region_code: MA
# latitude: 42.3626
# city: Cambridge
# region_name: Massachusetts
# country_code: US

# Open google maps? (y/n):
