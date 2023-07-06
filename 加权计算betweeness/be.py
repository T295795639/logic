import matplotlib.pyplot as plt
import networkx as nx
from temp import *
from comUsed.formatXg import *
import math

try:
    import queue
except ImportError:
    import Queue as queue

# 节点v的介值中间性 = 求和 取两点s和t, (s->t且经过v的最短路径条数)/(s->t的所有最短路径条数)

def getBE_weight():
    pass


# algorithm from networkx
def getBe(G):
    C = nx.centrality.betweenness_centrality(G, normalized=False)
    return C

def myGetBe(G):
    CB = dict.fromkeys(G, 0.0)
    for s in G.nodes():
        Pred = {w: [] for w in G.nodes()}
        dist = dict.fromkeys(G, None)
        sigma = dict.fromkeys(G, 0.0)
        dist[s] = 0
        sigma[s] = 1
        Q = queue.Queue()
        Q.put(s)
        S = []
        # 非空
        while not Q.empty():
            v = Q.get()
            S.append(v)
            for w in G.neighbors(v):
                if dist[w] == None:
                    dist[w] = dist[v] + 1
                    Q.put(w)
                if dist[w] == dist[v] + 1:
                    sigma[w] += sigma[v]
                    Pred[w].append(v)
        delta = dict.fromkeys(G, 0.0)
        for w in S[::-1]:
            for v in Pred[w]:
                delta[v] += sigma[v] / sigma[w] * (1 + delta[w])
            if w != s:
                # 此处加权
                CB[w] += delta[w]
    for v in CB:
        CB[v] /= 2.0

# compare with networkx's implements
# print(sum(abs(CB[v] - C[v]) for v in G))  # 1.59428026336e-13

if __name__ == '__main__':

    # 从网络数据中获取边
    dic = json_load(r'D:\pycharmProject\logic\加权计算betweeness\110.json')
    edges = getEdges(dic)
    G = nx.DiGraph()
    G.add_edges_from(edges)
    dic_be = getBe(G)
    beL = list(dic_be.values())
    beL = delZero(beL, 'fillMin')
    beL = [(x/max(beL)*0.1) for x in beL]
    plt.title("原始be")
    plt.plot(beL)
    plt.show()

    # 修改beL
    i = 0
    for cluId, be in dic_be.items():
        dic_be[cluId] = beL[i]

    cluId_length = json_load(r'D:\pycharmProject\logic\计算道路指标(通过sections)\roadLength\cluId_length.json')
    # roadLength
    cluId_Index = json_load(r'D:\pycharmProject\logic\计算道路指标(通过sections)\speed&travelTime\clu_Index.json')
    cluId_speed = {}
    cluId_spenTime = {}
    cluL = list(cluId_Index.keys())
    for cluId in cluL:
        cluId_speed[cluId] = cluId_Index[cluId][0]
        cluId_spenTime[cluId] = cluId_Index[cluId][1]

    # 原料: cluId_length cluId_speed cluId_spenTime be
    # length
    be_length = {}
    for cluId, be in dic_be.items():
        be_length[cluId] = cluId_length[cluId]*be
    # 归一化
    Max = max(list(be_length.values()))
    for cluId, be in dic_be.items():
        be_length[cluId] = be_length[cluId]/Max

    # speed
    be_speed = {}
    for cluId, be in dic_be.items():
        try:
            be_speed[cluId] = cluId_speed[cluId]*be
        except:
            print('')
    Max = max(list(be_speed.values()))
    for cluId, be in dic_be.items():
        be_speed[cluId] = be_speed[cluId]/Max

    # time
    be_time = {}
    for cluId, be in dic_be.items():
        be_time[cluId] = cluId_spenTime[cluId]*be
    Max = max(list(be_time.values()))
    for cluId, be in dic_be.items():
        be_time[cluId] = be_time[cluId]/Max

    # 打印一下
    print('be_length:', max(be_length))
    print('be_speed:', max(be_speed))
    print('be_time:', max(be_time))

    # be_lengthL = delMax(be_lengthL)
    # plt.plot(be_lengthL)
    # plt.show()
    # 存一下
    json_dump(be_length, 'be_110_roadLength.json')
    json_dump(be_speed, 'be_110_speed.json')
    json_dump(be_time, 'be_110_time.json')

    pass



