#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Aug  8 10:33:20 2019

@author: kevin_y_kuo
"""

import re

def choose_parser(log_dict, casetype, keyword_list, time_restriction_in_sec):
    catch_area = ''
    # Design to use which parser 
    if casetype == "single":
        log_dict = single_parser(log_dict, keyword_list)
    elif casetype == "exclude":
        log_dict = exclude_parser(log_dict, keyword_list)
    elif casetype == "catch":
        log_dict, catch_area = catch_parser(log_dict, keyword_list)
    elif casetype == "seconds":
        log_dict = seconds_parser(log_dict, keyword_list, time_restriction_in_sec)

    return log_dict, catch_area
    


def single_parser(log_dict, keyword_list):
    re_log_dict = {}
    for key in log_dict:
        temp_log = []
        for line in log_dict.get(key):
            for one_keyword in keyword_list:
                if one_keyword in line:
                    temp_log.append(line)
                    break

        if temp_log != []:
            re_log_dict.update({key:temp_log})

    return re_log_dict



def catch_parser(log_dict, keyword_list):
    re_log_dict = {}
    catch_area = []

    for key in log_dict:
        temp_log = []
        for line in log_dict.get(key):

            if keyword_list[0] in line and keyword_list[1] in line:
                temp_log.append(line)
                catch_area.append(line.split(keyword_list[0])[1].split(keyword_list[1])[0] + keyword_list[1])

        if temp_log != []:
            re_log_dict.update({key:temp_log})
            
    return re_log_dict, catch_area    



# max memory consumption, log_dict in this function
def exclude_parser(log_dict, keyword_list):
    re_log_dict = {}
    for key in log_dict:
        temp_log = []
        for line in log_dict.get(key):
            is_include = True

            for one_keyword in keyword_list:
                if one_keyword in line:
                    is_include = False
                    break

            if is_include:
                temp_log.append(line)

        if temp_log != []:
            re_log_dict.update({key:temp_log})

    return re_log_dict



def seconds_parser(log_dict, keyword_list, time_restriction_in_sec):
    re_log_dict = {}
    for key in log_dict:
        temp_log = []
        for line in log_dict.get(key):
            if "milli seconds" in line:
                if int("".join(re.findall(r'(\d*).milli seconds',line))) >= 1000*float(time_restriction_in_sec):
                    temp_log.append(line.strip() + "<< long seconds >>\n")
                else:
                    temp_log.append(line)
            elif "seconds" in line:
                if "".join(re.findall(r'(\d*\.\d*).seconds',line)) != "":
                    if float("".join(re.findall(r'(\d*\.\d*).seconds',line))) >= float(time_restriction_in_sec):
                        temp_log.append(line.strip() + "<< long seconds >>\n")
                    else:
                        temp_log.append(line)

        if temp_log != []:
            re_log_dict.update({key:temp_log})

    return re_log_dict

    

def process_id_collection(log_dict):
    pid_list = []
    for key in log_dict:
        for line in log_dict.get(key):
            pid_match = re.search(r'\[\d*:\d*\]',line)  # [12345:12345]

            if pid_match:
                pid_list.append(pid_match.group(0)) 

    return pid_list


