# Class Pinwheel

import datetime

class Pinwheel:

    LOG_PATH = "logs/"
    ts = datetime.datetime.now()
    
    #def __init__():
        
        
    def create_log_file(job_type):
        path = job_type + "-"  + ".log"

    # Create a log entry
    def log_entry(job_type, log_message):
        #ts = datetime.datetime.now()
        log_file = Pinwheel.LOG_PATH + job_type + ".txt"
        with open(log_file,"a", encoding="utf-8") as text:
            text.write("**************************************\n")
            text.write(str(Pinwheel.ts) + "\n" + job_type + ": " + log_message + "\n")
            text.write("**************************************")
        
