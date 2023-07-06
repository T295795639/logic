from temp import *

# 计算每条道路的长度
# road_sta_end []
# 计算道路长度

# 遍历每个cluId, road集合, 计算roads的平均长度

# ***************************************** 计算聚类簇里的道路平均长度 ************************************
cluId_roads = json_load(r'D:\pycharmProject\logic\roadLength\label2roads110.json')

cluId_aveLength = {}

for cluId, roads in cluId_roads.items():
    # road个数
    l = 0
    n = len(roads)
    for road in roads:
        l += getLength(road)
    l /= n
    cluId_aveLength[cluId] = l

json_dump(cluId_aveLength, 'cluId_length.json')

