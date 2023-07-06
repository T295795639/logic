import pandas as pd
from temp import *
from collections import defaultdict
from comUsed import cluXg, paintXg, formatXg

def getStationCluNodes():
    # 聚类+计算聚类中心点
    # 1、聚类
    cluXg.getStation_hieClu(100)
    # json_dump(dic, r'hieClu.json')
    # 2、聚类中心计算
    cluPoint = cluXg.getCluPoint()
    # 添加到nodes中
    nodes = []
    for cluId, cenPoint in cluPoint.items():
        nodes.append({
            "id": cluId,
            "x": cenPoint[0],
            "y": cenPoint[1]
        })
    return nodes
# json_dump(cluPoint, 'cluPointL.json')
# *******************************************  簇和簇之间的连接关系 **************************************
# 生成聚类中心的力导图的数据
# echarts数据集示例

# cluPointL = json_load(r'D:\pycharmProject\busRoute_nanchang\data\tempData\cluPointL.json')
# 簇之间连接的生成方式1
def getStationCluLink1():
    cluPoint = cluXg.getCluPoint()
    cluAns = list(cluPoint.keys())
    # 站点都在哪个簇？
    station2lables = json_load(r'D:\pycharmProject\logic\4.stationClu\station2lables.json')
    # 线路都有哪些站点？
    nameL, pathL = getPath(r'D:\pycharmProject\logic\3.lineRoadNet\route2station')
    links = set()

    for path in pathL:
        staList = [x[2] for x in json_load(path)]
        for i, sta in enumerate(staList):
            if i == 0:
                continue
            preSta, nextSta = str(staList[i - 1]), str(staList[i])
            # 站点不一致
            if preSta != nextSta:
                # 站点所在的簇存在吗
                if (preSta in list(station2lables.keys())) and (nextSta in list(station2lables.keys())):
                    # 站点在两个不同的簇里
                    if station2lables[preSta] != station2lables[nextSta]:
                        links.add((station2lables[preSta], station2lables[nextSta]))
    return list(links)


def getStationCluLink2():
    # 簇之间连接的生成方式2, 试着用road_sta_end生成连接关系
    links = set()
    # 画图的关系
    road_sta_end = json_load(r'D:\pycharmProject\logic\dataSet\road_sta_end.json')
    road_sta_end = [[x[0][2], x[1][2]] for x in road_sta_end]
    print('road_sta_end 长度:', len(road_sta_end))
    # 站点在哪个簇里？
    station2lables = json_load(r'D:\pycharmProject\logic\4.stationClu\station2lables.json')
    set_1 = set()
    for rate in road_sta_end:
        preSta, nextSta = str(rate[0]), str(rate[1])
        # 站点所在的簇存在吗
        if preSta not in list(station2lables.keys()): set_1.add(preSta)
        if nextSta not in list(station2lables.keys()): set_1.add(nextSta)
        if (preSta in list(station2lables.keys())) and (nextSta in list(station2lables.keys())):
            # 站点在两个不同的簇里
            if station2lables[preSta] != station2lables[nextSta]:
                links.add((station2lables[preSta], station2lables[nextSta]))
    return list(links)


if __name__ == '__main__':
    nodes = getStationCluNodes()
    links = getStationCluLink1()
    links2 = getStationCluLink2()
    # print("nodes:", nodes, '\n', "edges:", links)
    # print("nodes长度:", len(nodes))
    # print("links长度:", len(links))
    # print("links2长度:", len(links2))
    dic = formatXg.getNetData_antv(nodes, links2)
    # 是否保留边
    # del dic['edges']
    nodeL = list(set([x['id'] for x in nodes]))
    print(nodeL)
    json_dump(dic, r'D:\pycharmProject\busRoute_nanchang\static\json\rateData.json')





