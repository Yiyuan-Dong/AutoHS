from keras.models import Sequential
from keras.layers import Dense, Embedding
from keras.layers import LSTM, Masking, Dropout
from keras.preprocessing.sequence import pad_sequences
from FSM_action import read_data_x, read_data_y
import json
import numpy as np
from sklearn.model_selection import train_test_split

# def read_data_x():
#     data_x = []
#     with open('data_x.txt', 'r') as file:
#         for line in file:
#             item = json.loads(line)
#             data_x.append(item)
#     return data_x


# def read_data_y():
#     data_y = []
#     with open('data_y.txt', 'r') as file:
#         for line in file:
#             item = json.loads(line)
#             data_y.append(item)
#     return data_y




x = read_data_x()
y = read_data_y()
y2 = []
i = 0
for a, b , c in y:
    xt = x[i]
    handnum = -1
    for card in xt:
        if card[3] == 1 and card[4] == 1:
            handnum = handnum + 1

    temp = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    if a == -1:
        y2.append(temp)
        continue
    if a > handnum:
        temp[a - handnum + 10] = 1
    else:    
        temp[a] = 1
    if b != 0:
        temp[b + 10] = 1
    if c != 0:
        temp[c + 17] = 1
    i += 1
    y2.append(temp)

# print("y:                 ", y)
# print("y2:                 ",y2)

x = pad_sequences(x, padding='post', value = 0)
y = np.array(y2)

X_train, X_test, y_train, y_test = train_test_split(x, y, test_size=0.33, random_state=42)

model = Sequential()
model.add(Masking(mask_value=0.0, input_shape=(None, 13)))
model.add(LSTM(60, activation='relu', input_shape=(None, 13)))
# model.add(Dropout(0.1))
model.add(Dense(26, activation = 'sigmoid'))
model.compile(optimizer='adam', loss='mse', metrics=['accuracy'])
model.fit(X_train,y_train, epochs=1500)
np.set_printoptions(threshold=np.inf)
# print("===============================================")
# print(X_test)
# print("===============================================")
# print(y_test)
# print("===============================================")
# print(model.predict(X_test))
# print("===============================================")

loss, accuracy = model.evaluate(X_test, y_test)
print("loss is :", loss)
print("accuracy is :", accuracy)
# # 将模型保存为文件
model.save('my_hunter_model.keras')
# print("X_test: ", X_test)
# print("y_test: ", y_test)
# print("y_predict: ",model.predict(X_test))