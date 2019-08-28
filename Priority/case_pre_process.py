#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Aug  8 10:32:05 2019

@author: kevin_y_kuo
"""

import os


def casedata(case, casedir):
    case_type_name ,case_extension = os.path.splitext(case)  # ex: case_type_name=>"single_crash" ; case_extension=>".txt"
    case_name = "_".join(case_type_name.split("_")[1:])  # case_name=>"crash"
    case_type = "_".join(case_type_name.split("_")[:1]).lower()  # case_type=>"single"
    # temporary storage keywords
    keyword_list = []
    with open(os.path.join(casedir,case)) as case_file:
        for line in case_file:
            keyword_list.append(line.strip())
            
    return case_type ,case_name, keyword_list


def is_priority_file(casedir):
    priority_file_list = []
    for casename in os.listdir(casedir):
        if casename.lower().startswith("priority_"):
            priority_file_list.append(casename)

    return priority_file_list, (priority_file_list != [])


def case_execute_order(casedir, if_priority_exist, priority_file):
    exe_order = []
    if if_priority_exist:
        with open(os.path.join(casedir,priority_file),'r') as case_priority_file:
            for line in case_priority_file:
                exe_order.append(line.strip())
    else:
        exe_order = os.listdir(casedir)
        # MacOS needed
        if ".DS_Store" in exe_order:
            exe_order.remove(".DS_Store")
            
    return exe_order


