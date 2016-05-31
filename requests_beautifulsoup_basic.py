from bs4 import BeautifulSoup as bs
import requests
import re

page = requests.get('https://timezonedb.com/time-zones/Australia/Perth')
#print(page.content.decode('ascii'))

soup = bs(page.content, 'lxml')
# get title text
print(soup.title.text)

# get html body
print(soup) # or soup.prettify

'''
find methods:
find_all(tag_name, attributes)
find = find_all[0]
'''

#find a text of Label=GMT Offset (in next td tag)
#returns a whole tag --> get text only
gmt = soup.find(text="GMT Offset").findNext('td')
print(gmt.text)

# find all <a> tags (links)
links = soup.findAll('a')
for link in links:
    print(link.get('href')) # get value of href attribute in <a> tag
    #print(link.text)   # get link's lable

idtag = soup.find(id='nav')
all_text = soup.get_text()
all_a_and_b_tags = soup.find_all(['a','b'])
all_tags_started_w_b = soup.find_all(re.compile('^b'))
all_a_tags_w_href_contains_fwSlash_r = soup.find_all('a', {'href': re.compile('/r')})

for t in all_a_tags_w_href_contains_fwSlash_r:
    print(t)
