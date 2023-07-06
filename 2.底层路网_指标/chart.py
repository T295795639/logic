from comUsed import fileXg
from temp import *
# **************************************drawPr******************************************
pr = fileXg.json_load(r"D:\pycharmProject\logic\2.baseRoad_index\pr.json")
prL = list(pr.values())
prL2 = []
for x in prL:
    if x == 2.9703894897662785e-05:
        continue
    prL2.append(x)
prL2 = [x/max(prL2) for x in prL2]
# prL2 = [math.log(x) for x in prL2]
print(min(prL2), max(prL2))
plt.plot(prL2)
plt.show()

