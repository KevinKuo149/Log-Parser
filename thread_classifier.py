#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jul 12 15:10:39 2019

@author: kevin_y_kuo
"""

import os
import re

#print r"\n"


def matchDate(line):
    matchThis = ""
    matched = re.match(r'\d\d\d\d/\d\d/\d\d\ \d\d:\d\d:\d\d',line)  # 2018/03/14 13:53:18.266
    if matched:
        matchThis = line
    else:
        matchThis = "NONE"
    return matchThis


def getMdate(file):
    import time

    # os.stat return properties of a file
    tmpTime = time.localtime(os.stat(file).st_mtime)
    return time.strftime('%Y%m%d', tmpTime)



logDir = "/Users/kevin_y_kuo/Documents/Log/"
outputDir = '/Users/kevin_y_kuo/Documents/Thread/'


#%%
# 讀取檔案修改日期
import time 
#import os

date_file_list = []
for f in os.scandir(logDir):
    #form = f.name.split('.')[1]
    if f.name.endswith(".log"):
        print(f.name)
        t=os.stat(f)
        lastmod_date = time.localtime(t.st_mtime)  #最後修改日期時間
        print(time.strftime('%Y-%m-%d,%H:%M:%S', lastmod_date))
        date_file_tuple = lastmod_date, f.name
        date_file_list.append(date_file_tuple)
date_file_list.sort()
#print(date_file_list[0][1])



#%%
# 依照時間日期重新命名並排序
x = 0
for sfile in date_file_list:
    NewFileName = str(x).zfill(3) + '-' + sfile[1]
    os.rename(logDir+sfile[1],logDir+NewFileName)
    x += 1




#%%
# 比對所有file，找出不同的tread ID
matrix_str = ""
matrix_list = []
count = 0
for log in os.listdir(logDir):
    if log == ".DS_Store":
        continue
    else:
        with open(logDir+log,'r', encoding="utf-16") as f:
            for line in f:
                line = matchDate(line)
                if line == "NONE":
                    continue
                else:
                    new_line = line.strip().split(",")[1:2]  # 取出[process:thread]部分
                    str_line = ",".join(new_line)        
                    if count == 0:
                        matrix_str += str_line
                        matrix_list.append(str_line)
                        count += 1        
                    if str_line in matrix_str:
                        continue
                    else:
                        matrix_str += str_line
                        matrix_list.append(str_line)


#%%

import sys
# 依照不同threadID創建檔案
for thread in matrix_list: 
    output = sys.stdout
    sys.stdout = open(outputDir+thread+'.txt', 'w')
    for log in os.listdir(logDir):
        if log == ".DS_Store":
            continue
        else:
            with open(logDir+log,'r', encoding="utf-16") as f:
                for line in f:
                    if thread in line:
                        print(line)
    sys.stdout.close()                # ordinary file object
    sys.stdout = output

        
  

#%%    
'''
path_debug = '/Users/kevin_y_kuo/Documents/Log/Amsp_LocalDebugLog.log'

#test = []
matrix = ""
count = 0
with open(path_debug,'r', encoding="utf-16") as f:
    for line in f:
        line = matchDate(line)
        #test.append(line)
        if line == "NONE":
            continue
        else:
            new_line = line.strip().split(",")[1:2]
            str_line = ",".join(new_line)        
            if count == 0:
                matrix += str_line
                count += 1        
            if str_line in matrix:
                continue
            else:
                matrix += str_line
'''         

