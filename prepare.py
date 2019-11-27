import glob

import numpy as np
import pandas as pd

def prepare_data(data, time, length=100, sample_window_size=1, local_standardization=True):
    """
    Prepares data from a pandas Series to sample,label pairs fitting input shape of neural network
    
    It is recommended to use local standardization as it standardize independently samples
    sample_window_size can be used to draw randomly a number from the window of size sample_window_size. If 0, it is equivalent to taking the next value.
    """
    samples = [] # Samples (inputs to the neural net)
    labels = [] # Labels (true labels)
    timestamps = [] # timestamps of the (sample,label) pairs

    for index in range(len(data) - length - max(1,sample_window_size)):
        period_data = data.iloc[index : index + length]
        next_value = data.iloc[index + length + 1 + np.random.randint(sample_window_size)]
        if local_standardization:
            mean = period_data.mean()
            standard_deviation = period_data.std()
            period_data = (period_data - mean) / standard_deviation
            next_value = (next_value - mean) / standard_deviation
        samples.append(period_data)
        labels.append(next_value)
        timestamps.append(time[index : index + length + 1])
        
    # Global standardization (gives bad qualitative results)
    if not local_standardization:
        samples = (samples - data.mean()) / data.std()
        labels = (labels - data.mean()) / data.std()

    return samples, labels, timestamps

def prepare_max_return(data, time, length, position_max_length=100):
    """
    Prepare data for max return and position close timing prediction
    position_max_length contains the length of the window used to compute the max_return, as the openning of a position.
    """
    samples = [] # Samples (inputs to the neural net)
    labels = [] # Labels (true labels)
    timestamps = [] # timestamps of the (sample,label) pairs

    for index in range(len(data) - length - max(1,sample_window_size)):
        period_data = data.iloc[index : index + length]
        max_return_price, max_return_time = max_return(data.iloc[index + length : index + length ])

        # Standardize or normalize data
        mean = period_data.mean()
        standard_deviation = period_data.std()
        period_data = (period_data - mean) / standard_deviation
        max_return_price = (max_return - mean) / standard_deviation
        max_return_time /= length

        samples.append(period_data)
        labels.append([max_return_price, max_return_time])
        timestamps.append(time[index : index + length + 1])
        
    return samples, labels, timestamps
    
def max_return(window):
    '''
    Get max return price of a given window of historical prices, by looking at the first price of the window, and retrieving the best price (weather buy or sell), with its associated position in window.
    '''
    max_return_buy = window.max() - window[0]
    max_return_sell = window.min() - window[0]
    if max_return_buy > abs(max_return_sell):
        max_return = max_return_buy
        time = window.argmax()
    else:
        max_return = max_return_sell
        time = window.argmin()
    return max_return, time

from keras.utils imoport Sequence
class MaxReturnGenerator(Sequence):
    
