# am-log-analyzer

- am_log_analyzer.py
    - Main program, connecting four modules in series.
- in_out.py
    - Input uses command line argument, following the type : 
    **"python am_log_analyzer.py -l <log address> -c <case address> -o <output address>"**
    ![](https://i.imgur.com/8KDevtO.png)
    According to different needs, output can be divided into two part: ".log file" and ".csv file".
- log_pre_process.py
    1. Sort log files by the time of the first data.
    ![](https://i.imgur.com/mhxF8jy.png)
    2. Read all log files in order.
    3. Temporarily save the contents of all log files to the dictionary.
- case_pre_process.py
    1. Check whether the "Priority.txt" exist or not.
    2. Disassemble each case file, return "casetype", "casename" and "keyword list".
- parsing.py
    - Choose which parsing function to use according to the casetype.
