# I want [时间范围:{sectionId: [{记录1, 记录2, 记录3}]}}]
import datetime as dt
import pandas as pd
from temp import *
import time
from tqdm import tqdm

def timeSub(time1, time2):
    # a = dt.datetime.strptime(str(time1), "%Y-%m-%d %H:%M:%S")
    # b = dt.datetime.strptime(str(time2), "%Y-%m-%d %H:%M:%S")
    # return (a-b).second
    return dt.datetime.timestamp(dt.datetime.strptime(str(time1), '%Y-%m-%d %H:%M:%S')) - dt.datetime.timestamp(dt.datetime.strptime(str(time2), '%Y-%m-%d %H:%M:%S'))

# 生成一个dic_time_sectionId: path
def timeFilter(df, t1='2021-09-09 10:00:00', t2='2021-09-09 11:00:00'):
    # 筛选时间
    df = df[(df['start_date_time'] != '-1') & (df['start_date_time'] != 'start_date_time')]
    filter = df['start_date_time'].apply(lambda x: (timeSub(x, t1)) > 0 and (timeSub(t2, x)) > 0)
    df = df[filter]
    return df

def getTimeList(start, end, step):
    start, end = dt.datetime.strptime(start, "%Y-%m-%d %H:%M:%S"), dt.datetime.strptime(end, "%Y-%m-%d %H:%M:%S")
    timeL = []
    while True:
        tempTime = start
        if timeSub(tempTime, end)>0:
            break
        tempTime += dt.timedelta(hours=step)
        timeL.append([str(start), str(tempTime)])
        start = tempTime
    return timeL

def getJson_t_section(t1='2021-09-09 10:00:00', t2='2021-09-09 11:00:00'):
    # 输入时间,获得json块 时间_sectionId: [记录]
    dic = defaultdict(list)
    jsonList = []
    fNameL, pathL = getPath(r'D:\pycharmProject\logic\dataBase\section_driving\section_drivings')
    for fName, path in zip(fNameL, pathL):
        df = pd.read_csv(path)
        # 筛选 时间粒度 1小时
        df = timeFilter(df, t1, t2)
        valuesList = df.values.tolist()
        for i, value in enumerate(valuesList):
            valuesList[i][2] = json.loads(valuesList[i][2].replace("'", '"'))
        jsonList = [dict(zip(df.columns.tolist(), value)) for value in valuesList]

        for item in jsonList:
            dic[item['sectionId']].append(item)

    for sectionId, dataL in dic.items():
        for i, data in enumerate(dataL):
            dic[sectionId][i]["speed"] = getSpeed(data["path"])
            dic[sectionId][i]["length"] = getLength(data["path"])
    return dic

if __name__ == '__main__':
    ans = {}
    timeL = getTimeList('2021-09-08 19:20:00', '2021-09-14 14:15:00', 1/6)
    for i, time in enumerate(tqdm(timeL)):
        key = time[0]+'->'+time[1]
        ans[key] = getJson_t_section(time[0], time[1])
        print(key, i, 'done', end=' ', flush=True)
    json_dump(ans, r'D:\pycharmProject\logic\getJson\json\dic_t_sectionId_data.json')









