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
from utils_superpy.utils import buy_product, create_id_with_unused_highest_sequence_nr_to_buy_product
from utils_superpy.utils import get_path_to_file, get_system_date
from utils_superpy.utils import set_system_date_to, time_travel_system_date_with_nr_of_days

def main():

    #step: initialize parser
    parser = argparse.ArgumentParser(description="Welcome to inventory management tool Superpy.", epilog="The line between disorder and order lies in logistics.")

    # step: create container for all subparsers. --> 'command' is a container for [and name of] all the subparsers.
    subparsers = parser.add_subparsers(dest="command") 


    # Create subparser "set_date" with help text and add it to the container "command":
    subparser_set_date = subparsers.add_parser("set_date", help="use this to set_system_date_to a specific date in the file system__date.txt")
    #step: add the positional and optional arguments to the subparser with name 'subparser_set_date': 
    subparser_set_date.add_argument("new_system_date", type=str, help="specify the new system date in format YYYY-MM-DD") 


    # Create subparser "time_travel" with help text and add it to the container "command":
    subparser_set_date = subparsers.add_parser("time_travel", help="change system_date (e.g. if system_date is 2020-03-10 and you time_travel with 3, then new date becomes 2020-03-13. Another ex: starting at date 2020-03-10, if you time_travel with -3, then new date becomes 2020-03-07. ") 
    #step: add the positional and optional arguments to the subparser with name 'subparser_set_date': 
    subparser_set_date.add_argument("nr_of_days", type=int, help="specify the new system date in format YYYY-MM-DD") 

    # Create subparser "buy_date" with help text and add it to the container "command":
    subparser_buy_product = subparsers.add_parser("buy", help="arg1 = product (e.g. apple), arg2 = price (e.g. 0.25), arg3 = date of purchase (e.g. 2020-03-10), arg4 = date of expiration (e.g. 2020-03-20). arg3 is optional argument with default value 'system_date'.") 
    #step: add the positional and optional arguments to the subparser with name 'subparser_set_date': 
    subparser_buy_product.add_argument("product_name", type=str, help="e.g. apple, carrot, oats, etc.") 
    subparser_buy_product.add_argument("price", type=float, help="e.g. 1.20 means 1 euro and 20 cents. 0.2 or 0.20 means 20 cents.") 

    # -buy_date gets its default value from file system_date.txt in the data_directory.
    path_to_system_date = get_path_to_file("data_directory" , 'system_date.txt')
    subparser_buy_product.add_argument("-buy_date", "-b", default=get_system_date(path_to_system_date), type=str, help="date object with string representation following the format: '%Y-%m-%d'. ex: 2026-10-21 ") 
    subparser_buy_product.add_argument("-expiry_date", "-e", default="does not expire", type=str, help="supermarket also sells product that do not expire (e.g. cutlery, household equipment, etc. If product has expiry date, then it has following format: '%Y-%m-%d'. ex: 2026-10-21 ") 


    #step: parse the arguments
    args = parser.parse_args()

    print('--------------------------------------------------')
    # <reusable variables: >
    path_to_project_superpy  = str(os.getcwd()) 
    # print(path_to_project_superpy)
    # print('path_to_data_directory_inside_project_superpy:')
    path_to_data_directory_inside_project_superpy = os.path.abspath(os.path.join(path_to_project_superpy, "data_directory"))
    # print(path_to_data_directory_inside_project_superpy)
    # <end of reusable variables>


    print('--------------------------------------------------')
    print('args.command:')
    if args.command == "set_date":
        print("set_date")
        # step: call fn set_system_date_to to update file system__date.txt with following date:
        path_to_file_with_system_date = os.path.join(path_to_data_directory_inside_project_superpy, 'system_date.txt')
        system_date = set_system_date_to(args.new_system_date, path_to_file_with_system_date)
        print(system_date)



    print('--------------------------------------------------')
    # goal: dry run: run fn time_travel_system_date_with_nr_of_days() with nr_of_days_to_travel = 1. This is a dry run prior to 
    #       running this fn via argparse. 
    path_to_file_with_system_date = os.path.join(path_to_data_directory_inside_project_superpy, 'system_date.txt')
    # new_system_date = time_travel_system_date_with_nr_of_days(2, path_to_file_with_system_date, path_to_file_with_system_date)
    # print(new_system_date)

    if args.command == "time_travel":
        print("time_travel")
        # step: call fn time_travel_system_date_with_nr_of_days to update file system__date.txt with following date:
        new_system_date = time_travel_system_date_with_nr_of_days(args.nr_of_days, path_to_file_with_system_date, path_to_file_with_system_date)
        print(new_system_date)  


    print('--------------------------------------------------')
    # goal: dry run: run fn buy_product() before executing this fn from command line with argparse:  

    #arguments to call fn buy_product() in directory utils.py:


    # print('foo:')
    # print(id_of_row_in_csv_file_bought)
    # print(path_to_csv_bought_input_file)
    # print(path_to_csv_bought_output_file)
    # print('bar')
    # buy_product("carrot", 1.09, "3333-03-12", "3333-03-20", id_of_row_in_csv_file_bought, path_to_csv_bought_input_file, path_to_csv_bought_output_file) 

    if args.command == "buy":
        print("buy:")

        path_to_id_with_highest_sequence_number = os.path.join(path_to_data_directory_inside_project_superpy, 'id_to_use_in_fn_buy_product.txt')
        # print(path_to_id_with_highest_sequence_number)
        id_of_row_in_csv_file_bought = create_id_with_unused_highest_sequence_nr_to_buy_product(path_to_id_with_highest_sequence_number) 

        path_to_csv_bought_input_file = os.path.join(path_to_data_directory_inside_project_superpy, 'bought.csv')
        path_to_csv_bought_output_file = path_to_csv_bought_input_file
        buy_product(args.product_name, args.price, args.buy_date, args.expiry_date, id_of_row_in_csv_file_bought, path_to_csv_bought_input_file, path_to_csv_bought_output_file) 




if __name__ == "__main__":
    main()



