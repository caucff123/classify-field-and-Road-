#coding:utf-8
import math
def calculate_triangle_area(point_a, point_b, point_c):
    """利用边长计算面积"""
    triangle_area = 0
    a=point_a
    b=point_b
    c=point_c
    if a + b > c and a + c > b and b + c > a:
        e = (a + b + c) / 2
        triangle_area = math.sqrt(e * (e - a) * (e - b) * (e - c))
    return abs(triangle_area)
print(calculate_triangle_area(669.02,648.24,30.45))