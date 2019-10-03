from keras.models import Sequential
from keras.layers import Dense, Conv1D, Dropout, Flatten

def simple_convnet(n_classes=1, filters=128, kernel_size=5, optimizer='adam'):
    model = Sequential()
    model.add(Conv1D(filters=128, kernel_size=3,
                   activation='relu',
                   input_shape=(LENGTH, 1)))
    # model.add(Dropout(0.5))
    model.add(Flatten())
    model.add(Dense(256, activation='relu'))
    model.add(Dense(1))
    
    model.compile(loss='mean_squared_error', optimizer=optimizer)



