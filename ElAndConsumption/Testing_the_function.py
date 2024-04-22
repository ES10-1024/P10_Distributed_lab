import scipy.io
from ElAndConsumption import ElAndConsumption


print("hello world")
time=10; 
# Load the .mat file

consumptionActual, consumptionPred, ElPrice = ElAndConsumption(time)
print(consumptionActual)
print(consumptionPred)
print(ElPrice)
