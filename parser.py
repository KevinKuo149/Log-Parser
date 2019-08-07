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


def choose_Parser(log_file, casetype, keyword_list, catch_text):
    temp_log = ""
    # Design to use which parser 
    if casetype == "single":
        temp_log, count = single_Parser(log_file, keyword_list, temp_log)
        return temp_log, count
    if casetype == "unpair":
        temp_log, count = unpaired_Parser(log_file, keyword_list, temp_log)
        return temp_log, count
    if casetype == "exclude":
        temp_log, count = exclude_Parser(log_file, keyword_list, temp_log)
        return temp_log, count
    if casetype == "seconds":
        temp_log, count = seconds_Parser(log_file, keyword_list, temp_log)
        return temp_log, count
    if casetype == "catch":
        temp_log, count, catch_area = catch_Parser(log_file, keyword_list, temp_log)   
        catch_text += catch_area
        return temp_log, count, catch_text
    

def single_Parser(log_file, keyword_list, temp_log):
    # log single keyword parser implement
    count = 0
    for line in log_file:
        for one_keyword in keyword_list:
            if one_keyword in line:
                count += 1
                temp_log += line
                break
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
                

def seconds_Parser(log_file, keyword_list, temp_log):
    # re.findall(r'(\d*\.\d*).seconds',string)
    # re.findall(r'(\d*).milli seconds',string)
    count = 0
    
    for line in log_file:
        if keyword_list[1] in line:
            count += 1
            if int("".join(re.findall(r'(\d*).milli seconds',line))) >= 1000:
                temp_log += "-----------------------long seconds-------------------------\n"
            temp_log += line
        
        elif keyword_list[0] in line:
            count += 1
            if ("".join(re.findall(r'(\d*\.\d*).seconds',line))) != "":
                if float("".join(re.findall(r'(\d*\.\d*).seconds',line))) >= 1:
                    temp_log += "-----------------------long seconds-------------------------\n"
                temp_log += line
        
    return temp_log, count
            

def unpaired_Parser(log_file, keyword_list, temp_log):
    # log unpaired keyword parser implement
    count = 0  
    pair = 0  # pair為成對與否的判斷依據，初始為0，遇到former則＋1，遇到latter則減1
    line_list = []
    
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


def caseData(case, caseDir):
    casename ,caseextension = os.path.splitext(case)  # ex: casename=>"single_crash" ; caseextension=>".txt"
    casename_realname = "_".join(casename.split("_")[1:])  # casename_realname=>"crash"
    casename_type = "_".join(casename.split("_")[:1])  # casename_type=>"single"
    
    # temporary storage keywords
    keyword_list = []
    with open(caseDir+case) as case_file:
        for line in case_file:
            keyword_list.append(line.strip())
    return casename_type ,casename_realname, keyword_list



def output_logFile(output_target, output_log):
    # output log files
    output_file = open(output_target+'.log', 'w', encoding="utf-16")  # Create the output file
    output_file.write(output_log)
    output_file.close()


def output_csvFile(output_target, casetype, catch_text):
    # output csv files ＆ count different text
    if casetype == "catch" and catch_text != "":
        catch_list = catch_text.split('\n')
        catch_counting = Counter(catch_list)
        with open(output_target+'.csv', 'w') as csv_file:
            w = csv.writer(csv_file)
            w.writerows(catch_counting.items())
    
    
def main():
    logDir, caseDir, outputDir = getDir()
    sort_log = datetime_Sortfile(logDir)
    
    for case in os.listdir(caseDir):
        casetype, casename, keyword_list = caseData(case, caseDir)
        output_target = outputDir+casename
        # Ｎo keyword in this case file, skip to next case file.
        if keyword_list == []:
            continue
        
        boolean = bool(0)
        catch_text = ""     # Initial catch_text prepare to store catch_area
        output_log = ""
        for log in sort_log:
            if log == ".DS_Store":
                continue
            else:
                logname, logextension = os.path.splitext(log)
                with open(logDir+log,'r', encoding="utf-16") as log_file:
                    if casetype == "catch":
                        temp_log, count, catch_text = choose_Parser(log_file, casetype, keyword_list, catch_text)
                    else:
                        temp_log, count = choose_Parser(log_file, casetype, keyword_list, catch_text)
                
            # print output data on the output file
            if temp_log != "":
                boolean = bool(1)
                output_log += ('< '+logname+' >  ' + casename +' counting:'+ str(count) +'\n')
                output_log += (temp_log + '\n\n\n') 
        
        output_logFile(output_target, output_log)
        output_csvFile(output_target, casetype, catch_text)
        # delete the empty file
        if not boolean == bool(1):
            os.remove(outputDir+casename+'.log')
    



if __name__ == '__main__':
    main()

    