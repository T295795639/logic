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
    pointL = json_load(r'D:\pycharmProject\logic\4.cluterRegion\point.json')
    mextrix = json_load(r'D:\pycharmProject\logic\4.cluterRegion\mextrix.json')

    edges = []
    for point1, value1 in mextrix.items():
        for point2, value2 in value1.items():
            edges.append((point1, point2))
            edges.append((point2, point1))

    for i in range(len(pointL)):
        # G.add_node(i, weight=weightL[i])
        G.add_node(i)

    G.add_edges_from(edges)
    pr = nx.pagerank(G, alpha=0.85, personalization=None, max_iter=100,
                     tol=1.0e-6, nstart=None,
                     dangling=None)
    # json_dump(pr, 'pr.json')
    return pr

pr = getPr()
# *********************************************算出来的pr值 做分析************************************

prL = list(pr.values())
prL2 = []
for x in prL:
    if x == 0.0005795982316841325:
        continue
    prL2.append(x)
print(min(prL2), max(prL2))
plt.plot(prL2)
plt.show()
prL2 = [x/max(prL2) for x in prL2]
# prL2 = [math.log(x) for x in prL2]
# json_dump(prL, 'pr.json')

def addfront(prL):
    print(prL)
    rateData = json_load(r"D:\pycharmProject\busRoute_nanchang\tempData\rateData.json")
    nodes = rateData["nodes"]
    nodes2 = []
    for x, node in zip(prL, nodes):
        print(x)
        node['color'] = "rgba(0,0,0,{0})".format(x)
        nodes2.append(node)
    rateData["nodes"] = nodes2
    json_dump(rateData, r"D:\pycharmProject\busRoute_nanchang\tempData\rateData.json")

addfront(prL2)