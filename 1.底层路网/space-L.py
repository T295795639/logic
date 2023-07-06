from temp import *
from collections import defaultdict


# 1.*******************************************************  构建space-L模型(引入一部分道路路口) ****************************************************

# input: drawRoad.json staIdL.json  即路段和站点
# output: 底层网络 network1[station1_Id][station2_Id] = 0or1  pointL = [staId1, staId2......]
# space-P 点:站点 边:公交路段

# 计算road_sta_end 看一条边连接了哪两个站点
drawRoad = json_load(r'D:\pycharmProject\logic\dataSet\drawRoad.json')
stations = json_load(r'D:\pycharmProject\logic\dataSet\staIdL.json')

point = {
    "lng": 115.92608101584523,
    "lat": 28.66675493217606
}
pointA = {
    "lng": 115.92568237442924,
    "lat": 28.66729549647131
}
pointB = {
    "lng": 115.92647059722327,
    "lat": 28.667263698652405
}
# subLng = point['lng'] - pointA['lng']
# subLat = pointA['lat'] - point['lat']


def searchSta(point, stations):
    subLng = 0.0005405642952496237
    subLat = 0.0003986414159840024
    for station in stations:
        if abs(station[0]-point[0]) > subLng or abs(station[1]-point[1]) > subLat:
            continue
        if getdis_geo(point, station) < 50:
            return station
    return False

def genRoadStaEnd():
    '''
    将单元边转换为[sta1, sta2]的形式
    :return: 转换后的边集合
    '''
    searchAns = []
    searchErro = []
    for road in drawRoad:
        startP, endP = road[0], road[-1]
        # 搜索到两个站点
        A, B = searchSta(startP, stations), searchSta(endP, stations)
        searchAns.append([A, B, road])
        # if (A!=False and B!=False):
        #     searchAns.append([A, B])
        # else:
        #     searchErro.append([A, B, road])
    road_sta_end = searchAns
    json_dump(road_sta_end, r'D:\pycharmProject\logic\dataSet\road_sta_end.json')
    json_dump(searchErro, r'D:\pycharmProject\logic\dataSet\road_sta_end_erro.json')

# ****************************************************  给每条边匹配两侧端点  ***************************************************************
# 1143
# 1081
# 101314
# 101311
genRoadStaEnd()
road_sta_end = json_load(r'D:\pycharmProject\logic\dataSet\road_sta_end.json')
pointL = []
network1 = defaultdict(dict)

for i, road in enumerate(road_sta_end):
    # 遍历单位为一条边
    x, y = road[0], road[1]
    try:
       (x[2], y[2])
    except:
        print(x, y)
        break
    network1[x[2]][y[2]] = 1
    pointL.append(x[2])
    pointL.append(y[2])

pointL = list(set(pointL))
ans1, ans2 = pointL, network1

# *********************************************  最终结果:network1和pointL 即邻接矩阵和点集  **************************************
# print(subLat, subLng)