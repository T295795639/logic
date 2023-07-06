import pandas as pd
import os
from collections import defaultdict
from temp import *
# 目标数据
# route_id isUpOrDown car_id start_date_time end_date_time path
def oneRoadProcess(gps):
    '''
    处理该趟车的gps
    :param gps: 一辆车一趟的gps
    :return: [lat, lat, time, status],[lat2, lat2, time2, status2]......
    '''


if __name__ == '__main__':
    # 一条线路 一辆车的一趟gps
    gps = json_load(r"E:\output\GPS_oneTrip\2\706852\0.csv")
    oneRoadProcess(gps)