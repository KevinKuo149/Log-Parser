#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jul 15 16:13:48 2019

@author: kevin_y_kuo
"""


import sys
import os

logDir = '/Users/kevin_y_kuo/Documents/Log/'
caseDir = '/Users/kevin_y_kuo/Documents/Case_Pair/'
outputDir = '/Users/kevin_y_kuo/Documents/Log_Case_Pair/'


for log in os.listdir(logDir):
    if log == ".DS_Store":
        continue
    else:
        logname = log.split(".")[0]
        for case in os.listdir(caseDir):
            casename = case.split(".")[0]
            output = sys.stdout      # store original stdout object for later
            with open(logDir+log,'r', encoding="utf-16") as f, open(caseDir+case) as key:
                sys.stdout = open(outputDir+logname+'_'+casename+'.txt', 'w')      # redirect all prints to this log file
                keyword = []
                for line in key:
                    keyword.append(line.strip())
                
                count = 0  #設定一判斷標準，若最後count=0則刪除此檔案，因為檔案為空檔案
                pair = 0
                line_list = []
                for line in f:
                    if pair == 0:
                        if keyword[0] in line:
                            count += 1
                            pair += 1
                            line_list.append(line)
                        continue
                    
                    if pair == 1:
                        if keyword[0] in line:
                            pair += 1    # 加完pair變成2，會直接跳"if pair==2:"
                        elif keyword[1] in line:
                            pair -= 1
                            line_list = []
                            continue
                        else:
                            line_list.append(line)
                            continue
                    
                    if pair == 2:
                        str_line_list = "\n".join(line_list)
                        print(str_line_list)
                        # 因為pair==2的情況是發生在碰到第二個keyword[0]，elif結束後要回到pair==1才可繼續搜尋
                        pair = 1  
                        # 搜尋到第二次keyword[0]，刪除全部後，再加入此次的line值
                        line_list = []
                        line_list.append(line)
                        str_line_list = []
                
                if pair == 1:   #  到檔案尾時，若pair==1，表示仍有不成對，故也需print出到新文件
                    str_line_list = "\n".join(line_list)
                    print(str_line_list)
                
            sys.stdout.close()                # ordinary file object
            sys.stdout = output             # restore print commands to interactive prompt   
            
            if count == 0:
                os.remove(outputDir+logname+'_'+casename+'.txt')