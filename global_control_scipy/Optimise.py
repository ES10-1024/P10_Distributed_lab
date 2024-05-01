import casadi as ca
import numpy as np
from scipy.optimize import minimize

from constants import c_general, c_tower
from cost_const import define_cost_func_and_constraints
from Get_Electricity_Flow import electricity_price_and_flow


def performOptimisation(time, h):

    consumption, d, J_e = electricity_price_and_flow(time)
    J_e = np.round(J_e, 4)
    d = np.round(d, 4)

    V_0 = np.round(h/1000*c_tower['A_t'], 4)


    #Define cost function and constraints
    J_k, A, b = define_cost_func_and_constraints(d, V_0, J_e)

    def cost(Uc):
        return J_k(Uc)[0,0]
    
    # Inequality constraint function using lambda
    # AU = lambda Uc: A @ Uc
    # def constr(Uc):
    #     FUCK = - AU(Uc) + b
    #     print(np.shape(FUCK))
    #     return FUCK

    Uc = np.ones((c_general['N_c']*c_general['N_q'],))



    # print('A', np.shape(A))
    # print('b', np.shape(b))
    # print('U', np.shape(Uc))
    #print('AU', np.shape(AU(Uc)))

    

    # Define the constraint
    const = {'type': 'ineq', 'fun': lambda Uc: b - A @ Uc}


    # Optimization
    result = minimize(cost, Uc, constraints = const, method = 'trust-constr', options={'disp': True})
    return result


