from temp import *
import pandas as pd
import os
import matplotlib.pyplot as plt
from sklearn.cluster import AgglomerativeClustering
import numpy as np
# python自带的迭代器模块
from itertools import cycle
from collections import Counter, defaultdict
from comUsed import formatXg



# input: stations  output: lables
# 层次聚类
def hieCluster(X, n_clusters_, plot):
    '''
    :param X: 需要聚类的点,放到一个array中
    :param n_clusters_: 需要得到的聚类个数
    :return: 聚类lable标签
    '''
    # 设置分层聚类函数
    linkages = ['ward', 'average', 'complete']
    ac = AgglomerativeClustering(linkage=linkages[2], n_clusters = n_clusters_)
    # 训练数据
    ac.fit(X)
    # 每个数据的分类
    lables = ac.labels_
    if plot == True:
        plt.figure(1)  # 绘图
        plt.clf()
        colors = cycle('bgrcmykbgrcmykbgrcmykbgrcmyk')
        for k, col in zip(range(n_clusters_), colors):
            # 根据lables中的值是否等于k,重新组成一个True、False的数组
            my_members = lables == k
            # X[my_members,0]取出my_members对应位置为True的值的横坐标
            plt.plot(X[my_members, 0],X[my_members, 1], col+'.')
        plt.title('Estimated number of clusters:%d' % n_clusters_)
        plt.show()
    else:
        pass
    return lables


## 通过聚类得到站点聚类数据
def getStationClu(stations=json_load('D:\pycharmProject\logic\dataSet\staIdL.json')):
    '''
    得到站点的聚类结果 [新的站点, 站点标签]
    :param stations: [sta1, sta2, sta3]
    :return: [[sta1, cluId1], [sta2, cluId2]]
    '''
    # 筛选路口
    # stations = list(filter(lambda x: x[2]>10000, stations))
    cluDate_pre = np.array([x[0:2] for x in stations])
    # print(cluDate_pre)
    lables = hieCluster(cluDate_pre, 100, True)
    counted = Counter(lables)
    lables_valid = []
    for lable, count in counted.items():
        # if count>=10:
            lables_valid.append(lable)
    # 存储stations在哪个聚类中 站点id:聚类lable 还是 聚类lable:站点id 选第二种
    dic_lable2station = defaultdict(list)
    dic_station2lable = {}
    stationWithLable = []
    for lable, station in zip(lables, list(stations)):
        station.append(int(lable))
        stationWithLable.append(station)
        if lable in lables_valid:
            dic_lable2station[int(lable)].append(station[0:-1])
            dic_station2lable[station[2]] = int(lable)
    # print(stationWithLable)
    json_dump(stationWithLable, 'hieClu.json')
    json_dump(dic_lable2station, r'D:\pycharmProject\busRoute_nanchang\data\tempData\lable2stations.json')
    json_dump(dic_lable2station, 'lable2stations.json')
    json_dump(dic_station2lable, 'station2lables.json')
    # "输入:" stations   "输出:" dic_lable2station
    return dic_lable2station


if __name__ == '__main__':
    getStationClu()