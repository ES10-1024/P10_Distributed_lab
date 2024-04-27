import numpy as np
import random

                #Determine r #PROBLEM SSSSS ER IKKE LAVET TIL AT DER KUN HAVES EN SKALAR DETTE SKAL DER SES PÅ!


class SSSS: 
    def __init__(self,conn1,conn2, stakeholder: int):
        self.conn1 = conn1      #TCP connection
        self.conn2 = conn2      #TCP connection
        
        self.offset = 1 #Offset to avoid negative values  
        self.scaling = 10000 #Scaling such rounding becomes insignificant
        self.N_c = 24   #Control horizon
        self.N_q = 2    #number of pumps
        self.Beta = 10000019 # Prime number used for SSSS 
        self.N_s = 3 #Number of stakeholders
        self.stakeholder=stakeholder 
    
    #Hidding the secret in second degrees polyniums  
    def generatedOutFromFunction(self, secret): 
        # Predefining a few matrices
        b = np.zeros((3, self.N_q * self.N_c))
        
        # Going through each entry in the vector, scaling it and hiding it as described in SSSS 
        for index, element in enumerate(secret):
            #Offseting and rounding the secret 
            scaledOffset= np.round(self.scaling * (secret[index] + self.offset))
            #Determing the variables for the second degree polynium 
            a1 = random.randint(0, self.Beta - 1)
            a2 = random.randint(0, self.Beta - 1)
            #Determin b for x=1 x=2 and x=3: 
            for x in range(1,4):
                b[x-1, index]= (scaledOffset+a1*x+a2*x**2) % self.Beta 
        return b  # Return the resulting matrix b
    #Getting the summed secret out 
    
    def getSecret(self,summedFunctionValue): 
        #Predefing the matrix need 
        num_cols = summedFunctionValue.shape[1]
        summedSecret = np.zeros((num_cols, 1))        
        delta=np.array([3, -3, 1])
        for index in range(num_cols): 
            #Determing the secret remebering the modulu 
            summedSecret[index]= (delta @ summedFunctionValue[:,index]) % self.Beta
            #Descaling the result: 
            summedSecret[index]=(summedSecret[index]-(self.N_s*self.scaling))/self.scaling 
        return summedSecret
    
    def DoSSSS(self,secret): 
        #Defining a few matrix for start. 
        b1=np.zeros((1,self.N_c*self.N_q))
        b2=np.zeros((1,self.N_c*self.N_q))
        b3=np.zeros((1,self.N_c*self.N_q))
        #Starting by masking the secret by using a second degree polynium 
        maskedSecret=self.generatedOutFromFunction(secret)
        if self.stakeholder==1:  #Water tower ID 1
             #Distrubted row 2 and 3
             #conn1 = pump1 ID: 2
             #conn2 = pump2 ID: 3 
             #Picking out the differenct b: 
             b1x1=maskedSecret[0,:]
             b1x2=maskedSecret[1,:]
             b1x3=maskedSecret[2,:]
             #Distrubtion to the rest of the stakeholders: 
             self.conn1.sendall(b1x2.tobytes())  
             self.conn2.sendall(b1x3.tobytes())
             
             #Reciving from the others: 
             b2x1 = np.frombuffer(self.conn1.recv(8*self.N_c*self.N_q), dtype=b1.dtype) #Recive other z_i's
             b3x1 = np.frombuffer(self.conn2.recv(8*self.N_c*self.N_q), dtype=b1.dtype)
             #Reshaping the recevied data 
             b1x1= b1x1.reshape(-1, 1)
             b2x1= b2x1.reshape(-1, 1)
             b3x1= b3x1.reshape(-1, 1)
             # Adding the Recived up and sending it out: 
             b1=b1x1+b2x1+b3x1
             print("b1",b1.shape)
             self.conn1.sendall(b1.tobytes())  
             self.conn2.sendall(b1.tobytes())
             #Reciving b2 and b3 
             b2 = np.frombuffer(self.conn1.recv(8*self.N_c*self.N_q), dtype=b1.dtype) #Recive other z_i's
             b3 = np.frombuffer(self.conn2.recv(8*self.N_c*self.N_q), dtype=b1.dtype)
             #Reshaping the recevied data
             b1= b1.reshape(-1, 1) 
             b2= b2.reshape(-1, 1)
             b3= b3.reshape(-1, 1)
             
             
             
             
        if self.stakeholder==2: # pump 1 ID 2 
             #conn1 = tower ID: 1 
             #conn2 = pump2 ID: 3 
             #Picking out the differenct b: 
             b2x1=maskedSecret[0,:]
             b2x2=maskedSecret[1,:]
             b2x3=maskedSecret[2,:]
             #Distrubtion to the rest of the stakeholders: 
             self.conn1.sendall(b2x1.tobytes())  
             self.conn2.sendall(b2x3.tobytes())
             #Reciving from the others: 
             b1x2 = np.frombuffer(self.conn1.recv(8*self.N_c*self.N_q), dtype=b2.dtype) #Recive other z_i's
             b3x2 = np.frombuffer(self.conn2.recv(8*self.N_c*self.N_q), dtype=b2.dtype)
             #Reshaping the recevied data 
             b1x2= b1x2.reshape(-1, 1)
             b2x2= b2x2.reshape(-1, 1)
             b3x2= b3x2.reshape(-1, 1)
             # Adding the Recived up and sending it out: 
             b2=b1x2+b2x2+b3x2
             print("b2",b2.shape) 
             self.conn1.sendall(b2.tobytes())  
             self.conn2.sendall(b2.tobytes())
             #Reciving b1 and b3 
             b1 = np.frombuffer(self.conn1.recv(8*self.N_c*self.N_q), dtype=b2.dtype) #Recive other z_i's
             b3 = np.frombuffer(self.conn2.recv(8*self.N_c*self.N_q), dtype=b2.dtype)
             #Reshaping the recevied data 
             b1= b1.reshape(-1, 1)
             b2= b2.reshape(-1, 1)
             b3= b3.reshape(-1, 1)
             
        if self.stakeholder==3: # pump 2 ID 3
                 # conn1 = tower ID: 1 
                 # conn2 = pump 1 ID 2  
                 # Picking out the different b: 
                 print("stakeholder 3")
                 b3x1 = maskedSecret[0, :]
                 b3x2 = maskedSecret[1, :]
                 b3x3 = maskedSecret[2, :]
                
                 # Distribution to the rest of the stakeholders: 
                 self.conn1.sendall(b3x1.tobytes())  
                 self.conn2.sendall(b3x2.tobytes())
                
                 # Receiving from the others: 
                 b1x3 = np.frombuffer(self.conn1.recv(8*self.N_c*self.N_q), dtype=b3.dtype) # Receive other z_i's
                 b2x3 = np.frombuffer(self.conn2.recv(8*self.N_c*self.N_q), dtype=b3.dtype)
                
                 # Reshaping the received data 
                 b1x3 = b1x3.reshape(-1, 1)
                 b2x3 = b2x3.reshape(-1, 1)
                 b3x3 = b3x3.reshape(-1, 1)
                 print("Shape of b1x3:", b1x3.shape)
                 print("Shape of b2x3:", b2x3.shape)
                 print("Shape of b3x3:", b3x3.shape)
                 # Adding the received up and sending it out: 
                 b3 = b1x3 + b2x3 + b3x3 
                 print("b3",b3.shape)

                 self.conn1.sendall(b3.tobytes())  
                 self.conn2.sendall(b3.tobytes())
                
                 # Receiving b1 and b2 
                 b1 = np.frombuffer(self.conn1.recv(8*self.N_c*self.N_q), dtype=b3.dtype) # Receive other z_i's
                 b2 = np.frombuffer(self.conn2.recv(8*self.N_c*self.N_q), dtype=b3.dtype)
                
                 # Reshaping the received data 
                 b1 = b1.reshape(-1, 1)
                 b2 = b2.reshape(-1, 1)
                 b3 = b3.reshape(-1, 1)
# Assuming b1, b2, and b3 are NumPy arrays
        print("Shape of b1:", b1.shape)
        print("Shape of b2:", b2.shape)
        print("Shape of b3:", b3.shape)
        bstacked=np.vstack((b1.T,b2.T,b3.T))
        #Getting out the secret value: 
        summedSecret=self.getSecret(bstacked)
        
        return  summedSecret
    
    
            
            
            
                    
        
# Example usage
#ssss = SSSS()
#secret = np.ones((48, 1))
    
#result1 = ssss.generatedOutFromFunction(secret*2)
#result2 = ssss.generatedOutFromFunction(secret*5)
#result3 = ssss.generatedOutFromFunction(secret*1)

#summed=result1+result2+result3 

#result=ssss.getSecret(summed)

#print(result)

            