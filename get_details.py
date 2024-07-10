# Scrape data
# URL given

import requests
import datetime
import traceback
import sys
import os
import json

from bs4 import BeautifulSoup

# Begin loop
now = datetime.datetime.now()
print("Process started: " + str(now))

# Set headers
headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36'}

url = "http://biolegend.com/en-us/products/alexa-fluor-700-anti-human-cd64-antibody-17129"

page = requests.get(url, headers=headers)
soup_obj = BeautifulSoup(page.text,'html.parser')
product_info = soup_obj.find(id='productInfo')
product_info_items_headings = product_info.find_all('dt')
product_info_items_values = product_info.find_all('dd')

product_details = soup_obj.find(id='ProductDetailsContainer')
product_details_headings = product_details.find_all('dt')
product_details_values = product_details.find_all('dd')
#print(product_details_headings)
#print(product_details_values)

product_info_data = {}
product_details_data = {}
total_data = {}

# Add data to details list to Dictionary
index = 0
for item in (product_info_items_headings):
    product_info_data[item.get_text().strip()] = product_info_items_values[index].get_text().strip()
    total_data[item.get_text().strip()] = product_info_items_values[index].get_text().strip()
    index += 1
    
index = 0
for heading in (product_details_headings):
    product_details_data[heading.get_text().strip()] = product_details_values[index].get_text().strip()
    total_data[heading.get_text().strip()] = product_details_values[index].get_text().strip()
    index += 1

#total_data['product_info'] = product_info_data
#total_data['product_details'] = product_details_data

for x in (total_data):
    print("Heading : " + x + " \n" + total_data[x])
# Get Catalog ID(s)
table = soup_obj.find(id='variantsContainer')
tbody = table.find('tbody') # Catalog IDs are in rows
trows = tbody.find_all('tr') # Returns a list

for row in table.tbody.find_all('tr'):    
    # Find all data for each column
    columns = row.find_all('td')
    
    if(columns != []):
        
        catalog_id = columns[0].text.strip()
        if catalog_id:
            size = columns[1].text.strip()
            #print(catalog_id)
            #print(size)
            span_tag = columns[2].find('span') #find all span tags in data column
            for attr in span_tag.attrs:
                if(attr == 'data-price'):
                    # print(span_tag['data-price']) # get the value of attribute
                    price = span_tag['data-price']
                    #print(price)

            data = {"agent":{"catalog_id":catalog_id,"size":size,"price":price}}
            json_data = json.dumps(data)
            #print(json_data)
            y = json.loads(json_data)
            #print(y)
    
            #print(y)
            #create filename
            json_file = "json/" + str(catalog_id) + ".txt"
        
        '''
        zone = columns[1].text.strip()
        area = columns[2].span.contents[0].strip('&0.')
        population = columns[3].span.contents[0].strip('&0.')
        density = columns[4].span.contents[0].strip('&0.')
        homes_count = columns[5].span.contents[0].strip('&0.')

        #df = df.append({'Neighborhood': neighborhood,  'Zone': zone, 'Area': area, 'Population': population, 'Density': density, 'Homes_count': homes_count}, ignore_index=True)
        '''
#product_detail_items_values = product_detail.find_all('td')




