import random

from temp import *
from collections import defaultdict


# 2.******************************************************构建space-R模型*********************************************************
# pointL: [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]  Mextrix: {1: {0: 1}, 2: {1: 1}, 3: {2: 1}, 4: {3: 1}, 5: {4: 1}, 6: {3: 1, 4: 1}}
# 点:公交路段 边:路段之间是否有连接

road_sta_end = json_load(r'D:\pycharmProject\logic\dataSet\road_sta_end.json')

# road_sta_end 中每一段边 应变成一个点 矩阵存储边之间的连接关系 暂时按照无向图来写
def addIndex2Road():
    road_sta_end2 = []
    # 给每一个边一个编号
    for i, road in enumerate(road_sta_end):
        road.append(i)
        road_sta_end2.append(road)
    json_dump(road_sta_end2, r'D:\pycharmProject\logic\dataSet\road_sta_end.json')

def getPoint():
    pointL = []
    for i, road in enumerate(road_sta_end):
        pointL.append((road[0][2], road[1][2], i))
    return pointL

# 无向图 静态
def getMextrix():
    network2 = defaultdict(dict)
    # 复杂度可能比较高 O(n2)
    for road1 in road_sta_end:
        # 路1的开始站点、路1的结束站点、路1的编号
        road1_start, road1_end, road1_id = road1[0][2], road1[1][2], road1[-1]
        for road2 in road_sta_end:
            # 路2的开始站点、路2的结束、路2的编号
            road2_start, road2_end, road2_id = road2[0][2], road2[1][2], road2[-1]
            # 自己找自己 不行
            if road1==road2:
                break
            # 真的找到了
            if road1_start==road2_start or road1_end==road2_end or road1_start==road2_end or road1_end==road2_start:
                network2[road1_id][road2_id] = 1
    return network2






if __name__ == '__main__':

    # 给边加编号
    # addIndex2Road()
    pointL = getPoint()
    Mextrix = getMextrix()

    json_dump(pointL, 'point_R.json')
    json_dump(Mextrix, 'mextrix_R.json')