from tensorflow import keras
import numpy as np
from keras.preprocessing.sequence import pad_sequences
# 加载模型
model = keras.models.load_model('my_hunter_model.keras')


def predict_action(x):
    # 使用模型进行预测
    tmp = []
    tmp.append(x)
    tmp = np.array(tmp)
    res = model.predict(tmp)
    print("in origin x ==============", x)
    print("in predict ==============", res)
    result = []
    res[0][0] = int(round(res[0][0]))
    res[0][1] = int(round(res[0][1]))
    res[0][2] = int(round(res[0][2]))
    result.append(int(res[0][0]))
    result.append(int(res[0][1]))
    result.append(int(res[0][2]))
    return result