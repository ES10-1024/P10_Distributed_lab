import numpy as np
from Solve_each_ADMM import performOptimisation
from logging import logging
from SSSS02 import SSSS

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
        self.rho_last_solve = self.rho
        self.mu = 5       #Vary rho algorithm parameter
        self.tau = 1.5    #Vary rho algorithm parameter

        self.z=np.zeros((self.N_c*self.N_q,1)) #Initialization ADMM
        self.log = logging("ADMM"+str(stakeholder))

        self.smpc_summer = SSSS(self.conn1, self.conn1, stakeholder, self.log)

    def optimise(self, hour : int , water_height: float):
        self.lambda_i = np.zeros((self.N_c*self.N_q,1)) #ADMM Initialisation
        self.x_bar = np.zeros((self.N_c*self.N_q,1)) #ADMM Initialisation
        
        #Timeshift initial guess
        self.z = np.roll(self.z,1)
        self.z[-1] = self.z[-2]  

        self.rho = self.rho_last_solve

        self.log.log("simulated_hour", hour, 1)
        self.log.log("water_height", water_height,1)  

        #Solve problem
        for k in range(0,self.N_iterations):
            print("Iteration", k)
            self.log.log("k", k,1)
            #Solve local problem
            try: 
                self.x_i = performOptimisation(hour, water_height, self.stakeholder,self.rho,self.lambda_i,self.z)
                self.x_i= self.x_i.reshape(-1, 1)
            except:                                             #Have never seen this happen
                self.x_i = 3/4*self.x_i + 1/4*self.z    	    
                print("Local optimisation failed")
                self.log.log("optimisation failed", 1, 0)
            self.log.log("x_i", self.x_i, 5)

            ### BEGIN ADMM
            self.z_i = self.x_i + (1/self.rho)*self.lambda_i    #Stakeholders entry in calculation of z
            self.z = self.smpc_summer.sum(self.z_i) / self.N_s  #SMPC calculation of z
            self.log.log("z_i", self.z_i, 5)
            self.log.log("z", self.z, 5)
            
            self.lambda_i = self.lambda_i + self.rho*(self.x_i - self.z)   #Calculation of z 
            self.log.log("lambda_i", self.lambda_i, 5)       
            ### END ADMM 
            
            ### BEGIN find rho
            if(k<=self.N_vary_rho):
                self.x_bar_old = self.x_bar
                self.x_bar = 1/self.N_s*self.smpc_summer.sum(self.x_i)
                
                self.r_i = np.linalg.norm(self.x_i - self.x_bar, 2)**2
                
                self.r_norm_squared =  self.smpc_summer.sum(self.r_i)
                self.s_norm = self.N_s*self.rho**2*np.linalg.norm(self.x_bar - self.x_bar_old,2)
                self.log.log("r_norm_squred", self.r_norm_squared, 3)
                self.log.log("s_norm", self.s_norm, 3)

                if(np.sqrt(self.r_norm_squared)>self.mu*self.s_norm):
                    self.rho = self.rho * self.tau
                elif(self.s_norm > self.mu*np.sqrt(self.r_norm_squared)):
                    self.rho = self.rho / self.tau
                print("rho: ", self.rho)
                self.log.log("rho", self.rho, 2)
            ### End find rho

            #Increase rho with factor 500 at iteration 30
            if(k==30):
                self.rho_last_solve = self.rho
                self.rho = self.rho*500
                 
        return self.x_i       #return solution
    


class consumer_valve_controller:

    def __init__(self, flow_register, valve: int):
        self.reference = 0
        self.flow_reg = flow_register
        self.kp = 30    
        self.ki = 20
        self.saturation_upper = 100
        self.saturation_lower = 0 
        self.sampletime = 1
        self.integral = 0  
        self.log = logging("consumption_valve"+str(valve))

    def consumption_PI(self, ref, flow):

        self.log.log("flow", flow, 5)

        self.reference = ref
        self.log.log("reference", ref, 5)
        
        error = self.reference - flow
        self.integral = self.integral + error*self.sampletime

        #Prevention of integral windup
        if(self.integral*self.ki > self.saturation_upper):
            self.integral = self.saturation_upper/self.ki
            print("Integral saturated")

        if(self.integral*self.ki < self.saturation_lower):
            self.integral = self.saturation_lower/self.ki

        #
        PI_output = self.kp*error + self.ki*self.integral

        #Ensure that the saturation limits aren't breached
        if(PI_output>self.saturation_upper):
            opening_degree = self.saturation_upper
            print("Controller saturated, upper limit")
        elif(PI_output < self.saturation_lower):
            opening_degree = self.saturation_lower
            if(ref>0):
                print("Controller saturated, lower limit")
        else:
            opening_degree = PI_output
        
        self.log.log("opening_degree", opening_degree, 1)
        return opening_degree