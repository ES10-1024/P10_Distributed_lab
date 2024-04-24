import numpy as np

def local_optimiser(hour : int, water_height : float, z: np.array, rho : float, stakeholder : int):
     x_i = np.arange(48)*0.99
     return x_i

class ADMM_optimiser_WDN:
    def __init__(self, conn1, conn2, N_iterations : int,  N_vary_rho: int, stakeholder: int):
        self.conn1 = conn1
        self.conn2 = conn2
        self.N_vary_rho = N_vary_rho
        self.stakeholder = stakeholder
        self.N_iterations = N_iterations
        self.N_c = 24
        self.N_s = 3
        self.N_q = 2
        
        self.rho = 2
        self.mu = 10
        self.tau = 2

        self.z=np.zeros(self.N_c*self.N_q) #ADMM


    def optimise(self, hour : int , water_height: float):
        self.lambda_i = np.zeros(self.N_c*self.N_q) #ADMM
        self.x_bar = np.zeros(self.N_c*self.N_q) #ADMM
        
        #Timeshift initial guess
        self.z = np.roll(self.z,1)
        self.z[-1] = self.z[-2]    


        #Solve problem
        for k in range(0,self.N_iterations):
            print("Iteration", k)
            try: 
                self.x_i = local_optimiser(hour, water_height, self.z, self.rho, self.stakeholder) #Local optimisation (equation a)
            except:
                self.x_i = 3/4*self.x_i + 1/4*self.z
                print("Local optimisation failed")

            ### BEGIN ADMM
            self.z_i = self.x_i + 1/self.rho*self.lambda_i
            #print(self.z_i)

            self.conn1.sendall(self.z_i.tobytes())
            self.conn2.sendall(self.z_i.tobytes())
            print("z_i")
            print(type(self.z_i))
            print(type(self.z_i[1]))      
            print(len(self.z_i))    
            print(len(self.z_i.tobytes()))

            self.z_2 = np.frombuffer(self.conn1.recv(384), dtype=self.z_i.dtype)
            #print(self.z_2)
            self.z_3 = np.frombuffer(self.conn2.recv(384), dtype=self.z_i.dtype)
            #print(self.z_3)
            


            self.z_tilde = self.z_i + self.z_2+ self.z_3
            self.lambda_i_tilde = self.lambda_i + self.rho*(self.z - self.z_tilde)
            self.z = self.z - 1/(self.N_s + 1)*(self.z - self.z_tilde)
            self.lambda_i = self.lambda_i -1/(self.N_s + 1)*(self.lambda_i - self.lambda_i_tilde) 
            ### END ADMM 

            
            ### BEGIN find rho
            if(k<=self.N_vary_rho):
                self.conn1.sendall(self.x_i.tobytes())
                self.conn2.sendall(self.x_i.tobytes())
                print("x_i")
                print(type(self.x_i)) 
                print(type(self.x_i[1])) 
                print(len(self.x_i))    
                print(len(self.x_i.tobytes()))
                    

                self.x_2 = np.frombuffer(self.conn1.recv(384), dtype= self.x_i.dtype)
                self.x_3 = np.frombuffer(self.conn2.recv(384), dtype= self.x_i.dtype)

                self.x_bar_old = self.x_bar
                self.x_bar = self.x_i + self.x_2 + self.x_3
                self.r_norm_squared =  np.linalg.norm(self.x_i - self.x_bar, 2)**2 + np.linalg.norm(self.x_2 - self.x_bar, 2)**2 + np.linalg.norm(self.x_3 - self.x_bar, 2)**2
                self.s_norm = self.N_s*self.rho**2*np.linalg.norm(self.x_bar - self.x_bar_old,2)

                if(np.sqrt(self.r_norm_squared)>self.mu*self.s_norm):
                    self.rho = self.rho * self.tau
                elif(self.s_norm > self.mu*np.sqrt(self.r_norm_squared)):
                    self.rho = self.rho / self.tau
                print(self.rho)
            ### End find rho
            
        return self.x_i[:2]       