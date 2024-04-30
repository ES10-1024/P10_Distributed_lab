import numpy as np
from Solve_each_ADMM import performOptimisation
from SSSS import SSSS
from logging import logging 




#def local_optimiser(hour : int, water_height : float, z: np.array, rho : float, stakeholder : int):
#     x_i = np.arange(48)*0.99
#     return x_i

class ADMM_optimiser_WDN:
    def __init__(self, conn1, conn2, N_iterations : int,  N_vary_rho: int, stakeholder: int,log=None):
        self.conn1 = conn1      #TCP connection
        self.conn2 = conn2      #TCP connection
        self.log = log
        self.N_vary_rho = N_vary_rho        #Number of iterations with varying rho
        self.stakeholder = stakeholder      #My stakeholder id
        self.N_iterations = N_iterations    #Number of ADMM iterations
        self.N_c = 24   #Control horizon
        self.N_s = 3    #Number of stakeholders
        self.N_q = 2    #number of pumps
        
        self.rho = 4    #Initial
        self.mu = 10    #Vary rho algorithm parameter
        self.tau = 2    #Vary rho algorithm parameter

        self.z=np.zeros((self.N_c*self.N_q,1)) #Initialization ADMM
        




    def optimise(self, hour : int , water_height: float):
        self.lambda_i = np.zeros((self.N_c*self.N_q,1)) #ADMM Initialisation
        self.x_bar = np.zeros((self.N_c*self.N_q,1)) #ADMM Initialisation
        ssss_instance = SSSS(conn1=self.conn1, conn2=self.conn2,stakeholder=self.stakeholder,log=self.log) #Shamirs secret sharing initialisation

        
        #Timeshift initial guess
        self.z = np.roll(self.z,1)
        self.z[-1] = self.z[-2] 
           

        #Solve problem
        for k in range(0,self.N_iterations):
            print("Iteration", k)
            #Solve local problem
            try: 
                self.x_i = performOptimisation(hour, water_height, self.stakeholder,self.rho,self.lambda_i,self.z)
                #Reshaping the result 
                self.x_i= self.x_i.reshape(-1, 1)
            except:
                self.x_i = 3/4*self.x_i + 1/4*self.z
                print("Local optimisation failed")

            ### BEGIN ADMM
            #Determining z: 
            self.z_i = self.x_i + (1/self.rho)*self.lambda_i 
            #Doing SSSS to known the sum 
            self.summedSecretZ=self.ssss_instance.DoSSSS(self.z_i) 
            #Dividing to determine z_tilde
            self.z_tilde=self.summedSecretZ/self.N_s
           # self.conn1.sendall(self.z_i.tobytes())  #Distribute z_i
          #  self.conn2.sendall(self.z_i.tobytes())

            #self.z_2 = np.frombuffer(self.conn1.recv(8*self.N_c*self.N_q), dtype=self.z_i.dtype) #Recive other z_i's
           # self.z_3 = np.frombuffer(self.conn2.recv(8*self.N_c*self.N_q), dtype=self.z_i.dtype)
            #Reshaping the recevied data 
            #self.z_2= self.z_2.reshape(-1, 1)
           # self.z_3= self.z_3.reshape(-1, 1)
            #Determining ztilde and z 
            #self.z_tilde = 1/self.N_s*(self.z_i + self.z_2+ self.z_3)
            self.z = self.z - 1/(self.N_s + 1)*(self.z - self.z_tilde)   
            
            #Determining lambda: 
            self.lambda_i_tilde = self.lambda_i + self.rho*(self.x_i - self.z)         
            self.lambda_i = self.lambda_i -1/(self.N_s + 1)*(self.lambda_i - self.lambda_i_tilde) 
            
            ### END ADMM 
            print("rho er:", self.rho) 
            ### BEGIN find rho
            if(k<=self.N_vary_rho):
                #Determining sum of xi based on SSSS m 
                self.summedSecretX=self.ssss_instance.DoSSSS(self.x_i)   
                      
               # self.conn1.sendall(self.x_i.tobytes())  #Distribute x_i for residual calculation 
               # self.conn2.sendall(self.x_i.tobytes())

               # self.x_2 = np.frombuffer(self.conn1.recv(8*self.N_c*self.N_q), dtype= self.x_i.dtype) #Recive x_i's for reidual calculation
               # self.x_3 = np.frombuffer(self.conn2.recv(8*self.N_c*self.N_q), dtype= self.x_i.dtype)
                
               # self.x_2= self.x_2.reshape(-1, 1)
               # self.x_3= self.x_3.reshape(-1, 1)
                
                
                self.x_bar_old = self.x_bar
            
                self.x_bar =self.summedSecretX/self.N_s
                
                #self.x_bar = 1/self.N_s*(self.x_i + self.x_2 + self.x_3)
                #Determine r #PROBLEM SSSSS ER IKKE LAVET TIL AT DER KUN HAVES EN SKALAR DETTE SKAL DER SES PÅ!
                self.secretR=np.array([np.linalg.norm(self.x_i - self.x_bar, 2)**2])
                print("Shape of secret:", self.secretR.shape) 
                
                
                self.r_norm_squared=self.ssss_instance.DoSSSS(self.secretR) 
                
                #self.r_norm_squared =  np.linalg.norm(self.x_i - self.x_bar, 2)**2 + np.linalg.norm(self.x_2 - self.x_bar, 2)**2 + np.linalg.norm(self.x_3 - self.x_bar, 2)**2
                self.s_norm = self.N_s*self.rho**2*np.linalg.norm(self.x_bar - self.x_bar_old,2)

                if(np.sqrt(self.r_norm_squared)>self.mu*self.s_norm):
                    self.rho = self.rho * self.tau
                elif(self.s_norm > self.mu*np.sqrt(self.r_norm_squared)):
                    self.rho = self.rho / self.tau
                print(self.rho)
            ### End find rho
            
       # print("x_bar SSSS:", self.x_barSSSS) 
       # print("x_bar:", self.x_bar)
        
        return self.x_i[:2]       #Return actuation commands