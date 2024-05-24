import numpy as np 

array = np.array([1,2,3])

print(array.shape[0])

scalar = 67.5

scalar_array = np.array([scalar])

print(type(scalar_array))
print(scalar_array.shape)
shape = scalar_array.shape[0]
print(shape)