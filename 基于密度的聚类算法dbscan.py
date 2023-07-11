# coding:utf-8
"""
对于簇形状不规则的数据，像k-means（聚类分析: k-means算法）这种基于划分的方法就不再适用了，
因为划分方法（包括层次聚类算法）都是用于发现“球状簇”的。
解决这种任意簇形状的聚类问题，就要采用一种与划分聚类或者层次聚类不同的聚类方法——基于密度聚类
具有噪声应用的基于密度的空间聚类DBSCAN
param radius: the radius of a point's neighborhood  DBSCAN的半径参数
param minPts DBSCAN的密度阈值参数
"""
from numpy import *
import matplotlib.pyplot as plt

from matplotlib.pyplot import *
from collections import defaultdict
import pandas as pd


def createDataSet():
    data = pd.read_csv('点集.csv', index_col=0)
    data = data.values.tolist()
    return data


def dist(data1, data2):
    s1 = (math.cos(int(data1[0])) * (6378137 - int(data1[0]) * 237.61111) * 2 * math.pi / 360) * (data1[0] - data2[0])
    s2 = 111000 * (data1[1] - data2[1])
    distance = math.pow(s1, 2) + math.pow(s2, 2)
    return math.sqrt(distance)

def step2(data, t, zs):
    distance = 0
    index = 0
    for i in range(len(data)):
        temp_distance = dist(data[i], zs[0])
        if temp_distance > distance:
            distance = temp_distance
            index = i
    # 将Z2加入到聚类中心集中
    zs.append(data[index])
    # 计算阈值T
    T = t * distance
    return T

def dbscan():
    all_points = createDataSet()  # 返回经纬度的列表
    E = step2(all_points,0.8,[all_points[0]]) # Eps 是定义密度时的邻域半径，MmPts 为定义核心点时的阈值
    minPts = 10
    # find out the core points
    other_points = []
    core_points = []  # 核心点集合
    plotted_points = []  # 使用到的点   非噪声点
    for point in all_points:
        point.append(0)  # 在点的后面加上第三维度类别，初始类别为 一般
        total = 0
        for otherPoint in all_points:
            distance = dist(otherPoint, point)  # 遍历其他点并计算距离
            if distance <= E:
                total += 1  # 计算当前点的e领域内点的个数

        if total > minPts:
            core_points.append(point)  # 是核心点，添加到列表core
            plotted_points.append(point)  # 将核心点添加到列表 plotted
        else:
            other_points.append(point)  # 不是核心点，添加到其他点

            # find border points

    border_points = [] #边界点
    for core in core_points:  # 遍历核心点
        for other in other_points:  # 遍历非核心点
            if dist(core, other) <= E:
                border_points.append(other)  # 添加到非噪声点集合
                plotted_points.append(other)  # 添加到非噪声点集合
                # implement the algorithm
    cluster_label = 0

    for point in core_points:  # 遍历核心点
        if point[2] == 0:  # 核心点所属类别为0
            cluster_label += 1
            point[2] = cluster_label  # 每遍历一个核心点，类别栏就加1

        for point2 in plotted_points:  # 遍历非噪声点
            distance = dist(point2, point)
            if point2[2] == 0 and distance <= E:  # 非噪声点的类别为0 并且与核心点的距离小于e

                point2[2] = point[2]  # 将核心点的类别赋值给非噪声点
                # print point, point2
                # 在给点分配了相应的标签之后，我们对它们进行分组
    print(point[2])
    print(cluster_label)
    print(len(plotted_points))
    result = [[] for i in range(cluster_label)]
    #for point in plotted_points:

    cluster_list = defaultdict(lambda: [[], []])  # 定义一个字典，默认值是包含两个列表的列表
    for point in plotted_points:
        cluster_list[point[2]][0].append(point[0])  # 类别为键，值得第一个列表是非噪声点的x
        cluster_list[point[2]][1].append(point[1])  # 类别为键，值得第一个列表是非噪声点的y
    i = 0
    for i in range(len(cluster_list)):
        print("----------第" + str(i + 1) + "个聚类----------" + "点数:" + str(len(cluster_list[i])))
        print(cluster_list[i])

    # plot the noise points as well
    noise_points = []
    for point in all_points:
        #如果一个点既不是核心点也不是边界点，那么它就是噪声点
        if not point in core_points and not point in border_points:
            noise_points.append(point)
    noisex = []
    noisey = []
    for point in noise_points:
        noisex.append(point[0])
        noisey.append(point[1])
    print("noise_points:\n"+str(len(noise_points))+'\n'+str(noise_points))

p = dbscan()
