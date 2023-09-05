# -*- coding: utf-8 -*-
# sigmoid 函数
#####
# g(z) = 1/1+e**-z
#####
import numpy as np
import pandas as pd
from matplotlib import pyplot as plt


def sigmoid(z):
    return 1 / (1 + np.exp(-z))


# 绘制sigmoid 的图像
nums = np.arange(-10, 10, step=1)
fig, ax = plt.subplots(figsize=(12, 4))
ax.plot(nums, sigmoid(nums), 'r')
plt.show()


### 阈值 g: R ->[0,1]
### g(0) =0.5
### g(-∞) =0
### g(+∞) =1


#########################
# 预测函数 # hθ(x)
def model(X, theta):
    return sigmoid(np.dot(X, theta.T))


pdData = pd.read_csv('test.csv')
pdData.insert(0, 'Ones', 1)
orig_data = pdData
cols = orig_data.shape[1]
X = orig_data.iloc[:, 0:cols - 1]
y = orig_data.iloc[:, cols - 1:cols]

theta = np.zeros([1, 3])


# print(X[:5])
# print(y[:5])
# print(theta)
# print(X.shape, y.shape, theta.shape)

### 损失函数
def cost(X, y, theta):
    # 1. 将 对数似然函数去 负号
    # 2. 求平均损失
    left = np.multiply(-y, np.log(model(X, theta)))
    right = np.multiply(1 - y, np.log(1 - model(X, theta)))
    # 除以样本数量
    return np.sum(left - right) / (len(X))


print(cost(X, y, theta))


### 计算梯度  --> 求偏导
def gradient(X, y, theta):
    grad = np.zeros(theta.shape)
    error = (model(X, theta) - y).ravel()
    for j in range(len(theta.ravel())):
        # j 列
        term = np.multiply(error, X.iloc[:, j])
        grad[0, j] = np.sum(term) / len(X)

    return grad


### Gradient descent
# 比较 3 种不同的梯度下降方法
STOP_ITER = 0  # 迭代次数
STOP_COST = 1  # 根据损失值的变化
STOP_GRAD = 2  # 根据梯度


def stopCriterion(type, value, threshold):
    # 设定 3种不同的停止策略
    if type == STOP_ITER:
        return value > threshold
    elif type == STOP_COST:
        return abs(value[-1] - value[-2]) < threshold
    elif type == STOP_GRAD:
        return np.linalg.norm(value) > threshold


import numpy.random


# 数据 洗牌
def shuffleData(data):
    np.random.shuffle(data)
    cols = data.shape[1]
    X = data.iloc[:, 0:cols - 1]
    y = data.iloc[:, cols - 1]
    return X, y


import time


def descent(data, theta, batchSize, stopType, thresh, alpha):
    """
    :param data:  # 数据
    :param theta:  # 参数
    :param batchSize: # 1随机梯度下降, 2总的样本数下降 , 1-总体之间,minibatch
    :param stopType: # 停止策略
    :param thresh: # 停止策略对应的阈值
    :param alpha: # 学习率
    :return:
    """
    # 梯度下降 求解
    init_time = time.time()
    i = 0  # 迭代次数
    k = 0  # batch
    X, y = shuffleData(data)  # 打乱数据
    grad = np.zeros(theta.shape)  # 计算梯度
    costs = [cost(X, y, theta)]  # 计算损失值

    while True:
        # 梯度
        grad = gradient(X.iloc[k:k + batchSize], y.iloc[k:k + batchSize], theta)

        k += batchSize  # 取batch 数量个数数据
        if k >= i:
            x = 0
            X, y = shuffleData(data)  # 重新打乱数据

        theta = theta - alpha * grad  # 参数更新
        costs.append(cost(X, y, theta))  # 计算 新的损失
        i += 1

        if stopType == STOP_ITER:
            value = i
        elif stopType == STOP_COST:
            value = costs
        elif stopType == STOP_GRAD:
            value = grad

        if stopCriterion(stopType, value, tresh):
            break
