#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jul  9 09:57:55 2019

@author: kevin_y_kuo
"""

# string "in"  => time complexity (best case) : sublinear
# url: https://stackoverflow.com/questions/18139660/python-string-in-operator-implementation-algorithm-and-time-complexity



import sys
import os

def Exports():
    output = sys.stdout                 # store original stdout object for later
    sys.stdout = open('log.txt', 'w') # redirect all prints to this log file
    sys.stdout.close()                # ordinary file object
    sys.stdout = output                # restore print commands to interactive prompt

'''
path_debug = '/Users/kevin_y_kuo/Documents/Log/Amsp_LocalDebugLog.log'
path_event = '/Users/kevin_y_kuo/Documents/Log/Amsp_Event.log'
key_file = '/Users/kevin_y_kuo/Documents/Case/keyword.txt'


text = []
output = sys.stdout      # store original stdout object for later
with open(path_event,'r',encoding="utf-16") as f, open(key_file) as key:
    sys.stdout = open(logDir+'output.txt', 'w')      # redirect all prints to this log file
    keyword = []
    for line in key:
        keyword.append(line.strip())
        
    for line in f:
        #new_line = line.strip().split(",")[4:]     # choose log text
        #str_line = ",".join(new_line)      # list to string
        for index in range(len(keyword)):
            if keyword[index] in line:
                print(line)
sys.stdout.close()                # ordinary file object
sys.stdout = output             # restore print commands to interactive prompt   
'''


#'''
logDir = '/Users/kevin_y_kuo/Documents/Log/'
caseDir = '/Users/kevin_y_kuo/Documents/Case_Single/'
outputDir = '/Users/kevin_y_kuo/Documents/Log_Case_Single/'


for log in os.listdir(logDir):
    if log == ".DS_Store":
        continue
    else:
        logname = log.split(".")[0]
        for case in os.listdir(caseDir):
            if case == ".DS_Store":
                continue
            else:
                casename = case.split(".")[0]
                output = sys.stdout      # store original stdout object for later
                with open(logDir+log,'r', encoding="utf-16") as f, open(caseDir+case) as key:
                    sys.stdout = open(outputDir+logname+'_'+casename+'.txt', 'w')      # redirect all prints to this log file
                    keywords = []
                    for line in key:
                        keywords.append(line.strip())
                    
                    count = 0 #設定一判斷標準，若最後count=0則刪除此檔案，因為檔案為空檔案
                    for line in f:
                        #new_line = line.strip().split(",")[4:]     # choose log text
                        #str_line = ",".join(new_line)      # list to string
                        for keyword in keywords:
                            if keyword in line:
                                count += 1
                                print(line)
                sys.stdout.close()                # ordinary file object
                sys.stdout = output             # restore print commands to interactive prompt   
                
                if count == 0:
                    os.remove(outputDir+logname+'_'+casename+'.txt')
#'''







