#coding:utf-8
import tkinter as tk
import numpy as np
from tkinter import Button, LEFT
from tkinter.filedialog import askopenfile
import pandas as pd
windows=tk.Tk()
windows.title('农田地表外轮廓提取系统')
windows.geometry('400x250')
Buttonframe=tk.Frame(windows)
Buttonframe.pack(anchor='nw')
b1=tk.Button(Buttonframe,text='主界面',activebackground='red')
b1.grid(row=0,column=0)
def jump():
    windows1=tk.Tk()
    windows1.title('面积计算')
    windows1.geometry('400x250')
    label1=tk.Label(windows1,text='输入轨迹点集',font=12)
    label1.pack()

    #在创建多个窗口后，使用StringVar方法要添加master参数
    #传入点集资料
    path_var = tk.StringVar(windows1)
    path_entry = tk.Entry(windows1, textvariable=path_var)
    path_entry.place(x=120, y=40, anchor='nw')
    def click():
        file_name = tk.filedialog.askopenfilename()
        path_var.set(file_name)
    tk.Button(windows1, text='选择点集文件', command=click).place(x=10, y=40, anchor='nw')


    #传入精度参数，设置k值
    accuracy=tk.Label(windows1,text='设置精度k值:')
    accuracy.place(x=10, y=100,anchor='nw')
    accuracy_entry=tk.Entry(windows1)
    accuracy_entry.place(x=120, y=100)


    #将农田面积结果以平方米和亩数分别进行表示
    area_Lable=tk.Label(windows1,text='农田面积:')
    area_Lable.place(x=10, y=160,anchor='nw')
    area_var1=tk.StringVar(windows1)
    area_entry1=tk.Entry(windows1,textvariable=area_var1)
    area_entry1.place(x=120, y=160, anchor='nw')

    area_var2 = tk.StringVar(windows1)
    area_entry2 = tk.Entry(windows1, textvariable=area_var2)
    area_entry2.place(x=120, y=200, anchor='nw')


    windows1.mainloop()


b2=tk.Button(Buttonframe,text='面积计算',activebackground='red',command=jump)
b2.grid(row=0,column=1)
Labelframe=tk.Frame(windows)
Labelframe.pack()
Label1=tk.Label(Labelframe,text='地表外轮廓提取系统',font=12)
Label1.grid(row=0,column=0)
Label2=tk.Label(Labelframe,text='使用说明',font=10)
Label2.grid(row=1,column=0)
message1=''' 一般.本系统主要用于计算地表外轮廓面积，需要一组GPS轨迹点作为数据计算。
2.面积计算:选择包含轨迹点的excel文件,设置计算精确度k值，运行并查看结果及其面积'''
Label3=tk.Message(Labelframe,text=message1,bg='yellow')
Label3.grid(row=2,column=0)
windows.mainloop()