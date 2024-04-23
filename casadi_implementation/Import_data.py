import scipy as sci

#Import electricity prices
electricity_prices_file = sci.loadmat('casadi_implementation\Data\ElPrice.mat')
electricity_prices = electricity_prices_file['A']

#Import predicted demand
predicted_demand_file =sci.loadmat('casadi_implementation\Data\prediction_scaled2.mat')
predicted_demand = predicted_demand_file['scaled_prediction']

#Import actual demand (I think?)
consumption_file =sci.loadmat('casadi_implementation\Data\consumption_scaled2.mat')
consumption = consumption_file['scaled_consumption']