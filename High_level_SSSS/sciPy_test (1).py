import numpy as np
from scipy.optimize import minimize
import time

# Define the Rosenbrock function
def rosen(x):
    return np.sum(100.0 * (x[1:] - x[:-1]**2)**2 + (1 - x[:-1])**2)

# Define inequality constraints
def constraint(x):
    return np.array([x[0] + x[1] - 2, x[0] - x[1]])

# Initial guess
x0 = np.array([1.3, 0.7, 0.8, 1.9, 1.2])

start_time = time.time()

# Minimize the Rosenbrock function subject to the inequality constraints using SQP method
res = minimize(rosen, x0, method='SLSQP', constraints={'type': 'ineq', 'fun': constraint})

print(time.time()-start_time)

print("Optimized parameters:", res.x)
print("Minimum value found:", res.fun)
