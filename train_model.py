# from keras.models import Sequential
# from keras.layers import Dense, Embedding
# from keras.layers import LSTM
from FSM_action import read_data_x, read_data_y
import numpy as np

x = read_data_x()
y = read_data_y()
print(len(x))
print(len(x[0]))
# print(y)
# x = np.array(x)
y = np.array(y)
# print(y)
# model = Sequential()
# model.add(LSTM(50, activation='relu', input_shape=(None, 13)))
# model.add(Dense(3, activation = 'sigmoid'))
# model.compile(optimizer='adam', loss='mse')
# model.fit(x,y, epochs=200)
# print(model.predict(x[0]))
