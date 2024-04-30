import numpy as np
from Solve_each_ADMM import performOptimisation
from SSSS import SSSS

#def local_optimiser(hour : int, water_height : float, z: np.array, rho : float, stakeholder : int):
#     x_i = np.arange(48)*0.99
#     return x_i

class ADMM_optimiser_WDN:
    def __init__(self, conn1, conn2, N_iterations : int,  N_vary_rho: int, stakeholder: int):
        self.conn1 = conn1      #TCP connection
        self.conn2 = conn2      #TCP connection
        self.N_vary_rho = N_vary_rho        #Number of iterations with varying rho
        self.stakeholder = stakeholder      #My stakeholder id
        self.N_iterations = N_iterations    #Number of ADMM iterations
        self.N_c = 24   #Control horizon
        self.N_s = 3    #Number of stakeholders
        self.N_q = 2    #number of pumps
        self.under_relaxation=False # Using under relaxation
        
        self.rho = 1    #Initial
        self.mu = 5#10    #Vary rho algorithm parameter
        self.tau = 2    #Vary rho algorithm parameter

        self.z=np.zeros((self.N_c*self.N_q,1)) #Initialization ADMM



    def optimise(self, hour : int , water_height: float):
        self.lambda_i = np.zeros((self.N_c*self.N_q,1)) #ADMM Initialisation
        self.x_bar = np.zeros((self.N_c*self.N_q,1)) #ADMM Initialisation
        
        #Timeshift initial guess
        self.z = np.roll(self.z,1)
        self.z[-1] = self.z[-2]    

        #Solve problem
        for k in range(0,self.N_iterations):
            print("Iteration", k)
            #Solve local problem
            try: 
                self.x_i = performOptimisation(hour, water_height, self.stakeholder,self.rho,self.lambda_i,self.z)
                self.x_i= self.x_i.reshape(-1, 1)
            except:
                self.x_i = 3/4*self.x_i + 1/4*self.z
                print("Local optimisation failed")

            ### BEGIN ADMM
            #Determining z: 
            self.z_i = self.x_i + (1/self.rho)*self.lambda_i #Stakeholders entry in sum
            self.conn1.sendall(self.z_i.tobytes())  #Distribute z_i
            self.conn2.sendall(self.z_i.tobytes())

            self.z_2 = np.frombuffer(self.conn1.recv(8*self.N_c*self.N_q), dtype=self.z_i.dtype) #Recive other z_i's
            self.z_3 = np.frombuffer(self.conn2.recv(8*self.N_c*self.N_q), dtype=self.z_i.dtype)
            self.z_2= self.z_2.reshape(-1, 1)
            self.z_3= self.z_3.reshape(-1, 1)
            
            #Determining ztilde and z 
            self.z_tilde = 1/self.N_s*(self.z_i + self.z_2+ self.z_3)
            if  self.under_relaxation == True: 
                self.z = self.z - 1/(self.N_s + 1)*(self.z - self.z_tilde)   
            else:
                self.z = self.z_tilde 
                
            
            #Determining lambda: 
            self.lambda_i_tilde = self.lambda_i + self.rho*(self.x_i - self.z)   
            if self.under_relaxation == True: 
                 self.lambda_i = self.lambda_i -1/(self.N_s + 1)*(self.lambda_i - self.lambda_i_tilde) 
            else: 
                self.lambda_i = self.lambda_i_tilde       
            
            ### END ADMM 
            
            ### BEGIN find rho
            if(k<=self.N_vary_rho):
                self.conn1.sendall(self.x_i.tobytes())  #Distribute x_i for residual calculation 
                self.conn2.sendall(self.x_i.tobytes())

                self.x_2 = np.frombuffer(self.conn1.recv(8*self.N_c*self.N_q), dtype= self.x_i.dtype) #Recive x_i's for reidual calculation
                self.x_3 = np.frombuffer(self.conn2.recv(8*self.N_c*self.N_q), dtype= self.x_i.dtype)
                self.x_2=self.x_2.reshape(-1, 1)
                self.x_3=self.x_3.reshape(-1, 1)


                self.x_bar_old = self.x_bar
                self.x_bar = 1/self.N_s*(self.x_i + self.x_2 + self.x_3)
                self.r_norm_squared =  np.linalg.norm(self.x_i - self.x_bar, 2)**2 + np.linalg.norm(self.x_2 - self.x_bar, 2)**2 + np.linalg.norm(self.x_3 - self.x_bar, 2)**2
                self.s_norm = self.N_s*self.rho**2*np.linalg.norm(self.x_bar - self.x_bar_old,2)

                if(np.sqrt(self.r_norm_squared)>self.mu*self.s_norm):
                    self.rho = self.rho * self.tau
                elif(self.s_norm > self.mu*np.sqrt(self.r_norm_squared)):
                    self.rho = self.rho / self.tau
                print(self.rho)
            ### End find rho
            
            
        return self.x_i[:2]       #Return actuation commands