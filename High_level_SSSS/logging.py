'''Small script to log into a file. As init, it take the filename 
   Writting data is on the form:  
   ['ID',data]
   A matlab script to pick out the desire ID is present in the folder
   A bit of test code is presented in the buttom. 
'''
import csv 
import os 
from datetime import datetime
import numpy as np

class logging: 
    def __init__(self, filename):  
        #Getting timestamp for the filename
        timestamp = datetime.now().strftime("%m-%d_%H-%M-%S")
        self.filename = f"{filename}_{timestamp}.csv"
        self.header = ['ID','Data']  # Use the passed header value

        # Check if the file exists, if not, create it
        if not os.path.exists(self.filename):
            with open(self.filename, 'w', newline='') as csv_file:
                if self.header:
                    csv_writer = csv.writer(csv_file)
                    csv_writer.writerow(self.header)
                    
     # Writing data to the class              
    def write_data(self, data):
        
         with open(self.filename, 'a', newline='') as csv_file:
            csv_writer = csv.writer(csv_file)
            csv_writer.writerow(data)
         

            
#The following can be used to test the class             
'''
#Data to test the class 
data = [
    ['Pump 1',100],
    ['Pump 2', 25],
]

# Specify the filename
filename = 'example.csv'

# Create an instance of CSVHandler
log = logging(filename,header)

# Write data to the CSV file
for row in data:
    log.write_data(row)

print("Data has been written to the CSV file.")
'''