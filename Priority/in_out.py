#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Aug  8 09:45:46 2019

@author: kevin_y_kuo
"""


import csv
from collections import Counter
import sys, getopt


def getDir(argv):
   logDir = ''
   outputDir = ''
   caseDir = ''
   try:
      opts, args = getopt.getopt(argv,"hl:c:o:",["logdir=","casedir","outputdir="])
   except getopt.GetoptError:
      print('python am_log_analyzer.py -l <log address> -c <case address> -o <output address>')
      sys.exit(1)
   for opt, arg in opts:
       if opt == '-h':
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
           print('Enter the address of where you want to output the outcome.')
           print('- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -')
           sys.exit()
       elif opt in ("-l", "--logdir"):
           logDir = arg
       elif opt in ("-c", "--casedir"):
           caseDir = arg
       elif opt in ("-o", "--outputdir"):
           outputDir = arg
   print ('Log address is "', logDir)
   print ('Case address is "', caseDir)
   print ('Output address is "', outputDir)
   
   return logDir, caseDir, outputDir

'''
def getDir():   
    logDir = '/Users/kevin_y_kuo/Trend/Log'
    caseDir = '/Users/kevin_y_kuo/Trend/Case'
    outputDir = '/Users/kevin_y_kuo/Trend/Output'
    return logDir, caseDir, outputDir
'''

def output_logFile(output_target, log_dict):
    # output log files
    if log_dict != {}:
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


def output_csvFile(output_target, casetype, catch_area):
    # output csv files ＆ count different text
    if casetype == "catch" and catch_area != "":
        catch_list = catch_area.split('\n')
        catch_counting = Counter(catch_list)
        with open(output_target+'.csv', 'w') as csv_file:
            w = csv.writer(csv_file)
            w.writerows(catch_counting.items())    
            

        

    


