import pandas as pd
from temp import *
from collections import defaultdict
# *************************************  lable2Roads生成  *************************************

# 原料 lable2stations和drawRoad.json
# 需要生成 lable2Roads {"1": [point1, point2, point3]}
lable2stations = json_load(r'D:\pycharmProject\logic\4.stationClu\lable2stations.json')
roadL = json_load(r'D:\pycharmProject\logic\dataSet\drawRoad.json')
road_sta_end = json_load(r'D:\pycharmProject\logic\dataSet\road_sta_end.json')
print(len(roadL), len(road_sta_end))


dic_lable2Roads = defaultdict(list)
# 原料:lable2stations
# 由lable:staions 转换为 lable:Roads
# stations ----> roads
# 遍历 lable2stations lable stations
for lable, stations in lable2stations.items():
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
            if staId in stations or endId in stations:
                print(road[0], road[1])
                road[2].insert(0, road[0])
                road[2].append(road[1])
                dic_lable2Roads[lable].append(road[2])

# print(dic_lable2Roads)
# print(list(dic_lable2Roads.keys()), len(lable2stations.keys()))

# 字典key排序
dic_lable2Roads2 = {}
cluIdL = [int(x) for x in list(dic_lable2Roads.keys())]
cluIdL = sorted(cluIdL)
for cluId in cluIdL:
    cluId = str(cluId)
    dic_lable2Roads2[cluId] = dic_lable2Roads[cluId]

json_dump(dic_lable2Roads2, r'lable2roads.json')
json_dump(dic_lable2Roads2, r'D:\pycharmProject\busRoute_nanchang\data\tempData\lable2roads.json')





