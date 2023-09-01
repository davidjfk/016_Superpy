# Do not change these lines.
__winc_id__ = "a2bc36ea784242e4989deb157d527ba0"
__human_name__ = "superpy"
# Your code below this line.

# Imports
import argparse, os, sys
import csv
from datetime import date

sys.path.append('c:\\dev\\pytWinc\\superpy')
sys.path.append('c:\\dev\\pytWinc\\superpy\\utils_superpy')
from utils_superpy.utils import set_system_date_to


def main():


    '''
        GOAL: call fn set_system_date_to to update file system__date.txt
        (next step will be to do this from  argparse)

        os.getcwd() is static (i.e. always the same) when I run main.py from the command line.
        By comparison: when I run pytest, os.getcwd() is dynamic, i.e. different for each directory that 
        contains 1 [or more] testcases to test a fn from utils.pyGoedemorg: ex of such a directory: fn_set_system_date_testcase_01
    '''
    print('path_to_project_superpy:')
    path_to_project_superpy  = str(os.getcwd()) 
    print(path_to_project_superpy)
    # output: C:\dev\pytWinc\superpy

    # print(os.path.abspath(__file__))
    '''
        output: C:\dev\pytWinc\superpy\main.py
        desired result: I want path to end on "superpy". 
        qed: so use os.getcwd() instead of os.path.abspath(__file__) when calling fn from argparse.
    '''

    print('--------------------------------------------------')
    print('path_to_data_directory_inside_project_superpy:')
    path_to_data_directory_inside_project_superpy = os.path.abspath(os.path.join(path_to_project_superpy, "data_directory"))
    print(path_to_data_directory_inside_project_superpy)

    print('--------------------------------------------------')
    # step: call fn set_system_date_to to update file system__date.txt with following date:
    system_date = '2020-02-17'
    system_date = set_system_date_to(system_date, path_to_data_directory_inside_project_superpy)
    print(system_date)



if __name__ == "__main__":
    main()





