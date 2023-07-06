from comUsed.netXg import *

# 设定参数
# BPR参数 0.15、3
# 通行能力参数0.3 0.2 0.4 (a,b,c)
# 权重系数 0.4 0.6 0.3
# ******************************************* 计算通行能力Ve ********************************************
# 路段通行能力Ve

# **************************************** 计算网络平均度 平均效率 ********************************
# 调用netXg库



# ******************************************* 路段 staId,endId,t *************************************
# ********************************************** 计算路段的效率 ****************************************
# 通行能力模型
# 扰动后,路段"通行能力"的恢复满足该模型type=1或type=2 未扰动时,路段"通行能力"满足type=0
# 参数 类型 通行能力 时间 a,b,c设为0.3 0.2 0.4 扰动发生时间
# 通行能力Ve设为3600 a,b,c设为0.3\0.2\0.4
def getAccessAbility(type, Ve, t, a, b, c, td):
    global accessAbility
    e = 2.71496
    if type == 0:
        accessAbility = Ve
    elif type == 1:
        accessAbility = Ve * (1/pow(e, a*t))
    elif type == 2:
        accessAbility = Ve*b + Ve(1-b) * [1-1/pow(e, [-c*(t-td)])]

    return accessAbility


# ********************************************** 计算阻抗 *********************************************
# BPR 阻抗模型
# a、b (0.15、3)
# 通行能力 流量 扰动发生前的车辆出行时间
def BPR(a, b, acc, q, c0):
    ct = c0 * [1+a*[pow((q/acc), b)]]
    return ct


# ********************************************** 计算效率 **********************************************
# 效率模型 计算效率
# q0 c0 ct qt
# 自由流状态下e的流量 路段流量为0时车的自由流时间 路段e在t时刻的阻抗 路段e在t时刻的流量
def roadEfficiency(q0, c0, ct, qt):
    roadE = 0
    roadE = (q0*c0)/(qt*ct)
    return roadE









