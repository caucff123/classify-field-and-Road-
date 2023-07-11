# coding=utf-8
# 对数据进行导入,将其转化成所需的数据形式data=[[],[],...,[]]
# 先使用最大最小距离确定分多少类，在使用近邻聚类法将剩余的点分别分到各个类中
import pandas as pd
import numpy as np
def KNN():
    for i in range(5):
        data = pd.read_csv('点集.csv', index_col=0)
        #data1=data[data['纬度']<32.7522]
        #data1.to_excel(r'C:\Users/一般\Desktop\5(一般).xlsx')
        data = data.values.tolist()

        import math
        # 寻找Z2,并计算阈值T
        def step2(data, t, zs):
            distance = 0
            index = 0
            for i in range(len(data)):
                temp_distance = get_distance(data[i], zs[0])
                if temp_distance > distance:
                    distance = temp_distance
                    index = i
            # 将Z2加入到聚类中心集中
            zs.append(data[index])
            # 计算阈值T
            T = t * distance
            return T

        # 分类
        # 样本形式为data=[[],[],...,[]]
        # zs为选取的第一个聚类中心,T为距离阈值
        # 通过classify函数，基于距离实现分类功能

        def classify(data, zs, T):
            result = [[] for i in range(len(zs))]
            for aData in data:
                min_distance = T
                index = 0
                for i in range(len(zs)):
                    temp_distance = get_distance(aData, zs[i])
                    if temp_distance < min_distance:
                        min_distance = temp_distance
                        index = i
                result[index].append(aData)
            return result

        """
        利用经纬度计算两点间的距离
        def gps_discount(x1,y1,x2,y2):
            s1=(math.cos(int(x1))*(6378137-int(x1)*237.61111)*2*math.pi/360)*(x1-x2)
            s2=111000*(y1-y2)
            return float('%.2f' % math.sqrt(math.pow(s1,2)+math.pow(s2,2)))
        print(gps_discount(121.9768,33.9590,113.9681,29.0587))
        """

        # 计算两个模式样本之间的欧式距离
        def get_distance(data1, data2):
            s1 = (math.cos(int(data1[0])) * (6378137 - int(data1[0]) * 237.61111) * 2 * math.pi / 360) * (
                    data1[0] - data2[0])
            s2 = 111000 * (data1[1] - data2[1])
            distance = math.pow(s1, 2) + math.pow(s2, 2)
            return math.sqrt(distance)

        # print(get_distance([104.04394137,30.657982840],[104.04384447,30.65814383]))

        # coding=utf-8

        # 近邻聚类算法的Python实现
        # 数据集形式data=[[],[],...,[]]
        # 聚类结果形式result=[[[],[],...],[[],[],...],...]
        # 其中[]为一个模式样本，[[],[],...]为一个聚类

        def knn_cluster(data, t):
            # data：数据集，t：距离阈值
            # 算法描述中的介绍的是在寻找聚类中心的同时进行聚类，本次实现中并未采取这种方式，
            # 原因是同时进行的话要既要考虑聚类中心，又要考虑某个类，实现较为麻烦，
            # 此次采取与上次最大最小距离算法相同的方式，先寻找聚类中心，再根据最近邻原则分类，
            # 两种方式实现效果是相同的，同时又可以直接利用最大最小距离聚类算法中写好的classify()分类方法

            zs = [data[0]]  # 聚类中心集，选取第一个模式样本作为第一个聚类中心Z1
            # 计算聚类中心
            get_clusters(data, zs, t)
            # 分类
            result = classify(data, zs, t)
            return result

        # data为数据集,zs为选取的第一个数据中心，t为距离阈值
        def get_clusters(data, zs, t):
            for aData in data:
                min_distance = get_distance(aData, zs[0])
                for i in range(0, len(zs)):
                    distance = get_distance(aData, zs[i])
                    if distance < min_distance:
                        min_distance = distance
                if min_distance > t:
                    zs.append(aData)

        t = step2(data, 0.3, [data[0]])
        result = knn_cluster(data, t)
        end_result = []
        for i in range(len(result)):
            print("----------第" + str(i + 1) + "个聚类----------" + "点数:" + str(len(result[i])))
            print(result[i])
            if (len(result[i]) / len(data) > 0.01):
                for r_point in result[i]:
                    end_result.append(r_point)

        # 分类之后，如果点的个数少于某个值，则将这个类舍去
        end_data = pd.DataFrame(end_result, columns=['经度', '纬度'])
        end_data.to_csv('点集.csv')

    import matplotlib.pyplot as plt
    import random
    def Colourlist_Generator(n):
        Rangelist = ['一般', '2', '3', '4', '5', '6', '7', '8', '9', 'A', 'B', 'C', 'D', 'E', 'F']
        n = int(n)
        Colours = []  # 空列表，用于插入n个表示颜色的字符串
        j = 1
        while j <= n:  # 循环n次，每次在0到14间随机生成6个数，在加“#”符号，次次插入列表
            colour = ""  # 空字符串，用于插入字符组成一个7位的表示颜色的字符串（第一位为#，可最后添加）
            for i in range(6):
                colour += Rangelist[random.randint(0, 14)]  # 用randint生成0到14的随机整数作为索引
            colour = "#" + colour  # 最后加上不变的部分“#”
            Colours.append(colour)
            j = j + 1
        return Colours

    colors = Colourlist_Generator(len(result))
    for index in range(len(result)):
        x = []
        y = []
        for point in result[index]:
            x.append(point[0])
            y.append(point[1])
        plt.scatter(x, y, c=colors[index])
    plt.show()
KNN()











