#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Aug  8 10:27:54 2019

@author: kevin_y_kuo
"""

import re
import os
import datetime


def match_date(line):
    matchThis = None
    matched = re.match(r'\d\d\d\d/\d\d/\d\d\ \d\d:\d\d:\d\d.\d\d\d',line)  # 2018/03/14 13:53:18.266
    if matched:
        matchThis = matched.group()
    return matchThis


# Sort files based on the first date in each log file
def sort_file_by_datetime(logdir):
    log_datefile_list = []
    for log in os.listdir(logdir):
        if not log.endswith(".log"):
            continue
        with open(os.path.join(logdir,log),'r', encoding="utf-16") as log_file:
            for line in log_file:
                date = match_date(line)
                if date == None:
                    continue
                else:
                    date_time = datetime.datetime.strptime(date, '%Y/%m/%d %H:%M:%S.%f')
                    break
            ''' raise exception '''
            date_file_tuple = date_time, log
            log_datefile_list.append(date_file_tuple)
            
    log_datefile_list.sort()
    sort_logname_bytime = []
    
    for i in range(len(log_datefile_list)):
        sort_logname_bytime.append(log_datefile_list[i][1])

    return sort_logname_bytime


''' use a lot of memory, for example: 50MB * 10files = 500MB '''
def log_dictionary(sort_logname_bytime, logdir):
    log_dict = {}
    for log in sort_logname_bytime:
        temp_text = []
        logname, logextension = os.path.splitext(log)

        with open(os.path.join(logdir,log),'r', encoding="utf-16") as log_file:
            for line in log_file:
                temp_text.append(line)

        log_dict.update({logname:temp_text})

    return log_dict


