from comUsed import cluXg
from comUsed.fileXg import *
from comUsed.cluXg import *
from comUsed.formatXg import *
import numpy as np
from collections import Counter, defaultdict
import networkx as nx


## ******************************************************  生成站点聚类  ******************************************************
def getStationClu(k=100):
    '''
    得到站点的聚类结果 [新的站点, 站点标签]
    :param stations: [sta1, sta2, sta3]
    :return: [[sta1, cluId1], [sta2, cluId2]]
    '''
    stations = json_load(r'D:\pycharmProject\logic\dataSet\staIdL.json')
    # 筛选路口
    # stations = list(filter(lambda x: x[2]>10000, stations))
    cluData_pre = np.array([x[0:2] for x in stations])
    # print(cluDate_pre)
    # this is cluster
    lables = hieCluster(cluData_pre, k, False)
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
    # json_dump(stationWithLable, r'D:\pycharmProject\logic\4.stationClu\hieClu.json')
    # # json_dump(dic_lable2station, r'D:\pycharmProject\busRoute_nanchang\data\tempData\lable2stations.json')
    # json_dump(dic_lable2station, r'D:\pycharmProject\logic\4.stationClu\lable2stations.json')
    json_dump(dic_station2lable, r'D:\pycharmProject\logic\4.stationClu\station2lables.json')
    return dic_lable2station, dic_station2lable, stationWithLable

## ******************************************************* 生成label2roads ****************************************************
def getLabel2roads(label2stations):
    dic_lable2Roads = defaultdict(list)
    # 原料:lable2stations
    # 由lable：staions 转换为 lable：Roads
    # stations ----> roads
    # 遍历 lable2stations lable stations
    # lable2stations = json_load(r'D:\pycharmProject\logic\4.stationClu\lable2stations.json')
    road_sta_end = json_load(r'D:\pycharmProject\logic\dataSet\road_sta_end.json')
    for lable, stations in label2stations.items():
        # if lable == "215":
        # 使用 stations 生成 Roads
        # 看哪些roads的两个站点都在该lable的stations中
        # DEBUG
        # if lable != "50":
        #     continue
        # print(stations)
        # DEBUG 结束
        stations = [int(x[2]) for x in stations]
        # if 2471 not in stations:
        #     break
        # print(lable, stations)
        # print(stations)
        for i, road in enumerate(road_sta_end):
            # if road[0]!=False and road[1]!=False:
            staId, endId = int(road[0][2]), int(road[1][2])
            if staId in stations and endId in stations:
                # print(staId, endId)
                road[2].insert(0, road[0])
                road[2].append(road[1])
                dic_lable2Roads[lable].append(road[2])

    json_dump(dic_lable2Roads, r'D:\pycharmProject\logic\4.站点聚类\lable2roads.json')
    return dic_lable2Roads



## ******************************************************* 生成关系图数据 *******************************************************
def getStationCluNodes(cluAns):
    # 聚类+计算聚类中心点
    # 1、聚类
    # cluXg.getStation_hieClu(k)
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
def getStationCluLink1(cluAns):
    # cluPoint = cluXg.getCluPoint(cluAns)
    # cluAns = list(cluPoint.keys())
    # 站点都在哪个簇？
    station2lables = json_load(r'/4.站点聚类\station2lables.json')
    # 线路都有哪些站点？
    nameL, pathL = getPath(r'D:\pycharmProject\logic\3.线路网络\route2station')
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

def getStationCluLink2(station2lables):
    # 簇之间连接的生成方式2, 试着用road_sta_end生成连接关系
    links = set()
    # 画图的关系
    road_sta_end = json_load(r'D:\pycharmProject\logic\dataSet\road_sta_end.json')
    road_sta_end = [[x[0][2], x[1][2]] for x in road_sta_end]
    # print('road_sta_end 长度:', len(road_sta_end))
    # 站点在哪个簇里？
    station2lables = json_load(r'/4.站点聚类\station2lables.json')
    # debug 传进来的station2lables和读取的station2lables是否一致---->一致
    # dic = {}
    # dic['station2lales'], dic['station2lables2'] = station2lables, station2lables2
    # json_dump(dic, 'station2lables.json')
    # debug 结束
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

def getNetWorkCluData(cluAns, station2labels):
    nodes = getStationCluNodes(cluAns)
    # links = getStationCluLink1(cluAns)
    links2 = getStationCluLink2(station2labels)
    netWorkData_antv = getNetData_antv(nodes, links2)
    return netWorkData_antv

# ********************************************** 计算pr ***************************************************
def getPr(edges, points):
    '''
    计算pr
    :param edges: [(point1, point2), (point1, point2)]
    :param points: [point1, point2, point3......]
    :return: pr值字典
    '''
    # print(edges, points)
    G = nx.Graph()
    G.add_edges_from(edges)
    for point in points:
        G.add_node(point)
    pr = nx.pagerank(G, alpha=0.85, personalization=None, max_iter=100,
                     tol=1.0e-6, nstart=None,
                     dangling=None)
    prL = list(pr.values())
    pr_max = max(prL)
    for key, value in pr.items():
        pr[key] = value/pr_max
    return pr

def raods2SpaceR(roads):
    '''
    将roads生成spaceR模型
    :return: spaceR模型
    '''
    print("计算roads2spaceR")
    # 给每一个边一个编号
    for i, road in enumerate(roads):
        road.append(i)
        roads.append(road)

    # 节点 起,终,id
    pointL = []
    for i, road in enumerate(roads):
        pointL.append((road[0][2], road[1][2], i))

    # 无向图 静态
    network2 = defaultdict(dict)
    # 复杂度可能比较高 O(n2)
    for road1 in roads:
        # 路1的开始站点、路1的结束站点、路1的编号
        road1_start, road1_end, road1_id = road1[0][2], road1[1][2], road1[-1]
        for road2 in roads:
            # 路2的开始站点、路2的结束、路2的编号
            road2_start, road2_end, road2_id = road2[0][2], road2[1][2], road2[-1]
            # 自己找自己 不行
            if road1 == road2:
                break
            # 真的找到了
            if road1_start==road2_start or road1_end==road2_end or road1_start==road2_end or road1_end==road2_start:
                network2[road1_id][road2_id] = 1
    print(network2)
    return network2


# 需要一个方法筛选space-R模型
def getMinSpaceR(roads=json_load(r'D:\pycharmProject\busRoute_nanchang\data\tempData\lable2roads.json')["10"]):
    point_R = json_load(r'/1.底层路网\point_R.json')
    mextrix_R = json_load(r'/1.底层路网\mextrix_R.json')
    # 得到roads的首尾站点
    staEnd = [[road[0][2], road[-1][2]] for road in roads]
    print(len(staEnd))
    # 首站点\尾站点
    # 筛选后的节点和边
    Point, Edge = [], defaultdict(dict)
    # point_R mextrix_R
    # 筛选出点
    for staId, endId in staEnd:
        for point in point_R:
            if staId==point[0] and endId==point[1]:
                Point.append(point)

    idL = [x[2] for x in Point]
    for id1 in idL:
        for id2 in idL:
            id1, id2 = str(id1), str(id2)
            try:
                if mextrix_R[id1][id2] == 1:
                    Edge[id1][id2] = 1
            except:
                continue

    Point = [str(x[2]) for x in Point]
    Edge2 = []
    for key, value in Edge.items():
        for key2, value2 in value.items():
            Edge2.append((key, key2))
    # pr = getPr(points=Point, edges=Edge2)

    return Point, Edge2



    # for road in roads:




if __name__ == '__main__':
    # 测试站点聚类---ok
    # label2stations, station2label, cluAns = getStationClu(k=400)
    # 测试antv关系图数据---ok
    # getStationCluNodes(cluAns)
    # rateData = getNetWorkCluData(cluAns)
    # print(label2stations, station2label, rateData)
    getLabel2roads(json_load(r'D:\pycharmProject\logic\4.站点聚类\lable2stations.json'))
    pass
