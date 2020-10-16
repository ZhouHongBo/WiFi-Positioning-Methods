"""
对每周的数据分别使用所有的定位算法，计算75%定位误差并生成定位误差对比图
"""
import numpy as np
import matplotlib.pyplot as plt

from file import *
from estimate import *
from func import *

# 所有定位算法通用的变量
weekAmount = 3

# 保存75%定位误差的变量
metricRand = [0] * weekAmount
metricNn = [0] * weekAmount
metricKnn = [0] * weekAmount
metricWknn = [0] * weekAmount
metricStg = [0] * weekAmount
metricProb = [0] * weekAmount
metricGk = [0] * weekAmount

week = 1
while week <= weekAmount:
    # 加载本周数据(这里使用了一半的数据量，即晚上采集的数据)
    dataTrain = loadContentSpecific("db", 1, [2, 4], week)
    dataTest = loadContentSpecific("db", 2, [2, 4, 6, 8], week)

    # 处理无信号AP的数据
    dataTrain.rss[dataTrain.rss == 100] = -105
    dataTest.rss[dataTest.rss == 100] = -105

    # Rand方法
    predictionRandom = randomEstimation(dataTrain.rss, dataTest.rss, dataTrain.coords)
    errorRandom = customError(predictionRandom, dataTest.coords)
    metricRand[week-1] = np.percentile(errorRandom, 75)  # 计算75%误差, 与MATLAB中的prctile函数有细微差异

    # NN方法
    knnValue = 1
    predictionNn = kNNEstimation(dataTrain.rss, dataTest.rss, dataTrain.coords, knnValue)
    errorNn = customError(predictionNn, dataTest.coords)
    metricNn[week-1] = np.percentile(errorNn, 75)

    # KNN方法
    knnValue = 9
    predictionKnn = kNNEstimation(dataTrain.rss, dataTest.rss, dataTrain.coords, knnValue)
    errorKnn = customError(predictionKnn, dataTest.coords)
    metricKnn[week-1] = np.percentile(errorKnn, 75)

    # WKNN方法
    knnValue = 9
    predictionWknn = wknnEstimation(dataTrain.rss, dataTest.rss, dataTrain.coords, knnValue)
    errorWknn = customError(predictionWknn, dataTest.coords)
    metricWknn[week-1] = np.percentile(errorWknn, 75)

    # Stg方法
    stgValue = 3 # 信号最强AP的个数
    kValue = 5 # 选取的邻居节点个数
    predictionStg = stgKNNEstimation(dataTrain.rss, dataTest.rss, dataTrain.coords, stgValue, kValue)
    errorStg = customError(predictionStg, dataTest.coords)
    metricStg[week-1] = np.percentile(errorStg, 75)

    # Prob方法
    kValue = 1    # 选取概率最大节点的个数
    predictionProb = probEstimation(dataTrain.rss, dataTest.rss, dataTrain.coords, kValue, dataTrain.ids // 100)
    errorProb = customError(predictionProb, dataTest.coords)
    metricProb[week-1] = np.percentile(errorProb, 75)

    # Gk方法
    std_dB = 4 # 此参数影响不大
    kValue = 12
    predictionGk = gaussiankernelEstimation(dataTrain.rss, dataTest.rss, dataTrain.coords, std_dB, kValue)
    errorGk = customError(predictionGk, dataTest.coords)
    metricGk[week-1] = np.percentile(errorGk, 75)

    print(week)
    week += 1

# 绘制定位误差对比图
x = [i+1 for i in range(weekAmount)]
plt.plot(x, metricRand, label="Rand")
plt.plot(x, metricNn, label="NN")
plt.plot(x, metricKnn, label="KNN")
plt.plot(x, metricWknn, label="WKNN")
plt.plot(x, metricStg, label="Stg")
plt.plot(x, metricProb, label="Prob")
plt.plot(x, metricGk, label="Gk")

plt.xlabel("week number", {"size": 15})
plt.ylabel("75 percentile error (m)", {"size": 15})

plt.xlim((1, weekAmount))
plt.ylim((0, 6))

plt.xticks(np.arange(1, weekAmount+1, 1))
plt.yticks(np.arange(0, 7, 1))

plt.legend(loc="upper right")
plt.grid()
plt.show()