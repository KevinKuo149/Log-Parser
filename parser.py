#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jul 23 17:59:13 2019

@author: kevin_y_kuo
"""
#%%
import os
import time
import re
import datetime


def getDir():

    logDir = '/Users/kevin_y_kuo/Trend/Log/'
    caseDir = '/Users/kevin_y_kuo/Trend/Case/'
    outputDir = '/Users/kevin_y_kuo/Trend/Output/'
    '''
    logDir = input('Please enter a folder address where "log files" is stored : ')
    caseDir = input('Please enter a folder address where "case files" is stored : ')
    outputDir = input('Please enter a folder address where "you want to output" : ')
    '''
    return logDir, caseDir, outputDir


def matchDate(line):
    matchThis = ""
    matched = re.match(r'\d\d\d\d/\d\d/\d\d\ \d\d:\d\d:\d\d.\d\d\d',line)  # 2018/03/14 13:53:18.266
    if matched:
        matchThis = matched.group()
    else:
        matchThis = "NONE"
    return matchThis


# 不要rename
def sortFiles(logDir):
    date_file_list = []
    for file in os.scandir(logDir):
        if file.name.endswith(".log"):
            #print(f.name)
            t = os.stat(file)
            lastmod_date = time.localtime(t.st_mtime)  #最後修改日期時間
            #print(time.strftime('%Y-%m-%d,%H:%M:%S', lastmod_date))
            date_file_tuple = lastmod_date, file.name
            date_file_list.append(date_file_tuple)
    date_file_list.sort()
    sort_log = []
    for i in range(len(date_file_list)):
        sort_log.append(date_file_list[i][1])
    return sort_log


def testTime(logDir):
    #log_datetime_list = []
    log_datefile_list = []
    for log in os.listdir(logDir):
        if log == ".DS_Store":
            continue
        else:
            with open(logDir+log,'r', encoding="utf-16") as log_file:
                logname, logextension = os.path.splitext(log)
                for line in log_file:
                    date = matchDate(line)
                    if date == "NONE":
                        continue
                    else:
                        date_time_obj = datetime.datetime.strptime(date, '%Y/%m/%d %H:%M:%S.%f')
                        #log_datetime_list.append(date_time_obj)
                        break
                date_file_tuple = date_time_obj, logname
                log_datefile_list.append(date_file_tuple)
    log_datefile_list.sort()
    sort_log = []
    for i in range(len(log_datefile_list)):
        sort_log.append(log_datefile_list[i][1])
    return sort_log
    

def singleParser(f, key, output_file):
    # log single keyword parser implement
    keywords = []
    for line in key:
        keywords.append(line.strip())
    
    count = 0 #設定一判斷標準，若最後count=0則刪除此檔案，因為檔案為空檔案
    for line in f:
        for keyword in keywords:
            if keyword in line:
                count += 1
                output_file.write(line)


def pairedParser(f, key, output_file):
    # log paired keyword parser implement   # 會印出不成對的部分，成對則不印出
    keyword = []
    for line in key:
        keyword.append(line.strip())
    
    count = 0  #設定一判斷標準，若最後count=0則刪除此檔案，因為檔案為空檔案
    pair = 0  # pair為成對與否的判斷依據，初始為0，遇到former則＋1，遇到latter則減1
    line_list = []
    
    
    '''
    檢查是否keyword為空
    if...
    '''
    
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
            str_line_list = "".join(line_list)
            output_file.write(str_line_list)
            # 因為pair==2的情況是發生在碰到第二個keyword[0]，if結束後要回到pair==1才可繼續搜尋
            pair = 1  
            # 搜尋到第二次keyword[0]，刪除全部後，再加入此次的line值
            line_list = []
            line_list.append(line)
            str_line_list = []
            
    if pair == 1:   #  到檔案尾時，若pair==1，表示仍有不成對，故也需print出到新文件
        str_line_list = "".join(line_list)
        output_file.write(str_line_list)



#%%
def main():
    for case in os.listdir(caseDir):
        casename ,caseextension = os.path.splitext(case)
        casename_realname = "_".join(casename.split("_")[1:])
        casename_type = "_".join(casename.split("_")[:1])
        
        output_file = open(outputDir+casename_realname+'.log', 'w', encoding="utf-16")
        
        for log in sort_log:
            if log == ".DS_Store":
                continue
            else:
                logname, logextension = os.path.splitext(log)
                output_file.write('< '+logname+' >\n')
                
                with open(logDir+log,'r', encoding="utf-16") as log_file, open(caseDir+case) as case_file:
                    # 決定要使用哪種parser
                    if casename_type == "single":
                        singleParser(log_file, case_file, output_file)  
                    if casename_type == "pair":
                        pairedParser(log_file, case_file, output_file)
            output_file.write("\n\n\n")
        output_file.close()


#%%
if __name__ == '__main__':
    logDir, caseDir, outputDir = getDir()
    sort_log1 = sortFiles(logDir)
    sort_log = testTime(logDir)
    main()

    
