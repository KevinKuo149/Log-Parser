#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jul 31 12:05:53 2019

@author: kevin_y_kuo
"""

#import Input
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
                        break
                date_file_tuple = date_time_obj, log
                log_datefile_list.append(date_file_tuple)
    log_datefile_list.sort()
    sort_log = []
    for i in range(len(log_datefile_list)):
        sort_log.append(log_datefile_list[i][1])
    return sort_log


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



'''
def caseData(caseDir):
    #caseDir = Input.get_caseDir()
    case_data = {}
    for case in os.listdir(caseDir):
        casename ,caseextension = os.path.splitext(case)  # ex: casename=>"single_crash" ; caseextension=>".txt"
        #casename_realname = "_".join(casename.split("_")[1:])  # casename_realname=>"crash"
        #casename_type = "_".join(casename.split("_")[:1])  # casename_type=>"single"
        # temporary storage keywords
        keyword_list = []
        temp_dict = {}
        with open(caseDir+case) as case_file:
            for line in case_file:
                keyword_list.append(line.strip())
        temp_dict = {case:keyword_list}
        case_data.update(temp_dict)
'''

