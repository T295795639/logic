import pandas as pd
import os
import networkx as nx
import numpy as np

# 计算pr
def getPr(nodes, edges, nodeWeight):

    edges = [(1, 2), (2, 3)]
    # 创建一个图
    G = nx.DiGraph()
    # G.add_nodes_from([
    #     (1, {"wieght": 5}),
    #     (2, {"weight": 6}),
    #     (3, {"weight": 7})
    # ])

    G.add_edges_from([[1, 2], [2, 3], [3, 1], [2, 1]])
    G.add_edges_from(edges)

    # 计算指标
    pr = nx.pagerank(G,
                  alpha=0.85,
                  personalization=None,
                  max_iter=100,
                  tol=1e-06,
                  nstart=None,
                  weight='weight',
                  dangling=None)
    # 参数介绍
    # - 在networkx.pagerank中，PR值得计算为：*PR = alpha * (A * PR + dangling分配) + (1 - alpha) * 平均分配 *
    # - G：NetworkX图，对于无向图，默认会转化为双向有向图进行计算；
    # - alpha：即阻尼因子；
    # - personalization：自定义节点的PR值分配，默认为均匀分配；
    # - max_iter：最大迭代次数；
    # - tol：迭代阈值，若两次迭代差值低于该值，则跳出迭代;
    # - nstart：自定义网络各节点PageRank初始值，自定义的初始化PR值会在函数中自动归一化，见以下部分源码;
    # if nstart is None:
    #     x = dict.fromkeys(W, 1.0 / N)  # 和为1
    # else:  # 归一化nstart vector s = float(sum(nstart.values())) x = dict((k, v / s) for k, v in nstart.items())
    # - weight：默认为“weight”，边权重值；没有时默认为1。
    # - dangling：对于dangling节点（出度为0的节点），自定义其PR值得分配，默认为均匀分配。
    # 多数情况下, ** personalization ** 和 ** dangling ** 是相同的。
    # - Returns – 字典，每个节点及其对应的PR值。
    print(pr)


# 计算be
def getBe(nodes, edges, nodesWeight):
    pass


# 实现pagerank
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

    # 根据边获取节集
    nodes = []
    for edge in edges:
        if edge[0] not in nodes:
            nodes.append(edge[0])
        if edge[1] not in nodes:
            nodes.append(edge[1])
    # **********************************  基于edges生成nodes列表  *****************************************
    print('nodes', nodes)

    N = len(nodes)
    # 节点初始为1/N, 使用nodesWeight替代
    # P_n = np.ones(N) / N
    P_n = np.array(nodesWeight)
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
            S[i, j] /= sum_of_col
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

    while e > 1e-6:  # 开始迭代
        P_n1 = np.dot(A, P_n)  # 迭代公式
        e = P_n1 - P_n
        e = max(map(abs, e))  # 计算误差
        P_n = P_n1
        k += 1
        # print('iteration %s:' % str(k), P_n1)

    print('final result:', P_n)



if __name__ == '__main__':

    getPr('', '', '')
    getPrM(edges=[[1, 2], [2, 3], [3, 1], [2, 1]], nodesWeight=[2, 1, 3])




