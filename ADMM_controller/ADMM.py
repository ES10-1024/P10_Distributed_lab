#Trying to implement consensus ADMM 
#Solve problem
import numpy as np

from Solve_each_ADMM import performOptimisation


#performOptimisation(time, WaterHeightmm, stakeholderID,rho,Lambda,z) 
#Defining a few parameter needs for consensus ADMM: 
lambda_1=np.zeros((48,1))
lambda_2=np.zeros((48,1))
lambda_3=np.zeros((48,1)) 

x_1=np.zeros((48,1))
x_2=np.zeros((48,1))
x_3=np.zeros((48,1))

z_1=np.zeros((48,1))
z_2=np.zeros((48,1))
z_3=np.zeros((48,1))

x_bar=np.zeros((48,1))

z=np.zeros((48,1))
#Defining a few constant values 
rho=4 
N_iterations=125 

N_s=3 
time=1
WaterHeightmm=300 

mu=10
tau=2
N_vary_rho=10


for k in range(0,N_iterations):
#for k in range(0,1):
    print("Iteration", k)
    #Solve local problem
    #Solving the optimization problem for the two pumps and the water tower 
    x_1=performOptimisation(time, WaterHeightmm, 1,rho,lambda_1,z)
    x_2=performOptimisation(time, WaterHeightmm, 2,rho,lambda_2,z)
    x_3=performOptimisation(time, WaterHeightmm, 3,rho,lambda_3,z)
    #Needs to reshape the solution 
    x_1 = x_1.reshape(-1, 1)
    x_2 = x_2.reshape(-1, 1)
    x_3 = x_3.reshape(-1, 1)    
    
    ### BEGIN ADMM
    z_1 = x_1 + (1 / rho) * lambda_1
    z_2 = x_2 + (1 / rho) * lambda_2
    z_3 = x_3 + (1 / rho) * lambda_3

    z_tilde = 1/(N_s)*(z_1 + z_2 + z_3)
    z = z - 1/(N_s + 1)*(z - z_tilde)

    
    lambda_1_tilde = lambda_1 + rho*(x_1 - z)
    lambda_2_tilde = lambda_2 + rho*(x_2 - z)
    lambda_3_tilde = lambda_3 + rho*(x_3 - z)
               
    lambda_1 = lambda_1 -1/(N_s + 1)*(lambda_1 - lambda_1_tilde) 
    lambda_2 = lambda_2 -1/(N_s + 1)*(lambda_2 - lambda_2_tilde)
    lambda_3 = lambda_3 -1/(N_s + 1)*(lambda_3 - lambda_3_tilde) 
    
    if(k<=N_vary_rho):

      x_bar_old = x_bar
      x_bar = 1/N_s*(x_1 + x_2 + x_3)
      r_norm_squared =  np.linalg.norm(x_1 - x_bar, 2)**2 + np.linalg.norm(x_2 - x_bar, 2)**2 + np.linalg.norm(x_3 - x_bar, 2)**2
      s_norm = N_s*rho**2*np.linalg.norm(x_bar - x_bar_old,2)

      if(np.sqrt(r_norm_squared)>mu*s_norm):
        rho = rho * tau
      elif(s_norm > mu*np.sqrt(r_norm_squared)):
        rho = rho / tau
      print(rho)


  ### END ADMM 
print(x_1)
print(x_2)
print(x_3)