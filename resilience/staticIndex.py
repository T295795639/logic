import os
import pandas as pd
from temp import *
from comUsed.formatXg import *
from comUsed.netXg import *

# 这是一个引入了路口的 baseRoad 拓扑模型
# 原料: road_sta_end.json
# 生成: [[起点\终点],[起点\终点]]

# 针对城市道路网络的抽象方法主要分为 Primal Approach 方法和 Dual Approach方法两类。Primal Approach法将交叉口视为节点，将道路视为边;而Dual Approach法
# 则将道路视为节点，将交叉口视为边。前者是对城市道路网最直观、最简单的映射，由该法获得的网络图可直接反映实际交通网络的连通性与可达性，各连接节点间的几何距离可简单映射到两节点之间的边上。
# Primal Approach法  将交叉口视作点,将道路视作边

# **************************************  通过road_sta_end.json生成[staId, endId]  ******************************************
roads = json_load(r'D:\pycharmProject\logic\dataSet\road_sta_end.json')

edges, nodes = [], []
netWork = {}

for road in roads:
    staId, endId = road[0][2], road[1][2]
    staLat, staLng, endLat, endLng = road[0][0], road[0][1], road[1][0], road[1][1]
    edges.append(Edge(staId, endId))
    # edges.append([staId, endId])
    idL = []
    if staId not in idL:
        nodes.append(Node(id=staId, x=staLat, y=staLng, degree=''))
        idL.append(staId)
    if endId not in idL:
        nodes.append(Node(id=endId, x=endLat, y=endLng, degree=''))
        idL.append(endId)
    edges.append(Edge(staId=staId, endId=endId))
# 生成 edges和nodes
netWork["nodes"], netWork["edges"] = nodes, edges
# json_dump(netData_antv, 'netData_antv.json')

# **************************************************  1、计算节点度  ****************************************************
def data2one(data):
    data = [int(x) for x in data]
    data_max = max(data)
    return [x/data_max for x in data]

# 获取节点度
nodaL = getNet_nodality(nodes=nodes, edges=edges)
indexL = data2one([x[1] for x in nodaL])
for node, index in zip(nodes, indexL):
    node.degree = index

# antv_G6
data_antvG6 = getNetData_antv(nodes, edges)
# json_dump(data_antvG6, r'../tempData/rateData.json')

# **************************************************  2、计算介数  *****************************************************
# 获取介数
a, b = getNet_betweeness(nodes, edges)
# print(beL)


# *********************************************** 3、计算网络平均效率(少车流数据) ***************************************************
# 网络效率
efficience = getNet_aveEffciency(nodes, edges)
# print(efficience)




