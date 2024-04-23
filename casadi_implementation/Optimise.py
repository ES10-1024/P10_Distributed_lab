import casadi as ca
import numpy as np

from constants import c_general, c_tower
from cost_const import define_cost_func_and_constraints
from cost_const import Uc


def performOptimisation():

    h = 300
    V_0 = h/1000*c_tower['A_t']
    d = 0.01* np.ones((c_general['N_c'],1)) #Placeholder for en vektor af demand over prediction horizon
    J_e = np.ones((c_general['N_c'], 1)) #Endnu en placeholder


    #Define cost function and constraints
    J_k, A, b = define_cost_func_and_constraints(d, V_0, J_e)

    #Gotta turn the function into a casadi function, potherwise casadi will not work with me
    J_k_c = ca.Function('J_k_c', [Uc], [J_k])

    #Initialise optimisation problem
    opti = ca.Opti()
    #Define optimisation variable
    U_k = opti.variable(c_general["N_c"]*c_general['N_q'], 1)
    #Define optimisation problem
    opti.minimize(J_k_c(U_k))
    #Define constraints
    opti.subject_to(A @ U_k <= b)
    #Choose solver
    opti.solver('ipopt')
    #Solve
    sol = opti.solve()
    #Print solution
    u_hat = sol.value(U_k)
    print('I AM ALIVE!!!')
    print(u_hat)

    return u_hat

