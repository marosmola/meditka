import json
import ebooklib
import lxml.etree
import xml.etree.ElementTree as ET


from datetime import datetime
from ebooklib import epub
from bs4 import BeautifulSoup

book = epub.read_epub('LC2020.epub')

# today = datetime.now()
# formatted_date = today.strftime("%Y-%m-%d")

# # formatted_date = '2019-04-02'


# item = book.get_item_with_href('{}.html'.format(formatted_date))
# item_body = item.get_body_content().decode('utf-8')

# # print(item)

# parsed_html = BeautifulSoup(item.get_body_content(), 'html.parser')
# readings = parsed_html.body.find_all('div', attrs={'class':'lcCITANIE'})

# e = readings.pop(len(readings) - 1)

# parsed_data = json.dumps({
#     formatted_date: str(e),
# })

# print(parsed_data)


# print(len(readings))
# print(readings[2])

# New parser
files = [x for x in book.get_items_of_type(ebooklib.ITEM_DOCUMENT)]
item = files[20].get_body_content()
new_item = item.decode('utf-8').replace('\xa0', ' ')

print(new_item)

root = ET.fromstring(new_item)
# root = lxml.etree.fromstring(new_item)

# Datum
print(root.find('.//span[@class="lcWD"]').text) # Streda
print(root.find('.//span[@class="lcMD"]').text + root.find('.//span[@class="lcMY"]').text) # 18. december 2019
print(root.find('.//span[@class="lcND"]').text) # meniny: Sláva, Slávka


citania = root.findall('.//div[@class="lcCITANIE"]')

for x in citania:
    if x.find('./p[@class="lcVPEblock"]') is not None:
        print('Evanjelium')
        print(x.find('.//span[@class="lcVERS"]').text) # Pane, vodca svojho ľudu, ty si dal Mojžišovi zákon na Sinaji; príď, vystri svoju ruku a vysloboď nás!
        print(x.find('.//h4').text) # Čítanie zo svätého evanjelia podľa Matúša
        print(x.find('.//h4/span').text) # Mt 1, 18-24
        print(x.find('.//h5').text) # Ježiš sa narodí z Márie, zasnúbenej s Jozefom, Dávidovým synom
        # Text in paragraphs
        for z in x.findall('.//p'): # .//p[not(@class)]
            if z.text is not None:
                print(z.text)
