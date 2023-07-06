import matplotlib.pyplot as plt
import pandas as pd
import os
from temp import *

fnameL, pathL = getPath(r'D:\pycharmProject\logic\dataBase\section_driving\section_drivings')

print(pathL)

# 天数和小时
day, hour, min, secondes = [], [], [], []
# 遍历路径数组
for path in pathL:
    df = pd.read_csv(path)
    p = df.apply(lambda x: [x['start_date_time'], x['end_date_time']], axis=1).values.tolist()
    day.extend([int(x[0][8:10]) for x in p])
    hour.extend([int(x[0][11:13]) for x in p])
    min.extend([int(x[0][14:16]) for x in p])
    secondes.extend([int(x[0][17:20]) for x in p])

sca1 = [[x[0], x[1]] for x in zip(day, hour)]
sca2 = [[x[0], x[1]] for x in zip(min, secondes)]
# print(sca1)
drawSca(list=sca1)
plt.title("day+hour")
plt.show()
drawSca(list=sca2)
plt.title("min+second")
plt.show()

# print('day', day)
# print('hour', hour)
# print('min', min)
# print('secondes', secondes)


# str = "2021-09-08 17:47:00"
# print('Day Hour Min Second===>', str[8:10], str[11:13], str[14:16], str[17:20])



















