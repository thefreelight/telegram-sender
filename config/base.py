import time
import re
import os

import sqlite3
import win32gui

# from airtest.core.api import *
# from airtest.cli.parser import cli_setup
# from airtest.core.win.win import *


#创建数据库
conn = sqlite3.connect('linglufa.db')





#带参数的精确查询
def query(sql,*keys):
    db = conn
    cursor = db.cursor()
    cursor.execute(sql,keys)
    result = cursor.fetchall()
    cursor.close()
    return result

#不带参数的模糊查询
def query2(sql):
    db = conn
    cursor = db.cursor()
    cursor.execute(sql)
    result = cursor.fetchall()
    cursor.close()
    return result

#获取当前时间
def current_time():
    return time.strftime("%Y-%m-%d %H:%M:%S",time.localtime())

#更新数据库
def update(sql):
    db = conn
    try:
        cursor = db.cursor()
        cursor.execute(sql)
        db.commit()
    except:
        #发生错误时回滚
        db.rollback()


#获取所有窗口的句柄
def get_all_windows():
    hWnd_list = []
    win32gui.EnumWindows(lambda hWnd, param: param.append(hWnd), hWnd_list)
    # print(hWnd_list)
    return hWnd_list

#根据窗口标题获取窗口句柄
def get_hwnd(title):
    hWnd_list = get_all_windows()
    for i in hWnd_list:
        current_title = win32gui.GetWindowText(i)
        current_class_name = win32gui.GetClassName(i)
        # print(current_title)
        # print(current_class_name)
        if re.match(title,current_title):
            return i,current_title

#判断文件是否存在
def is_txt_exists(filename):
    if os.path.exists(filename):
        with open(filename, 'r', encoding='utf-8') as f:
            f = open(filename, 'r', encoding='utf-8')
            return f
    else:
        with open(filename, 'w+', encoding='utf-8') as f:
            print('文件创建成功')
            f = open(filename, 'r', encoding='utf-8')
            return f




























