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
    # 创建无向图
    G = nx.Graph()
    # 创建有向图
    # G = nx.DiGraph()

    pointL = json_load(r'/1.底层路网\point_R.json')
    mextrix = json_load(r'/1.底层路网\mextrix_R.json')

    edges = []
    for point1, value1 in mextrix.items():
        for point2, value2 in value1.items():
            edges.append((int(point1), int(point2)))
            # edges.append((point2, point1))

    for i in range(len(pointL)):
        # G.add_node(i, weight=weightL[i])
        G.add_node(i)

    G.add_edges_from(edges)
    print("G.nodes", G.nodes, "G.edges", G.edges)
    pr = nx.pagerank(G, alpha=0.85, personalization=None, max_iter=100,
                     tol=1.0e-6, nstart=None,
                     dangling=None)
    json_dump(pr, 'pr.json')
    return pr

# 将它添加到前端
def addfront(prL, isDeletePre):
    roadL = json_load(r"D:\pycharmProject\logic\dataSet\drawRoad.json")
    print(len(prL), len(roadL))
    roadL2 = []
    for pr, road in zip(prL, roadL):
        if isDeletePre:
            del road[-1]
        road.append(pr)
        roadL2.append(road)
    json_dump(roadL2, r"D:\nanChang\unitCode\json\road.json")

# 算betweenness
# be = nx.centrality.betweenness_centrality(G, normalized=False, max_iter=100, weight='weight')
# bc = nx.centrality.betweenness_centrality(G, normalized=False, weight='weight')

pr = getPr()
# *********************************************算出来的pr值 做分析************************************

prL = list(pr.values())
prL2 = []
for x in prL:
    if x == 2.9703894897662785e-05:
        continue
    prL2.append(x)
prL2 = [x/max(prL2) for x in prL2]
# prL2 = [math.log(x) for x in prL2]
print(min(prL2), max(prL2))
plt.plot(prL2)
plt.show()
addfront(prL2, False)

