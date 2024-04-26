import numpy as np
import random

class SSSS: 
    def __init__(self):
        self.offset = 1 #Offset to avoid negative values  
        self.scaling = 10000 #Scaling such rounding becomes insignificant
        self.N_c = 24   #Control horizon
        self.N_q = 2    #number of pumps
        self.Beta = 10000019 # Prime number used for SSSS 
        self.N_s = 3 #Number of stakeholders
    
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
            
            
            
                    
        
# Example usage
ssss = SSSS()
secret = np.ones((48, 1))
    
result1 = ssss.generatedOutFromFunction(secret*2)
result2 = ssss.generatedOutFromFunction(secret*5)
result3 = ssss.generatedOutFromFunction(secret*1)

summed=result1+result2+result3 

result=ssss.getSecret(summed)

print(result)

            