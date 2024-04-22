import scipy.io

def ElAndConsumption(time):
    """
    Extracts data from position x and 24 steps forward from the given vector.

    Parameters:
    - time (int): The starting position.

    Returns:
    - data_subset (numpy array): The subset of data extracted.
    """
    dataTemp = scipy.io.loadmat('Data/average_scaled_consumption.mat')
    consumptionActual = dataTemp['average_scaled_consumption']

    dataTemp = scipy.io.loadmat('Data/average_scaled_prediction.mat')
    consumptionPred = dataTemp['average_scaled_prediction']

    dataTemp= scipy.io.loadmat('Data/ElPrice.mat')
    ElPrice=dataTemp['ElPrice']

    # Access the vector (assuming its name is 'vector')
    
    return consumptionActual[time],  consumptionPred[time:time+24], ElPrice[time:time+24]
