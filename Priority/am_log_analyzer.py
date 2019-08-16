#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Aug  8 10:27:11 2019

@author: kevin_y_kuo
"""
# import module
import in_out
import log_pre_process
import case_pre_process
import parsing

import os
import sys
#import re


def main():
    logDir, caseDir, outputDir = in_out.getDir(sys.argv[1:])
    sort_log = log_pre_process.datetime_Sortfile(logDir)
    log_dict = log_pre_process.log_Dictionary(sort_log, logDir)
    exe_priority = case_pre_process.case_Priority(caseDir)
    #priority = re.compile(r'priority(\S*)')
    
    if os.path.isfile(os.path.join(caseDir,"Priority.txt")):
        for case in exe_priority:
            casetype, casename, keyword_list = case_pre_process.caseData(case, caseDir)
            output_target = os.path.join(outputDir,casename)
            catch_area = ""
            # Ｎo keyword in this case file, skip to next case file.
            if keyword_list == []:
                continue      
            if casetype == "catch":
                log_dict, catch_area = parsing.choose_Parser(log_dict, casetype, keyword_list)
            else:
                log_dict = parsing.choose_Parser(log_dict, casetype, keyword_list)   
        in_out.output_logFile(output_target, log_dict)
        in_out.output_csvFile(output_target, casetype, catch_area)     
        
    else:
        for case in exe_priority:
            casetype, casename, keyword_list = case_pre_process.caseData(case, caseDir)
            output_target = os.path.join(outputDir,casename)
            catch_area = ""
            # Ｎo keyword in this case file, skip to next case file.
            if keyword_list == []:
                continue
            if casetype == "catch":
                re_log_dict, catch_area = parsing.choose_Parser(log_dict, casetype, keyword_list)
            else:
                re_log_dict = parsing.choose_Parser(log_dict, casetype, keyword_list)
            in_out.output_logFile(output_target, re_log_dict)  
            in_out.output_csvFile(output_target, casetype, catch_area)
    print("Parsing is successful")
      
    
if __name__ == '__main__':
    main()


'''
l = ["priority_rgsfv", "priority_12355_6", "priorityj1i4_7o", "priority_loki4567_3o_l"]
priority = re.compile(r'priority(\S*)')

for string in l:
    match = priority.search(string)
    print(match)

'''




