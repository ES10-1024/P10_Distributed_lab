from scipy.optimize import minimize
import numpy as np

# Objective function
def cost_function(x):
    return x[0]**2 + x[1]**2  # Example cost function

# Initial guess
x0 = [1, 1]

# Constraint matrix and vector
A = [[1, 2], [-3, 1], [1 , 2], [1, 4]] # Coefficient matrix for constraints
b1 = np. array([[4, 2, 4, 4]])  # Constraint vector
b = b1.squeeze()

print('A', np.shape(A))
print('b1', np.shape(b1))
print('b', np.shape(b))
print('x0', np.shape(x0))
print('Cost:', np.shape(cost_function(x0)))

# Bounds for variables
bounds = [(None, None), (None, None)]  # No bounds specified for this example

# Constraints dictionary
constraints = {'type': 'ineq', 'fun': lambda x: b - A @ x}

# Optimization
result = minimize(cost_function, x0, bounds=bounds, constraints=constraints)

print("Optimal solution:", result.x)
print("Optimal value:", result.fun)
