# 效果完全不行, 放在这里当失败案例

import pickle
import time

import numpy as np
from sklearn import svm
from tensorflow.keras.datasets import mnist
from tensorflow.keras.optimizers import Adam

if __name__ == "__main__":
    ((trainData, trainLabels), (testData, testLabels)) = mnist.load_data()
    trainData = trainData.reshape((trainData.shape[0], 28 * 28))

    testData = testData.reshape((testData.shape[0], 28 * 28))

    svc = svm.SVC(kernel='poly')
    svc.fit(trainData, trainLabels)

    result = svc.predict(testData)

    count = 0
    for i in range(len(result)):
        print(result[i], testLabels[i])
        if result[i] != testLabels[i]:
            count += 1

    print(count, len(testData))

    with open("SVC_poly", "wb") as f:
        pickle.dump(svc, f)
