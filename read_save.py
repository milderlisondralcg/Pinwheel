#Read text files and save each URL to db
# As of 04/30/2024 processed 155 files in 7 minutes

import mysql.connector
import os, sys
import time
import datetime
import traceback
from pinwheel import Pinwheel
#Pinwheel.__init__()

try:
    mydb = mysql.connector.connect(host='localhost',user='root',password='',database='pinwheel')
except Exception:
    print("Could not connect to data store")
    log_message = traceback.format_exc()    
    Pinwheel.log_entry("Data store error", log_message)    
    #print(traceback.format_exc())
    sys.exit(1)
baseurl = 'http://biolegend.com'
basepath = 'json/'
basepath_completed = 'json_processed/'
total_urls_saved = 0

now = datetime.datetime.now()
print("Process started: " + str(now))

# Loop through entire directory
for entry in os.listdir(basepath):
    print("Processing file: " + entry)
    if os.path.isfile(os.path.join(basepath, entry)):
        time.sleep(2)
        fs = open(basepath + "/" + entry)
        json_source = basepath + entry
        json_source_destination = basepath_completed + entry
        file_content = fs.readlines()

        # Read through all lines within text file
        for line in file_content:
            product_url = baseurl + line.strip()
            try:
                mycursor = mydb.cursor()

                sql = "SELECT url from products_urls WHERE url = '" + product_url + "'"
                mycursor.execute(sql)
                mycursor.fetchall()
                if mycursor.rowcount == 0:
                    try:
                        sql = "INSERT INTO products_urls (url) VALUES (%s)"
                        val = (product_url,) # comma added to allow 1 column to be inserted
                        mycursor.execute(sql,val)
                        mydb.commit()
                        total_urls_saved += 1
                    except Exception:
                        print(traceback.format_exc())    
                else:
                    log_message = "Product url exists: " + product_url
                    Pinwheel.log_entry("SaveURL", log_message)
               
            except Exception:
                print(traceback.format_exc())
                
        fs.close() #close file to ensure it can be moved
        os.replace(json_source, json_source_destination)

now = datetime.datetime.now()
print("Process completed: " + str(now))
print("Total urls saved: " + str(total_urls_saved))

# as of 4/30/2024 this process takes 3 minutes to complete for 11,749 records
# from 95 files
