import datetime
import json
import numpy as np
import pandas as pd
import os
from temp import *
from comUsed.gpsXg import *

# ***************************************** 原料:drawRoad.json和section_drivings ******************************************
# ************************************************ 将公交道路映射到road上 ***************************************************

# 对每一条section_drivings
# def getRoadByGps(gpsPoint, staL):
#     '''
#     通过GPS找到起始站点和结束站点
#     :param gpsPoint: [point1, point2, point3]
#     :return: 路网道路Id [staId, endId]
#     '''
#     # 获得起点和终点
#     staPoint, endPoint = gpsPoint[0], gpsPoint[-1]
#     # 通过起点和终点获得路网的road [staId, endId] 首尾匹配
#     # staPoint-->stationId
#     staId, endId = -1, -1
#     dis1_min, dis2_min = 10e9, 10e9
#     for sta in staL:
#         dis1 = getGpsDis(staPoint, sta)
#         dis2 = getGpsDis(endPoint, sta)
#         if dis1 < dis1_min:
#             staId = [sta[0], sta[-1]]
#             dis1_min = dis1
#         if dis2 < dis2_min:
#             endId = [sta[0], sta[-1]]
#             dis2_min = dis2
#     return [staId, endId]

def getRoadByGps():
    '''
    通过gps获取道路
    :return: [sta1, sta2]
    '''
    dic = {}
    fNameL, pathL = getPath(r'D:\pycharmProject\logic\dataBase\section\sections')
    for name, path in zip(fNameL, pathL):
        list = json_load(path)
        sta1, sta2 = list[0], list[1]
        name = name.replace('.json', '')
        if name[-2] == '0':
            name = name[0:-2]+name[-1]
        name = name.split('_')[0]+'_'+name.split('_')[1]+name.split('_')[2]
        dic[name] = [sta1, sta2]
    json_dump(dic, 'sectionId2road2.json')
    # print(dic)

# 弃用方法
# def getSection2Road():
#     # df = pd.read_csv(r'D:\pycharmProject\logic\dataBase\section_driving\section_drivings\2_down.csv')
#     fNameL, fPathL = getPath(r'D:\pycharmProject\logic\dataBase\section\sections')
#     staL = json_load(r'D:\pycharmProject\logic\dataSet\staIdL.json')
#     # sectionId--->gpsPoint--->[staId, endId]
#     # sections = []
#     dic = {}
#     n = len(fPathL)
#     i = 1
#     for name, path in zip(fNameL, fPathL):
#         # 遍历每个sections
#         points = json_load(path)[4]
#         sectionId = name.replace('.csv', '')
#         dic[sectionId] = getRoadByGps()
#         print(str(round((i / n) * 100, 2)) + '%', i, '----done----')
#         i += 1
#     # print(dic)
#     json_dump(dic, 'sectionId2road2.json')

def getSpeed(gpsPoints):
    '''
    通过gps 获得行驶时长和车速
    :param gpsPoints: [[经度,纬度,t1], [经度,纬度,t2], [经度,纬度,t3]..., [经度,纬度,tn]]
    :return: speed
    '''
    gpsPoints = gpsPoints.replace('\'', '\"')
    # print(gpsPoints)
    gpsPoints = json.loads(gpsPoints)
    t1, t2 = gpsPoints[0][-1], gpsPoints[-1][-1]
    # print(t1, t2)
    t1 = datetime.datetime.strptime(t1, "%Y-%m-%d %H:%M:%S")
    t2 = datetime.datetime.strptime(t2, "%Y-%m-%d %H:%M:%S")
    t = (t2-t1).seconds
    speed = 0 if t == 0 else getLength(gpsPoints)/t
    return t, speed

def getRoad2Section():
    section2road = json_load(r'D:\pycharmProject\logic\计算映射\section2roads.json')
    dic = defaultdict(list)
    for sectionId, roads in section2road.items():
        for road in roads:
            # key = str(road[0])+'_'+str(road[1]) if road[0] < road[1] else str(road[1])+'_'+str(road[0])
            key = str(road[0])+'_'+str(road[1])
            dic[key].append(sectionId)
    json_dump(dic, 'road2sections.json')

# sections
def getSections():
    f = r'D:\pycharmProject\logic\dataBase\section\sections'
    sections = []
    fNameL, pathL = getPath(f)
    for name, path in zip(fNameL, pathL):
        list = json_load(path)
        sta1, sta2 = (list[0], list[1]) if list[0] < list[1] else (list[1], list[0])
        name = name.replace('.json', '')
        if name[-2] == '0':
            name = name[0:-2] + name[-1]
        name = name.split('_')[0] + '_' + name.split('_')[1] + name.split('_')[2]
        sections.append([sta1, sta2, name])
    return sections

# def getRoads():
#     roads = []
#     road_sta_end = json_load(r'D:\pycharmProject\logic\dataSet\road_sta_end.json')
#     for road in road_sta_end:
#         sta, end = road[0][2], road[1][2]
#         roads.append([sta, end])
#     return roads

def getRoads():
    '''
    从sections中提取roads
    :return: roads: [[sta1, sta2], [sta3, sta4], [sta5, sta6]]
    '''
    dic_section2roads = defaultdict(list)
    section2stations = json_load(r'D:\pycharmProject\logic\计算映射\section2stations.json')
    roads = json_load(r'D:\pycharmProject\logic\计算映射\roads.json')
    # print(section2stations, roads)
    false, true = 0, 0
    for sectionId, stations in section2stations.items():
        # print(len(stations))
        for i in range(len(stations)-1):
            if stations[i][2]!=stations[i+1][2]:
                road1 = [stations[i][2], stations[i+1][2]]
                road2 = [stations[i+1][2], stations[i][2]]
                # print(road1, road2)
                if road1 in roads or road2 in roads:
                    true += 1
                else:
                    print(sectionId, i, road1)
                    false += 1
    print(true, false)

# 数据:section:stations ----> section:roads (roads必须在路网中存在)
# 公交路段(A站-->B站):stations ----> roads
def getSection2Roads():
    section2stations = json_load(r'D:\pycharmProject\logic\计算映射\section2stations.json')
    roads = json_load(r'D:\pycharmProject\logic\计算映射\roads.json')

    dic_section2roads = defaultdict(list)
    false, true = 0, 0
    for sectionId, stations in section2stations.items():
        # print(len(stations))
        for i in range(len(stations)-1):
            if stations[i][2]!=stations[i+1][2]:
                road1 = [stations[i][2], stations[i+1][2]]
                road2 = [stations[i+1][2], stations[i][2]]
                # print(road1, road2)
                if road1 in roads:
                    true += 1
                    dic_section2roads[sectionId].append(road1)
                elif road2 in roads:
                    true += 1
                    dic_section2roads[sectionId].append(road2)
                else:
                    # print(sectionId, i, road1)
                    false += 1
    print("sections映射到roads成功个数:", true, "sections映射到roads失败个数:", false)
    json_dump(dic_section2roads, 'section2roads.json')

# 点到直线的距离
def get_distance_from_point_to_line(point, line_point1, line_point2):
    #对于两点坐标为同一点时,返回点与点的距离
    if line_point1 == line_point2:
        point_array = np.array(point)
        point1_array = np.array(line_point1)
        return np.linalg.norm(point_array -point1_array)
    #计算直线的三个参数
    A = line_point2[1] - line_point1[1]
    B = line_point1[0] - line_point2[0]
    C = (line_point1[1] - line_point2[1]) * line_point1[0] + \
        (line_point2[0] - line_point1[0]) * line_point1[1]
    #根据点到直线的距离公式计算距离
    distance = np.abs(A * point[0] + B * point[1] + C) / (np.sqrt(A**2 + B**2))
    return distance

def getSection2stations():
    # 逻辑:计算sections经过哪些站点
    staL = json_load(r'D:\pycharmProject\logic\dataSet\staIdL.json')
    # 对每一个section 计算两点和sta之间的距离
    sections = pd.read_csv(r'D:\pycharmProject\logic\dataBase\section\sections.csv')
    dic = {}
    error = []
    n = 2
    for index, row in sections.iterrows():
        sectionId, path = row['section_id'], row['path']
        if (sectionId != '711_down_41'):
            continue
        # try:
        # if sectionId!='103_down_08':
        #     continue
        section_staList = []
        # section的轨迹
        points = json.loads(path)
        # 给轨迹加上序号
        for i, point in enumerate(points):
            points[i].append(i)
        n = len(points)
        staL2 = []
        for sta in staL:
            if getdis_geo(points[0], sta) > 1000 and getdis_geo(points[-1], sta) > 1000:
                pass
            else:
                staL2.append(sta)
        for i in range(n - 1):
            # 取section中的连续两点
            line_point1, line_point2 = points[i], points[i + 1]
            minPoint = center_geolocation([line_point1, line_point2])
            # 端点到中心的距离
            # 中点 半径
            # r = 9e10
            r = getdis_geo(minPoint, line_point1)
            # print(i,line_point1,line_point2, 'r=>', r)
            for sta in staL2:
                # 几何距离 垂线
                dis = get_distance_from_point_to_line(sta, line_point1, line_point2)
                # 加筛选条件 地理距离
                dis_minPoint = getdis_geo(sta, minPoint)
                # print("dis_minPoint==>", dis_minPoint)
                if (dis < 0.001) and (dis_minPoint <= r + 0.1):
                    section_staList.append(sta)
        dic[sectionId] = section_staList
        if (index % 10 == 0):
            json_dump(dic, 'section2stations.json')
        print("==============================", sectionId, "done=================================")
        # except:
        #     error.append(sectionId)
        #     if len(error)%10==0:
        #         json_dump(error, 'section2stations_error.json')
        #     print("==============================", sectionId, "false================================")

        # if (sectionId == '711_down_41'):
        #     json_dump([points], r"D:\nanChang\paint\json\drawRoad.json")
        #     json_dump(points, r"D:\nanChang\paint\json\gpsPoints.json")
        #     json_dump(section_staList, r"D:\nanChang\paint\json\station_2.json")
        #     print(len(section_staList), section_staList)
        #     print('path:\n', [points], '\nstaList:\n', section_staList)



if __name__ == '__main__':

    # section2stations = json_load(r'D:\pycharmProject\logic\计算映射\section2stations.json')
    # sections = pd.read_csv(r'D:\pycharmProject\logic\dataBase\section\sections.csv')
    # print(len(section2stations), len(sections))
    getRoad2Section()
    pass

