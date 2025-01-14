# Scrape data
# URL given

import mysql.connector
import requests
import datetime
import traceback
import sys, os, json

from pinwheel import Pinwheel
#Pinwheel.__init__()

from bs4 import BeautifulSoup

# Set headers
headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36'}

# Begin loop
now = datetime.datetime.now()
print("Process started: " + str(now))

try:
    mydb = mysql.connector.connect(host='localhost',user='root',password='',database='pinwheel')
    
except Exception:
    print("Could not connect to data store")
    log_message = traceback.format_exc()    
    Pinwheel.log_entry("Data store error", log_message)    
    #print(traceback.format_exc())
    sys.exit(1)

def get_urls(limit):
    """Retrieves urls with given limit.
    Parameters
    ----------
    limit : int, required
    The number of records to retrieve

    Raises
    ------
    NotImplementedError
        If no sound is set for the animal or passed in as a
        parameter.
    """
    try:
        mycursor = mydb.cursor()

        sql = "SELECT url from products_urls WHERE `status` = 'Open' LIMIT " + str(limit)
        mycursor.execute(sql)
        result_urls = mycursor.fetchall()

        for x in result_urls:
            url = x[0]
            get_details_result = get_url_details(url)
            if(get_details_result is None):
                update_sql = "UPDATE products_urls SET `status` = 'Closed' WHERE url = '" + url + "'"
                mycursor.execute(update_sql)
            commit_result = mydb.commit()
    except Exception:
        print(traceback.format_exc())

    # END Select a limited amount of URLs to read 


# Method to retrieve details from given url
def get_url_details(url):

    #url = "http://biolegend.com/en-us/products/brilliant-violet-510-mouse-igg2b-kappa-isotype-ctrl-8016"
    print("Retrieving URL: ")
    print(url)
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

    # Dictionaries
    product_info_data = {}
    product_details_data = {}
    total_data = {}
    reagent = {}
    reagent_attributes = {}
    reagent_product_details = {}
    antigen_details = {}

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

    '''
    for x in (total_data):
        print("Heading : " + x + " \n" + total_data[x])
    '''

    # Get Catalog ID(s)
    table = soup_obj.find(id='variantsContainer')
    tbody = table.find('tbody') # Catalog IDs are in rows
    trows = tbody.find_all('tr') # Returns a list

    for row in table.tbody.find_all('tr'):    
        # Find all data for each column
        columns = row.find_all('td')

        if(columns != []):
            
            inventory = 0
            catalog_id = columns[0].text.strip()
            print(catalog_id)
            if(catalog_id):
                try:
                    size = columns[1].text.strip()
                    span_tag = columns[2].find('span') #find all span tags in data column
                    for attr in span_tag.attrs:
                        if(attr == 'data-price'):
                            price = span_tag['data-price']
                    try:
                        quantity_label = columns[3].find('label')

                        #if quantity_label is not None:
                            #if quantity_label.has_attr('find'):
                        quantity_input = quantity_label.find('input')
                        #print(quantity_input)
                        #print(quantity_input['data-stock'])
                        inventory = quantity_input['data-stock']
                    except Exception:
                        inventory = 0
                        #print(traceback.format_exc())                            

                except Exception:
                    size = 0
                    span_tag = columns[2].find('span') #find all span tags in data column
                    print(span_tag)
                    for attr in span_tag.attrs:
                        print(attr)
                        if(attr == 'data-price'):
                            print("attr is data-price")
                            print(span_tag['data-price']) # get the value of attribute
                            price = span_tag['data-price']
                    ''''''
                    try:       
                        inventory = 0
                        quantity_label = columns[3].find('label')
                        if quantity_label is not None:
                            if quantity_label.has_attr('find'):
                                quantity_input = quantity_label.find('input')
                                inventory = quantity_input['data-stock']
                    except Exception:
                        inventory = 0
                        #print(traceback.format_exc())
                    ''''''   
                    

                reagent_attributes.update({"size":size,"price":price,"inventory":inventory})
                reagent['catalog_id'] = catalog_id
                reagent['attributes'] = reagent_attributes
                
        

                # TODO: Insert Reagent information into data store
                
                # Product Details 
                product__details_section = soup_obj.find(id='ProductDetailsContainer')
                labels = product__details_section.find_all('dt')
                label_val = product__details_section.find_all('dd')

                for val in labels:
                    label = val.decode_contents().strip()
                    #print(val.decode_contents().strip())
                    #print(val.findNext('dd').contents[0].strip())
                    label_val = val.findNext('dd').contents[0]

                    reagent_product_details.update({label:label_val})

                #print(reagent_product_details)

                reagent['product_details'] = reagent_product_details
                # Antigen Details
                antigen_details_section = soup_obj.find(id='antigenDetails')
                labels = antigen_details_section.find_all('dt')

                for val in labels:
                    label = val.decode_contents().strip()
                    label_val = val.findNext('dd').contents[0].strip()

                    antigen_details.update({label:label_val})

                #print(antigen_details)
                reagent['antigen_details'] = antigen_details
                json_string = json.dumps(reagent, indent=4)
                print(json_string)

                #create JSON file of current reagent
                json_file = "json/" + str(catalog_id) + ".txt"
                with open(json_file,"a", encoding="utf-8") as text:
                    text.write(json_string)

                try:
                    mydb = mysql.connector.connect(host='localhost',user='root',password='',database='pinwheel')

                    try:
                        mycursor = mydb.cursor()

                        sql = "SELECT catalog_id from products WHERE catalog_id = '" + catalog_id + "'"
                        mycursor.execute(sql)
                        mycursor.fetchall()
                        if mycursor.rowcount == 0:
                            try:
                                sql = "INSERT INTO products (catalog_id, price, size, inventory) VALUES (%s, %s, %s, %s)"
                                val = (catalog_id, price, size, inventory) # comma added to allow 1 column to be inserted
                                mycursor.execute(sql,val)
                                commit_result = mydb.commit()
                                return commit_result
                                #return(commit_result)
                                #total_urls_saved += 1
                            except Exception:
                                print(traceback.format_exc())    
                        else:
                            log_message = "Catalog id exists: " + catalog_id
                            Pinwheel.log_entry("Save Reagent", log_message)
                            #print(log_message)
                    except Exception:
                        print(traceback.format_exc())

                except Exception:
                    print("Could not connect to data store")
                    log_message = traceback.format_exc()    
                    Pinwheel.log_entry("Data store error", log_message)
                    sys.exit(1)
                
                
                #data = {"agent":{"catalog_id":catalog_id,"size":size,"price":price,"inventory":inventory}}
                #json_data = json.dumps(data)
                #print(json_data)
                #y = json.loads(json_data)
    
                #create filename
                json_file = "json/" + str(catalog_id) + ".txt"
            else:
                mydb = mysql.connector.connect(host='localhost',user='root',password='',database='pinwheel')
                mycursor = mydb.cursor()
                update_sql = "UPDATE products_urls SET `status` = 'Error' WHERE url = '" + url + "'"
                mycursor.execute(update_sql)
                commit_result = mydb.commit()

get_urls(20)

