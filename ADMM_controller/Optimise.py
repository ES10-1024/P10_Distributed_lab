import casadi as ca
import numpy as np

from constants import c_general, c_tower
from cost_const import define_cost_func_and_constraints, Uc
from Get_Electricity_Flow import electricity_price_and_flow


def performOptimisation(time, h):

    consumption, d, J_e = electricity_price_and_flow(time)
    J_e = np.round(J_e, 4)
    d = np.round(d, 4)

    V_0 = np.round(h/1000*c_tower['A_t'], 4)


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
    u_hat = np.round(u_hat, 4)
    #print('Predicted Demand:', d)
    #print('Electricity prices: ', J_e)
    print('U: ', u_hat)
    #print('Initial Volume: ', V_0)

    return u_hat

