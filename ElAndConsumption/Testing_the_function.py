import scipy.io
#loading in the function for the to get the electricty price and consumption
from ElAndConsumption import ElAndConsumption
print("hello world")


#Setting the time it is desired to get the electricty price, and consumption from
time=10; 
#Getting the consumption and electricty price 
consumptionActual, consumptionPred, ElPrice = ElAndConsumption(time)

#Printing the results out 
print(consumptionActual)
print(consumptionPred)
print(ElPrice)
