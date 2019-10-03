import glob

import numpy as np
import pandas as pd

def load_csv_folder(path_list, separator=';', columns=['time', "open","high", "low", "close", "volume"]):
    dataframe_list = []
    for file_path in path_list:
        data = pd.read_csv(file_path, names=columns, sep=separator)
        dataframe_list.append(data)
        print('Appended', file_path, 'to dataset')
    return pd.concat(dataframe_list, axis=0, ignore_index=True)

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
