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

# the following 4 imported fns are arguments in fn create_data_for_csv_files_bought_and_sold() below.
from utils_superpy.utils import add_days_to_date
from utils_superpy.utils import generate_random_buy_date_for_buy_transaction_in_future_in_time_interval
from utils_superpy.utils import create_id_for_each_row_in_boughtcsv_while_script_generates_this_boughtcsv
from utils_superpy.utils import get_path_to_directory_of_file

from utils_superpy.utils import buy_product, create_data_for_csv_files_bought_and_sold
from utils_superpy.utils import create_id_with_unused_highest_sequence_nr_to_buy_product_as_superpy_user
from utils_superpy.utils import get_path_to_file, get_system_date
from utils_superpy.utils import sell_product, set_system_date_to, time_travel_system_date_with_nr_of_days


def main():

    DATA_DIRECTORY = "data_used_in_superpy"
    FILE_WITH_SYSTEM_DATE = "system_date.txt"

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


    # Create subparser "buy" with help text and add it to the container "command":
    subparser_buy_product = subparsers.add_parser("buy", help="arg1 = product (e.g. apple), arg2 = price (e.g. 0.25), arg3 = date of purchase (e.g. 2020-03-10), arg4 = date of expiration (e.g. 2020-03-20). arg5 = optional argument with default value 'system_date'.") 
    #step: add the positional and optional arguments to the subparser with name 'subparser_set_date': 
    subparser_buy_product.add_argument("product_name", type=str, help="e.g. apple, carrot, oats, etc.") 
    subparser_buy_product.add_argument("price", type=float, help="e.g. 1.20 means 1 euro and 20 cents. 0.2 or 0.20 means 20 cents.") 
    # -buy_date gets its default value from file system_date.txt in the DATA_DIRECTORY:
    path_to_system_date = get_path_to_file(DATA_DIRECTORY , FILE_WITH_SYSTEM_DATE)
    subparser_buy_product.add_argument("-buy_date", "-b", default=get_system_date(path_to_system_date), type=str, help="date object with string representation following the format: '%Y-%m-%d'. ex: 2026-10-21 ") 
    subparser_buy_product.add_argument("-expiry_date", "-e", default="does not expire", type=str, help="supermarket also trades products that do not expire (e.g. cutlery, household equipment, etc. If product has expiry date, then it has following format: '%Y-%m-%d'. ex: 2026-10-21 ") 



    # Create subparser "sell" with help text and add it to the container "command":
    subparser_buy_product = subparsers.add_parser("sell", help="arg1 = buy_id (e.g. b_15), arg2 = price (e.g. 1.25), arg3 = selling date (e.g. 2020-03-10), arg4 = path_to_csv_sold_output_file. arg5 = path_to_csv_sold_output_file. When testing this fn in pytest, then arg4 and arg5 do not point to the same file.")
    #step: add the positional and optional arguments to the subparser with name 'subparser_set_date': 
    subparser_buy_product.add_argument("buy_id", type=str, help="e.g. apple, carrot, oats, etc.") 
    subparser_buy_product.add_argument("price", type=float, help="e.g. 1.20 means 1 euro and 20 cents. 0.2 or 0.20 means 20 cents.") 
    # -buy_date gets its default value from file system_date.txt in the DATA_DIRECTORY:
    path_to_system_date = get_path_to_file(DATA_DIRECTORY , FILE_WITH_SYSTEM_DATE)
    subparser_buy_product.add_argument("-sell_date", "-s", default=get_system_date(path_to_system_date), type=str, help="date object with string representation following the format: '%Y-%m-%d'. ex: 2026-10-21 ") 
    subparser_buy_product.add_argument("-expiry_date", "-e", default="does not expire", type=str, help="supermarket also trades products that do not expire (e.g. cutlery, household equipment, etc. If product has expiry date, then it has following format: '%Y-%m-%d'. ex: 2026-10-21 ") 


    #step: parse the arguments
    args = parser.parse_args()


    print('--------------------------------------------------')
    # reusable variables: 
    path_to_project_superpy  = str(os.getcwd()) 
    # print(path_to_project_superpy)
    # print('path_to_data_directory_inside_project_superpy:')
    path_to_data_directory_inside_project_superpy = os.path.abspath(os.path.join(path_to_project_superpy, DATA_DIRECTORY))
    # print(path_to_data_directory_inside_project_superpy)
    # <end of reusable variables>
    path_to_file_with_system_date = os.path.join(path_to_data_directory_inside_project_superpy, FILE_WITH_SYSTEM_DATE)


    print('--------------------------------------------------')
    print('args.command:')
    if args.command == "set_date":
        print("set_date")
        # step: call fn set_system_date_to to update file system__date.txt with following date:
        path_to_file_with_system_date = os.path.join(path_to_data_directory_inside_project_superpy, FILE_WITH_SYSTEM_DATE)
        system_date = set_system_date_to(args.new_system_date, path_to_file_with_system_date)
        print(system_date)


    print('--------------------------------------------------')
    # goal: dry run: run fn time_travel() before executing this fn from command line with argparse:
    '''
    new_system_date = time_travel_system_date_with_nr_of_days(2, path_to_file_with_system_date, path_to_file_with_system_date)
    print(new_system_date)
    '''
    if args.command == "time_travel":
        print("time_travel")
        # step: call fn time_travel_system_date_with_nr_of_days to update file system__date.txt with following date:
        new_system_date = time_travel_system_date_with_nr_of_days(args.nr_of_days, path_to_file_with_system_date, path_to_file_with_system_date)
        print(new_system_date)  


    print('--------------------------------------------------')
    # goal: dry run: run fn buy_product() before executing this fn from command line with argparse:
    '''
    path_to_id_with_highest_sequence_number = os.path.join(path_to_data_directory_inside_project_superpy, 'id_to_use_in_fn_buy_product.txt')
    # print(path_to_id_with_highest_sequence_number)
    id_of_row_in_csv_file_bought = create_id_with_unused_highest_sequence_nr_to_buy_product_as_superpy_user(path_to_id_with_highest_sequence_number) 

    path_to_csv_bought_input_file = os.path.join(path_to_data_directory_inside_project_superpy, 'bought.csv')
    path_to_csv_bought_output_file = path_to_csv_bought_input_file
    buy_product("carrot", 1.09, "3333-03-12", "3333-03-20", id_of_row_in_csv_file_bought, path_to_csv_bought_input_file, path_to_csv_bought_output_file) 
    '''
    if args.command == "buy":
        print("buy:")
        path_to_id_with_highest_sequence_number = os.path.join(path_to_data_directory_inside_project_superpy, 'id_to_use_in_fn_buy_product.txt')
        # print(path_to_id_with_highest_sequence_number)
        id_of_row_in_csv_file_bought = create_id_with_unused_highest_sequence_nr_to_buy_product_as_superpy_user(path_to_id_with_highest_sequence_number) 

        path_to_csv_bought_input_file = os.path.join(path_to_data_directory_inside_project_superpy, 'bought.csv')
        path_to_csv_bought_output_file = path_to_csv_bought_input_file # but not the same in pytest.
        buy_product(args.product_name, args.price, args.buy_date, args.expiry_date, id_of_row_in_csv_file_bought, path_to_csv_bought_input_file, path_to_csv_bought_output_file) 


    # goal: dry run: run fn sell_product() before executing this fn from command line with argparse:
    '''
    path_to_csv_sold_output_file = os.path.join(path_to_data_directory_inside_project_superpy, 'sold.csv')
    path_to_csv_sold_output_file = path_to_csv_bought_input_file
    sell_product("b_5", 1.09, "3333-03-12", path_to_csv_sold_output_file, path_to_csv_sold_output_file)
    '''
    if args.command == "sell":
        print("sell:")
        path_to_csv_sold_input_file = os.path.join(path_to_data_directory_inside_project_superpy, 'sold.csv')
        path_to_csv_sold_output_file = path_to_csv_sold_input_file # but not the same in pytest.
        sell_product(args.buy_id, args.price, args.sell_date, path_to_csv_sold_input_file, path_to_csv_sold_output_file)


    # to create testdata for bought.csv and sold.csv configure following variables to your liking:
    product_range = 2
    # see produt_range definition in README_SOFTWARE_DESIGN.md --> ch definitions. 

     # variable 'every_nth_row' makes sense inside the assignment statement below it
    every_nth_row = 2
    delete_every_nth_row_in_soldcsv_so_every_nth_row_in_boughtcsv_can_expire_when_time_travelling = every_nth_row

    shelf_life = 9
    # see shelf_life definition in README_SOFTWARE_DESIGN.md --> ch definitions.

    turnover_time = 3
    # see turnover_time definition in README_SOFTWARE_DESIGN.md --> ch definitions.
    
    markup = 3
    # see markup definition in README_SOFTWARE_DESIGN.md --> ch definitions.


    # see time_interval definition in README_SOFTWARE_DESIGN.md --> ch definitions:
    lower_boundary_year_of_time_interval_in_which_to_create_random_testdata = 2023
    lower_boundary_month_of_time_interval_in_which_to_create_random_testdata = 10
    lower_boundary_week_of_time_interval_in_which_to_create_random_testdata = 1
    upper_boundary_nr_of_months_to_add_to_calculate = 2
    upper_boundary_nr_of_weeks_to_add_to_calculate = 0
    upper_boundary_nr_of_days_to_add_to_calculate = 0

    # set path to file bought.csv:
    path_to_directory_testdata = ''
    path_to_directory_testdata = get_path_to_directory_of_file('data_used_in_superpy')
    path_to_file_bought_csv = os.path.join(path_to_directory_testdata, 'bought.csv')

    # set path to file sold.csv:
    path_to_file_sold_csv = os.path.join(path_to_directory_testdata, 'sold.csv')

    create_data_for_csv_files_bought_and_sold(
        product_range,
        delete_every_nth_row_in_soldcsv_so_every_nth_row_in_boughtcsv_can_expire_when_time_travelling,
        shelf_life,
        turnover_time,
        markup,
        lower_boundary_year_of_time_interval_in_which_to_create_random_testdata,
        lower_boundary_month_of_time_interval_in_which_to_create_random_testdata,
        lower_boundary_week_of_time_interval_in_which_to_create_random_testdata,
        upper_boundary_nr_of_months_to_add_to_calculate,
        upper_boundary_nr_of_weeks_to_add_to_calculate,
        upper_boundary_nr_of_days_to_add_to_calculate,
        path_to_file_bought_csv,
        path_to_file_sold_csv,
        add_days_to_date,
        create_id_for_each_row_in_boughtcsv_while_script_generates_this_boughtcsv,
        generate_random_buy_date_for_buy_transaction_in_future_in_time_interval
    )

if __name__ == "__main__":
    main()



