import networkx as nx
import pandas as pd
import math
from temp import *
import matplotlib.pyplot as plt
def delteIndex(list, i):
    for x in list:
        del x[i]
    return list

def getPr():
    G = nx.Graph()
    pointL = json_load(r'D:\pycharmProject\logic\baseRoad\point_R.json')
    mextrix = json_load(r'D:\pycharmProject\logic\baseRoad\mextrix_R.json')

    edges = []
    for point1, value1 in mextrix.items():
        for point2, value2 in value1.items():
            edges.append((point1, point2))
            edges.append((point2, point1))

    # for i in range(len(pointL)):
    #     # G.add_node(i, weight=weightL[i])
    #     G.add_node(i)

    G.add_edges_from(edges)
    pr = nx.pagerank(G, alpha=0.85, personalization=None, max_iter=100,
                     tol=1.0e-6, nstart=None,
                     dangling=None)

    json_dump(pr, 'pr.json')
    return pr


def getBe():
    G = nx.Graph()
    pointL = json_load(r'/1.底层路网\point_R.json')
    mextrix = json_load(r'/1.底层路网\mextrix_R.json')

    edges = []
    for point1, value1 in mextrix.items():
        for point2, value2 in value1.items():
            edges.append((point1, point2))
            edges.append((point2, point1))

    for i in range(len(pointL)):
        # G.add_node(i, weight=weightL[i])
        G.add_node(i)

    G.add_edges_from(edges)
    # pr = nx.pagerank(G, alpha=0.85, personalization=None, max_iter=100,
    #                  tol=1.0e-6, nstart=None,
    #                  dangling=None)
    be = nx.centrality.betweenness_centrality(G, normalized=False)
    json_dump(be, 'be.json')
    return be



# 将它添加到前端
def addfront(prL, isDeletePre):
    roadL = json_load(r"D:\test_nanChang\unitCode\json\road.json")
    roadL2 = []
    for pr, road in zip(prL, roadL):
        if isDeletePre:
            del road[-1]
        road.append(pr)
        roadL2.append(road)
    json_dump(roadL2, r"D:\test_nanChang\unitCode\json\road.json")

# 算betweenness
# bc = nx.centrality.betweenness_centrality(G, normalized=False, weight='weight')

# pr = getPr()
be = getBe()
# *********************************************算出来的pr值 做分析************************************

beL = list(be.values())
beL2 = []
for x in beL:
    if x == 2.9703894897662785e-05:
        continue
    beL2.append(x)
beL2 = [x/max(beL2) for x in beL2]
# beL2 = [math.log(x) for x in beL2]
print(min(beL2), max(beL2))
plt.plot(beL2[0:500])
plt.show()

# addfront(beL2, True)

beL = json_load(r'D:\pycharmProject\logic\2.baseRoad_index\be.json')
beL2 = {}
for x, value in beL.items():
    if value != 0:
        beL2[x] = value
print(beL2["1"])

json_dump(beL2, 'be.json')

