import os.path
import matplotlib.pyplot as plt
import pandas as pd
from temp import *

items = []

# 拿到线路的gps点 线路id：线路gps
namel_Gps, pathl_Gps = getPath(r'E:\buStation_nanChang_netWork\output\4_getRoadGps\sum')
dic_lineId_gps = {}
for name, path in zip(namel_Gps, pathl_Gps):
    lineId = name.split('.')[0]
    dic_lineId_gps[lineId] = pd.read_csv(path).loc[:, ['lng', 'lat']].values.tolist()

F = False
# 线路有哪些站点 线路id：站点id
namel_stations, pathl_stations = getPath(r'D:\pycharmProject\logic\3.lineRoadNet\route2station')
for name, path in zip(namel_stations, pathl_stations):
    errorL = []
    lineId = name.split('.')[0]
    print(lineId, F)
    ## debug代码
    if str(lineId)=="5029_up":
        F = True
    ## 不是5029_up 疯狂跳过
    if not F:
        continue
    print("开始执行了")
    ## debug代码结束
    stationL = json_load(path)
    stationIdL = [x[2] for x in stationL]
    stations = [[x[0], x[1]] for x in stationL]
    # type 0 是找到最近的两个点 切割后的线路 也就是section
    try:
        ans = gpSplit(gpsList=dic_lineId_gps[lineId], staList=stations, type=0)
    except:
        print('error', lineId)
        errorL.append(lineId)
        continue

    for i in range(len(stationIdL)-1):
        sectionId = lineId+'_' + str(i) if i>=10 else lineId+'_'+'0'+str(i)
        start_station_id, end_station_id = stationIdL[i], stationIdL[i+1]
        item = [start_station_id, end_station_id, lineId, sectionId, ans[i]]
        items.append(item)
        tof = 'sections//'+sectionId+'.json'
        if ~os.path.exists(tof):
            json_dump(item, 'sections//'+sectionId+'.json')

    json_dump(errorL, 'errorL.json')

print(items)
# 测试一下
# ans = gpSplit(gpsList=, staList=) 178, 129039


