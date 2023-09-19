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
from utils_superpy.utils import create_id_for_each_row_in_boughtcsv_while_script_generates_this_boughtcsv
from utils_superpy.utils import get_path_to_directory_of_file

from utils_superpy.utils import buy_product, create_data_for_csv_files_bought_and_sold
from utils_superpy.utils import create_id_with_unused_highest_sequence_nr_to_buy_product_as_superpy_user
from utils_superpy.utils import get_path_to_file, get_system_date
from utils_superpy.utils import sell_product, set_system_date_to, time_travel_system_date_with_nr_of_days
from utils_superpy.utils import show_csv_file_in_console_with_module_rich
from utils_superpy.utils import calculate_revenue_in_time_range_between_start_date_and_end_date_inclusive
from utils_superpy.utils import get_highest_buy_id_after_running_script_to_create_mock_data_for_boughtcsv_and_soldcsv
from utils_superpy.utils import set_buy_id_after_running_script_to_create_mock_data_for_boughtcsv_and_soldcsv
from utils_superpy.utils import calculate_cost_in_time_range_between_start_date_and_end_date_inclusive
from utils_superpy.utils import calculate_profit_in_time_range_between_start_date_and_end_date_inclusive
from utils_superpy.utils import calculate_sales_volume_in_time_range_between_start_date_and_end_date_inclusive
from utils_superpy.utils import calculate_expired_products_on_day
from utils_superpy.utils import show_list_with_nested_lists_in_console_with_module_rich
from utils_superpy.utils import calculate_inventory_on_day


def main():

    # CONSTANTS:
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
    subparsers = parser.add_subparsers(dest="command", help='Commands: \n buy\n delete\n create_mock_data\n sell\n set_date\n show_bought_csv\n show_cost\n show_expired_products\n show_inventory\n show_profit\n show_revenue\n show_sales_volume\n show_sold_csv\n time_travel\n\n')


    # BUY: create subparser "buy" with help text and add it to the container "command":
    subparser_buy_product = subparsers.add_parser("buy", help="goal: buy product and add to file bought.csv \n   ex: py super.py buy apple 1.75 23-09-15 23-09-27 --> buy_date is 23-09-15 .\n   expiry_date is 23-09-27\n   ex: py super.py buy apple 3.00 23-09-28 --> taking system_date as default buy_date. \n   expiry_date is 23-09-20\n   ex: py super.py buy cabbage 0.73 --> taking system_date as default sell_date, and \n   'does not expire' as default expiry_date\n   arg1: product: e.g. apple, potato, milk\n   arg2: price in euros: e.g. 1.24, 0.3, 0.35\n   arg3: buy_date e.g. 2023-09-15\n   arg4: expiry_date, e.g. 2023-09-29\n\n") 
    #step: add the positional and optional arguments to  'subparser_buy_product': 
    subparser_buy_product.add_argument("product_name", type=str, help="e.g. apple, carrot, oats, etc.") 
    subparser_buy_product.add_argument("price", type=float, help="e.g. 1.20 means 1 euro and 20 cents. 0.2 or 0.20 means 20 cents.") 
    # -buy_date gets its default value from file system_date.txt in the DATA_DIRECTORY:
    
    subparser_buy_product.add_argument("-buy_date", "-b", default= SYSTEM_DATE, type=str, help="date object with string representation following the format: '%Y-%m-%d'. ex: 2026-10-21 ") 
    subparser_buy_product.add_argument("-expiry_date", "-e", default="does not expire", type=str, help="supermarket also trades products that do not expire (e.g. cutlery, household equipment, etc. If product has expiry date, then it has following format: '%Y-%m-%d'. ex: 2026-10-21 ") 




    # CREATE_MOCK_DATE: Create subparser "create_mock_data" with help text and add it to the container "command":
    subparser_create_mock_data = subparsers.add_parser("create_mock_data", help="goal: create mock data for bought.csv and sold.csv. \n   ex: py super.py create_mock_data \n   result: bought.csv and sold.csv are filled with mockdata that has \n   been created with default values.   \n\narg1 = product_range.     product_range == product_assortment == the amount of different products in a shop . \n   e.g. ['apple', 'cabbage', 'beetroot'], or e.g. ['coffee', 'potato', 'orange']. \n   more products in product_range lead to more rows in bought.csv and sold.csv. \n   flags: -pr, -product_range \n   ex: py super.py -pr 3 \n   result: 3 random products are selected from a pre-filled list to \n   create the testdata. The more products, the more records in bought.csv and \n   sold.csv will be generated. \n\narg2 = delete_every_nth_row == 'deleting each nth list in list': this sets nr of rows \n   to delete from sold.csv: \n   flags: -del_row, -delete_every_nth_row  \n   ex: py super.py -del_row 3 \n   result: delete every 3rd row in sold.csv\n   The idea behind this fn-argument is the following \n   fn creates data for bought.csv. Then to create sold.csv a deepcopy is made from \n   bought.csv . Then rows are deleted from sold.csv (e.g. every 3rd row). \n   By time travelling to the future these bought_products (e.g. every 3rd row) will expire.  \n\narg3 = shelf_life. shelf_life == shelf_time == number of days between buying a product and \n   its expiry_date. ex: 3 is three days. \n   flags: -sl, -shelf_life  \n   ex: py super.py -sl 10 \n   result: a bought product will expire after 10 days.\n\narg4 = turnover_time == inventory turnover == the number of days \n   between buying and selling a product. \n   flags:  \n   ex: py super.py  \n   result:  \n\narg5 = markup = the amount of money a business adds to the cost of a product or service in order to make a profit. \n   In super.py markup is calculated as a factor: ex: if buy_price is 3 euro and sell_price is 4 euro, then markup is 4/3 = 1.33 \n   flags: -mu, -markup  \n   ex: py super.py -mu 3  \n   result: if price_bought is 3 euro, then price_sell will be 9 euro.  \n\narg6 = lower_boundary_year_of_time_interval_in_which_to_create_random_testdata. \n   flags: -lby, -lower_boundary_year  \n   ex: py super.py -lby 2024  \n   result: lower boundary year of time interval in which to create data is 2024. \n   system_date provides default value. \n\narg7 = lower_boundary_month_of_time_interval_in_which_to_create_random_testdata. \n   flags: -lbm, -lower_boundary_month  \n   ex: py super.py -lbm 10  \n   result: lower boundary month of time interval in which to create data is October.  \n   system_date provides default value.\n\narg8 = lower_boundary_day_of_time_interval_in_which_to_create_random_testdata.  \n   flags: -lbd, -lower_boundary_day  \n   ex: py super.py -lbd 15  \n   result: lower boundary day of time interval in which to create data is day 15 \n   system_date provides default value.\n\narg9 = upper_boundary_nr_of_months_to_add_to_calculate.  \n   flags: -ubm, -upper_boundary_month   \n   ex: py super.py -ubm 3  \n   result: upper boundary month of time interval in which to create data is 3 months in the future. \n   default value: 0 months.  \n\narg10 = upper_boundary_nr_of_weeks_to_add_to_calculate. \n   flags: -ubw, -upper_boundary_week  \n   ex: py super.py -ubm 8  \n   result: upper boundary week of time interval in which to create data is 8 weeks in the future.  \n   default value: 4 weeks. So by default time interval is from system_date as lower \n   boundary to 4 weeks in the future as its upper boundary.\n\narg11 = upper_boundary_nr_of_days_to_add_to_calculate. \n   flags: -ubd, -upper_boundary_day  \n   ex: py super.py  -ubd 3  \n   result: upper boundary day of time interval in which to create data is 3 days in the future.  \n   default value: 0 days.\n\n")
    #step: add the optional arguments to 'subparser_create_mock_data':
    subparser_create_mock_data.add_argument("-product_range", "-pr", default=2, type=int, help=" ") 
    subparser_create_mock_data.add_argument("-delete_every_nth_row", "-del_nth_row", default=3, type=int, help=" ") 
    subparser_create_mock_data.add_argument("-shelf_life", "-sl", default=10, type=int, help="supermarket also trades products that do not expire (e.g. cutlery, household equipment, etc. If product has expiry date, then it has following format: '%Y-%m-%d'. ex: 2026-10-21 ") 
    subparser_create_mock_data.add_argument("-turnover_time", "-tt", default=3, type=int, help=" ")
    subparser_create_mock_data.add_argument("-markup", "-mu", default=3, type=int, help=" ")
    # ex of system_date: 2023-10-11
    default_year = int(SYSTEM_DATE[:4])
    default_month = int(SYSTEM_DATE[5:7])
    default_day = int(SYSTEM_DATE[8:])
    subparser_create_mock_data.add_argument("-lower_boundary_year_of_time_interval_in_which_to_create_random_testdata", "-lby","-lower_boundary_year", default=default_year, type=int, help="lower_boundary_year_of_time_interval_in_which_to_create_random_testdata")
    subparser_create_mock_data.add_argument("-lower_boundary_month_of_time_interval_in_which_to_create_random_testdata","-lower_boundary_month", "-lbm", default=default_month, type=int, help="lower_boundary_month_of_time_interval_in_which_to_create_random_testdata")
    subparser_create_mock_data.add_argument("-lower_boundary_day_of_time_interval_in_which_to_create_random_testdata","-lower_boundary_day", "-lbd", default=default_day, type=int, help="lower_boundary_day_of_time_interval_in_which_to_create_random_testdata")

    subparser_create_mock_data.add_argument("-upper_boundary_nr_of_months_to_add_to_calculate","-upper_boundary_month", "-ubm", "-ubm", default=2, type=int, help="upper_boundary_nr_of_months_to_add_to_calculate")
    subparser_create_mock_data.add_argument("-upper_boundary_nr_of_weeks_to_add_to_calculate","-upper_boundary_week", "-ubw", "-upper_boundary_nr_of_weeks_to_add_to_calculate", default=0, type=int, help="upper_boundary_nr_of_weeks_to_add_to_calculate")
    subparser_create_mock_data.add_argument("-upper_boundary_nr_of_days_to_add_to_calculate","-upper_boundary_day", "-ubd", "-upper_boundary_nr_of_days_to_add_to_calculate", default=0, type=int, help="upper_boundary_nr_of_days_to_add_to_calculate")
    # The remaining fn-arguments are NOT supposed to be changed via argparse-cli


    # DELETE: Create subparser "delete" with help text and add it to the container "command":
    subparser_delete_data = subparsers.add_parser("delete", help="goal: delete all data in bought.csv and sold.csv. \n   ex: py super.py delete \n   result: bought.csv and sold.csv are empty.   \n\n")
    # subparser does not need any arguments.


    # SELL: create subparser "sell" with help text and add it to the container "command":
    subparser_sell_product = subparsers.add_parser("sell", help="goal: sell product and add to file sold.csv \n   ex: py super.py b_15 3.75 2023-11-15 --> taking 2023-11-15 as sell_date \n   ex: py super.py b_16 5.15 --> taking system_date as default sell_date. \n   ex: py super.py b_128 2.42 --> taking system_date as default sell_date.\n   arg1: buy_id: e.g. b_7, b_18, etc. See bought.csv for buy_ids\n   arg2: price in euros: e.g. 1.24, 0.3, 0.35\n   arg3: sell_date e.g. 2023-09-15\n\n")
    #step: add the positional and optional arguments to 'subparser_set_date': 
    subparser_sell_product.add_argument("buy_id", type=str, help="e.g. apple, carrot, oats, etc.") 
    subparser_sell_product.add_argument("price", type=float, help="e.g. 1.20 means 1 euro and 20 cents. 0.2 or 0.20 means 20 cents.") 
    # -buy_date gets its default value from file system_date.txt in the DATA_DIRECTORY:
    subparser_sell_product.add_argument("-sell_date", "-s", default= SYSTEM_DATE, type=str, help="date object with string representation following the format: '%Y-%m-%d'. ex: 2026-10-21 ") 
    subparser_sell_product.add_argument("-expiry_date", "-e", default="does not expire", type=str, help="supermarket also trades products that do not expire (e.g. cutlery, household equipment, etc. If product has expiry date, then it has following format: '%Y-%m-%d'. ex: 2026-10-21") 


    # SET_DATE: create subparser "set_date" with help text and add it to the container "command":
    subparser_set_date = subparsers.add_parser("set_date", help="goal: set_system_date_to a specific date in the file system__date.txt\n   Use string representation following format 'yyy-mm-dd'\n   ex: py super.py set_date 2020-03-10 \n   Result: system_date is set to 2020-03-10 in file system_date.txt\n   arg1: system_date e.g. 2023-10-11\n   arg2: system_date e.g. 2023-10-11\n\n")
    #step: add the positional and optional arguments to 'subparser_set_date': 
    subparser_set_date.add_argument("new_system_date", type=str, help="specify the new system date in format YYYY-MM-DD") 


    # SHOW_BOUGHT_CSV: Create subparser "show_bought_csv" with help text and add it to the container "command":
    subparser_show_bought_csv = subparsers.add_parser("show_bought_csv", help="goal: show all data in bought.csv. \n   ex: py super.py show_bought_csv \n   result: bought.csv is shown in the terminal.   \n\n")   


    # SHOW_COST: Create subparser "show_cost" with help text and add it to the container "command":
    subparser_show_cost = subparsers.add_parser("show_cost", help="goal: show cost in time range between start_date and end_date inclusive. \n   ex1: py super.py show_cost -sd 2023-09-01 -ed 2023-10-10 \n   result in terminal: \n   'Cost from start_date: 2023-09-01 to end_date: 2023-10-10 inclusive: Euro 27.9'  \n\n   ex2: py super.py show_cost -ed 2023-10-05 \n   result in terminal: \n   'Cost from start_date: 2023-01-01 to end_date: 2023-10-05 inclusive: Euro 18.6' \n   start_date is start of financial  year of system_date. e.g. system_date 23-06-08 --> 23-01-01.  \n\n   ex3: py super.py show_profit -sd 2023-07-01 \n   result in terminal: \n   'Cost from start_date: 2023-07-01 to end_date: 2023-09-17 inclusive: Euro 9.9' \n   end_date is system_date.  \n\n   arg1: start_date in format 'YYYY-MM-DD'. ex: 2023-09-01 \n   default value is january 1st of year from system_date: e.g. if system_date is 23-06-28, then default value is 23-01-01. \n   reason: often you want to know the cost of the current financial year until today inclusive. \n\n   arg2: end_date in format 'YYYY-MM-DD'. ex: 2023-10-15 \n   default value is system_date, because often you want to know the cost of the current financial year until today  inclusive.  \n\n")
    #step: add the positional and optional arguments to 'subparser_show_cost':
    subparser_show_cost.add_argument("-start_date","-sd",default=START_DATE_OF_CURRENT_FINANCIAL_YEAR, type=str, help="specify the start date in format YYYY-MM-DD")
    subparser_show_cost.add_argument("-end_date","-ed",default=SYSTEM_DATE, type=str, help="specify the end date in format YYYY-MM-DD")

    # SHOW_EXPIRED_PRODUCTS: create subparser "show_expired_products" with help text and add it to the container "command":
    subparser_buy_product = subparsers.add_parser("show_expired_products", help="goal: calculate expired products on a day in format 'YYYY-MM-DD' (e.g. 2023-09-18) \n   ex: py super.py expired_products -d 23-09-28  \n   result is displayed in a table in the console. \n   ex: py super.py expired_products.\n   results is displayed in a table in the console. \n\n   arg1: date is optional argument in following format: 'YYYY-MM-DD'. ex: 2026-10-21 \n   default value is system_date.  \n\n") 
    subparser_buy_product.add_argument("-date", "-d", default=SYSTEM_DATE, type=str, help="date in following format: '%Y-%m-%d'. ex: 2026-10-21 ") 

    # SHOW_INVENTORY: create subparser "show_inventory" with help text and add it to the container "command":
    subparser_buy_product = subparsers.add_parser("show_inventory", help="goal: calculate inventory on a day in format 'YYYY-MM-DD' (e.g. 2023-09-18) \n   ex: py super.py inventory -d 23-09-28  \n   result is displayed in a table in the console. \n   ex: py super.py inventory.\n   results is displayed in a table in the console. \n\n   arg1: date is optional argument in following format: 'YYYY-MM-DD'. ex: 2026-10-21 \n   default value is system_date.  \n\n") 
    subparser_buy_product.add_argument("-date", "-d", default=SYSTEM_DATE, type=str, help="date in following format: '%Y-%m-%d'. ex: 2026-10-21 ") 

    # SHOW_PROFIT: Create subparser "show_profit" with help text and add it to the container "command":
    subparser_show_cost = subparsers.add_parser("show_profit", help="goal: show profit in time range between start_date and end_date inclusive. \n   ex1: py super.py show_profit -sd 2023-09-01 -ed 2023-10-10 \n   result in terminal: \n   'Profit from start_date: 2023-09-01 to end_date: 2023-10-10 inclusive: Euro 27.9'  \n\n   ex2: py super.py show_profit -ed 2023-10-05 \n   result in terminal: \n   'Profit from start_date: 2023-01-01 to end_date: 2023-10-05 inclusive: Euro 18.6' \n   start_date is start of financial  year of system_date. e.g. system_date 23-06-08 --> 23-01-01.  \n\n   ex3: py super.py show_profit -sd 2023-07-01 \n   result in terminal: \n   'Profit from start_date: 2023-07-01 to end_date: 2023-09-17 inclusive: Euro 9.9' \n   end_date is system_date.  \n\n   arg1: start_date in format 'YYYY-MM-DD'. ex: 2023-09-01 \n   default value is january 1st of year from system_date: e.g. if system_date is 23-06-28, then default value is 23-01-01. \n   reason: often you want to know the profit of the current financial year until today inclusive. \n\n   arg2: end_date in format 'YYYY-MM-DD'. ex: 2023-10-15 \n   default value is system_date, because often you want to know the profit of the current financial year until today  inclusive.  \n\n")
    #step: add the positional and optional arguments to 'subparser_show_profit':
    subparser_show_cost.add_argument("-start_date","-sd",default=START_DATE_OF_CURRENT_FINANCIAL_YEAR, type=str, help="specify the start date in format YYYY-MM-DD")
    subparser_show_cost.add_argument("-end_date","-ed",default= SYSTEM_DATE, type=str, help="specify the end date in format YYYY-MM-DD")


    # SHOW_REVENUE: Create subparser "show_revenue" with help text and add it to the container "command":
    subparser_show_revenue = subparsers.add_parser("show_revenue", help="goal: show revenue in time range between start_date and end_date inclusive. \n   ex1: py super.py show_revenue -sd 2023-09-01 -ed 2023-10-10 \n   result in terminal: \n   'Revenue from start_date: 2023-09-01 to end_date: 2023-10-10 inclusive: Euro 27.9'  \n\n   ex2: py super.py show_revenue -ed 2023-10-05 \n   result in terminal: \n   'Revenue from start_date: 2023-01-01 to end_date: 2023-10-05 inclusive: Euro 18.6' \n   start_date is start of financial  year of system_date. e.g. system_date 23-06-08 --> 23-01-01.  \n\n   ex3: py super.py show_revenue -sd 2023-07-01 \n   result in terminal: \n   'Revenue from start_date: 2023-07-01 to end_date: 2023-09-17 inclusive: Euro 9.9' \n   end_date is system_date.  \n\n   arg1: start_date in format 'YYYY-MM-DD'. ex: 2023-09-01 \n   default value is january 1st of year from system_date: e.g. if system_date is 23-06-28, then default value is 23-01-01. \n   reason: often you want to know the revenue of the current financial year until today inclusive. \n\n   arg2: end_date in format 'YYYY-MM-DD'. ex: 2023-10-15 \n   default value is system_date, because often you want to know the revenue of the current financial year until today  inclusive.  \n\n")
    #step: add the positional and optional arguments to 'subparser_show_revenue':
    subparser_show_revenue.add_argument("-start_date","-sd",default=START_DATE_OF_CURRENT_FINANCIAL_YEAR, type=str, help="specify the start date in format YYYY-MM-DD")
    subparser_show_revenue.add_argument("-end_date","-ed",default=SYSTEM_DATE, type=str, help="specify the end date in format YYYY-MM-DD")


    # SHOW_SALES_VOLUME: Create subparser "show_sales_volume" with help text and add it to the container "command":
    subparser_show_revenue = subparsers.add_parser("show_sales_volume", help="goal: show sales volume in time range between start_date and end_date inclusive. \n   ex1: py super.py show_sales_volume -sd 2023-09-01 -ed 2023-10-10 \n   result in terminal: \n   'Sales volume from start_date: 2023-09-01 to end_date: 2023-10-10 inclusive: 18 products'  \n\n   ex2: py super.py show_sales_volume -ed 2023-10-05 \n   result in terminal: \n   'Sales volume from start_date: 2023-01-01 to end_date: 2023-10-05 inclusive: 117 products' \n   start_date is start of financial  year of system_date. e.g. system_date 23-06-08 --> 23-01-01.  \n\n   ex3: py super.py show_sales_volume -sd 2023-07-01 \n   result in terminal: \n   'Sales volume from start_date: 2023-07-01 to end_date: 2023-09-17 inclusive: 2241 products' \n   end_date is system_date.  \n\n   arg1: start_date in format 'YYYY-MM-DD'. ex: 2023-09-01 \n   default value is january 1st of year from system_date: e.g. if system_date is 23-06-28, then default value is 23-01-01. \n   reason: often you want to know the sales volume of the current financial year until today inclusive. \n\n   arg2: end_date in format 'YYYY-MM-DD'. ex: 2023-10-15 \n   default value is system_date, because often you want to know the sales volume of the current financial year until today  inclusive.  \n\n")
    #step: add the positional and optional arguments to 'subparser_show_revenue':
    subparser_show_revenue.add_argument("-start_date","-sd",default=START_DATE_OF_CURRENT_FINANCIAL_YEAR, type=str, help="specify the start date in format YYYY-MM-DD")
    subparser_show_revenue.add_argument("-end_date","-ed",default=SYSTEM_DATE, type=str, help="specify the end date in format YYYY-MM-DD")


    # SHOW_SOLD_CSV: Create subparser "show_sold_csv" with help text and add it to the container "command":
    subparser_show_sold_csv = subparsers.add_parser("show_sold_csv", help="goal: show all data in sold.csv on the command line with tool rich. \n   ex: py super.py show_sold_csv \n   result: sold.csv is shown in the terminal.   \n\n") 


    # TIME_TRAVEL: create subparser "time_travel" with help text and add it to the container "command":
    subparser_time_travel = subparsers.add_parser("time_travel", help="goal: change system_date \n   ex: py super.py time_travel 3.  \n   Result: you travel with 3 days. So if system_date is 2020-03-10, then new date becomes 2020-03-13 in the future.\n   ex: py super.py time_travel 3 and again current date is 2020-03-10. \n   Result: new date betcomes 2020-03-07 in the past.\n   arg1: days to add or subtract from system_date: e.g. 9, -8, etc.\n ") 
    #step: add the positional and optional arguments to  'subparser_time_travel': 
    subparser_time_travel.add_argument("nr_of_days", type=int, help="specify the new system date in format YYYY-MM-DD") 


    args = parser.parse_args()


    if args.command == "set_date":
        print("set_date")
        # step: call fn set_system_date_to to update file system__date.txt with following date:
        system_date = set_system_date_to(args.new_system_date, PATH_TO_FILE_WITH_SYSTEM_DATE)
        print(system_date) 

    if args.command == "time_travel":
        print("time_travel")
        # step: call fn time_travel_system_date_with_nr_of_days to update file system__date.txt with following date:
        new_system_date = time_travel_system_date_with_nr_of_days(args.nr_of_days, PATH_TO_FILE_WITH_SYSTEM_DATE, PATH_TO_FILE_WITH_SYSTEM_DATE)
        print(new_system_date) 

    if args.command == "buy":
        print("buy:")
        path_to_id_with_highest_sequence_number = os.path.join(PATH_TO_DATA_DIRECTORY_INSIDE_PROJECT_SUPERPY, 'id_to_use_in_fn_buy_product.txt')
        # print(path_to_id_with_highest_sequence_number)
        id_of_row_in_csv_file_bought = create_id_with_unused_highest_sequence_nr_to_buy_product_as_superpy_user(path_to_id_with_highest_sequence_number) 

        path_to_csv_bought_input_file = os.path.join(PATH_TO_DATA_DIRECTORY_INSIDE_PROJECT_SUPERPY, 'bought.csv')
        path_to_csv_bought_output_file = path_to_csv_bought_input_file # but not the same in pytest.
        buy_product(args.product_name, args.price, args.buy_date, args.expiry_date, id_of_row_in_csv_file_bought, path_to_csv_bought_input_file, path_to_csv_bought_output_file) 

    if args.command == "sell":
        print("sell:")
        path_to_csv_sold_input_file = os.path.join(PATH_TO_DATA_DIRECTORY_INSIDE_PROJECT_SUPERPY, 'sold.csv')
        path_to_csv_sold_output_file = path_to_csv_sold_input_file # but not the same in pytest.
        sell_product(args.buy_id, args.price, args.sell_date, path_to_csv_sold_input_file, path_to_csv_sold_output_file)


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
            create_id_for_each_row_in_boughtcsv_while_script_generates_this_boughtcsv,
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

        highest_buy_id_in_boughtcsv = get_highest_buy_id_after_running_script_to_create_mock_data_for_boughtcsv_and_soldcsv(path_to_csv_bought_file)
        print(f"highest_buy_id_from_boughtcsv: {highest_buy_id_in_boughtcsv}")
        # pitfall: do not increment buy_id with 1: e.g. b_1 --> b_2. This will be done at other point in the code. 

        path_to_file_with_name_id_to_use_in_fn_buy_product = get_path_to_file("data_used_in_superpy", "id_to_use_in_fn_buy_product.txt")

        buy_id = set_buy_id_after_running_script_to_create_mock_data_for_boughtcsv_and_soldcsv(highest_buy_id_in_boughtcsv, path_to_file_with_name_id_to_use_in_fn_buy_product)
        print(f"new_system_date: {buy_id}")
        '''
        suppose fn 'create_data_for_csv_files_bought_and_sold' has just created 132 rows of mock data for bought.csv 
        (the nr of rows in sold.csv depend on how many are deleted from these 132 rows by the script).
        That means that the nex buy_transaction to be added to bought.csv by the USER of the superpy-app, must have buy_id b_133. 
        For this to happen, in directory 'data_used_in_superpy': file 'id_to_use_in_fn_buy_product.txt' must now be set to buy_id 'b_132'.
        
        When creating this next buy_transaction, fn 'create_id_with_unused_highest_sequence_nr_to_buy_product_as_superpy_user 
        will increment 'b_132' with 1, so this next transaction will show up in bought.csv as 'b_133'.
        '''    

    if args.command == "delete":
        print("delete:")
        path_to_csv_bought_input_file = os.path.join(PATH_TO_DATA_DIRECTORY_INSIDE_PROJECT_SUPERPY, 'bought.csv')
        path_to_csv_sold_input_file = os.path.join(PATH_TO_DATA_DIRECTORY_INSIDE_PROJECT_SUPERPY, 'sold.csv')
        # step: delete all data in bought.csv and sold.csv:


        # to delete all data in bought.csv and sold.csv, all you need to do is set product_range to 0.
        # it does not matter what the values of the other fn-arguments are.
        product_range = 0
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

    if args.command == "show_bought_csv":
        # set path to file bought.csv:
        path_to_directory_testdata = ''
        path_to_directory_testdata = get_path_to_directory_of_file('data_used_in_superpy')
        path_to_file_bought_csv = os.path.join(path_to_directory_testdata, 'bought.csv') 
        show_csv_file_in_console_with_module_rich(path_to_file_bought_csv)

    if args.command == "show_sold_csv":
        # set path to file sold.csv:
        path_to_directory_testdata = ''
        path_to_directory_testdata = get_path_to_directory_of_file('data_used_in_superpy')
        path_to_file_bought_csv = os.path.join(path_to_directory_testdata, 'sold.csv') 
        show_csv_file_in_console_with_module_rich(path_to_file_bought_csv)

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

if __name__ == "__main__":
    main()