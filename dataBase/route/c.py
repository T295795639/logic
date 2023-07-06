# 三个字段 route_name route_id  isUporDown
# 线路名称 线路id 上行还是下行?
import pandas as pd

from temp import *

import sqlite3

conn = sqlite3.connect(r'E:\buStation_nanChang_netWork\db\nanChang.db')

## 拿到数据线路名称数据
route_name_list = pd.read_sql(con=conn, sql="SELECT 线路 FROM BUS_STATION").iloc[:, 0].unique().tolist()
## 拿到线路id数据
lineNo_lineName = pd.read_csv(r'E:\buStation_nanChang_netWork\output\1_lineNo_clearOut\lineNo.csv')
# 一行数据
dataItem = []
# 所有数据
dataItems = []

for route_name in route_name_list:
    lineNo = lineNo_lineName.loc[lineNo_lineName['线路名称'] == route_name, 'lineNo'].values
    if len(lineNo)!=0:
        for i in range(2):
            dataItem = []
            dataItem.append(route_name)
            dataItem.append(lineNo[0])
            dataItem.append('上行' if i==0 else '下行')
            dataItems.append(dataItem)

df_route = pd.DataFrame(data=dataItems, columns=['route_name', 'route_id', 'isUporDown'])
df_route.to_csv('route.csv', index=False)