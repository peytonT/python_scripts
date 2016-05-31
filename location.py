# get location from ip address
# using database from maxmind
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
    print('Invid input!')
