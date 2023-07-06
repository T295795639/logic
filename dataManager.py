# 数据访问相关
import pandas as pd
import time
import temp
from comUsed.timeXg import timeSub

# 查询时间为xxx-xxx 的section_driving
def getSectionDriving(t1='2021-09-09 10:00:00', t2='2021-09-09 11:00:00'):
    dic_t_sectionId_data = temp.json_load(r'D:\pycharmProject\logic\getJson\json\dic_t_sectionId_data.json')
    if (t1+'->'+t2) in list(dic_t_sectionId_data.keys()):
        return dic_t_sectionId_data[t1+'->'+t2]
    else:
        return "时间格式错误"


# 查询时间为xxx 的station_parking
def getStationParking(t1='2021-09-09 10:00:00', t2='2021-09-09 11:00:00'):
    dic_t_stationId_data = temp.json_load(r'D:\pycharmProject\logic\getJson\json\dic_t_stationId_data.json')
    if (t1+'->'+t2) in list(dic_t_stationId_data.keys()):
        return dic_t_stationId_data[t1+'->'+t2]
    else:
        return "时间格式错误"




# 逻辑三





# 逻辑四





# 逻辑五






if __name__ == '__main__':

    t1 = time.time()
    getSectionDriving()
    t2 = time.time()
    print(t2-t1)


