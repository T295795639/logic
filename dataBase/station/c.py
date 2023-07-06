# station表 station_id station_name lng lat
# 路口编号+路口名称+经度+纬度
import sqlite3

import pandas as pd

from temp import *

conn = sqlite3.connect(r'E:\buStation_nanChang_netWork\db\nanChang.db')

## 拿到站点数据 主要用到站点ID 站名
BUS_STATION = pd.read_sql(con=conn, sql="SELECT * FROM BUS_STATION")
print(BUS_STATION.columns)

stations = json_load(r'D:\pycharmProject\logic\dataSet\staIdL.json')

items = []
for station in stations:
    stationId = station[2]
    boolist = (BUS_STATION['站点ID']==stationId).values
    # print(boolist)
    if boolist.any():
        statioName = BUS_STATION.loc[boolist, '站名'].values[0]
    else:
        statioName = str(stationId)+'路口'
    # station_id station_name lng lat
    items.append([stationId, statioName, station[0], station[1]])

station = pd.DataFrame(data=items, columns=['station_id', 'station_name', 'lng', 'lat'])
station.to_csv('station.csv', index=False)