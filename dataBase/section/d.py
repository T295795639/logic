import pandas as pd

from temp import *

sections = json_load(r'D:\pycharmProject\logic\dataBase\section\sections.json')

df = pd.DataFrame(data=sections, columns=['start_station_id', 'end_station_id', 'route_id', 'section_id', 'path'])

df.to_csv('sections.csv', index=False)





