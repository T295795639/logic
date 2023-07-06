import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from logic.logicalCode import *
from comUsed.formatXg import *


# ***************************************************** 核心算法pageRank *********************************************
def getPr(edges, points):
    '''
    计算pr
    :param edges: [(point1, point2), (point1, point2)]
    :param points: [point1, point2, point3......]
    :return: pr值字典
    '''
    # print(edges, points)
    G = nx.DiGraph()
    G.add_edges_from(edges)
    for point in points:
        G.add_node(point)
    pr = nx.pagerank(G, alpha=0.85, personalization=None, max_iter=100,
                     tol=1.0e-6, nstart=None,
                     dangling=None)
    # print(pr)
    return pr


# 实现pagerank 自制
def getPrM(edges, nodesWeight):
    '''
    自制算法 计算pagerank
    :param edges: [(1, 2), (3, 4), (5, 6)]
    :param nodesWeight: 根据edges->nodes, 列表:[权1, 权2, 权3......]
    :return: nodes的pr值
    '''
    # 读入有向图，存储边
    # f = open('input_1.txt', 'r')
    # edges = [line.strip('\n').split(' ') for line in f]
    # print(edges)
    # print("nodesWeight", nodesWeight)
    # 根据边获取节集
    nodes = []
    for edge in edges:
        if edge[0] not in nodes:
            nodes.append(edge[0])
        if edge[1] not in nodes:
            nodes.append(edge[1])
    # **********************************  基于edges生成nodes列表  *****************************************
    # print('nodes', nodes)

    N = len(nodes)
    # 节点初始为1/N, 使用nodesWeight替代
    if len(nodesWeight)==0:
        P_n = np.ones(N) / N
    else:
        P_n = np.array(nodesWeight)
    # print('P_n', P_n)
    # 将节点符号（字母），映射成阿拉伯数字，便于后面生成A矩阵/S矩阵
    i = 0
    # 字典 node_to_num key:node value:num
    node_to_num = {}
    for node in nodes:
        node_to_num[node] = i
        i += 1
    for edge in edges:
        edge[0] = node_to_num[edge[0]]
        edge[1] = node_to_num[edge[1]]
    # print('edges', edges)

    # 生成初步的S矩阵
    S = np.zeros([N, N])
    for edge in edges:
        S[edge[1], edge[0]] = 1
    # print('S', S)

    # 计算比例：即一个网页对其他网页的PageRank值的贡献，即进行列的归一化处理
    for j in range(N):
        sum_of_col = sum(S[:, j])
        for i in range(N):
            if sum_of_col != 0:
                S[i, j] /= sum_of_col
            else:
                S[i, j] = 1/N
    # print('S', S)

    # 计算矩阵A
    alpha = 0.85
    A = alpha * S + (1 - alpha) / N * np.ones([N, N])
    # print('A', A)

    # 生成初始的PageRank值，记录在P_n中，P_n和P_n1均用于迭代
    P_n1 = np.zeros(N)

    e = 100000  # 误差初始化
    k = 0  # 记录迭代次数
    # print('loop...')

    while e > 0.00000001:  # 开始迭代
        P_n1 = np.dot(A, P_n)  # 迭代公式
        e = P_n1 - P_n
        e = max(map(abs, e))  # 计算误差
        P_n = P_n1
        k += 1
        # print('iteration %s:' % str(k), P_n1)

    # print('final result:', P_n)
    return P_n


# 封装一下该方法
def myGetpr(edges, dic_node_weight, Max):
    '''
    获得pr值
    :param edges: 边列表
    :param nodesWeight: 字典 {节点: 权重}
    :return: pr值 字典
    '''
    # 处理一下 dic_node_weight
    weights = list(dic_node_weight.values())
    nodes = list(dic_node_weight.keys())
    # weights = [x*100 for x in weights]
    # 权重归一化
    weights = [x/max(weights) for x in weights]
    # plt.plot(weights)
    # plt.show()
    for node, weight in zip(nodes, weights):
        dic_node_weight[node] = weight
    # 权重平均值
    aveWeight = 0 if len(weights)==0 else sum(weights)/len(weights)
    # print('aveWeight', aveWeight)
    # print('归一化dic_node_weight', dic_node_weight)
    # 使用edges生成nodes
    nodes = []
    for edge in edges:
        if edge[0] not in nodes:
            nodes.append(edge[0])
        if edge[1] not in nodes:
            nodes.append(edge[1])
    # 按照edges节点的顺序生成nodesWeight
    nodesWeight = []
    if len(dic_node_weight) != 0:
        for node in nodes:
            if node in list(dic_node_weight.keys()):
                nodesWeight.append(dic_node_weight[node])
            else:
                nodesWeight.append(aveWeight)
    prs = getPrM(edges, nodesWeight)
    # pr值归一化
    prs2 = [x / max(prs) for x in prs]
    # prs2_ave = np.average(prs2)
    # prs2 = [prs2_ave if x > Max else x for x in prs2]
    # prs2 = prs
    # plt.plot(prs2)
    # plt.show()
    ans = {}
    for node, pr in zip(nodes, prs2):
        ans[node] = pr
    # print('max=>', max(prs))
    return ans

def getPR_weight(edges, dic_node_weight):
    # 从网络数据中获取边
    prs = myGetpr(edges, dic_node_weight, 1)
    # json_dump(prs, 'pr_110_roadLength.json')
    # print(prs)
    return prs


def myGetprTest():
    dic_node_weight = json_load(r'D:\pycharmProject\logic\计算道路指标(通过sections)\roadLength\cluId_length.json')
    netAntv = json_load(r'D:\pycharmProject\logic\加权计算betweeness\110.json')
    edges = getEdges(netAntv)
    prs = getPR_weight(edges, dic_node_weight)
    return prs


if __name__ == '__main__':
    ans = myGetprTest()
    df = pd.DataFrame()
    df.to_json()
    print(ans)





