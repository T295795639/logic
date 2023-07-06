import json

import pandas as pd
import requests
from temp import *

def track_similarity(points1, points2):
    url = "https://api.map.baidu.com/trackmatch/v1/track?" # POST请求
    ak = "BZjB1AYSZ8ulwVAWs8dKw66rUuSUXTkj"
    # 基准轨迹 [{latitude,longitude,loc_time,radius,speed,direction,height},...]
    standard_track = [{}]
    # 待匹配轨迹 同上
    track = []

    # 基准轨迹的纠偏参数设置 非必选
    standard_option = []

    road_131_down = json_load(r'E:\buStation_nanChang_netWork\DP\DP\101_down.json')["coordinates"]
    road_131_up = json_load(r'E:\buStation_nanChang_netWork\DP\DP\101_up.json')["coordinates"]
    # road_131_up.reverse()

    def convert(pointL):
        ansL = []
        for x in pointL:
            ansL.append(str(x[1]) + ',' + str(x[0]))
        return json.dumps(ansL)

    standard_track = convert(road_131_up)
    track = convert(road_131_down)

    # print(standard_track)
    body = {
        'ak': ak,
        'standard_track': standard_track,
        'track': track,
        "coord_type_input": "wgs84"
    }

    res = requests.post(url=url, data=body)
    print(json.loads(res.text)["data"]["similarity"])

if __name__ == '__main__':
    track_similarity('', '')
    pass