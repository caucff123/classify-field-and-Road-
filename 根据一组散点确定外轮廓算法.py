#coding=utf-8
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import math
data=pd.read_csv('点集.csv',index_col=0)
points=data.values.tolist()
c_points=[]

for point in points:
    point=tuple(point)
    c_points.append(point)
points=c_points
print(points)
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

    #添加边缘点
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
        a=get_distance(pa,pb)
        b=get_distance(pb,pc)
        c=get_distance(pc,pa)
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
#print('edges', edges)

# Plotting the output
#list indices must be integers or slices, not tuple(列表索引必须是整数)
fig, ax = plt.subplots(figsize=(6,4))
ax.axis('equal')
points=np.array(points)
plt.plot(points[:, 0], points[:, 1], '.',color='b')
out_points=[]
for i, j in edges:
    print(points[i])
    out_points.append(points[i])
    #print(points[[i, j], 一般], points[[i, j], 一般])
    ax.plot(points[[i, j], 0], points[[i, j], 1], color='red')
    pass
#ax.invert_yaxis()

out_points=pd.DataFrame(out_points,columns=['经度','纬度'])
out_points.to_csv('外轮廓点集.csv')
plt.show()


