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
from utils_superpy.utils import set_system_date_to, time_travel_system_date_with_nr_of_days


def main():

    #step: initialize parser
    parser = argparse.ArgumentParser(description="Welcome to inventory management tool Superpy.", epilog="The line between disorder and order lies in logistics.")

    # step: create container for all subparsers. --> 'command' is a container for [and name of] all the subparsers.
    subparsers = parser.add_subparsers(dest="command") 


    # Create subparser "set_date" with help text and add it to the container "command":
    subparser_set_date = subparsers.add_parser("set_date", help="use this to set_system_date_to a specific date in the file system__date.txt")

    #step: add the positional and optional arguments to the subparser with name 'subparser_calculate': 
    subparser_set_date.add_argument("new_system_date", type=str, help="specify the new system date in format YYYY-MM-DD") 

    #step: parse the arguments
    args = parser.parse_args()

    print('--------------------------------------------------')
    # reusable variables: 
    path_to_project_superpy  = str(os.getcwd()) 
    print(path_to_project_superpy)
    print('path_to_data_directory_inside_project_superpy:')
    path_to_data_directory_inside_project_superpy = os.path.abspath(os.path.join(path_to_project_superpy, "data_directory"))
    print(path_to_data_directory_inside_project_superpy)

    print('--------------------------------------------------')
    print('args.command:')
    if args.command == "set_date":
        print("set_date")
        # step: call fn set_system_date_to to update file system__date.txt with following date:
        system_date = set_system_date_to(args.new_system_date, path_to_data_directory_inside_project_superpy)
        print(system_date)


    print('--------------------------------------------------')
    # goal: run fn time_travel_system_date_with_nr_of_days() with nr_of_days_to_travel = 1. This is a dry run prior to 
    #       running this fn via argparse. 
    new_system_date = time_travel_system_date_with_nr_of_days(-5, path_to_data_directory_inside_project_superpy)
    print(new_system_date)


if __name__ == "__main__":
    main()



