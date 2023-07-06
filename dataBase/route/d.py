# 关系表 route_Id  station_Id
# 线路名称 线路id 上行还是下行?
import pandas as pd

from temp import *

nameL, pathL = getPath(r'D:\pycharmProject\logic\3.lineRoadNet\route2station')

items = []
for name, path in zip(nameL, pathL):
    route_Id = name.split('_')[0]
    # 线路的gps点 如果长度是3 则是站点
    gpsList = json_load(path)
    for gpsPoint in gpsList:
        if len(gpsPoint)==3:
            items.append([route_Id, gpsPoint[2]])

df_routeId_stationId = pd.DataFrame(data=items, columns=['route_Id', 'station_Id'])

print(df_routeId_stationId.head(10))

df_routeId_stationId.to_csv(r'D:\pycharmProject\logic\dataBase\route\route-station.csv', index=False)