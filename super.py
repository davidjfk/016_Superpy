# Do not change these lines.
__winc_id__ = "a2bc36ea784242e4989deb157d527ba0"
__human_name__ = "superpy"
# Your code below this line.

# Imports
import argparse, os, sys
import csv
from datetime import date, datetime

from rich.table import Table
from rich.console import Console

sys.path.append('c:\\dev\\pytWinc\\superpy')
sys.path.append('c:\\dev\\pytWinc\\superpy\\utils_superpy')

# the following 4 imported fns are arguments in fn create_data_for_csv_files_bought_and_sold() below.
from utils_superpy.utils import add_days_to_date
from utils_superpy.utils import generate_random_buy_date_for_buy_transaction_in_future_in_time_interval
from utils_superpy.utils import create_buy_id_for_each_row_in_boughtcsv_as_part_of_mockdata_that_is_being_created
from utils_superpy.utils import get_path_to_directory_of_file

from utils_superpy.utils import buy_product, create_data_for_csv_files_bought_and_sold
from utils_superpy.utils import create_buy_id_that_increments_highest_buy_id_in_boughtcsv
from utils_superpy.utils import get_path_to_file, get_system_date
from utils_superpy.utils import sell_product, set_system_date_to, time_travel_system_date_with_nr_of_days
from utils_superpy.utils import show_csv_file_in_console_with_module_rich
from utils_superpy.utils import calculate_revenue_in_time_range_between_start_date_and_end_date_inclusive
from utils_superpy.utils import get_highest_buy_id_from_boughtcsv_after_running_fn_to_create_mock_data_for_boughtcsv_and_soldcsv
from utils_superpy.utils import set_buy_id_in_file_id_to_use_in_fn_to_buy_product_txt_after_running_fn_to_create_mock_data_for_boughtcsv_and_soldcsv
from utils_superpy.utils import calculate_cost_in_time_range_between_start_date_and_end_date_inclusive
from utils_superpy.utils import calculate_profit_in_time_range_between_start_date_and_end_date_inclusive
from utils_superpy.utils import calculate_sales_volume_in_time_range_between_start_date_and_end_date_inclusive
from utils_superpy.utils import calculate_expired_products_on_day
from utils_superpy.utils import show_list_with_nested_lists_in_console_with_module_rich
from utils_superpy.utils import calculate_inventory_on_day


def main():

    # CONFIGURATION:
    '''
    Scope: only subparser create_mock_data uses the following variables as default values for its optional arguments. 
    Change them at your liking.
    ex: if you want to create mock data for 5 products very often, then change PRODUCT_RANGE to 5 below, so you can do:
    
    py super.py create_mock_data
    
    instead of using the optional flag -pr 5 in the command line:
    e.g.:
    py super.py create_mock_data -pr 5
    or: 
    py super.py create_mock_data -pr 5 -del_row 3 -sl 10 -tt 3 -mu 3 -lby 2024 -lbm 10 -lbd 15 -ubmnr 3 -ubwnr 8 -ubdnr 3

    '''
    PRODUCT_RANGE = 3
    # see 'produt_range' definition in README_SOFTWARE_DESIGN.md --> ch definitions. 

    DELETE_EVERY_NTH_ROW_IN_SOLDCSV_SO_EVERY_NTH_ROW_IN_BOUGHTCSV_CAN_EXPIRE_WHEN_TIME_TRAVELLING = 2
    '''
    explanation:
    In subparser create_mock_data, fn create_data_for_csv_files_bought_and_sold() first creates mockdata for bought.csv, 
    based on the supplied arguments. Then it creates a copy of bought.csv and calls it sold.csv.
    Then it deletes every nth row in sold.csv, so that when time travelling, every nth row in bought.csv will expire.
    '''
    SHELF_LIFE = 10 # days
    # see shelf_life definition in README_SOFTWARE_DESIGN.md --> ch definitions.

    TURNOVER_TIME = 3 # days
    # see turnover_time definition in README_SOFTWARE_DESIGN.md --> ch definitions.
    
    MARKUP = 3
    # see markup definition in README_SOFTWARE_DESIGN.md --> ch definitions.

    # see time_interval definition in README_SOFTWARE_DESIGN.md --> ch definitions:

    '''
    pitfall / for future reference: do not (try to) assign a default value here in this section to  the following variables:
        lower_boundary_year_of_time_interval_in_which_to_create_random_testdata = 2023
        lower_boundary_month_of_time_interval_in_which_to_create_random_testdata = 10
        lower_boundary_week_of_time_interval_in_which_to_create_random_testdata = 1

        Reason: variable system_date sets / assigns the default values of these variables in the subparser create_mock_data below! 
    '''


    UPPER_BOUNDARY_NR_OF_MONTHS_TO_ADD_TO_CALCULATE = 2
    UPPER_BOUNDARY_NR_OF_WEEKS_TO_ADD_TO_CALCULATE = 0
    UPPER_BOUNDARY_NR_OF_DAYS_TO_ADD_TO_CALCULATE = 0



    # CONSTANTS: (do not change these lines!!)
    DATA_DIRECTORY = "data_used_in_superpy"
    FILE_WITH_SYSTEM_DATE = "system_date.txt"
    PATH_TO_SYSTEM_DATE = get_path_to_file(DATA_DIRECTORY , FILE_WITH_SYSTEM_DATE)
    SYSTEM_DATE = get_system_date(PATH_TO_SYSTEM_DATE) # e.g. 2023-10-11

    path_to_project_superpy  = str(os.getcwd()) # only used once, so not a constant. 
    PATH_TO_DATA_DIRECTORY_INSIDE_PROJECT_SUPERPY = os.path.abspath(os.path.join(path_to_project_superpy, DATA_DIRECTORY))
    PATH_TO_FILE_WITH_SYSTEM_DATE = os.path.join(PATH_TO_DATA_DIRECTORY_INSIDE_PROJECT_SUPERPY, FILE_WITH_SYSTEM_DATE)

    '''
    goal: create constant  START_DATE_OF_CURRENT_FINANCIAL_YEAR

    If system_date is 2023-10-11, then start date of current financial year is 2023-01-01.
    If system_date is 2024-06-24, then start date of current financial year is 2024-01-01.
    If system_date is 2025-09-06, then start date of current financial year is 2025-01-01.
    '''
    year = int(SYSTEM_DATE[:4]) 
    start_date_of_current_financial_year_unformatted = date(year, 1, 1) 
    # a date object does not have a format. It is just a date object.
    # data type of start_date_of_current_financial_year_unformatted: <class 'datetime.date'>
    START_DATE_OF_CURRENT_FINANCIAL_YEAR = start_date_of_current_financial_year_unformatted.strftime('%Y-%m-%d') 
    # output: e.g. 2023-01-01 (i.e. in prescribed format '%Y-%m-%d')
    # data type of START_DATE_OF_CURRENT_FINANCIAL_YEAR: <class 'str'>


    #step: initialize parser
    parser = argparse.ArgumentParser(prog='super.py',description="Welcome to inventory management tool Superpy.", epilog="The line between disorder and order lies in logistics.", formatter_class=argparse.RawTextHelpFormatter)

    # step: create container for all subparsers. --> 'command' is a container for [and name of] all the subparsers.
    subparsers = parser.add_subparsers(dest="command", help='Commands: \n buy\n create_mock_data\n delete\n sell\n set_date\n show_bought_csv\n show_cost\n show_expired_products\n show_inventory\n show_profit\n show_revenue\n show_sales_volume\n show_sold_csv\n time_travel\n\n')


    # 1_BUY: create subparser "buy" with help text and add it to the container "command":
    subparser_buy_product = subparsers.add_parser("buy", help="goal: buy product and add to file bought.csv \n   ex1: py super.py buy apple 1.75 -bd 23-09-15 -sd 23-09-27 \n   product: apple,  price: E 1.75, buy_date: 23-09-15, expiry_date: 23-09-27\n\n   ex2: py super.py buy linseed 3.00 -exd 23-09-28 \n   product: linseed, price: &euro; 3.00, buy_date: system_date as default, expiry_date: 23-09-28\n\n   ex3: py super.py buy cabbage 0.73 \n   product: cabbage, price: E 0.73, buy_date: system_date as default, expiry_date:  'does not expire' as default \n\n   arg1: positional argument product: e.g. apple, potato, milk\n   arg2: positional argument price, in euros: e.g. 1.24, 0.3, 0.35\n   arg3: optional argument -buy_date, -bd (ex: 2023-09-15) with system_date as default value. \n   arg4: optional argument -expiry_date, -exd (ex: 2023-10-03) with default value 'does not expire' \n\n") 
    #step: add the positional and optional arguments to  'subparser_buy_product': 
    subparser_buy_product.add_argument("product_name", type=str, help="e.g. apple, carrot, oats, etc.") 
    subparser_buy_product.add_argument("price", type=float, help="e.g. 1.20 means 1 euro and 20 cents. 0.2 or 0.20 means 20 cents.") 
    # -buy_date gets its default value from file system_date.txt in the DATA_DIRECTORY:
    subparser_buy_product.add_argument("-buy_date", "-bd", default= SYSTEM_DATE, type=str, help="date object with string representation following the format: '%Y-%m-%d'. ex: 2026-10-21 ") 
    subparser_buy_product.add_argument("-expiry_date", "-ed", default="does not expire", type=str, help="supermarket also trades products that do not expire (e.g. cutlery, household equipment, etc. If product has expiry date, then it has following format: '%Y-%m-%d'. ex: 2026-10-21 ") 




    # 2_CREATE_MOCK_DATE: Create subparser "create_mock_data" with help text and add it to the container "command":
    subparser_create_mock_data = subparsers.add_parser("create_mock_data", help="goal: create mock data for bought.csv and sold.csv\n   All 11 arguments have default values that can be changed in (...\superpy\super.py --> goto CONSTANTS at start of main.py()) \n   All 11 arguments are optional, so you can do this:  \n\n   ex1: py super.py create_mock_data \n   result: bought.csv and sold.csv are filled with mockdata that has \n   been created with default values.   \n\n   arg1 = product_range \n   flags: -pr, -product_range.\n   product_range == product_assortment == the amount of different products in Superpy. \n   ex1: py super.py create_mock_data -pr 3 \n   product_range: 3 random products: e.g. 'apple', 'cabbage' and 'beetroot' as input to create mock data \n   ex2: py super.py create_mock_data -pr 2 \n   product_range: 2 random products: e.g. 'coffee' and 'potato' as input to create mock data. \n   More products in product_range lead to more rows in bought.csv and sold.csv. \n   flags: -pr, -product_range \n   ex2: py super.py create_mock_data -pr 3 \n   result: 3 random products are selected from a pre-filled list to \n   create the testdata.  \n\n   arg2 =  delete every nth row in sold.csv \n   purpose: deleting rows makes them expire while time travelling: \n   After creating mock data for bought.csv, a copy is made to create sold.csv. \n   Then rows are deleted from sold.csv (e.g. every 3rd row). \n   By time travelling to the future these bought_products (e.g. every 3rd row) will expire. \n   flags: -del_row, -delete_every_nth_row  \n   ex1: py super.py create_mock_data -del_row 3 \n   delete_every_nth_row: 3  \n\n   arg3 = shelf_life == shelf_time == number of days between buying a product and \n   its expiry_date. \n   flags: -sl, -shelf_life  \n   ex1: py super.py create_mock_data -sl 10\n   shelf_life: 10 days \n   result: a bought product will expire after 10 days.\n\n   arg4 = turnover_time == inventory turnover == the number of days \n   between buying and selling a product. \n   flags: -turnover_time, -tt  \n   ex1: py super.py create_mock_data -tt 4\n   turnover_time: 4 days  \n\n   arg5 = markup = the amount of money a business adds to the cost of a product or service in order to make a profit. \n   In super.py markup is calculated as a factor: ex: if buy_price is 3 euro and sell_price is 4 euro, then markup is 4/3 = 1.33 \n   flags: -mu, -markup  \n   ex: py super.py create_mock_data -mu 3 \n    markup: factor 3  \n   result: if buy_price in bought.csv is 3 euro, then sell_price will be 9 euro in sold.csv.  \n\n   arg6 = lower_boundary_year == lower_boundary_year_of_time_interval_in_which_to_create_random_testdata. \n   flags: -lby, -lower_boundary_year  \n   ex1: py super.py create_mock_data -lby 2024\n   lower_boundary_year: 2024  \n\n   arg7 = lower_boundary_month == lower_boundary_month_of_time_interval_in_which_to_create_random_testdata. \n   flags: -lbm, -lower_boundary_month  \n   ex1: py super.py create_mock_data -lbm 10\n   lower_boundary_month: October  \n\n   arg8 = lower_boundary_day == lower_boundary_day_of_time_interval_in_which_to_create_random_testdata.  \n   flags: -lbd, -lower_boundary_day  \n   ex1: py super.py create_mock_data -lbd 15  \n   lower_boundary_day: 15th day of  the  month \n\n   arg9 =  nr_of_months_to_calculate_upper_boundary_month    \n   flags: -ubmnr, -upper_boundary_month_nr   \n   ex1: py super.py create_mock_data -ubmnr 3\n   nr_of_months_to_calculate_upper_boundary_month: 3 months  \n   result: upper boundary month of time interval in which to create data is 3 months in the future. \n   default value: 0 months.  \n\n   arg10 = nr_of_weeks_to_calculate_upper_boundary_week. \n   flags: -ubwnr, -upper_boundary_weeknr  \n   ex1: py super.py create_mock_data -ubwnr 8\n   nr_of_weeks_to_calculate_upper_boundary_week: 8 months  \n   result: upper boundary week of time interval in which to create data is 8 weeks in the future.  \n\n   arg11 = nr_of_days_to_calculate_upper_boundary_day. \n   flags: -ubdnr, -upper_boundary_day_nr  \n   ex: py super.py create_mock_data -ubdnr 3\n   nr_of_days_to_calculate_upper_boundary_day: 3 days  \n   result: upper boundary day of time interval in which to create data is 3 days in the future.  \n   default value: 0 days.\n\n")
    #step: add the optional arguments to 'subparser_create_mock_data':
    subparser_create_mock_data.add_argument("-product_range", "-pr", default=PRODUCT_RANGE, type=int, help=" ") 
    subparser_create_mock_data.add_argument("-delete_every_nth_row", "-del_nth_row", default=DELETE_EVERY_NTH_ROW_IN_SOLDCSV_SO_EVERY_NTH_ROW_IN_BOUGHTCSV_CAN_EXPIRE_WHEN_TIME_TRAVELLING, type=int, help=" ") 
    subparser_create_mock_data.add_argument("-shelf_life", "-sl", default=SHELF_LIFE, type=int, help="supermarket also trades products that do not expire (e.g. cutlery, household equipment, etc. If product has expiry date, then it has following format: '%Y-%m-%d'. ex: 2026-10-21 ") 
    subparser_create_mock_data.add_argument("-turnover_time", "-tt", default=TURNOVER_TIME, type=int, help=" ")
    subparser_create_mock_data.add_argument("-markup", "-mu", default=MARKUP, type=int, help=" ")
    # ex of system_date: 2023-10-11
    default_year = int(SYSTEM_DATE[:4])
    default_month = int(SYSTEM_DATE[5:7])
    default_day = int(SYSTEM_DATE[8:])
    subparser_create_mock_data.add_argument("-lower_boundary_year_of_time_interval_in_which_to_create_random_testdata", "-lby","-lower_boundary_year", default=default_year, type=int, help="lower_boundary_year_of_time_interval_in_which_to_create_random_testdata")
    subparser_create_mock_data.add_argument("-lower_boundary_month_of_time_interval_in_which_to_create_random_testdata","-lower_boundary_month", "-lbm", default=default_month, type=int, help="lower_boundary_month_of_time_interval_in_which_to_create_random_testdata")
    subparser_create_mock_data.add_argument("-lower_boundary_day_of_time_interval_in_which_to_create_random_testdata","-lower_boundary_day", "-lbd", default=default_day, type=int, help="lower_boundary_day_of_time_interval_in_which_to_create_random_testdata")

    subparser_create_mock_data.add_argument("-upper_boundary_nr_of_months_to_add_to_calculate","-upper_boundary_month", "-ubm", "-ubm", default=UPPER_BOUNDARY_NR_OF_MONTHS_TO_ADD_TO_CALCULATE, type=int, help="upper_boundary_nr_of_months_to_add_to_calculate")
    subparser_create_mock_data.add_argument("-upper_boundary_nr_of_weeks_to_add_to_calculate","-upper_boundary_week", "-ubw", "-upper_boundary_nr_of_weeks_to_add_to_calculate", default=UPPER_BOUNDARY_NR_OF_WEEKS_TO_ADD_TO_CALCULATE, type=int, help="upper_boundary_nr_of_weeks_to_add_to_calculate")
    subparser_create_mock_data.add_argument("-upper_boundary_nr_of_days_to_add_to_calculate","-upper_boundary_day", "-ubd", "-upper_boundary_nr_of_days_to_add_to_calculate", default=UPPER_BOUNDARY_NR_OF_DAYS_TO_ADD_TO_CALCULATE, type=int, help="upper_boundary_nr_of_days_to_add_to_calculate")
    # The remaining fn-arguments are NOT supposed to be changed via argparse-cli


    # 3_DELETE: Create subparser "delete" with help text and add it to the container "command":
    subparser_delete_data = subparsers.add_parser("delete", help="goal: delete all data in bought.csv and sold.csv. \n   ex: py super.py delete \n   result: all transaction records in bought.csv and sold.csv have been deleted   \n\n")
    # subparser does not need any arguments.


    # 4_SELL: create subparser "sell" with help text and add it to the container "command":
    subparser_sell_product = subparsers.add_parser("sell", help="goal: sell product and add to file sold.csv \n   ex1: py super.py b_15 3.75 -sd 2023-11-15 \n   product: row with id b_15 in bought.csv is sold, price: E 3.75, sell_date: 23-11-15\n\n   ex2: py super.py b_16 5.15 \n   product: row with id b_15 in bought.csv is sold, price: E 5.15, sell_date: system_date as default\n\n   ex3: py super.py b_128 2.42 \n   product: row with id b_128 in bought.csv is sold, price: E 2.42, sell_date: system_date as default\n\n   arg1: positional argument buy_id: e.g. b_7, b_18, etc. See bought.csv for buy_ids\n   arg2: positional argument price, in euros: e.g. 1.24, 0.3, 0.35\n   arg3: optional argument -sell_date, -sd (ex: -sd 2023-09-15) with system_date as default value. \n \n\n")
    #step: add the positional and optional arguments to 'subparser_set_date': 
    subparser_sell_product.add_argument("buy_id", type=str, help="e.g. apple, carrot, oats, etc.") 
    subparser_sell_product.add_argument("price", type=float, help="e.g. 1.20 means 1 euro and 20 cents. 0.2 or 0.20 means 20 cents.") 
    # -buy_date gets its default value from file system_date.txt in the DATA_DIRECTORY:
    subparser_sell_product.add_argument("-sell_date", "-sd", default= SYSTEM_DATE, type=str, help="date object with string representation following the format: '%Y-%m-%d'. ex: 2026-10-21 ") 
    # subparser_sell_product.add_argument("-expiry_date", "-ed", default="does not expire", type=str, help="supermarket also trades products that do not expire (e.g. cutlery, household equipment, etc. If product has expiry date, then it has following format: '%Y-%m-%d'. ex: 2026-10-21") 


    # 5_SET_DATE: create subparser "set_date" with help text and add it to the container "command":
    subparser_set_date = subparsers.add_parser("set_date", help="goal: set_system_date_to a specific date in the file system_date.txt\n   ex1: py super.py set_date 2025-01-01 \n   system_date: 2025-01-01 \n\n   arg1: positional argument system_date, e.g. 2023-10-11. \n   --> string representation in format 'yyy-mm-dd'\n\n")
    #step: add the positional and optional arguments to 'subparser_set_date': 
    subparser_set_date.add_argument("-new_system_date", type=str, help="specify the new system date in format YYYY-MM-DD") 


    # 6_SHOW_BOUGHT_CSV: Create subparser "show_bought_csv" with help text and add it to the container "command":
    subparser_show_bought_csv = subparsers.add_parser("show_bought_csv", help="goal: show all data from bought.csv in a table in the terminal \n   ex: py super.py show_bought_csv \n   result: bought.csv is shown in the terminal as a table.   \n\n")   


    # 7_SHOW_COST: Create subparser "show_cost" with help text and add it to the container "command":
    subparser_show_cost = subparsers.add_parser("show_cost", help="goal: show cost in time range between start_date and end_date inclusive. \n   ex1: py super.py show_cost -sd 2023-09-01 -ed 2023-10-10 \n   start_date: 2023-09-01 \n   end_date: 2023-10-10 \n   result in terminal: \n   'Cost from start_date: 2023-09-01 to end_date: 2023-10-10 inclusive: Euro 27.9'  \n\n   ex2: py super.py show_cost -ed 2023-10-05 \n   start_date is start of financial  year of system_date. e.g. if system_date 23-06-08, then: 23-01-01.\n   end_date: 2023-10-05 \n   result in terminal: \n   'Cost from start_date: 2023-01-01 to end_date: 2023-10-05 inclusive: Euro 18.6'   \n\n   ex3: py super.py show_profit -sd 2023-07-01 \n   start_date: 2023-07-01 \n   end_date is by default system_date \n   result in terminal: \n   'Cost from start_date: 2023-07-01 to end_date: 2023-09-17 inclusive: Euro 9.9' \n   end_date has by default system_date.  \n\n   arg1: optional argument start_date in format 'YYYY-MM-DD'. ex: -sd 2023-09-01, or: -start_date 2023-09-01 \n   default value is january 1st of year from system_date: e.g. if system_date is 23-06-28, then default value is 23-01-01. \n   reason: often you want to know the cost of the current financial year until today inclusive. \n\n   arg2: optional argument end_date in format 'YYYY-MM-DD'. ex: -ed 2023-10-15, or: -end_date 2023-10-15 \n   default value is system_date, because often you want to know the cost of the current financial year until today  inclusive.  \n\n")
    #step: add the positional and optional arguments to 'subparser_show_cost':
    subparser_show_cost.add_argument("-start_date","-sd",default=START_DATE_OF_CURRENT_FINANCIAL_YEAR, type=str, help="specify the start date in format YYYY-MM-DD")
    subparser_show_cost.add_argument("-end_date","-ed",default=SYSTEM_DATE, type=str, help="specify the end date in format YYYY-MM-DD")

    # 8_SHOW_EXPIRED_PRODUCTS: create subparser "show_expired_products" with help text and add it to the container "command":
    subparser_buy_product = subparsers.add_parser("show_expired_products", help="goal: calculate expired products on a day in format 'YYYY-MM-DD' (e.g. 2023-09-28) \n   ex1: py super.py show_expired_products -d 2023-09-28\n   date: 2023-09-28   \n   result is displayed in a table in the terminal. \n\n   ex2: py super.py show_expired_products\n   date: by default system_date\n   results is displayed in a table in the terminal. \n\n   arg1: optional argument date in following format: 'YYYY-MM-DD'. ex: -d 2026-10-21 \n   default value is system_date.\n   reason: often you want to know which products expire today.  \n\n") 
    subparser_buy_product.add_argument("-date", "-d", default=SYSTEM_DATE, type=str, help="date in following format: '%Y-%m-%d'. ex: 2026-10-21 ") 

    # 9_SHOW_INVENTORY: create subparser "show_inventory" with help text and add it to the container "command":
    subparser_buy_product = subparsers.add_parser("show_inventory", help="goal: calculate inventory on a day in format 'YYYY-MM-DD' (e.g. 2023-09-28) \n   ex1: py super.py show_inventory -d 2023-09-28\n   date: 2023-09-28   \n   result is displayed in a table in the terminal. \n\n   ex2: py super.py show_inventory\n   date: by default system_date\n   results is displayed in a table in the terminal. \n\n   arg1: optional argument date in following format: 'YYYY-MM-DD'. ex: -d 2026-10-21 \n   default value is system_date.\n   reason: often you want to know which products expire today.  \n\n")  
    subparser_buy_product.add_argument("-date", "-d", default=SYSTEM_DATE, type=str, help="date in following format: '%Y-%m-%d'. ex: 2026-10-21 ") 

    # 10_SHOW_PROFIT: Create subparser "show_profit" with help text and add it to the container "command":
    subparser_show_cost = subparsers.add_parser("show_profit", help="goal: show profit in time range between start_date and end_date inclusive. \n   ex1: py super.py show_profit -sd 2023-09-01 -ed 2023-10-10 \n   start_date: 2023-09-01 \n   end_date: 2023-10-10 \n   result in terminal: \n   'Profit from start_date: 2023-09-01 to end_date: 2023-10-10 inclusive: Euro 27.9'  \n\n   ex2: py super.py show_profit -ed 2023-10-05 \n   start_date is start of financial  year of system_date. e.g. if system_date 23-06-08, then: 23-01-01.\n   end_date: 2023-10-05 \n   result in terminal: \n   'Profit from start_date: 2023-01-01 to end_date: 2023-10-05 inclusive: Euro 18.6'   \n\n   ex3: py super.py show_profit -sd 2023-07-01 \n   start_date: 2023-07-01 \n   end_date is by default system_date \n   result in terminal: \n   'Profit from start_date: 2023-07-01 to end_date: 2023-09-17 inclusive: Euro 9.9' \n   end_date has by default system_date.  \n\n   arg1: optional argument start_date in format 'YYYY-MM-DD'. ex: -sd 2023-09-01, or: -start_date 2023-09-01 \n   default value is january 1st of year from system_date: e.g. if system_date is 23-06-28, then default value is 23-01-01. \n   reason: often you want to know the profit of the current financial year until today inclusive. \n\n   arg2: optional argument end_date in format 'YYYY-MM-DD'. ex: -ed 2023-10-15, or: -end_date 2023-10-15 \n   default value is system_date, because often you want to know the cost of the current financial year until today  inclusive.  \n\n")
    #step: add the positional and optional arguments to 'subparser_show_profit':
    subparser_show_cost.add_argument("-start_date","-sd",default=START_DATE_OF_CURRENT_FINANCIAL_YEAR, type=str, help="specify the start date in format YYYY-MM-DD")
    subparser_show_cost.add_argument("-end_date","-ed",default= SYSTEM_DATE, type=str, help="specify the end date in format YYYY-MM-DD")


    # 11_SHOW_REVENUE: Create subparser "show_revenue" with help text and add it to the container "command":
    subparser_show_revenue = subparsers.add_parser("show_revenue", help="goal: show revenue in time range between start_date and end_date inclusive. \n   ex1: py super.py show_revenue -sd 2023-09-01 -ed 2023-10-10 \n   start_date: 2023-09-01 \n   end_date: 2023-10-10 \n   result in terminal: \n   'Revenue from start_date: 2023-09-01 to end_date: 2023-10-10 inclusive: Euro 27.9'  \n\n   ex2: py super.py show_revenue -ed 2023-10-05 \n   start_date is start of financial  year of system_date. e.g. if system_date 23-06-08, then: 23-01-01.\n   end_date: 2023-10-05 \n   result in terminal: \n   'Revenue from start_date: 2023-01-01 to end_date: 2023-10-05 inclusive: Euro 18.6'   \n\n   ex3: py super.py show_revenue -sd 2023-07-01 \n   start_date: 2023-07-01 \n   end_date is by default system_date \n   result in terminal: \n   'Revenue from start_date: 2023-07-01 to end_date: 2023-09-17 inclusive: Euro 9.9' \n   end_date has by default system_date.  \n\n   arg1: optional argument start_date in format 'YYYY-MM-DD'. ex: -sd 2023-09-01, or: -start_date 2023-09-01 \n   default value is january 1st of year from system_date: e.g. if system_date is 23-06-28, then default value is 23-01-01. \n   reason: often you want to know the revenue of the current financial year until today inclusive. \n\n   arg2: optional argument end_date in format 'YYYY-MM-DD'. ex: -ed 2023-10-15, or: -end_date 2023-10-15 \n   default value is system_date, because often you want to know the cost of the current financial year until today  inclusive.  \n\n")
    #step: add the positional and optional arguments to 'subparser_show_revenue':
    subparser_show_revenue.add_argument("-start_date","-sd",default=START_DATE_OF_CURRENT_FINANCIAL_YEAR, type=str, help="specify the start date in format YYYY-MM-DD")
    subparser_show_revenue.add_argument("-end_date","-ed",default=SYSTEM_DATE, type=str, help="specify the end date in format YYYY-MM-DD")


    # 12_SHOW_SALES_VOLUME: Create subparser "show_sales_volume" with help text and add it to the container "command":
    subparser_show_revenue = subparsers.add_parser("show_sales_volume", help="goal: show sales volume in time range between start_date and end_date inclusive. \n   ex1: py super.py show_sales_volume -sd 2023-09-01 -ed 2023-10-10 \n   start_date: 2023-09-01 \n   end_date: 2023-10-10 \n   result in terminal: \n   'Sales Volume from start_date: 2023-09-01 to end_date: 2023-10-10 inclusive: Euro 27.9'  \n\n   ex2: py super.py show_sales_volume -ed 2023-10-05 \n   start_date is start of financial  year of system_date. e.g. if system_date 23-06-08, then: 23-01-01.\n   end_date: 2023-10-05 \n   result in terminal: \n   'Sales volume from start_date: 2023-01-01 to end_date: 2023-10-05 inclusive: Euro 18.6'   \n\n   ex3: py super.py show_sales_volume -sd 2023-07-01 \n   start_date: 2023-07-01 \n   end_date is by default system_date \n   result in terminal: \n   'Sales volume from start_date: 2023-07-01 to end_date: 2023-09-17 inclusive: Euro 9.9' \n   end_date has by default system_date.  \n\n   arg1: optional argument start_date in format 'YYYY-MM-DD'. ex: -sd 2023-09-01, or: -start_date 2023-09-01 \n   default value is january 1st of year from system_date: e.g. if system_date is 23-06-28, then default value is 23-01-01. \n   reason: often you want to know the sales volume of the current financial year until today inclusive. \n\n   arg2: optional argument end_date in format 'YYYY-MM-DD'. ex: -ed 2023-10-15, or: -end_date 2023-10-15 \n   default value is system_date, because often you want to know the cost of the current financial year until today  inclusive.  \n\n")
    #step: add the positional and optional arguments to 'subparser_show_revenue':
    subparser_show_revenue.add_argument("-start_date","-sd",default=START_DATE_OF_CURRENT_FINANCIAL_YEAR, type=str, help="specify the start date in format YYYY-MM-DD")
    subparser_show_revenue.add_argument("-end_date","-ed",default=SYSTEM_DATE, type=str, help="specify the end date in format YYYY-MM-DD")


    # 13_SHOW_SOLD_CSV: Create subparser "show_sold_csv" with help text and add it to the container "command":
    subparser_show_sold_csv = subparsers.add_parser("show_sold_csv", help="goal: show all data from sold.csv in a table in the terminal. \n   ex: py super.py show_sold_csv \n   result: sold.csv is shown in the terminal as a table   \n\n") 


    # 14_TIME_TRAVEL: create subparser "time_travel" with help text and add it to the container "command":
    subparser_time_travel = subparsers.add_parser("time_travel", help="goal: change system_date by adding or subtracting nr of day(s) \n   ex1: py super.py time_travel 3.\n   nr_of_days: 3 \n   result: you travel with 3 days to the future. So if system_date is 2024-03-10, then \n   new date becomes 2024-03-13 in the future.\n\n   ex2: py super.py time_travel -3\n   nr_of_days: -3 \n   result: you travel with 3 days to the past. So if system date is 2024-03-10, \n   then new date becomes 2024-03-07 in the past.\n\n   arg1: positional argument days to add or subtract from system_date: e.g. 9, -8, etc.\n ") 
    #step: add the positional and optional arguments to  'subparser_time_travel': 
    subparser_time_travel.add_argument("nr_of_days", type=int, help="specify the new system date in format YYYY-MM-DD") 


    args = parser.parse_args()




    if args.command == "buy":
        print("buy:")
        path_to_id_with_highest_sequence_number = os.path.join(PATH_TO_DATA_DIRECTORY_INSIDE_PROJECT_SUPERPY, 'id_to_use_in_fn_buy_product.txt')
        # print(path_to_id_with_highest_sequence_number)
        id_of_row_in_csv_file_bought = create_buy_id_that_increments_highest_buy_id_in_boughtcsv(path_to_id_with_highest_sequence_number) 

        path_to_csv_bought_input_file = os.path.join(PATH_TO_DATA_DIRECTORY_INSIDE_PROJECT_SUPERPY, 'bought.csv')
        path_to_csv_bought_output_file = path_to_csv_bought_input_file # but not the same in pytest.
        buy_product(args.product_name, args.price, args.buy_date, args.expiry_date, id_of_row_in_csv_file_bought, path_to_csv_bought_input_file, path_to_csv_bought_output_file) 


    if args.command == "create_mock_data":
        print("create_mock_data:")
        path_to_csv_bought_input_file = os.path.join(PATH_TO_DATA_DIRECTORY_INSIDE_PROJECT_SUPERPY, 'bought.csv')
        path_to_csv_sold_input_file = os.path.join(PATH_TO_DATA_DIRECTORY_INSIDE_PROJECT_SUPERPY, 'sold.csv')
        create_data_for_csv_files_bought_and_sold(
            args.product_range,
            args.delete_every_nth_row,
            args.shelf_life,
            args.turnover_time,
            args.markup,
            args.lower_boundary_year_of_time_interval_in_which_to_create_random_testdata,
            args.lower_boundary_month_of_time_interval_in_which_to_create_random_testdata,
            args.lower_boundary_day_of_time_interval_in_which_to_create_random_testdata,
            args.upper_boundary_nr_of_months_to_add_to_calculate,
            args.upper_boundary_nr_of_weeks_to_add_to_calculate,
            args.upper_boundary_nr_of_days_to_add_to_calculate,
            path_to_csv_bought_input_file,
            path_to_csv_sold_input_file,
            add_days_to_date,
            create_buy_id_for_each_row_in_boughtcsv_as_part_of_mockdata_that_is_being_created,
            generate_random_buy_date_for_buy_transaction_in_future_in_time_interval
        )
        '''

        subject: synchronize buy_ids that can be created and deleted by user in following ways: 

        There are 2 ways in the superpy-app to create buy_ids:

        a. in argparse cli interface, user can create mock data with
        with following command: python super.py --create_mock_data (plus
        optional parameters) --> invoking fn create_data_for_csv_files_bought_and_sold right above this comment.

        b. in argparse cli interface, user can create buy-transaction with e.g.
        following command: python super.py --buy apple 0.39 (plus optional parameters)

        There is 1 way in the superpy-app to delete buy_ids:
        c. in argparse cli interface, user can delete all data from bought.csv and sold.csv
        with following command: python super.py delete

        If e.g. script creates 149 buy-transactions (b_1, b_2, (...) b_149), 
        then the next buy-transaction should start with b_150. 
        Challenge: created mock data can contain any number of buy-transactions.
        Another challenge: script can delete all data from bought.csv and sold.csv.
        No matter how a. , b. and c. are mixed together, the next buy-transaction created by the user must be 
        either b_1 (if bought.csv is empty) or be the next buy_id in bought.csv (if e.g. bought.csv has 149 rows, then last
        buy_id is b_149, so the next buy_id must be b_150)
        
        The following code makes that happen:
        '''
        path_to_csv_bought_file = get_path_to_file("data_used_in_superpy", "bought.csv")

        highest_buy_id_in_boughtcsv = get_highest_buy_id_from_boughtcsv_after_running_fn_to_create_mock_data_for_boughtcsv_and_soldcsv(path_to_csv_bought_file)
        print(f"highest_buy_id_from_boughtcsv: {highest_buy_id_in_boughtcsv}")
        # pitfall: do not increment buy_id with 1 for the next buy-transaction: e.g. b_1 --> b_2. This will be done at other point in the code. 

        path_to_file_with_name_id_to_use_in_fn_buy_product = get_path_to_file("data_used_in_superpy", "id_to_use_in_fn_buy_product.txt")

        buy_id = set_buy_id_in_file_id_to_use_in_fn_to_buy_product_txt_after_running_fn_to_create_mock_data_for_boughtcsv_and_soldcsv(highest_buy_id_in_boughtcsv, path_to_file_with_name_id_to_use_in_fn_buy_product)
        print(f"new_system_date: {buy_id}")
        '''
        suppose fn 'create_data_for_csv_files_bought_and_sold' has just created 132 rows of mock data for bought.csv 
        (the nr of rows in sold.csv depend on how many are deleted from these 132 rows by the script).
        That means that the nex buy_transaction to be added to bought.csv by the USER of the superpy-app, must have buy_id b_133. 
        For this to happen, in directory 'data_used_in_superpy': file 'id_to_use_in_fn_buy_product.txt' must now be set to buy_id 'b_132'.
        
        When creating this next buy_transaction, fn 'create_buy_id_that_increments_highest_buy_id_in_boughtcsv 
        will increment 'b_132' with 1, so this next transaction will show up in bought.csv as 'b_133'.
        '''    

    if args.command == "delete":
        print("delete:")
        path_to_csv_bought_input_file = os.path.join(PATH_TO_DATA_DIRECTORY_INSIDE_PROJECT_SUPERPY, 'bought.csv')
        path_to_csv_sold_input_file = os.path.join(PATH_TO_DATA_DIRECTORY_INSIDE_PROJECT_SUPERPY, 'sold.csv')
        # step: delete all data in bought.csv and sold.csv:

        '''
        Goal: delete all transaction records in bought.csv and sold.csv.
        How2: assign 0 to variable 'product_range_to_delete_all_records_in_bought_csv_and_sold_csv'.
        It does not matter what the values of the other fn-arguments are, as long as
        the datatypes of the other fn-arguments remain correct. So do not do e.g. this:
        shelf_life = 'foo'.
        '''
        product_range_to_delete_all_records_in_bought_csv_and_sold_csv = 0
        # see 'product_range' definition in README_SOFTWARE_DESIGN.md --> ch definitions. 

        '''
        The following 10 variables never change. So to avoid bugs, I do not use the CONSTANTS at the beginning of 
        main.py to define them: 
        '''

        delete_every_nth_row_in_soldcsv_so_every_nth_row_in_boughtcsv_can_expire_when_time_travelling = 2

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
            product_range_to_delete_all_records_in_bought_csv_and_sold_csv,
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
            create_buy_id_for_each_row_in_boughtcsv_as_part_of_mockdata_that_is_being_created,
            generate_random_buy_date_for_buy_transaction_in_future_in_time_interval
        )

    if args.command == "sell":
        print("sell:")
        path_to_csv_sold_input_file = os.path.join(PATH_TO_DATA_DIRECTORY_INSIDE_PROJECT_SUPERPY, 'sold.csv')
        path_to_csv_sold_output_file = path_to_csv_sold_input_file # but not the same in pytest.
        sell_product(args.buy_id, args.price, args.sell_date, path_to_csv_sold_input_file, path_to_csv_sold_output_file)

    if args.command == "set_date":
        print("set_date")
        # step: call fn set_system_date_to to update file system__date.txt with following date:
        system_date = set_system_date_to(args.new_system_date, PATH_TO_FILE_WITH_SYSTEM_DATE)
        print(system_date) 


    if args.command == "show_bought_csv":
        # set path to file bought.csv:
        path_to_directory_testdata = ''
        path_to_directory_testdata = get_path_to_directory_of_file('data_used_in_superpy')
        path_to_file_bought_csv = os.path.join(path_to_directory_testdata, 'bought.csv') 
        show_csv_file_in_console_with_module_rich(path_to_file_bought_csv)


    if args.command == "show_cost":
        # set path to file sold.csv:
        path_to_directory_testdata = ''
        path_to_directory_testdata = get_path_to_directory_of_file('data_used_in_superpy')
        path_to_file_bought_csv = os.path.join(path_to_directory_testdata, 'bought.csv') 
        cost = calculate_cost_in_time_range_between_start_date_and_end_date_inclusive(args.start_date, args.end_date, path_to_file_bought_csv)
        print('---------------------------------------------------------------------------------------------------')
        print('                                                                                                   ')
        print(f"Cost from start_date: {args.start_date} to end_date: {args.end_date} inclusive: Euro {cost}")
        print('                                                                                                   ')
        print('---------------------------------------------------------------------------------------------------')


    if args.command == "show_expired_products":
        path_to_directory_testdata = ''
        path_to_file_bought_csv = ''
        path_to_file_bought_csv = get_path_to_file('data_used_in_superpy', "bought.csv")
        path_to_directory_testdata = get_path_to_directory_of_file('data_used_in_superpy')
        path_to_file_sold_csv = os.path.join(path_to_directory_testdata, 'sold.csv') 
        expired_products = calculate_expired_products_on_day(args.date, path_to_file_sold_csv, path_to_file_bought_csv)
        
        print('---------------------------------------------------------------------------------------------------')
        print('                                                                                                   ')
        print(f"Expired products on date: {args.date}: ")
        print('                                                                                                   ')
        
        show_list_with_nested_lists_in_console_with_module_rich(expired_products)

    if args.command == "show_inventory":
        path_to_directory_testdata = ''
        path_to_file_bought_csv = ''
        path_to_file_bought_csv = get_path_to_file('data_used_in_superpy', "bought.csv")
        path_to_directory_testdata = get_path_to_directory_of_file('data_used_in_superpy')
        path_to_file_sold_csv = os.path.join(path_to_directory_testdata, 'sold.csv') 
        inventory = calculate_inventory_on_day(args.date, path_to_file_sold_csv, path_to_file_bought_csv)
        print('---------------------------------------------------------------------------------------------------')
        print('                                                                                                   ')
        print(f"Inventory on date: {args.date}: ")
        print('                                                                                                   ')
        
        show_list_with_nested_lists_in_console_with_module_rich(inventory)

    if args.command == "show_profit":
        # set path to file sold.csv:
        path_to_csv_sold_file = get_path_to_file('data_used_in_superpy', "sold.csv")
        path_to_csv_bought_file = get_path_to_file('data_used_in_superpy', "bought.csv")
        profit = calculate_profit_in_time_range_between_start_date_and_end_date_inclusive(args.start_date, args.end_date, path_to_csv_sold_file, path_to_csv_bought_file, calculate_revenue_in_time_range_between_start_date_and_end_date_inclusive, calculate_cost_in_time_range_between_start_date_and_end_date_inclusive)
        print('---------------------------------------------------------------------------------------------------')
        print('                                                                                                   ')
        print(f"Profit from start_date: {args.start_date} to end_date: {args.end_date} inclusive: Euro {profit}")
        print('                                                                                                   ')
        print('---------------------------------------------------------------------------------------------------')

    if args.command == "show_revenue":
        # set path to file sold.csv:
        path_to_directory_testdata = ''
        path_to_directory_testdata = get_path_to_directory_of_file('data_used_in_superpy')
        path_to_file_sold_csv = os.path.join(path_to_directory_testdata, 'sold.csv') 
        revenue = calculate_revenue_in_time_range_between_start_date_and_end_date_inclusive(args.start_date, args.end_date, path_to_file_sold_csv)
        show_csv_file_in_console_with_module_rich
        print('---------------------------------------------------------------------------------------------------')
        print('                                                                                                   ')
        print(f"Revenue from start_date: {args.start_date} to end_date: {args.end_date} inclusive: Euro {revenue}")
        print('                                                                                                   ')
        print('---------------------------------------------------------------------------------------------------')



    if args.command == "show_sales_volume":
        # set path to file sold.csv:
        path_to_directory_testdata = ''
        path_to_directory_testdata = get_path_to_directory_of_file('data_used_in_superpy')
        path_to_file_sold_csv = os.path.join(path_to_directory_testdata, 'sold.csv') 
        sales_volume = calculate_sales_volume_in_time_range_between_start_date_and_end_date_inclusive(args.start_date, args.end_date, path_to_file_sold_csv)
        print('---------------------------------------------------------------------------------------------------')
        print('                                                                                                   ')
        print(f"Sales volume from start_date: {args.start_date} to end_date: {args.end_date} inclusive: {sales_volume} products")
        print('                                                                                                   ')
        print('---------------------------------------------------------------------------------------------------')

    if args.command == "show_sold_csv":
        # set path to file sold.csv:
        path_to_directory_testdata = ''
        path_to_directory_testdata = get_path_to_directory_of_file('data_used_in_superpy')
        path_to_file_bought_csv = os.path.join(path_to_directory_testdata, 'sold.csv') 
        show_csv_file_in_console_with_module_rich(path_to_file_bought_csv)



    if args.command == "time_travel":
        print("time_travel")
        # step: call fn time_travel_system_date_with_nr_of_days to update file system__date.txt with following date:
        new_system_date = time_travel_system_date_with_nr_of_days(args.nr_of_days, PATH_TO_FILE_WITH_SYSTEM_DATE, PATH_TO_FILE_WITH_SYSTEM_DATE)
        print(new_system_date) 

if __name__ == "__main__":
    main()