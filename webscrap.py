import requests
from bs4 import BeautifulSoup


url = "https://www.nytimes.com"
html = requests.get(url).text

#these two lines recieves html code file as python string

soup = BeautifulSoup(html, 'html.parser')

#gonna use BeautifulSoup to parse data from the whole data file

#html tag parsing

print(soup.title)

#returns title tage
#<title data-rh="true">The New York Times - Breaking News, US News, World News and Videos</title>

print(soup.title.name)
#returns title tag value which will be "The New York Times - Breaking News, US News, World News and Videos"

# BeautifulSoup let traverse through html structure through .html_tag
# div, p, h1, all tags

# find() : returns a signle tag that matches the parameter
# find_all() : returns all the tags that matches the parameter
# select() : Style CSS selector = gives same parameter as that

print(soup.find("div").prettify())
# return list [...]
print(soup.find_all('h3', {'class' : 'css-codfme e1sjycav0'}))
# specific source paramter from <a href="something"> ... </a> we can get href value using .get
print(soup.find('a').get('href'))
# only return the string part
print(soup.find('a').get_text())
# find_all
hrefs = soup.find_all('a')
for name in hrefs:
    print(name.get('href'))

#select = like css, follows how css identifies each id, class etc ex)# = id, . = class
#also returns list
id_select = soup.select('div#id')
class_select = soup.select('div.class')
# can 'select' strcutre inside structure
# ex) <div class: 'class'>
#       <a> ... </a>
#     </div>
class_a_select = soup.select('div.class a') # or 'div.class > a' can be used to show the structure
