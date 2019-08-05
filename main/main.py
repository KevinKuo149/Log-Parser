#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Aug  5 14:32:36 2019

@author: kevin_y_kuo
"""

import in_out
import preparse
import parse

import os


def main():
    logDir, caseDir, outputDir = in_out.getDir()
    sort_log = preparse.datetime_Sortfile(logDir)
    for case in os.listdir(caseDir):
        if case == ".DS_Store":
            continue
        else:
            casetype, casename, keyword_list = preparse.caseData(case, caseDir)
            output_target = outputDir+casename
            boolean = bool(0)
            catch_text = ""     # Initial catch_text prepare to store catch_area
            output_log = ""
            for log in sort_log:
                if log == ".DS_Store":
                    continue
                else:
                    logname, logextension = os.path.splitext(log)
                    with open(logDir+log,'r', encoding="utf-16") as log_file:
                        if casetype == "catch":
                            temp_log, count, catch_text = parse.choose_Parser(log_file, casetype, keyword_list, catch_text)
                        else:
                            temp_log, count = parse.choose_Parser(log_file, casetype, keyword_list, catch_text)
                # print output data on the output file
                if temp_log != "":
                    boolean = bool(1)
                    output_log += ('< '+logname+' >  ' + casename +' counting:'+ str(count) +'\n')
                    output_log += (temp_log + '\n\n\n') 
            
            in_out.output_logFile(output_target, output_log)
            in_out.output_csvFile(output_target, casetype, catch_text)
            # delete the empty file
            if not boolean == bool(1):
                os.remove(outputDir+casename+'.log')
        

if __name__ == '__main__':
    main()