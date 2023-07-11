#coding=utf-8
import math
import re

import pandas as pd

#定义一个点类，以及一些基本功能
class Point:
    #x表示经度，y表示纬度
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
                self.x- other_point.x)
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
        points=pd.read_csv('外轮廓点集.csv',index_col=0)
        points = points.values.tolist()
        for point in points:
            point=(point[0],point[1])
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
    """
    #计算周长
    def perimeter(self):
        perimeter = 0
        points = self.vertices + [self.vertices[0]]
        for i in range(len(self.vertices)):
            perimeter += points[i].calculate_distance(points[i + 1])
        return perimeter


    def area(self):
        n = len(self.vertices)
        if n < 3:
            return 0
        area = 0
        for i in range(n - 2):
            # 以第一个坐标点为原点，将多边形分割为n-2个三角形，分别计算每个三角形面积后累加得多边形面积
            #计算凸多边形的面积
            area += self.calculate_triangle_area(self.vertices[0], self.vertices[i + 1], self.vertices[i + 2])
        return area

    @staticmethod
    def calculate_triangle_area(point_a, point_b, point_c):
        """利用边长计算面积"""
        triangle_area=0
        a=Point.calculate_distance(point_a,point_b)
        b=Point.calculate_distance(point_a,point_c)
        c=Point.calculate_distance(point_b,point_c)
        if a + b > c and a + c > b and b + c > a:
            e = (a + b + c) / 2
            triangle_area = math.sqrt(e * (e - a) * (e - b) * (e - c))
        return abs(triangle_area)


if __name__ == "__main__":
    polygon1 = Polygon()
    print("面积：{:.3f},周长：{:.3f}".format(polygon1.area(), polygon1.perimeter()))