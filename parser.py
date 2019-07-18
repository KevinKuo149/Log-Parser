#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jul 17 15:01:01 2019

@author: kevin_y_kuo
"""

import os
import time
import sys

def GetDir():
    logDir = '/Users/kevin_y_kuo/Documents/Log/'
    caseDir = '/Users/kevin_y_kuo/Documents/Case/'
    outputDir = '/Users/kevin_y_kuo/Documents/Output/'
    
    return logDir, caseDir, outputDir



def SortAndRename(logDir):
    # 依照檔案修改日期排序
    date_file_list = []
    for f in os.scandir(logDir):
        if f.name.endswith(".log"):
            #print(f.name)
            t = os.stat(f)
            lastmod_date = time.localtime(t.st_mtime)  #最後修改日期時間
            #print(time.strftime('%Y-%m-%d,%H:%M:%S', lastmod_date))
            date_file_tuple = lastmod_date, f.name
            date_file_list.append(date_file_tuple)
    date_file_list.sort()
    
    # 依照檔案順序重新命名
    x = 0
    for sfile in date_file_list:
        NewFileName = str(x).zfill(3) + '-' + sfile[1]
        os.rename(logDir+sfile[1],logDir+NewFileName)
        x += 1

def OriginName(logDir):
    # 將被編號的檔案名稱還原
    for log in os.listdir(logDir):
        os.rename(logDir+log,logDir+log.split("-")[1])

def mkdir(path):
    isExists = os.path.exists(path)
    # 判斷结果
    if not isExists:
        os.makedirs(path)
    
    return path+'/'   # 路徑for macOS，若要在windows上執行，則改成+'\'

def SingleParser(f, key):
    keywords = []
    for line in key:
        keywords.append(line.strip())
    
    count = 0 #設定一判斷標準，若最後count=0則刪除此檔案，因為檔案為空檔案
    for line in f:
        for keyword in keywords:
            if keyword in line:
                count += 1
                print(line)
    return count


def PairedParser(f, key):
    keyword = []
    for line in key:
        keyword.append(line.strip())
    
    count = 0  #設定一判斷標準，若最後count=0則刪除此檔案，因為檔案為空檔案
    pair = 0
    line_list = []
    
    for line in f:
        if pair == 0:
            if keyword[0] in line:
                count += 1
                pair += 1
                line_list.append(line)
            continue
        if pair == 1:
            if keyword[0] in line:
                pair += 1    # 加完pair變成2，會直接跳"if pair==2:"
            elif keyword[1] in line:
                pair -= 1
                line_list = []
                continue
            else:
                line_list.append(line)
                continue
        if pair == 2:
            str_line_list = "\n".join(line_list)
            print(str_line_list)
            # 因為pair==2的情況是發生在碰到第二個keyword[0]，elif結束後要回到pair==1才可繼續搜尋
            pair = 1  
            # 搜尋到第二次keyword[0]，刪除全部後，再加入此次的line值
            line_list = []
            line_list.append(line)
            str_line_list = []
            
    if pair == 1:   #  到檔案尾時，若pair==1，表示仍有不成對，故也需print出到新文件
        str_line_list = "\n".join(line_list)
        print(str_line_list)
    
    return count




def main():
    for log in os.listdir(logDir):
        log_name, log_extension = os.path.splitext(log)
        logname = "_".join(log_name.split("-")[1:])
        for case in os.listdir(caseDir):
            case_name ,case_extension = os.path.splitext(case)
            casename = "_".join(case_name.split("_")[1:])
            casetype = "_".join(case_name.split("_")[:1])

            output = sys.stdout      # store original stdout object for later
            
            path = mkdir(outputDir+casetype)
            
            with open(logDir+log,'r', encoding="utf-16") as f, open(caseDir+case) as key:
                sys.stdout = open(path+log_name+'<'+casename+'>.txt', 'w')      # redirect all prints to this log file
                
                print(logname+'<'+casename+'>'+'\n')
                if casetype == "Single":
                    count = SingleParser(f, key)
                    print(count)
                if casetype == "Paired":
                    count = PairedParser(f, key)
                    print(count)
                    
                #count = ChooseCase(f, key, casetype)
                
                sys.stdout.close()                # ordinary file object
                sys.stdout = output             # restore print commands to interactive prompt   
                
            if count == 0:
                os.remove(path+log_name+'<'+casename+'>.txt')



if __name__ == '__main__':
    logDir, caseDir, outputDir = GetDir()
    SortAndRename(logDir)
    main()
    # OriginName(logDir) 
    
    
