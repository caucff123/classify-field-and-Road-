#coding:utf-8
#上面代码加在第一行才有用
#已知两点的经度和纬度，利用经纬度计算计算两点之间的距离
#x1,x2分别表示两个点的经度，y1,y2分别表示两个点的纬度
#s1表示经度弧长距离，s2表示纬度弧长距离
#返回两点之间的距离
import math
def gps_discount(x1,y1,x2,y2):
    s1=(math.cos(int(x1))*(6378137-int(x1)*237.61111)*2*math.pi/360)*(x1-x2)
    s2=111000*(y1-y2)
    return float('%.2f' % math.sqrt(math.pow(s1,2)+math.pow(s2,2)))
print(gps_discount(109.735045,27.136089,109.734723,27.136291))