import scipy.io

def electricity_price_and_flow(time):
    """
    Extracts data from position x and 24 steps forward, 
    for the electricty and prediction consumption data.
    For the acutal consumption a entire is returned  

    Parameters:
    - time (int): The starting position/time .
    """
    #Loading in the actual consumption 
    dataTemp = scipy.io.loadmat('global_control_scipy/Data/average_scaled_consumption.mat')
    consumptionActual = dataTemp['average_scaled_consumption']
    #Loading the predicted consumption 
    dataTemp = scipy.io.loadmat('global_control_scipy/Data/average_scaled_prediction.mat')
    consumptionPred = dataTemp['average_scaled_prediction']
    #Loading in the electricty price 
    dataTemp= scipy.io.loadmat('global_control_scipy/Data/ElPrice.mat')
    ElPrice=dataTemp['ElPrice']
    #Returning the desired entires     
    return consumptionActual[time],  consumptionPred[time:time+24], ElPrice[time:time+24]
