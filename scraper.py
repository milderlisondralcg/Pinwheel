# Scrape data
# URL given

import requests
import datetime

now = datetime.datetime.now()

from bs4 import BeautifulSoup

products_per_page = 100
last_page = 309

# Print when loop starts

now = datetime.datetime.now()
print("Process started: " + str(now))
for i in range(last_page):
    try:
        page_num = i + 1
        # Retrieve base url
        url = 'https://www.biolegend.com/en-us/search-results?GroupID=&PageNum=' + str(page_num) + '&PageSize=200'
        # print(url)
        page = requests.get(url)

        # Create Beautiful Soup object
        soup_obj = BeautifulSoup(page.text,'html.parser')


        product_list = soup_obj.find(id='productsHolder')
        products_list_items = product_list.find_all('h2')

        for link in products_list_items:
            atags = link.find_all('a')
            for tag in atags:
                href = tag.get('href')
                # print(href)
        if(i % 10 == 0):
            now = datetime.datetime.now()
            print("10 pages completed: " + str(now))
            #print("10 pages completed")
    except:
        print("An error occured")
        
# Print after loop completes
now = datetime.datetime.now()
print("10 pages completed: " + str(now))

