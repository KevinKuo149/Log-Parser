#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Aug  8 10:27:54 2019

@author: kevin_y_kuo
"""

import re
import os
import datetime


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
            with open(os.path.join(logDir,log),'r', encoding="utf-16") as log_file:
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


def log_Dictionary(sort_log, logDir):
    log_dict = {}
    for log in sort_log:
        temp = []
        if log == ".DS_Store":
            continue
        else:
            logname, logextension = os.path.splitext(log)
            # print(logname)
            with open(os.path.join(logDir,log),'r', encoding="utf-16") as log_file:
                for line in log_file:
                    temp.append(line)
            log_dict.update({logname:temp})
    return log_dict

