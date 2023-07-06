from temp import *
import pandas as pd
import os
import matplotlib.pyplot as plt
from sklearn.cluster import AgglomerativeClustering
import numpy as np
from itertools import cycle  # python自带的迭代器模块
from collections import Counter

# 获得route2station 线路:station
p = r'E:\buStation_nanChang_netWork\output\4_getRoadGps\sum'
tof = r'D:\pycharmProject\logic\3.nextRoadNet\route2station\\'
fNameL, pathL = getPath(p)
# ************************************************穿起来 每条线路的GPS穿过哪些站点 存起来************************************
def chuanqilai():
    i = 0
    stations = json_load('D:\pycharmProject\logic\dataSet\staIdL.json')
    for name, path in zip(fNameL, pathL):
        routeName = name.replace('.csv', '')
        if routeName.find('erro')!=-1:
            continue
        print(routeName)
        i = i + 1
        gpsL = pd.read_csv(path).loc[:, ['lng', 'lat']].values.tolist()
        L = []
        for gps in gpsL:
            ans = searchSta(gps, stations)
            if ans!=False:
                L.append(ans)

        json_dump(L, tof+routeName+'.json')

        # if i > 20:
        #     break

# *******************************************************用gps匹配站点后 需要去重**************************************************
def dropDup(list):
    new_list = []
    for l in list:
        if l not in new_list:
            new_list.append(l)
    return new_list

def dropDupInF():
    fNameL, pathL = getPath(r'D:\pycharmProject\logic\3.nextRoadNet\route2station')
    for fName, path in zip(fNameL, pathL):
        stations = dropDup(json_load(path))
        json_dump(stations, path)


# chuanqilai()
dropDupInF()
# getStationClu()
