# 计算路段的车速
# section路段切割
# 用轨迹数据去算

# section_driving
# data_id car_id section_id start_date_time end_date_time stay_time path

# 现在有切好的数据
# 文件名索引--> 线路:车辆id:趟次(0, 1, 2, 3, 4......)
# 需要输出: data_id(car_id, section_id, trips) car_id section_id "start_date_time" "end_date_time" "stay_time" "path"
# data_id: 车id 路id 车次id
import datetime
import os
import time
from tqdm import tqdm, trange
import pandas as pd

from comUsed import gpsXg
from temp import *

# 字典 route-->stations
# 存入内存
def getDicRoute2Station():
    dic_route2station = {}
    for path in getPath(r"D:\pycharmProject\logic\3.线路网络\route2station")[1]:
        routeName = path.split("\\")[-1].replace(".json", '')
        List = json_load(path)
        List2 = []
        for x in List:
            if (x[2]>100000):
                List2.append(x)
        dic_route2station[routeName] = List2
    return dic_route2station

# 判断数据上行或者下行
def isUpOrDown(df):
    # 1、判断上下行 上行是3 00000 4  下行是4 11111 3
    lastRow = len(df) - 1
    first_row, last_row = df.iloc[0, :]['isUpDown'], df.iloc[lastRow, :]['isUpDown']
    if (first_row == 3 and last_row == 4):
        return 'up'
    elif (first_row == 4 and last_row == 3):
        return 'down'
    else:
        return False

# 切出GPS
# 形参 dataFrame和routeName
def cutGps(df, routeName):
    # 知道了routeName, gps
    # 2.1、切分：返回切分前插入位置的index, 切分后的插入位置index_shift, 生成gps
    gpsList = df.loc[:, ['lng', 'lat']].values.tolist()
    if routeName not in list(dic_route2station.keys()):
        error01.append(routeName)
        raise Exception('error01, 原因dic_route2station中找不到该线路', routeName)

    # 站点拿到 轨迹拿到 插入位置
    # 将站点插入, 返回插入位置
    staList, staList_shift, gps = sta2Gps(gpsList=gpsList, staList=dic_route2station[routeName], type=0)

    # 2.2、使用站点的插入位置, 取出station_parking的gps  section_driving的gps
    # 生成 stations
    gpsL = gpsList
    stations = []
    stationIndexs = []
    for i, staIndex in enumerate(staList):
        station_p1, station_p2 = gpsXg.getGpsAroundPos(gpsL=gpsL, radius=5, pointIndex=staIndex)
        # gps_station = df.iloc[station_p1:station_p2, ]
        stationIndexs.append([station_p1, station_p2])
        stations.append(station_p1)
        stations.append(station_p2)
    # 生成 sections
    sections = []
    for i, sta in enumerate(stations):
        if i == 0:
            sections.append([0, sta])
        elif i == len(stations) - 1:
            sections.append([sta, len(stations) - 1])
        elif i % 2 != 0:
            sections.append([sta, stations[i + 1]])
    return stationIndexs, sections


def getTables(stations, sections, itemName):
    # 生成section_parkings
    station_parkings = []
    for i, station in enumerate(stations):
        if len(station)==0:
           station_parkings.append([-1, -1, -1, -1, -1])
        else:
            a1, a2 = station[0], station[1]
            gps_station = df.iloc[a1:a2, ].loc[:, ['lng', 'lat', 'time']].values.tolist()
            stationId = dic_route2station[routeName][i][2]
            if len(gps_station)==0 or len(gps_station[0])<3 or len(gps_station[-1])<3:
                error02.append(itemName)
                raise Exception("station-gps出错", gps_station)
            start_date_time, end_date_time = gps_station[0][2], gps_station[-1][2]
            station_parkings.append([stationId, carId, gps_station, start_date_time, end_date_time])

    # 生成section_drivings
    section_drivings = []
    for i, section in enumerate(sections):
        if len(section)==0:
           section_drivings.append([-1, -1, -1, -1, -1])
        else:
            a1, a2 = section[0], section[1]
            gps_section = df.iloc[a1:a2 + 1, :].loc[:, ['lng', 'lat', 'time']].values.tolist()
            if (len(gps_section) == 0):
                section_drivings.append([-1, -1, -1, -1, -1])
            else:
                sectionId = routeName + str(i)
                start_date_time, end_date_time = gps_section[0][2], gps_section[-1][2]
                section_drivings.append([sectionId, carId, gps_section, start_date_time, end_date_time])

    df_station_parkings = pd.DataFrame(data=station_parkings,
                                       columns=['stationId', 'carId', 'path', 'start_date_time', 'end_date_time'])
    df_section_drivings = pd.DataFrame(data=section_drivings,
                                       columns=['sectionId', 'carId', 'path', 'start_date_time', 'end_date_time'])

    return df_station_parkings, df_section_drivings


if __name__ == '__main__':

    routeNameComplete = []
    isCompleteL = json_load(r"D:\pycharmProject\logic\dataBase\section_driving\routeNameComplete.json")

    error01 = [["error01, 原因dic_route2station中找不到该线路"]]
    error02 = [["station-gps出错"]]
    # 预留两个空的dataFrame
    df_parkings = pd.DataFrame(columns=['stationId', 'carId', 'path', 'start_date_time', 'end_date_time'])
    df_drivings = pd.DataFrame(columns=['sectionId', 'carId', 'path', 'start_date_time', 'end_date_time'])

    # 路径数组 [路径1, 路径2, 路径3, 路径4, 路径5] 很多个数据
    # gps_oneTrip中的数据 pathL
    pathL = json_load(r'D:\pycharmProject\logic\dataBase\section_driving\pathL.json')

    # 跑数据 需要计数 每条线路要跑多少车
    dic_route_carId = json_load(r'D:\pycharmProject\logic\dataBase\section_driving\route_carId.json')
    errorL = []
    path_num = len(pathL)
    # 这条线路都有哪些站点
    dic_route2station = getDicRoute2Station()

    runtime = 0
    # 遍历数据
    for i, path in enumerate(tqdm(pathL)):
        if i <= 116708:
            continue
        start_time = time.time()
        try:
            # **************************************** 拿到线路名字 ******************************************
            # 单次循环是一条线路 output中的一个文件
            # path = os.path.join(filepath, filename)
            itemNameL = path.split('\\')
            # 算出 线路号 车ID 趟次
            routeName, carId, tripNo = itemNameL[3], itemNameL[4], itemNameL[5].replace('.csv', '')
            itemName = routeName+'_'+carId+'_'+tripNo
            # 拿出一条路的GPS数据
            # 从GPS中 1.判断上下行 2.切分 3.计算section_id data_id start_date_time end_date_time stay_time path
            # 1.判断上下行 上行是3 00000 4  下行是4 11111 3
            df = pd.read_csv(path)
            # 找到线路的方向 df
            direct = isUpOrDown(df)
            if direct == False:
                continue
            else:
                routeName = routeName + '_' + direct
            # ******************************************* 只跑6条数据 ****************************************************
            # routeName_carId = routeName+carId
            # if routeName_carId not in dic_route_carId[routeName]:
            #     dic_route_carId[routeName].append(routeName_carId)
            # if len(dic_route_carId[routeName]) > 6:
            #     dic_route_carId[routeName].pop()
            #     continue
            # 如果这条线路数据跑过 跳过循环
            # 2.切分Gps
            #  ******************** debug **********************
            # if routeName != '10_down':
            #     break
            #  ******************* debug结束 ********************

            #  ****************** 时间复杂度高 *******************
            stations, sections = cutGps(df, routeName)
            #  *************************************************

            # 3.生成station_prking和section_driving两张表
            # 生成station_parking

            df_station_parkings, df_section_drivings = getTables(stations, sections, itemName)

            # df_parkings = df_parkings.append(df_station_parkings)
            # df_drivings = df_drivings.append(df_section_drivings)

            # print(df_parkings.head(1), df_drivings.head(1))
            df_station_parkings.to_csv('station_parkings\\'+routeName+'.csv', index=False, mode='a')
            df_section_drivings.to_csv('section_drivings\\'+routeName+'.csv', index=False, mode='a')
            end_time = time.time()
            runtime += end_time - start_time
            print(str(round((i/path_num)*100, 2))+'%', i, '----------done---------', flush=True, end='')

        except Exception as err:
            # print('报错了', path, str(err))
            errorL.append([path, str(err)])
            json_dump(errorL, 'errorL.json')










