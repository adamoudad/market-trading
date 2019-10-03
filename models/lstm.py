from keras.models import Sequential
from keras.layers import Dense, Dropout, Activation
from keras.layers import LSTM

def two_layers_lstm(sequence_length=100, n_classes=1, embedding_size=128, optimizer='adam'):
    model = Sequential()
    model.add(LSTM(embedding_size,
                   return_sequences=True,
                   input_shape=(sequence_length, n_classes)))
    model.add(Dropout(0.2))
    model.add(LSTM(embedding_size,
                        return_sequences=False))
    model.add(Dropout(0.2))
    model.add(Dense(n_classes))
    # model.add(Activation('linear'))
    model.compile(loss='mean_squared_error', optimizer=optimizer)

    return model

