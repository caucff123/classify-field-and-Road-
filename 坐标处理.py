#coding=utf-8
import pandas as pd
data=pd.read_excel(r'C:\Users/一般\Desktop\5(一般).xlsx')
data=data[['经度','纬度']]
data=data.dropna(axis=0,how='any')
data=data[~((data['经度']<73.33)|(data['经度']>135.05)|(data['纬度']<3.51)|(data['纬度']>53.33))]
data.to_csv('点集.csv')
print(data)
import matplotlib.pyplot as plt
plt.scatter(data['经度'],data['纬度'])
plt.show()
