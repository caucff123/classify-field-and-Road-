# coding:utf-8
# 生成一组随机经纬度
import random
import math


#  参数含义
# base_log：经度基准点，
# base_lat：维度基准点，
# radius：距离基准点的半径
def generate_random_gps(base_log=None, base_lat=None, radius=None):
    radius_in_degrees = radius / 111300
    u = float(random.uniform(0.0, 1.0))
    v = float(random.uniform(0.0, 1.0))
    w = radius_in_degrees * math.sqrt(u)
    t = 2 * math.pi * v
    x = w * math.cos(t)
    y = w * math.sin(t)
    longitude = y + base_log
    latitude = x + base_lat
    # 这里是想保留4位小数
    loga = float('%.4f' % longitude)
    lata = float('%.4f' % latitude)
    return loga, lata


# 生成指定数量的经纬度
import numpy as np


def generate_random_gpss(numbers=None):
    logas = []
    latas = []
    for i in range(0, numbers):
        longitude_, latitude_ = generate_random_gps(base_log=120.7, base_lat=30, radius=100)
        logas = np.append(logas, longitude_)
        latas = np.append(latas, latitude_)
    return logas, latas


# 随机生成一组经纬度
import pandas as pd

logas, latas = generate_random_gpss(50)
data = {"经度": logas.T, "纬度": latas.T}
data = pd.DataFrame(data)
print(data)
data.to_csv('点集.csv')

import matplotlib.pyplot as plt
plt.scatter(data['经度'],data['纬度'])
plt.show()
