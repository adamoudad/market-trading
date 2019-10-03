import numpy as np

def predict_trend(seed, model, iterations, standardization='local'):
    mean = seed.mean()
    standard_deviation = seed.std()
    generated_series = np.zeros((len(seed) + iterations, 1))
    if standardization == 'local':
        generated_series[:len(seed)] = np.reshape((seed - mean) / standard_deviation, (len(seed), 1))
    else:
        generated_series[:len(seed)] = np.reshape((seed - data.close.mean()) / data.close.std(), (len(seed), 1))

    for i in range(iterations):
        input_data = np.expand_dims(generated_series[i:len(seed) + i], axis=0)
        prediction = model.predict(input_data)
        generated_series[len(seed) + i] = prediction[0]

    # Inverse normalization
    if standardization == 'local':
        generated_series = (generated_series * standard_deviation) + mean
    else:
        raise NotImplemented()
        generated_series = (generated_series * data.close.std() + data.close.mean())
    return generated_series.squeeze()
