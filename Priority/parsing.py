#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Aug  8 10:33:20 2019

@author: kevin_y_kuo
"""

import re

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
    restrict_time = 1
    #input('enter the time: ')
    re_log_dict = {}
    for key in log_dict.keys():
        temp_log = []
        for index in range(len(log_dict[key])):
            line = log_dict[key][index]
            if "milli seconds" in line:
                if int("".join(re.findall(r'(\d*).milli seconds',line))) >= 1000*float(restrict_time):
                    temp_log.append(line.strip() + "<< long seconds >>\n")
                else:
                    temp_log.append(line)
            
            elif "seconds" in line:
                if "".join(re.findall(r'(\d*\.\d*).seconds',line)) != "":
                    if float("".join(re.findall(r'(\d*\.\d*).seconds',line))) >= float(restrict_time):
                        temp_log.append(line.strip() + "<< long seconds >>\n")
                    else:
                        temp_log.append(line)
        if temp_log != []:
            re_log_dict.update({key:temp_log})
    return re_log_dict

    
