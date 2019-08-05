#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jul 31 10:03:29 2019

@author: kevin_y_kuo
"""

import csv
from collections import Counter

def getDir():
    
    logDir = '/Users/kevin_y_kuo/Trend/Log/'
    caseDir = '/Users/kevin_y_kuo/Trend/Case/'
    #outputDir = '/Users/kevin_y_kuo/Trend/Output/'
    
    #logDir = input('log address: ')
    #caseDir = input('case address: ')
    outputDir = input('output address: ')
    
    return logDir, caseDir, outputDir


def output_logFile(output_target, output_log):
    # output log files
    output_file = open(output_target+'.log', 'w', encoding="utf-16")  # Create the output file
    output_file.write(output_log)
    output_file.close()



def output_csvFile(output_target, casetype, catch_text):
    # output csv files ＆ count different text
    if casetype == "catch" and catch_text != "":
        catch_list = catch_text.split('\n')
        catch_counting = Counter(catch_list)
        with open(output_target+'.csv', 'w') as csv_file:
            w = csv.writer(csv_file)
            w.writerows(catch_counting.items())