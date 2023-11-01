from keras.models import Sequential
from keras.layers import Dense, Embedding
from keras.layers import LSTM, Masking, Dropout
from keras.preprocessing.sequence import pad_sequences
from FSM_action import read_data_x, read_data_y
import numpy as np
from sklearn.model_selection import train_test_split

x = read_data_x()
y = read_data_y()
# print(len(x))
# print(len(x[0]))
# x = [[[1, 2, 0, 0, 0, 8 , 1, 5, 2, 32, 1, 2, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]], [[1, 2, 0, 0, 0, 8 , 1, 5, 2, 32, 1, 2, 0], [1, 2, 0, 0, 0, 8 , 1, 5, 2, 32, 1, 2, 0]]]
# x = [[[1, 2, 0, 0, 0, 8 , 1, 5, 2, 32, 1, 2, 0]], [[1, 2, 0, 0, 0, 8 , 1, 5, 2, 32, 1, 2, 0], [1, 2, 0, 0, 0, 8 , 1, 5, 2, 32, 1, 2, 0]]]
# y = [[1, 0, 0], [2, 0, 8]]
x = pad_sequences(x, padding='post', value = 0)
y = np.array(y)

X_train, X_test, y_train, y_test = train_test_split(x, y, test_size=0.33, random_state=42)

model = Sequential()
model.add(Masking(mask_value=0.0, input_shape=(None, 13)))
model.add(LSTM(50, activation='relu', input_shape=(None, 13)))
# model.add(Dropout(0.1))
model.add(Dense(3, activation = 'linear'))
model.compile(optimizer='adam', loss='mse', metrics=['accuracy'])
model.fit(X_train,y_train, epochs=1200)
# print(x[0])
# print(model.predict(x))

loss, accuracy = model.evaluate(X_test, y_test)
print("loss is :", loss)
print("accuracy is :", accuracy)
# 将模型保存为文件
model.save('my_old_hunter_model.keras')