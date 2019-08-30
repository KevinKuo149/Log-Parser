#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Aug  8 10:27:11 2019

@author: kevin_y_kuo
"""

import in_out
import log_pre_process
import case_pre_process
import am_log_parser

import os
import sys



def main():
    logdir, casedir, outputdir, time_restriction_in_sec, is_pid_needed = in_out.get_input(sys.argv[1:])
    sort_logname_bytime = log_pre_process.sort_file_by_datetime(logdir)
    log_dict = log_pre_process.log_dictionary(sort_logname_bytime, logdir)
    original_log_dict = log_dict
    priority_file_list, is_priority_exist = case_pre_process.is_priority_file(casedir)
    
    if is_pid_needed:
        process_id_collect = am_log_parser.process_id_collection(log_dict)
        output_target = os.path.join(outputdir, "PID_TID")
        in_out.output_process_id_csvfile(output_target, process_id_collect)
        
    if is_priority_exist:
        print("Priority file is exist!!!\n")
        for priority_file in priority_file_list:
            log_dict = original_log_dict
            exe_order = case_pre_process.case_execute_order(casedir, is_priority_exist, priority_file)
            priority_file_name ,priority_file_extension = os.path.splitext(priority_file)
            print(priority_file,":")

            for case in exe_order:
                print('   -- ',case, end = " ... ")
                casetype, casename, keyword_list = case_pre_process.casedata(case, casedir)
                output_target = os.path.join(outputdir, priority_file_name)
                catch_area = []

                # Ｎo keyword in this case file, skip to next case file.
                if keyword_list == []:
                    continue

                if casetype == "catch":
                    log_dict, catch_area = am_log_parser.choose_parser(log_dict, casetype, keyword_list, time_restriction_in_sec)
                else:
                    log_dict, _ = am_log_parser.choose_parser(log_dict, casetype, keyword_list, time_restriction_in_sec)   
                print("completed.")

            in_out.output_logfile(output_target, log_dict)
            in_out.output_csvfile(output_target, casetype, catch_area)     
        
    else:
        exe_order = case_pre_process.case_execute_order(casedir, is_priority_exist, priority_file_list)
        for case in exe_order:
            print('   -- ',case, end = " ... ")
            casetype, casename, keyword_list = case_pre_process.casedata(case, casedir)
            output_target = os.path.join(outputdir,casename)
            catch_area = []

            # Ｎo keyword in this case file, skip to next case file.
            if keyword_list == []:
                continue

            if casetype == "catch":
                re_log_dict, catch_area = am_log_parser.choose_parser(log_dict, casetype, keyword_list, time_restriction_in_sec)
            else:
                re_log_dict, _ = am_log_parser.choose_parser(log_dict, casetype, keyword_list, time_restriction_in_sec)

            in_out.output_logfile(output_target, re_log_dict)
            in_out.output_csvfile(output_target, casetype, catch_area)
            print("completed.")

    print("<< am_log_parser is totally successful. >>")


if __name__ == '__main__':
    main()




