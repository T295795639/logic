# 计算section上的车速和行驶时长
import matplotlib.pyplot as plt

from temp import *
import pandas as pd
from datetime import datetime
# 拿到sections的车速和行驶时长
def getSpeed(T="2021-09-08 22:00:00"):
    '''
    计算时间范围内sections的车速和
    :param sections: 路段id
    :param time: 时刻 格式为 ['2021-09-08 17:10:15', '2021-09-08 17:33:00']
    :return: {sectionId+'_'+: }
    '''
    # print(t1, t2)
    # fnameL, pathL
    T = datetime.strptime(T, "%Y-%m-%d %H:%M:%S")
    fnameL, pathL = getPath(r'D:\pycharmProject\logic\dataBase\section_driving\section_drivings')
    # 对每一个sections
    num = 0
    dic = defaultdict(list)
    for path in pathL:
        df = pd.read_csv(path)
        for index, row in df.iterrows():
            key = str(row["sectionId"])
            # 格式化每行的时间和需要检索的时间
            t1, t2, = datetime.strptime(row['start_date_time'], "%Y-%m-%d %H:%M:%S"), datetime.strptime(row['end_date_time'], "%Y-%m-%d %H:%M:%S")
            # 找到匹配的那一行
            if (T-t1).days >= 0 and (t2-T).days <= 0:
                # print(row["sectionId"], row['aveSpeed'], row['spentTime'])
                dic[key].append([row['aveSpeed'], row['spentTime']])
                num = num + 1
    dic2 = {}
    # key变成线路 求平均
    for key, value in dic.items():
        if 'n' in key:
            key = key.split('n')[0] + 'n_' + '0' + key.split('n')[-1] if len(key.split('n')[-1]) == 1 else key.split('n')[0] + 'n_' + key.split('n')[-1]

        if 'p' in key:
            key = key.split('p')[0] + 'p_' + key.split('p')[-1] if len(key.split('p')[-1]) == 1 else key.split('p')[0] + 'p_' + key.split('p')[-1]

        N = len(value)
        speedSum, timeSum = 0, 0
        for item in value:
           speedSum += item[0]
           timeSum += item[1]
        dic2[key] = [speedSum/N, timeSum/N]

    json_dump(dic2, '1.json')
    # json_dump(dic, 'output\\'+T.strftime("%Y-%m-%d %H:%M:%S").replace(' ', '/')+'.json')
    print('num', num)
    pass

## 计算聚类中的指标 (簇--->roads×-->section-->index)  (簇-->stations-->section-->index)
def getCluId2Index():
    # 计算每个clu的指标
    clu_Index = defaultdict(list)
    true, false = 0, 0
    # cluId ==> roads ==> sections ==> Index(指标)
    # Index ==> cluId
    label2roads = json_load(r'D:\pycharmProject\logic\dataSet\label2roads110.json')
    road2sections = json_load(r'D:\pycharmProject\logic\计算映射\road2sections.json')
    section2Index = json_load(r'D:\pycharmProject\logic\计算道路指标(通过sections)\speed&travelTime\output\1.json')
    # 对每一个簇 计算每条路上的section
    for cluId, roads in label2roads.items():
        roads = label2roads[cluId]
        roads = [[road[0][2], road[-1][2]] for road in roads]
        # print("cluId==>", cluId)
        # print("======================= 聚类簇 ==============================")
        # 对簇中的每一条路
        for road in roads:
            # print('road', road)
            # 得到road2sections中的key
            # key = str(road[0])+'_'+str(road[1]) if road[0]<road[1] else str(road[1])+'_'+str(road[0])\
            key = str(road[0])+'_'+str(road[1])
            # 路对应的sections
            if key in list(road2sections.keys()):
                sections = road2sections[key]
                # print('sections=>', sections)
                true += 1
                # print(sections)
                for section in sections:
                    try:
                        clu_Index[cluId].append(section2Index[section])
                    except:
                        print(cluId)
            else:
                false += 1

    aveSpeed, aveSpentTime = 0, 0
    # 求平均
    for key, value in clu_Index.items():
        speedList = [x[0] for x in value]
        spentTime = [x[1] for x in value]
        aveSpeed = sum(speedList)/len(speedList) if len(speedList)!=0 else 0
        aveSpentTime = sum(spentTime)/len(spentTime) if len(spentTime)!=0 else 0
        clu_Index[key] = [aveSpeed, aveSpentTime]

    num_false, num_true = 0, 0
    # 遍历
    for i in range(109):
        if str(i) in list(clu_Index.keys()):
            num_true += 1
        else:
            num_false += 1
    # print(num_true, num_false)

    speedList = []
    timeList = []
    # cluId_index
    for cluId, index in clu_Index.items():
        if index[0] != 0:
            speed = index[0]
            speedList.append(speed)
        if index[1] != 0:
            spentTime = index[1]
            timeList.append(spentTime)
    speed_ave = sum(speedList)/len(speedList)
    time_ave = sum(timeList)/len(timeList)
    # 填补空簇
    cluIdL = list(label2roads.keys())
    cluIdL_index = list(clu_Index.keys())
    for cluId in cluIdL:
        if cluId not in cluIdL_index:
            clu_Index[cluId] = [aveSpeed, aveSpentTime]

    # 使用平均值填充
    for cluId, index in clu_Index.items():
        if index[0] == 0:
            clu_Index[cluId][0] = speed_ave
        if index[1] == 0:
            clu_Index[cluId][1] = time_ave
    json_dump(clu_Index, 'clu_Index.json')



if __name__ == '__main__':
    # t1 = datetime.strptime('2021-09-08 17:10:15', "%Y-%m-%d %H:%M:%S")
    # t2 = datetime.strptime('2021-09-08 17:10:00', "%Y-%m-%d %H:%M:%S")
    # print((t2-t1).days)
    # getSpeed()
    getCluId2Index()
    pass