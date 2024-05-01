from Optimise import performOptimisation
import numpy as np
#import numpy as np
#import scipy.io as sci


# hours = 48
# for time in range(1, hours+1):
#     h = np.random.randint(200, 300)
#     U_hat = performOptimisation(time, h)

time = 1
h = 300
U_hat = performOptimisation(time, h)
u = np.round(U_hat.x, 4)
print(U_hat)
print('Afrundet', u)
print('Sum', np.sum(u))

#print(U_hat.x)
