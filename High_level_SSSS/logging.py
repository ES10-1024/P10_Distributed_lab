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
import time 

class logging: 
    def __init__(self, filename):  
        #Getting timestamp for the filename
        timestamp = datetime.now().strftime("%m-%d_%H-%M-%S")
        self.filename = f"{filename}_{timestamp}.csv"
        self.header = ['ID','Data','Time']  # Use the passed header value

        # Check if the file exists, if not, create it
        if not os.path.exists(self.filename):
            with open(self.filename, 'w', newline='') as csv_file:
                if self.header:
                    csv_writer = csv.writer(csv_file)
                    csv_writer.writerow(self.header)
                    
     # Writing data to the class              
    def write_data(self, data):
         data=data+[time.time()]
        
         with open(self.filename, 'a', newline='') as csv_file:
            csv_writer = csv.writer(csv_file)
            csv_writer.writerow(data)
         

            
#The following can be used to test the class             
# Specify the filename
filename = 'example.csv'

# Create an instance of CSVHandler
log = logging(filename)
#Data to test the class 

for i in range(1,6):
    test=np.ones((42,1))*0.1*1/i
    data=["test1",test]
    log.write_data(data)
    test2=i 
    data=["test2",test2]
    log.write_data(data)
    time.sleep(2)
    test3=1/(i**2) 
    data=["test3",test]
    log.write_data(data)
    time.sleep(3)
data=["test4",1e-3] 
log.write_data(data)
print("Printing data")
