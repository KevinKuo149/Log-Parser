#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Aug  5 17:12:00 2019

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
    return logDir, caseDir, outputDir


def matchDate(line):
    matchThis = ""
    matched = re.match(r'\d\d\d\d/\d\d/\d\d\ \d\d:\d\d:\d\d.\d\d\d',line)  # 2018/03/14 13:53:18.266
    if matched:
        matchThis = matched.group()
    else:
        matchThis = "NONE"
    return matchThis


# Sort files based on the first date in each log file
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


def log_Storage(sort_log, logDir):
    log_dict = {}
    for log in sort_log:
        temp = []
        if log == ".DS_Store":
            continue
        else:
            logname, logextension = os.path.splitext(log)
            # print(logname)
            with open(logDir+log,'r', encoding="utf-16") as log_file:
                for line in log_file:
                    temp.append(line)
            log_dict.update({logname:temp})
    return log_dict
                
             
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



def case_Priority(caseDir):
    # Check whether the file "Priority.txt" is exit 
    # Create exe_priority according to "Priority.txt"
    exe_priority = []
    if os.path.isfile(caseDir+"Priority.txt"):
        with open(caseDir+"Priority.txt",'r') as priority_file:
            for line in priority_file:
                exe_priority.append(line.strip())
    else:
        if ".DS_Store" in os.listdir(caseDir):
            exe_priority = os.listdir(caseDir)
            exe_priority.remove(".DS_Store")
        else:
            exe_priority = os.listdir(caseDir)
    return exe_priority
    
         

def choose_Parser(log_dict, casetype, keyword_list):
    # Design to use which parser 
    if casetype == "single":
        log_dict = single_Parser(log_dict, keyword_list)
        return log_dict
    if casetype == "exclude":
        log_dict = exclude_Parser(log_dict, keyword_list)
        return log_dict
    if casetype == "catch":
        log_dict, catch_area = catch_Parser(log_dict, keyword_list)
        return log_dict, catch_area
    if casetype == "seconds":
        log_dict = seconds_Parser(log_dict, keyword_list)
        return log_dict


def single_Parser(log_dict, keyword_list):
    # log single keyword parser implement
    re_log_dict = {}
    for key in log_dict.keys():
        temp_log = []
        for index in range(len(log_dict[key])):
            line = log_dict[key][index]
            for one_keyword in keyword_list:
                if one_keyword in line:
                    temp_log.append(line)
                    break
        if temp_log != []:
            re_log_dict.update({key:temp_log})
    return re_log_dict


def catch_Parser(log_dict, keyword_list):
    re_log_dict = {}
    catch_area = ""  
    for key in log_dict.keys():
        temp_log = []
        for index in range(len(log_dict[key])):
            line = log_dict[key][index]
            if keyword_list[0] in line and keyword_list[1] in line:
                temp_log.append(line)
                catch_area += (line.split(keyword_list[0])[1].split(keyword_list[1])[0] + '.exe\n')
        if temp_log != []:
            re_log_dict.update({key:temp_log})
    return re_log_dict, catch_area    


def exclude_Parser(log_dict, keyword_list):
    re_log_dict = {}
    for key in log_dict.keys():
        temp_log = []
        for index in range(len(log_dict[key])):
            line = log_dict[key][index]
            boolean = bool(1)
            for one_keyword in keyword_list:
                if one_keyword in line:
                    boolean = bool(0)
                    break
            if boolean == bool(1):
                temp_log.append(line)
        if temp_log != []:
            re_log_dict.update({key:temp_log})
    return re_log_dict


def seconds_Parser(log_dict, keyword_list):
    # re.findall(r'(\d*\.\d*).seconds',string)
    # re.findall(r'(\d*).milli seconds',string)
    re_log_dict = {}
    for key in log_dict.keys():
        temp_log = []
        for index in range(len(log_dict[key])):
            line = log_dict[key][index]
            if "milli seconds" in line:
                if int("".join(re.findall(r'(\d*).milli seconds',line))) >= 1000:
                    temp_log.append(line.strip() + "<< long seconds >>\n")
                else:
                    temp_log.append(line)
            
            elif "seconds" in line:
                if "".join(re.findall(r'(\d*\.\d*).seconds',line)) != "":
                    if float("".join(re.findall(r'(\d*\.\d*).seconds',line))) >= 1:
                        temp_log.append(line.strip() + "<< long seconds >>\n")
                    else:
                        temp_log.append(line)
        if temp_log != []:
            re_log_dict.update({key:temp_log})
    return re_log_dict


def output_logFile(output_target, log_dict):
    # output log files
    if log_dict != {}:
        output_log = ""
        for key in log_dict.keys():
            temp_log = ""
            for line in range(len(log_dict[key])):
                temp_log += log_dict[key][line]        
            output_log += ('< '+key+' >  ' +' counting:'+ str(len(log_dict[key])) +'\n')
            output_log += (temp_log + '\n\n\n')     
            
        output_file = open(output_target+'.log', 'w', encoding="utf-16")  # Create the output file
        output_file.write(output_log)
        output_file.close()


def output_csvFile(output_target, casetype, catch_area):
    # output csv files ＆ count different text
    if casetype == "catch" and catch_area != "":
        catch_list = catch_area.split('\n')
        catch_counting = Counter(catch_list)
        with open(output_target+'.csv', 'w') as csv_file:
            w = csv.writer(csv_file)
            w.writerows(catch_counting.items())    

    
def main():
    logDir, caseDir, outputDir = getDir()
    sort_log = datetime_Sortfile(logDir)
    log_dict = log_Storage(sort_log, logDir)
    exe_priority = case_Priority(caseDir)
    
    if os.path.isfile(caseDir+"Priority.txt"):
        for case in exe_priority:
            casetype, casename, keyword_list = caseData(case, caseDir)
            output_target = outputDir+casename
            catch_area = ""
            # Ｎo keyword in this case file, skip to next case file.
            if keyword_list == []:
                continue      
            if casetype == "catch":
                log_dict, catch_area = choose_Parser(log_dict, casetype, keyword_list)
            else:
                log_dict = choose_Parser(log_dict, casetype, keyword_list)   
        output_logFile(output_target, log_dict)
        output_csvFile(output_target, casetype, catch_area)     
        
    else:
        for case in exe_priority:
            casetype, casename, keyword_list = caseData(case, caseDir)
            output_target = outputDir+casename
            catch_area = ""
            # Ｎo keyword in this case file, skip to next case file.
            if keyword_list == []:
                continue
            if casetype == "catch":
                re_log_dict, catch_area = choose_Parser(log_dict, casetype, keyword_list)
            else:
                re_log_dict = choose_Parser(log_dict, casetype, keyword_list)
            output_logFile(output_target, re_log_dict)  
            output_csvFile(output_target, casetype, catch_area)
            
      
    
if __name__ == '__main__':
    main()




