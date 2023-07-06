import pandas as pd

from temp import *

edges = json_load(r'D:\pycharmProject\logic\1.baseRoad\mextrix_R.json')
# 无向图 字典到边的转换
startPointL = list(edges.keys())
edges2 = []
for point in startPointL:
    endPointL = list(edges[point].keys())
    for endPoint in endPointL:
        edges2.append([point, endPoint])

df = pd.DataFrame(data=edges2, columns=['source', 'target'])
df.to_csv("edges.csv", index=False)