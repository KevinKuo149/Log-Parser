#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jul 31 11:29:43 2019

@author: kevin_y_kuo
"""

import re


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
            catch_area += (line.split(keyword_list[0])[1].split(keyword_list[1])[0] + keyword_list[1] +'\n')
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
            if float("".join(re.findall(r'(\d*\.\d*).seconds',line))) >= 1:
                temp_log += "-----------------------long seconds-------------------------\n"
            temp_log += line
    return temp_log, count


def unpaired_Parser(log_file, keyword_list, temp_log):
    # log paired keyword parser implement   # 會印出不成對的部分，成對則不印出

    count = 0  #設定一判斷標準，若最後count=0則刪除此檔案，因為檔案為空檔案
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




'''
if __name__ == '__main__':
    #print(preparse.sort_log)
    #print(preparse.case_data)
    for dict_key in preparse.case_data:
        temp_log = ""
        if "single" in dict_key:
            with open(logDir+log,'r', encoding="utf-16") as log_file:
                temp_log, count = single_Parser(log_file, preparse.case_data[dict_key], temp_log) 
            #print(preparse.case_data[dict_key])
'''
    