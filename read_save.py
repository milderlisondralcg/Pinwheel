#Read text files and save each URL to db

import mysql.connector
import os
import time
import datetime
import traceback

mydb = mysql.connector.connect(host='localhost',user='root',password='',database='pinwheel')
baseurl = 'http://biolegend.com'
basepath = 'json/'

now = datetime.datetime.now()
print("Process started: " + str(now))

# Loop through entire directory
for entry in os.listdir(basepath):
    print(entry)
    if os.path.isfile(os.path.join(basepath, entry)):
        time.sleep(2)
        fs = open(basepath + "/" + entry)
        file_content = fs.readlines()

        # Read through all lines within text file
        for line in file_content:
            product_url = baseurl + line

            try:
                mycursor = mydb.cursor()
                sql = "INSERT INTO product_urls (url) VALUES (%s)"
                val = (product_url)
                mycursor.execute(sql,(val,))

                mydb.commit()
            except Exception:
                print(traceback.format.exect())

now = datetime.datetime.now()
print("Process completed: " + str(now))
