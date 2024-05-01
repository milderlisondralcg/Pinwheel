#Read text files and save each URL to db
# As of 04/30/2024 processed 155 files in 7 minutes

import mysql.connector
import os
import time
import datetime
import traceback

mydb = mysql.connector.connect(host='localhost',user='root',password='',database='pinwheel')
baseurl = 'http://biolegend.com'
basepath = 'json/'
basepath_completed = 'json_processed/'

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

                sql = "SELECT url from product_urls WHERE url = '" + product_url + "'"
                mycursor.execute(sql)
                mycursor.fetchall()
                if mycursor.rowcount == 0:
                    try:
                        sql = "INSERT INTO product_urls (url) VALUES (%s)"
                        val = (product_url,) # comma added to allow 1 column to be inserted
                        mycursor.execute(sql,val)
                        mydb.commit()
                    except Exception:
                        print(traceback.format_exc())    
                else:
                    print("Product url exists: " + product_url)
               
            except Exception:
                print(traceback.format_exc())
                
        fs.close() #close file to ensure it can be moved
        os.replace(json_source, json_source_destination)

now = datetime.datetime.now()
print("Process completed: " + str(now))

# as of 4/30/2024 this process takes 3 minutes to complete for 11,749 records
# from 95 files
