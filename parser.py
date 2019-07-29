#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jul 23 17:59:13 2019

@author: kevin_y_kuo
"""

import os
import re
import datetime
import csv
from collections import Counter



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


# 依log檔內第一個日期為依據，對檔案進行排序
def datetime_Sortfile(logDir):
    log_datefile_list = []
    for log in os.listdir(logDir):
        if log == ".DS_Store":
            continue
        else:
            with open(logDir+log,'r', encoding="utf-16") as log_file:
                for line in log_file:
                    date = matchDate(line)
                    if date == "NONE":
                        continue
                    else:
                        date_time_obj = datetime.datetime.strptime(date, '%Y/%m/%d %H:%M:%S.%f')
                        #log_datetime_list.append(date_time_obj)
                        break
                date_file_tuple = date_time_obj, log
                log_datefile_list.append(date_file_tuple)
    log_datefile_list.sort()
    sort_log = []
    for i in range(len(log_datefile_list)):
        sort_log.append(log_datefile_list[i][1])
    return sort_log



def single_Parser(log_file, keyword_list, temp_log):
    # log single keyword parser implement
    count = 0 #設定一判斷標準，若最後count=0則刪除此檔案，因為檔案為空檔案
    for line in log_file:
        for one_keyword in keyword_list:
            if one_keyword in line:
                count += 1
                temp_log += line
                continue
    return temp_log, count

def catch_Parser(log_file, keyword_list, temp_log):
    count = 0
    catch_area = ""
    for line in log_file:
        if keyword_list[0] in line and keyword_list[1] in line:
            temp_log += line
            count += 1
            catch_area += (line.split(keyword_list[0])[1].split(keyword_list[1])[0] + '.exe\n')
    return temp_log, count, catch_area

def exclude_Parser(log_file, keyword_list, temp_log):
    count = 0
    for line in log_file:
        for one_keyword in keyword_list:
            if one_keyword in line:
                count += 1
            else:
                temp_log += line
    return temp_log, count
                


def notpaired_Parser(log_file, keyword_list, temp_log):
    # log paired keyword parser implement   # 會印出不成對的部分，成對則不印出
    '''
    keyword = []
    for line in key:
        keyword.append(line.strip())
    '''
    count = 0  #設定一判斷標準，若最後count=0則刪除此檔案，因為檔案為空檔案
    pair = 0  # pair為成對與否的判斷依據，初始為0，遇到former則＋1，遇到latter則減1
    line_list = []
    
    
    '''
    檢查是否keyword為空
    if...
    '''
    
    for line in log_file:
        if pair == 0:
            if keyword_list[0] in line:
                count += 1
                pair += 1
                line_list.append(line)
            continue
        if pair == 1:
            if keyword_list[0] in line:
                pair += 1    # 加完pair變成2，會直接跳"if pair==2:"
            elif keyword_list[1] in line:
                pair -= 1
                line_list = []
                continue
            else:
                line_list.append(line)
                continue
        if pair == 2:
            str_line_list = "".join(line_list)
            temp_log = temp_log + str_line_list
            #output_file.write(str_line_list)
            # 因為pair==2的情況是發生在碰到第二個keyword[0]，if結束後要回到pair==1才可繼續搜尋
            pair = 1  
            # 搜尋到第二次keyword[0]，刪除全部後，再加入此次的line值
            line_list = []
            line_list.append(line)
            str_line_list = []
            
    if pair == 1:   #  到檔案尾時，若pair==1，表示仍有不成對，故也需print出到新文件
        str_line_list = "".join(line_list)
        #output_file.write(str_line_list)
        temp_log = temp_log + str_line_list
    return temp_log, count




def main():
    for case in os.listdir(caseDir):
        #print(case)
        casename ,caseextension = os.path.splitext(case)  # ex: casename=>"single_crash" ; caseextension=>".txt"
        casename_realname = "_".join(casename.split("_")[1:])  # casename_realname=>"crash"
        casename_type = "_".join(casename.split("_")[:1])  # casename_type=>"single"
        
        # temporary storage keywords
        keyword_list = []
        with open(caseDir+case) as case_file:
            for line in case_file:
                keyword_list.append(line.strip())   
        
        output_file = open(outputDir+casename_realname+'.log', 'w', encoding="utf-16")  # create output file
        catch_text = ""
        boolean = bool(0)
        
        for log in sort_log:
            temp_log = ""
            if log == ".DS_Store":
                continue
            else:
                logname, logextension = os.path.splitext(log)
                
                with open(logDir+log,'r', encoding="utf-16") as log_file:
                    # Design to use which parser 
                    if casename_type == "single":
                        temp_log, count = single_Parser(log_file, keyword_list, temp_log)  
                    if casename_type == "notpair":
                        temp_log, count = notpaired_Parser(log_file, keyword_list, temp_log)
                    if casename_type == "catch":
                        temp_log, count, catch_area = catch_Parser(log_file, keyword_list, temp_log)   
                        catch_text += catch_area
                    if casename_type == "exclude":
                        temp_log, count = exclude_Parser(log_file, keyword_list, temp_log)

            # print output data on the output file
            if temp_log != "":
                boolean = bool(1)
                output_file.write('< '+logname+' >  ' + casename_realname +' counting:'+ str(count) +'\n')
                output_file.write(temp_log)
                output_file.write('\n\n\n')
        output_file.close()
        # delete the empty file
        if not boolean == bool(1):
            os.remove(outputDir+casename_realname+'.log')
            
        if casename_type == "catch" and catch_text != "":
            catch_list = catch_text.split('\n')
            catch_counting = Counter(catch_list)
            with open(outputDir+casename_realname+'.csv', 'w') as csv_file:
                w = csv.writer(csv_file)
                w.writerows(catch_counting.items())
    



if __name__ == '__main__':
    logDir, caseDir, outputDir = getDir()
    sort_log = datetime_Sortfile(logDir)
    main()

    