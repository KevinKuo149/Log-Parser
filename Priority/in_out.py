#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Aug  8 09:45:46 2019

@author: kevin_y_kuo
"""


import csv
from collections import Counter
import sys, getopt


def get_input(argv):
    logdir = ''
    outputdir = ''
    casedir = ''
    time_restriction_in_sec = 1
    is_pid_needed = False

    try:
        opts, args = getopt.getopt(argv,"hl:c:o:t:p:",["logdir=","casedir＝","outputdir=","time_restriction_in_sec=","is_pid_needed="])
    except getopt.GetoptError:
        print('python am_log_analyzer.py -l <log address> -c <case address> -o <output address>')
        sys.exit(1)
    for opt, arg in opts:
        if opt in ("-l", "--logdir"):
            logdir = arg
        elif opt in ("-c", "--casedir"):
            casedir = arg
        elif opt in ("-o", "--outputdir"):
            outputdir = arg
        elif opt in ("-t", "--time_restriction_in_sec"):
            time_restriction_in_sec = float(arg)     # in sec
        elif opt in ("-p", "--is_pid_needed"):
            yes = 'Y'.lower()
            if arg == yes:
              is_pid_needed = True
        elif opt == '-h':
            print('python am_log_analyzer.py -l <log address> -c <case address> -o <output address>')
            print('- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -')
            print('-l :')
            print('Enter the address of log folder.\n'
                 'All log files that you want to parse are stored in log folder.\n')
            print('-c :')
            print('Enter the address of case folder.\n'
                 'Case files can be added by users as lon as following the spec : "casetype_casename"\n'
                 'Please see the wiki for details. => wiki: https://wiki.jarvis.trendmicro.com/display/DS/AM+Log+Analyzer+-+Windows\n')
            print('-o :')
            print('Enter the address of where you want to output the outcome.\n')
            print('-t :')
            print('Enter the number which is the time restriction of long seconds.\n'
                  'Default restriction time is 1 seconds.\n')
            print('-p :')
            print("Enter 'Y' to ensure 'PID_TID' is needed.\n"
                  "Default is False. 'PID_TID' won't be output.")
            print('- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -')
            sys.exit()
    print('Log address is :', logdir)
    print('Case address is :', casedir)
    print('Output address is :', outputdir)
    print('long seconds restriction time :', time_restriction_in_sec, 'seconds')
    print('is process id needed :', is_pid_needed)
    print()
    return logdir, casedir, outputdir, time_restriction_in_sec, is_pid_needed


def output_logfile(output_target, log_dict):
    # output log files
    if log_dict:
        output_log = ""
        for key in log_dict.keys():
            temp_log = ""
            for line in range(len(log_dict[key])):
                temp_log += log_dict[key][line]        
            output_log += ('< '+key+' >  ' +' counting:'+ str(len(log_dict[key])) +'\n')
            output_log += (temp_log + '\n\n\n')     
            
        output_file = open(output_target+'.log', 'w', encoding="utf-16")  # Create the output file
        output_file.write(output_log)
        output_file.close()


def output_csvfile(output_target, casetype, catch_area):
    # output csv files ＆ count different text
    if casetype == "catch" and catch_area != []:
        catch_counting = Counter(catch_area)
        with open(output_target+'.csv', 'w', newline = '') as csv_file:
            w = csv.writer(csv_file)
            w.writerows(catch_counting.most_common())  


def output_process_id_csvfile(output_target, process_id_collect):
    process_counting = Counter(process_id_collect)
    with open(output_target+'.csv', 'w') as csv_file:
        w = csv.writer(csv_file)
        w.writerows(process_counting.most_common())  
        

    


