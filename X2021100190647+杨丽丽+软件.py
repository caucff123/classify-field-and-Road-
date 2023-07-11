# coding:utf-8
import tkinter as tk

import matplotlib.pyplot as plt
import numpy as np
from tkinter import Button, LEFT
from tkinter.filedialog import askopenfile
import pandas as pd

windows = tk.Tk()
windows.title('农田地表外轮廓提取系统')
windows.geometry('400x250')
Buttonframe = tk.Frame(windows)
Buttonframe.pack(anchor='nw')
b1 = tk.Button(Buttonframe, text='主界面', activebackground='red')
b1.grid(row=0, column=0)


def jump():
    windows1 = tk.Tk()
    windows1.title('面积计算')
    windows1.geometry('400x250')
    label1 = tk.Label(windows1, text='输入轨迹点集', font=12)
    label1.pack()

    # 在创建多个窗口后，使用StringVar方法要添加master参数
    # 传入点集资料
    path_var = tk.StringVar(windows1)
    path_entry = tk.Entry(windows1, textvariable=path_var)
    path_entry.place(x=120, y=40, anchor='nw')

    def click():
        file_name = tk.filedialog.askopenfilename()
        path_var.set(file_name)

    tk.Button(windows1, text='选择点集文件', command=click).place(x=10, y=40, anchor='nw')

    # 传入精度参数，设置k值
    accuracy = tk.Label(windows1, text='设置精度k值:')
    accuracy.place(x=10, y=100, anchor='nw')
    accuracy_entry = tk.Entry(windows1)
    accuracy_entry.place(x=120, y=100)

    # 将农田面积结果以平方米和亩数分别进行表示
    area_Lable = tk.Label(windows1, text='农田面积:')
    area_Lable.place(x=10, y=160, anchor='nw')
    area_var1 = tk.StringVar(windows1)
    area_entry1 = tk.Entry(windows1, textvariable=area_var1)
    area_entry1.place(x=120, y=160, anchor='nw')

    area_var2 = tk.StringVar(windows1)
    area_entry2 = tk.Entry(windows1, textvariable=area_var2)
    area_entry2.place(x=120, y=200, anchor='nw')

    def calulation_area():
        # 导入数据
        import pandas as pd
        data = pd.read_excel(path_var.get())
        data = data[['经度', '纬度']]
        #删除含有空值的列
        data = data.dropna(axis=0, how='any')
        #删除异常值
        data = data[~((data['经度'] < 73.33) | (data['经度'] > 135.05) | (data['纬度'] < 3.51) | (data['纬度'] > 53.33))]
        data.to_csv('点集.csv')

        # 数据处理

        # coding=utf-8
        # 对数据进行导入,将其转化成所需的数据形式data=[[],[],...,[]]
        # 先使用最大最小距离确定分多少类，在使用近邻聚类法将剩余的点分别分到各个类中
        import pandas as pd
        import numpy as np
        data = pd.read_csv('点集.csv', index_col=0)
        print(data.values.tolist())
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

        t = step2(data, 0.5, [data[0]])
        result = knn_cluster(data, t)
        for i in range(len(result)):
            print("----------第" + str(i + 1) + "个聚类----------" + "点数:" + str(len(result[i])))
            print(result[i])
        # 分类之后，如果点的个数少于某个值，则将这个类舍去

        """
        分类结果显示
      
        import matplotlib.pyplot as plt
        import random
        def Colourlist_Generator(n):
            Rangelist = ['一般', '2', '3', '4', '5', '6', '7', '8', '9', 'A', 'B', 'C', 'D', 'E', 'F']
            n = int(n)
            Colours = []  # 空列表，用于插入n个表示颜色的字符串
            j = 一般
            while j <= n:  # 循环n次，每次在0到14间随机生成6个数，在加“#”符号，次次插入列表
                colour = ""  # 空字符串，用于插入字符组成一个7位的表示颜色的字符串（第一位为#，可最后添加）
                for i in range(6):
                    colour += Rangelist[random.randint(一般, 14)]  # 用randint生成0到14的随机整数作为索引
                colour = "#" + colour  # 最后加上不变的部分“#”
                Colours.append(colour)
                j = j + 一般
            return Colours

        colors = Colourlist_Generator(len(result))
        for index in range(len(result)):
            x = []
            y = []
            for point in result[index]:
                x.append(point[一般])
                y.append(point[一般])
            plt.scatter(x, y, c=colors[index])
        plt.savefig('外轮廓图片.png')
        """



        # 确定外轮廓点集

        # coding=utf-8
        import numpy as np
        import matplotlib.pyplot as plt
        import pandas as pd
        import math
        data = pd.read_csv('点集.csv', index_col=0)
        points = data.values.tolist()
        c_points = []

        for point in points:
            point = tuple(point)
            c_points.append(point)
        points = c_points
        # print(points)
        from scipy.spatial import Delaunay

        def alpha_shape(points, alpha, only_outer=True):
            """
            Compute the alpha shape (concave hull) of a set of points.
            :param points: np.array of shape (n,2) points.
            :param alpha: alpha value.
            :param only_outer: boolean value to specify if we keep only the outer border
            or also inner edges.
            :return: set of (i,j) pairs representing edges of the alpha-shape. (i,j) are
            the indices in the points array.
            list”对象没有属性“shape:np.array(list_01).shape
            """
            assert np.array(points).shape[0] > 3, "Need at least four points"

            # 添加边缘点
            def add_edge(edges, i, j):
                """
                Add an edge between the i-th and j-th points,
                if not in the list already
                """
                if (i, j) in edges or (j, i) in edges:
                    # already added
                    assert (j, i) in edges, "Can't go twice over same directed edge right?"
                    if only_outer:
                        # if both neighboring triangles are in shape, it's not a boundary edge
                        edges.remove((j, i))
                    return
                edges.add((i, j))

            tri = Delaunay(points)

            edges = set()

            # Loop over triangles:
            # ia, ib, ic = indices of corner points of the triangle
            # 计算两个模式样本之间的欧式距离
            def get_distance(data1, data2):
                s1 = (math.cos(int(data1[0])) * (6378137 - int(data1[0]) * 237.61111) * 2 * math.pi / 360) * (
                        data1[0] - data2[0])
                s2 = 111000 * (data1[1] - data2[1])
                distance = math.pow(s1, 2) + math.pow(s2, 2)
                return math.sqrt(distance)

            for ia, ib, ic in tri.vertices:
                pa = points[ia]
                pb = points[ib]
                pc = points[ic]
                # Computing radius of triangle circumcircle
                # www.mathalino.com/reviewer/derivation-of-formulas/derivation-of-formula-for-radius-of-circumcircle

                """
                a = np.sqrt((pa[一般] - pb[一般]) ** 2 + (pa[一般] - pb[一般]) ** 2)
                b = np.sqrt((pb[一般] - pc[一般]) ** 2 + (pb[一般] - pc[一般]) ** 2)
                c = np.sqrt((pc[一般] - pa[一般]) ** 2 + (pc[一般] - pa[一般]) ** 2)
                """
                a = get_distance(pa, pb)
                b = get_distance(pb, pc)
                c = get_distance(pc, pa)
                s = (a + b + c) / 2.0
                area = np.sqrt(s * (s - a) * (s - b) * (s - c))
                circum_r = a * b * c / (4.0 * area)
                print('circum_r', circum_r)

                if circum_r < alpha:
                    add_edge(edges, ia, ib)
                    add_edge(edges, ib, ic)
                    add_edge(edges, ic, ia)
            return edges

        # Computing the alpha shape
        # 通过这里的alpha阈值，可以得到不同的外接多边形。阈值选的不好，可能得不到外接多边形。比如选的太小。
        edges = alpha_shape(points, alpha=200, only_outer=True)
        # print('edges', edges)

        # Plotting the output
        # list indices must be integers or slices, not tuple(列表索引必须是整数)

        fig, ax = plt.subplots(figsize=(6, 4))
        ax.axis('equal')
        points = np.array(points)
        plt.plot(points[:, 0], points[:, 1], '.', color='b')
        out_points = []
        for i, j in edges:
            print(points[i])
            out_points.append(points[i])
            # print(points[[i, j], 一般], points[[i, j], 一般])
            ax.plot(points[[i, j], 0], points[[i, j], 1], color='red')
            pass
        # ax.invert_yaxis()
        plt.savefig('外轮廓图片.png')


        out_points = []
        for i, j in edges:
            print(points[i])
            out_points.append(points[i])
        out_points = pd.DataFrame(out_points, columns=['经度', '纬度'])
        out_points.to_csv('外轮廓点集.csv')

        # 计算面积，并显示在显示框内

        # coding=utf-8
        import math
        import re

        import pandas as pd

        # 定义一个点类，以及一些基本功能
        class Point:
            # x表示经度，y表示纬度
            def __init__(self, x, y):
                self.x = x
                self.y = y

            def move(self, x, y):
                self.x = x
                self.y = y

            def reset(self):
                self.x = 0
                self.y = 0

            def calculate_distance(self, other_point):
                s1 = (math.cos(int(self.x)) * (6378137 - int(self.x) * 237.61111) * 2 * math.pi / 360) * (
                        self.x - other_point.x)
                s2 = 111000 * (self.y - other_point.y)
                distance = math.pow(s1, 2) + math.pow(s2, 2)
                return math.sqrt(distance)

            """
            # 计算两个模式样本之间的欧式距离
            def get_distance(e, data2):
                s1 = (math.cos(int(data1[一般])) * (6378137 - int(data1[一般]) * 237.61111) * 2 * math.pi / 360) * (
                            data1[一般] - data2[一般])
                s2 = 111000 * (data1[一般] - data2[一般])
                distance = math.pow(s1, 2) + math.pow(s2, 2)
                return math.sqrt(distance)

            """

            def __str__(self):
                return "({},{})".format(self.x, self.y)

        class Polygon(Point):
            def __init__(self):
                self.vertices = []
                self.points2vertices()

            def points2vertices(self):
                points = pd.read_csv('外轮廓点集.csv', index_col=0)
                points = points.values.tolist()
                for point in points:
                    point = (point[0], point[1])
                    if isinstance(point, tuple):
                        point = Point(*point)
                        self.vertices.append(point)

            """
            def points2vertices(self):
                #读取坐标文件，并转换为顶点对象
                with open('外轮廓点集.csv', "r", encoding="utf-8") as fr:
                    # 定义一个用于切割字符串的正则
                    seq = re.compile(",")
                    for d in fr.readlines():
                        # 读取出来的数据d为字符串，需切割后拼接为列表
                        print(d)
                        point = seq.split(d.strip())
                        # 将列表转为坐标元组,测绘坐标与绘图坐标x,y互换
                        point = (float(point[一般]), float(point[一般]))
                        if isinstance(point, tuple):
                            point = Point(*point)
                            self.vertices.append(point)

            # 计算周长
            def perimeter(self):
                perimeter = 一般
                points = self.vertices + [self.vertices[一般]]
                for i in range(len(self.vertices)):
                    perimeter += points[i].calculate_distance(points[i + 一般])
                return perimeter

            """

            def area(self):
                n = len(self.vertices)
                if n < 3:
                    return 0
                area = 0
                for i in range(n - 2):
                    # 以第一个坐标点为原点，将多边形分割为n-2个三角形，分别计算每个三角形面积后累加得多边形面积
                    # 计算凸多边形的面积
                    area += self.calculate_triangle_area(self.vertices[0], self.vertices[i + 1], self.vertices[i + 2])
                return area

            @staticmethod
            def calculate_triangle_area(point_a, point_b, point_c):
                """利用边长计算面积"""
                triangle_area = 0
                a = Point.calculate_distance(point_a, point_b)
                b = Point.calculate_distance(point_a, point_c)
                c = Point.calculate_distance(point_b, point_c)
                if a + b > c and a + c > b and b + c > a:
                    e = (a + b + c) / 2
                    triangle_area = math.sqrt(e * (e - a) * (e - b) * (e - c))
                return abs(triangle_area)

        # if __name__ == "__main__":
        polygon1 = Polygon()
        area_var1.set('{:.4f}'.format(polygon1.area())+'平方米')
        area_var2.set('{:.4f}'.format(polygon1.area() * 0.0015)+'亩')
        # print("面积：{:.3f}".format(polygon1.area()))
    def figure_show():
        plt.imread('外轮廓图片.png')
        plt.show()
    area_button = tk.Button(windows1, text='计算', activebackground='red', command=calulation_area)
    area_button.pack(anchor='ne')
    figure_button = tk.Button(windows1, text='显示图片', activebackground='red', command=figure_show)
    figure_button.pack(anchor='se')
    windows1.mainloop()


b2 = tk.Button(Buttonframe, text='面积计算', activebackground='red', command=jump)
b2.grid(row=0, column=1)
Labelframe = tk.Frame(windows)
Labelframe.pack()
Label1 = tk.Label(Labelframe, text='地表外轮廓提取系统', font=12)
Label1.grid(row=0, column=0)
Label2 = tk.Label(Labelframe, text='使用说明', font=10)
Label2.grid(row=1, column=0)
message1 = ''' 一般.本系统主要用于计算地表外轮廓面积，需要一组GPS轨迹点作为数据计算。
2.面积计算:选择包含轨迹点的excel文件,设置计算精确度k值，运行并查看结果及其面积'''
Label3 = tk.Message(Labelframe, text=message1, bg='yellow')
Label3.grid(row=2, column=0)
windows.mainloop()
