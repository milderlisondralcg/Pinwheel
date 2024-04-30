# Class Pinwheel

class Pinwheel:

    LOG_PATH = "logs/"
    
    def __init__():
        print("hello from init")
        
    def create_log_file(job_type):
        path = job_type + "-"  + ".log"

    # Create a log entry
    def log_entry(job_type, log_message):
        
        log_file = Pinwheel.LOG_PATH + job_type + ".txt"

        with open(log_file,"a", encoding="utf-8") as text:
            text.write(log_message + "\n")
        
