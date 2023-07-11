#coding=utf-8
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
data = pd.read_csv('点集.csv', index_col=0)
plt.scatter(data['经度'], data['纬度'])
plt.show()