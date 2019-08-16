#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Aug  8 10:32:05 2019

@author: kevin_y_kuo
"""

import os


def caseData(case, caseDir):
    casename ,caseextension = os.path.splitext(case)  # ex: casename=>"single_crash" ; caseextension=>".txt"
    casename_realname = "_".join(casename.split("_")[1:])  # casename_realname=>"crash"
    casename_type = "_".join(casename.split("_")[:1])  # casename_type=>"single"
    casename_type = casename_type.lower() 
    # temporary storage keywords
    keyword_list = []
    with open(os.path.join(caseDir,case)) as case_file:
        for line in case_file:
            keyword_list.append(line.strip())
    return casename_type ,casename_realname, keyword_list



def case_Priority(caseDir):
    # Check whether the file "Priority.txt" is exit 
    # Create exe_priority according to "Priority.txt"
    exe_priority = []
    #priority = re.compile(r'priority(\S*)')
    if os.path.isfile(os.path.join(caseDir,"Priority.txt")):
        with open(os.path.join(caseDir,"Priority.txt"),'r') as priority_file:
            for line in priority_file:
                exe_priority.append(line.strip())
    else:
        if ".DS_Store" in os.listdir(caseDir):
            exe_priority = os.listdir(caseDir)
            exe_priority.remove(".DS_Store")
        else:
            exe_priority = os.listdir(caseDir)
    return exe_priority