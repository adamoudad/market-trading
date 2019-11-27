import numpy as np

def predict_max_return(data, model):
    mean = data.mean()
    standard_deviation = data.std()
    input_data = np.reshape((data - mean) / standard_deviation, (len(data), 1))
    input_data = np.expand_dims(input_data, axis=0)
    max_return_price, max_return_time = model.predict(input_data)[0]

    # Inverse normalization
    max_return_price = (max_return_price * standard_deviation)
    max_return_time *= len(data)

    return max_return_price, max_return_time
