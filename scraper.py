# Scrape data
# URL given
    
import requests
import datetime
import traceback
import sys
import os
import json
from pinwheel import Pinwheel

Pinwheel.__init__()


now = datetime.datetime.now()

from bs4 import BeautifulSoup

products_per_page = 200
last_page = 155
total_links_captured = 0
products_info = {}

# Begin loop
now = datetime.datetime.now()
print("Process started: " + str(now))

# Set headers
headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36'}

#for i in range(last_page):
for i in range(100,last_page):
    try:
        page_num = i + 1
        print(page_num)
        # Retrieve base url
        url = 'https://www.biolegend.com/en-us/search-results?GroupID=&PageNum=' + str(page_num) + '&PageSize=' + str(products_per_page)
        print(url)
        page = requests.get(url, headers=headers)
        
        # Create Beautiful Soup object
        soup_obj = BeautifulSoup(page.text,'html.parser')

        try:
            product_list = soup_obj.find(id='productsHolder')
            #print(product_list)
            products_list_items = product_list.find_all('h2')
            print(len(products_list_items))
            for link in products_list_items:
                atags = link.find_all('a')
                for tag in atags:
                    href = tag.get('href')
                    # print(href)
                
            for i in range(len(product_list)):
                atags = link.find_all('a')
                #print(atags)
            
            #create filename
            json_file = "json/page" + str(page_num) + ".txt"
            
            if os.path.exists(json_file):
                os.remove(json_file)
                print(f"File removed: {json_file}")
            
            total_links_captured =+ len(products_list_items)
            for link in products_list_items:
                atags = link.find_all('a')
                for tag in atags:
                    href = tag.get('href')
                    with open(json_file,"a", encoding="utf-8") as text:
                        text.write(href+"\n")
            log_message = json_file + ":" + " Total links captured " + str(total_links_captured)
            job_type = "Scrape"
            Pinwheel.log_entry(job_type, log_message)
            
        except:
            print(traceback.format_exc())
            print("Could not get the list of urls from productsHolder element:")
            Pinwheel.log_entry("hello")
            print(url)
    except Exception:
        print(traceback.format_exc())
        print("An error occured")
        
# Print after loop completes
print(total_links_captured)
now = datetime.datetime.now()
print(now)


