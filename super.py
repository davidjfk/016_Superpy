# Do not change these lines.
__winc_id__ = "a2bc36ea784242e4989deb157d527ba0"
__human_name__ = "superpy"
# Your code below this line.

import argparse, os, sys, socket, csv
from datetime import date, datetime, timedelta
from dateutil.relativedelta import relativedelta
from rich.console import Console
from rich.table import Table

sys.path.append('c:\\dev\\pytWinc\\superpy')
sys.path.append('c:\\dev\\pytWinc\\superpy\\utils_superpy')
from utils.utils import add_days_to_date
from utils.utils import generate_random_buy_date_for_buy_transaction_in_future_in_time_interval
from utils.utils import create_buy_id_for_each_row_in_mock_data
from utils.utils import buy_product, create_data_for_csv_files_bought_and_sold
from utils.utils import increment_buy_id_counter_txt
from utils.utils import get_path_to_file, get_system_date
from utils.utils import sell_product_by_buy_id, set_system_date_to, time_travel
from utils.utils import show_csv_file_in_console_with_module_rich
from utils.utils import get_highest_buy_id_from_boughtcsv
from utils.utils import set_buy_id_in_file_id_to_use_in_fn_to_buy_product_txt
from utils.utils import calculate_profit
from utils.utils import calculate_sales_volume
from utils.utils import calculate_expired_products
from utils.utils import show_selected_buy_transactions_in_console_with_module_rich
from utils.utils import calculate_inventory, calculate_middle_of_time_interval
from utils.utils import get_system_date, get_dates_of_next_7_days
from utils.utils import show_weekday_from_date, is_product_bought_with_product_name
from utils.utils import sell_product_by_product_name 
from utils.utils import show_last_added_sales_transaction_in_console_with_module_rich
from utils.utils import calculate_amount_in_interval
from utils.utils import show_extra_system_information
SUPERPY_PRODUCT_PRICES = '' # prevent UnboundLocalError
PRODUCT_LIST_TO_CREATE_PRODUCT_RANGE = '' # prevent UnboundLocalError
from data_used_in_superpy.product_prices import superpy_product_prices as SUPERPY_PRODUCT_PRICES
from data_used_in_superpy.product_list_to_create_product_range import product_list_to_create_product_range as PRODUCT_LIST_TO_CREATE_PRODUCT_RANGE

def main():
    # CONFIGURATION:
    '''
    For definitions: see README_USAGE_GUIDE.md --> ch definitions.
    For explanation of argparse commands and arguments --> see README_USAGE_GUIDE.md --> ch argparse commands and arguments.
    For ucs with these commands and arguments --> see README_USAGE_GUIDE.md --> ch use cases (ucs)

    Scope: only subparser create_mock_data uses the following configurable variables as default values for its optional arguments. 
    Change them at your liking.
    '''
    PRODUCT_RANGE = 3 
    DELETE_EVERY_NTH_ROW_IN_SOLDCSV = 2
    SHELF_LIFE = 10 # days
    TURNOVER_TIME = 3 # days
    MARKUP = 3 # factor
    UPPER_BOUNDARY_NR_OF_MONTHS_TO_ADD_TO_CALCULATE = 0
    UPPER_BOUNDARY_NR_OF_WEEKS_TO_ADD_TO_CALCULATE = 4
    UPPER_BOUNDARY_NR_OF_DAYS_TO_ADD_TO_CALCULATE = 0
    '''
    SYSTEM_DATE sets / assigns the default values of following 3 variables in the argparse subparser 'create_mock_data':
        lower_boundary_year_of_time_interval_in_which_to_create_random_testdata 
        lower_boundary_month_of_time_interval_in_which_to_create_random_testdata 
        lower_boundary_week_of_time_interval_in_which_to_create_random_testdata 

        Update their default values by updating SYSTEM_DATE:
        e.g.: py super.py set_system_date 2030-10-11  
    '''
    # <end of CONFIGURATION>

    # CONSTANTS: (do not change these)
    DATA_DIRECTORY = "data_used_in_superpy"  # 'data' would not be unique / robust enough to use in fn get_path_to_file.
    FILE_WITH_SYSTEM_DATE = "system_date.txt"
    PATH_TO_SYSTEM_DATE = get_path_to_file(DATA_DIRECTORY , FILE_WITH_SYSTEM_DATE)
    SYSTEM_DATE = get_system_date(PATH_TO_SYSTEM_DATE) # e.g. 2023-10-11
    path_to_project_superpy  = str(os.getcwd()) # only used once, so not a constant. 
    PATH_TO_DATA_DIRECTORY_INSIDE_PROJECT_SUPERPY = os.path.abspath(os.path.join(path_to_project_superpy, DATA_DIRECTORY))
    PATH_TO_FILE_WITH_SYSTEM_DATE = os.path.join(PATH_TO_DATA_DIRECTORY_INSIDE_PROJECT_SUPERPY, FILE_WITH_SYSTEM_DATE)
    PATH_TO_FILE_BOUGHT_CSV = get_path_to_file('data_used_in_superpy', 'bought.csv')
    PATH_TO_FILE_SOLD_CSV = get_path_to_file('data_used_in_superpy', 'sold.csv')
    year = int(SYSTEM_DATE[:4]) 
    start_date_of_current_financial_year_unformatted = date(year, 1, 1) # e.g. 2023-01-01
    START_DATE_OF_CURRENT_FINANCIAL_YEAR = start_date_of_current_financial_year_unformatted.strftime('%Y-%m-%d') # e.g. 2023-01-01 
    today = SYSTEM_DATE # e.g. 2023-10-11
    TOMORROW = add_days_to_date(today, 1)
    OVERMORROW = add_days_to_date(today, 2) # yes, this is English...google surprised me.
    YESTERDAY = add_days_to_date(today, -1)
    [NEXT_MONDAY, NEXT_TUESDAY, NEXT_WEDNESDAY, NEXT_THURSDAY, NEXT_FRIDAY, NEXT_SATURDAY, NEXT_SUNDAY] = get_dates_of_next_7_days(today)
    # <end of CONSTANTS>
    class ValidDate(argparse.Action):
        def __call__(self, parser, namespace, values, option_string=None):    
            if values == 'today':
                setattr(namespace, self.dest, SYSTEM_DATE)
                return 
            if values == 'tomorrow':
                setattr(namespace, self.dest, TOMORROW)
                return
            if values == 'overmorrow':
                setattr(namespace, self.dest, OVERMORROW)
                return
            if values == 'yesterday':
                setattr(namespace, self.dest, YESTERDAY)
                return
            if values == 'next_monday':
                setattr(namespace, self.dest, NEXT_MONDAY)
                return
            if values == 'next_tuesday':
                setattr(namespace, self.dest, NEXT_TUESDAY)
                return
            if values == 'next_wednesday':
                setattr(namespace, self.dest, NEXT_WEDNESDAY)
                return
            if values == 'next_thursday':
                setattr(namespace, self.dest, NEXT_THURSDAY)
                return
            if values == 'next_friday':
                setattr(namespace, self.dest, NEXT_FRIDAY)
                return
            if values == 'next_saturday':
                setattr(namespace, self.dest, NEXT_SATURDAY)
                return
            if values == 'next_sunday':
                setattr(namespace, self.dest, NEXT_SUNDAY)
                return                   
            try:
                datetime.strptime(values, '%Y-%m-%d')
                setattr(namespace, self.dest, values)
            except ValueError:
                parser.error(f"Wrong: format of  date should be YYYY-MM-DD, " \
                f" e.g. 2024-06-28 instead of 24-06-28." \
                f" Or use instead of YYYY-MM-DD, one of the following temporal deictics: today, tomorrow, " \
                f" overmorrow, yesterday, next_monday (...) next_sunday. See help file or"
                f" the README_USAGE_GUIDE.md.for more info.")

    parser = argparse.ArgumentParser(prog='super.py',description="Welcome to inventory management tool Superpy.", epilog="The line between disorder and order lies in logistics.", formatter_class=argparse.RawTextHelpFormatter)
    # step: create container for all subparsers. --> 'command' is a container for [and name of] all the subparsers:
    subparsers = parser.add_subparsers(dest="command", help='Commands: \n buy\n create_mock_data\n delete\n sell\n set_date\n show_bought_csv\n show_cost\n show_expired_products\n show_inventory\n show_profit\n show_revenue\n show_sales_volume\n show_sold_csv\n time_travel\n\n')

    # 1_BUY: create subparser "buy" with help text and add it to the container "command":
    subparser_buy_product = subparsers.add_parser("buy", help="   Goal: buy product and add to file bought.csv \n   ex1: py super.py buy apple 1.75 -b 23-09-15 -e 23-09-27 \n   product: apple,  price: E 1.75, buy_date: 23-09-15, expiry_date: 23-09-27\n\n   ex2: py super.py buy linseed 3.00 -e 23-09-28 \n   product: linseed, price: &euro; 3.00, buy_date: system_date as default, expiry_date: 23-09-28\n\n   ex3: py super.py buy cabbage 0.73 \n   product: cabbage, price: E 0.73, buy_date: system_date as default, expiry_date:  'does not expire' as default \n\n   arg1: positional argument product: e.g. apple, potato, milk\n   arg2: positional argument price, in euros: e.g. 1.24, 0.3, 0.35\n   arg3: optional argument -buy_date, -b (ex: 2023-09-15) with system_date as default value. \n   arg4: optional argument -expiry_date, -e (ex: 2023-10-03) with default value 'does not expire' \n\n   arg with date value can be entered in format YYYY-MM-DD: e.g. 2029-02-03 , or as a word (exhaustive list):\n   today, tomorrow, overmorrow, yesterday, next_monday (...) next_sunday.\n   Reference point: today == system_date (see definition of system_date) \n\n", description= "See 'py super.py -h' for more info.") 
    #step: add the positional and optional arguments to  'subparser_buy_product': 
    subparser_buy_product.add_argument("product_name", type=str, help="e.g. apple, quinoa, bulgur, linseed, soft cheeese, etc.") 
    subparser_buy_product.add_argument("price", type=float, help="e.g. 1.20 == 1 euro and 20 cents. 0.2 == 0.20 == 20 cents.") 
    # -buy_date gets its default value from file system_date.txt in the DATA_DIRECTORY:
    subparser_buy_product.add_argument("-buy_date", "-b", default= SYSTEM_DATE, type=str, action=ValidDate, help="format: 'YYYY-MM-DD'. ex: 2026-10-21 ") 
    subparser_buy_product.add_argument("-expiry_date", "-e", default="does not expire", type=str, action=ValidDate, help="format: 'YYYY-MM-DD'. ex: 2026-10-21 ") 

    # 2_CREATE_MOCK_DATE: Create subparser "create_mock_data" with help text and add it to the container "command":
    subparser_create_mock_data = subparsers.add_parser("create_mock_data", help="   Goal: create mock data for bought.csv and sold.csv\n   All 11 arguments have default values that can be changed in (...\superpy\super.py --> goto CONSTANTS at start of main.py()) \n   All 11 arguments are optional, so you can do this:  \n\n   ex1: py super.py create_mock_data \n   result: bought.csv and sold.csv are filled with mockdata that has \n   been created with default values.   \n\n   arg1 = product_range \n   flags: -pr, -product_range.\n   product_range == product_assortment == the amount of different products in Superpy.\n   minimum value: 1 (generates 8 transactions in bought.csv) \n   maximum value: 40 (generates 280 transactions in bought.csv)\n   ex1: py super.py create_mock_data -pr 3 \n   product_range: 3 random products: e.g. 'apple', 'cabbage' and 'beetroot' as input to create mock data \n   ex2: py super.py create_mock_data -pr 2 \n   product_range: 2 random products: e.g. 'coffee' and 'potato' as input to create mock data. \n   More products in product_range lead to more rows in bought.csv and sold.csv. \n   flags: -pr, -product_range \n   ex2: py super.py create_mock_data -pr 3 \n   result: 3 random products are selected from a pre-filled list to \n   create the testdata.  \n\n   arg2 =  delete every nth row in sold.csv \n   purpose: deleting rows makes them expire while time travelling: \n   After creating mock data for bought.csv, a copy is made to create sold.csv. \n   Then rows are deleted from sold.csv (e.g. every 3rd row). \n   By time travelling to the future these bought_products (e.g. every 3rd row) will expire. \n   flags: -denr, -delete_every_nth_row  \n   ex1: py super.py create_mock_data -denr 3 \n   delete_every_nth_row: 3  \n\n   arg3 = shelf_life == shelf_time == number of days between buying a product and \n   its expiry_date. \n   flags: -sl, -shelf_life  \n   ex1: py super.py create_mock_data -sl 10\n   shelf_life: 10 days \n   result: a bought product will expire after 10 days.\n\n   arg4 = turnover_time == inventory turnover == the number of days \n   between buying and selling a product. \n   flags: -turnover_time, -tt  \n   ex1: py super.py create_mock_data -tt 4\n   turnover_time: 4 days  \n\n   arg5 = markup = the amount of money a business adds to the cost of a product or service in order to make a profit. \n   In super.py markup is calculated as a factor: ex: if buy_price is 3 euro and sell_price is 4 euro, then markup is 4/3 = 1.33 \n   flags: -mu, -markup  \n   ex: py super.py create_mock_data -mu 3 \n    markup: factor 3  \n   result: if buy_price in bought.csv is 3 euro, then sell_price will be 9 euro in sold.csv.  \n\n   arg6 = lower_boundary_year == lower_boundary_year_of_time_interval_in_which_to_create_random_testdata. \n   flags: -lby, -lower_boundary_year  \n   ex1: py super.py create_mock_data -lby 2024\n   lower_boundary_year: 2024  \n\n   arg7 = lower_boundary_month == lower_boundary_month_of_time_interval_in_which_to_create_random_testdata. \n   flags: -lbm, -lower_boundary_month  \n   ex1: py super.py create_mock_data -lbm 10\n   lower_boundary_month: October  \n\n   arg8 = lower_boundary_day == lower_boundary_day_of_time_interval_in_which_to_create_random_testdata.  \n   flags: -lbd, -lower_boundary_day  \n   ex1: py super.py create_mock_data -lbd 15  \n   lower_boundary_day: 15th day of  the  month \n\n   arg9 =  nr_of_months_to_calculate_upper_boundary_month    \n   flags: -ubm, -upper_boundary_month_nr   \n   ex1: py super.py create_mock_data -ubm 3\n   nr_of_months_to_calculate_upper_boundary_month: 3 months  \n   result: upper boundary month of time interval in which to create data is 3 months in the future. \n   default value: 0 months.  \n\n   arg10 = nr_of_weeks_to_calculate_upper_boundary_week. \n   flags: -ubw, -upper_boundary_weeknr  \n   ex1: py super.py create_mock_data -ubw 8\n   nr_of_weeks_to_calculate_upper_boundary_week: 8 months  \n   result: upper boundary week of time interval in which to create data is 8 weeks in the future.  \n\n   arg11 = nr_of_days_to_calculate_upper_boundary_day. \n   flags: -ubd, -upper_boundary_day_nr  \n   ex: py super.py create_mock_data -ubd 3\n   nr_of_days_to_calculate_upper_boundary_day: 3 days  \n   result: upper boundary day of time interval in which to create data is 3 days in the future.  \n   default value: 0 days.\n\n", description= "See 'py super.py -h' for more info.")
    #step: add the optional arguments to 'subparser_create_mock_data':
    subparser_create_mock_data.add_argument("-product_range", "-pr", default=PRODUCT_RANGE, type=int, help=" ") 
    subparser_create_mock_data.add_argument("-delete_every_nth_row", "-denr", default=DELETE_EVERY_NTH_ROW_IN_SOLDCSV, type=int, help=" ") 
    subparser_create_mock_data.add_argument("-shelf_life", "-sl", default=SHELF_LIFE, type=int, help="supermarket also trades products that do not expire (e.g. cutlery, household equipment, etc. If product has expiry date, then it has following format: '%Y-%m-%d'. ex: 2026-10-21 ") 
    subparser_create_mock_data.add_argument("-turnover_time", "-tt", default=TURNOVER_TIME, type=int, help=" ")
    subparser_create_mock_data.add_argument("-markup", "-mu", default=MARKUP, type=float, help=" ")
    default_year = int(SYSTEM_DATE[:4])
    default_month = int(SYSTEM_DATE[5:7])
    default_day = int(SYSTEM_DATE[8:])
    subparser_create_mock_data.add_argument("-lower_boundary_year_of_time_interval_in_which_to_create_random_testdata", "-lby","-lower_boundary_year", default=default_year, type=int, help="lower_boundary_year_of_time_interval_in_which_to_create_random_testdata")
    subparser_create_mock_data.add_argument("-lower_boundary_month_of_time_interval_in_which_to_create_random_testdata","-lower_boundary_month", "-lbm", default=default_month, type=int, help="lower_boundary_month_of_time_interval_in_which_to_create_random_testdata")
    subparser_create_mock_data.add_argument("-lower_boundary_day_of_time_interval_in_which_to_create_random_testdata","-lower_boundary_day", "-lbd", default=default_day, type=int, help="lower_boundary_day_of_time_interval_in_which_to_create_random_testdata")
    subparser_create_mock_data.add_argument("-upper_boundary_nr_of_months_to_add_to_calculate","-upper_boundary_month", "-ubm", "-ubm", default=UPPER_BOUNDARY_NR_OF_MONTHS_TO_ADD_TO_CALCULATE, type=int, help="upper_boundary_nr_of_months_to_add_to_calculate")
    subparser_create_mock_data.add_argument("-upper_boundary_nr_of_weeks_to_add_to_calculate","-upper_boundary_week", "-ubw", "-upper_boundary_nr_of_weeks_to_add_to_calculate", default=UPPER_BOUNDARY_NR_OF_WEEKS_TO_ADD_TO_CALCULATE, type=int, help="upper_boundary_nr_of_weeks_to_add_to_calculate")
    subparser_create_mock_data.add_argument("-upper_boundary_nr_of_days_to_add_to_calculate","-upper_boundary_day", "-ubd", "-upper_boundary_nr_of_days_to_add_to_calculate", default=UPPER_BOUNDARY_NR_OF_DAYS_TO_ADD_TO_CALCULATE, type=int, help="upper_boundary_nr_of_days_to_add_to_calculate")

    # 3_DELETE: Create subparser "delete" with help text and add it to the container "command":
    subparser_delete_data = subparsers.add_parser("delete", help="   Goal1: delete all transaction records in bought.csv and sold.csv. \n   ex: py super.py delete \n   result: all transaction records in bought.csv and sold.csv have been deleted   \n\n", description= "See 'py super.py -h' for more info.")
    # subparser does not need any arguments.

    # 4_RESET_SYSTEM_DATE: Create subparser "reset_system_date" with help text and add it to the container "command":
    subparser_reset_system_date = subparsers.add_parser("reset_system_date", help="   Goal: reset system_date in system_date.txt (...\superpy\data_used_in_superpy\system_date.txt) to \n  current date on the device Superpy is running on.\n   ex: py super.py reset_system_date \n   result: system_date.txt now contains current system_date from the  device Superpy is running on.  \n\n", description= "See 'py super.py -h' for more info.")
    # subparser does not need any arguments.

    # 5_SELL: create subparser "sell" with help text and add it to the container "command":
    subparser_sell_product = subparsers.add_parser("sell", help="   Goal: sell product and add to file sold.csv \n   Preparation:  lookup products and their buy_ids in the inventory: e.g. \n   py super.py show_inventory -d 2024-03-15 \n\n   then:\n   ex1: \n   py super.py sell fig 3.75 -s 2023-11-15 \n   py super.py b_492 3.75 -s 2023-11-15 \n   product fig with buy_id b_15 in bought.csv is sold, price: E 3.75, sell_date: 23-11-15\n   tip: quicker to buy with product name here.\n\n   ex2:\n   py super.py Cold_Pressed_Extra_Virgin_Olive_Oil_with_Lemon_and_Garlic 5.15 \n   py super.py b_16 5.15 \n   product Cold...Oil with buy_id b_15 in bought.csv is sold, price: E 5.15, sell_date: system_date as default\n   tip: quicker to buy with buy_id here.\n\n   arg1: positional argument product_name_or_buy_id: ex as product: apple, quinoa, bulgur, linseed, soft cheeese,\n   etc. ex as buy_id: b_01, b_02 (...), b_103, etc. \n   arg2: positional argument price, in euros: e.g. 1.24, 0.3, 0.35\n   arg3: optional argument -sell_date, -s (ex: -sd 2023-09-15) with system_date as default value. \n\n   arg with date value can be entered in format YYYY-MM-DD: e.g. 2029-02-03 , or as a word (exhaustive list):\n   today, tomorrow, overmorrow, yesterday, next_monday (...) next_sunday.\n   Reference point: today == system_date (see definition of system_date) \n\n", description= "See 'py super.py -h' for more info.")
    #step: add the positional and optional arguments to 'subparser_set_date': 
    subparser_sell_product.add_argument("product_name_or_buy_id", type=str, help="Ex of product name: apple, quinoa, bulgur, linseed, soft cheeese, etc. Ex of product buy_id: b_01, b_02 (...), b_103, etc.") 
    subparser_sell_product.add_argument("price", type=float, help="e.g. 1.20 means 1 euro and 20 cents. 0.2 or 0.20 means 20 cents.") 
    # -buy_date gets its default value from file system_date.txt in the DATA_DIRECTORY:
    subparser_sell_product.add_argument("-sell_date", "-s", default= SYSTEM_DATE, type=str, action=ValidDate, help="format: 'YYYY-MM-DD'. ex: 2026-10-21 ") 
    # subparser_sell_product.add_argument("-expiry_date", "-ed", default="does not expire", type=str, help="supermarket also trades products that do not expire (e.g. cutlery, household equipment, etc. If product has expiry date, then it has following format: '%Y-%m-%d'. ex: 2026-10-21") 

    # 6_SET_DATE: create subparser "set_system_date" with help text and add it to the container "command":
    subparser_set_date = subparsers.add_parser("set_system_date", help = "   Goal: set_system_date_to a specific date in the file system_date.txt\n   ex1: py super.py set_date 2025-01-01 \n   system_date: 2025-01-01\n result: 'Superpy system_date is set to date (e.g.) 2028-03-10' \n\n   arg1: positional argument system_date, e.g. 2023-10-11. \n   --> string representation in format 'yyy-mm-dd'\n\n   arg with date value can be entered in format YYYY-MM-DD: e.g. 2029-02-03 , or as a word (exhaustive list):\n   today, tomorrow, overmorrow, yesterday, next_monday (...) next_sunday.\n   Reference point: today == system_date (see definition of system_date) \n\n", description= "See 'py super.py -h' for more info.")
    #step: add the positional and optional arguments to 'subparser_set_date': 
    subparser_set_date.add_argument("new_system_date", type=str, action=ValidDate, help="specify the new system date in format YYYY-MM-DD") 

    # 7_SHOW_BOUGHT_CSV: Create subparser "show_bought_csv" with help text and add it to the container "command":
    subparser_show_bought_csv = subparsers.add_parser("show_bought_csv", help="   Goal: show all data from bought.csv in a table in the terminal \n   ex: py super.py show_bought_csv \n   result: bought.csv is shown in the terminal as a table.   \n\n", description= "See 'py super.py -h' for more info.")   

    # 8_SHOW_COST: Create subparser "show_cost" with help text and add it to the container "command":
    subparser_show_cost = subparsers.add_parser("show_cost", help="   Goal: show cost in time range between start_date and end_date inclusive. \n   ex1: py super.py show_cost -sd 2023-09-01 -ed 2023-10-10 \n   start_date: 2023-09-01 \n   end_date: 2023-10-10 \n   result in terminal: \n   'Cost from start_date: 2023-09-01 to end_date: 2023-10-10 inclusive: Euro 27.9'  \n\n   ex2: py super.py show_cost -ed 2023-10-05 \n   start_date is start of financial  year of system_date. e.g. if system_date 23-06-08, then: 23-01-01.\n   end_date: 2023-10-05 \n   result in terminal: \n   'Cost from start_date: 2023-01-01 to end_date: 2023-10-05 inclusive: Euro 18.6'   \n\n   ex3: py super.py show_profit -sd 2023-07-01 \n   start_date: 2023-07-01 \n   end_date is by default system_date \n   result in terminal: \n   'Cost from start_date: 2023-07-01 to end_date: 2023-09-17 inclusive: Euro 9.9' \n   end_date has by default system_date.  \n\n   arg1: optional argument start_date in format 'YYYY-MM-DD'. ex: -sd 2023-09-01, or: -start_date 2023-09-01 \n   default value is january 1st of year from system_date: e.g. if system_date is 23-06-28, then default value is 23-01-01. \n   reason: often you want to know the cost of the current financial year until today inclusive. \n\n   arg2: optional argument end_date in format 'YYYY-MM-DD'. ex: -ed 2023-10-15, or: -end_date 2023-10-15 \n   default value is system_date, because often you want to know the cost of the current financial year until today  inclusive.  \n\n", description= "See 'py super.py -h' for more info.")
    #step: add the positional and optional arguments to 'subparser_show_cost':
    subparser_show_cost.add_argument("-start_date","-sd",default=START_DATE_OF_CURRENT_FINANCIAL_YEAR, type=str, action=ValidDate, help="format: 'YYYY-MM-DD'. ex: 2026-10-21 ")
    subparser_show_cost.add_argument("-end_date","-ed",default=SYSTEM_DATE, type=str, action=ValidDate, help="format: 'YYYY-MM-DD'. ex: 2026-10-28 ")

    # 9_SHOW_EXPIRED_PRODUCTS: create subparser "show_expired_products" with help text and add it to the container "command":
    subparser_buy_product = subparsers.add_parser("show_expired_products", help="   Goal: calculate expired products on a day in format 'YYYY-MM-DD' (e.g. 2023-09-28) \n   ex1: py super.py show_expired_products -d 2023-09-28\n   date: 2023-09-28   \n   result is displayed in a table in the terminal. \n\n   ex2: py super.py show_expired_products\n   date: by default system_date\n   results is displayed in a table in the terminal. \n\n   arg1: optional argument date in following format: 'YYYY-MM-DD'. ex: -d 2026-10-21 \n   default value is system_date.\n   reason: often you want to know which products expire today.  \n\n", description= "See 'py super.py -h' for more info.") 
    subparser_buy_product.add_argument("-date", "-d", default=SYSTEM_DATE, type=str, action=ValidDate, help="format: 'YYYY-MM-DD'. ex: 2026-10-21 ") 

    # 10_SHOW_INVENTORY: create subparser "show_inventory" with help text and add it to the container "command":
    subparser_buy_product = subparsers.add_parser("show_inventory", help="   Goal: calculate inventory on a day in format 'YYYY-MM-DD' (e.g. 2023-09-28) \n   ex1: py super.py show_inventory -d 2023-09-28\n   date: 2023-09-28   \n   result is displayed in a table in the terminal. \n\n   ex2: py super.py show_inventory\n   date: by default system_date\n   results is displayed in a table in the terminal. \n\n   arg1: optional argument date in following format: 'YYYY-MM-DD'. ex: -d 2026-10-21 \n   default value is system_date.\n   reason: often you want to know which products expire today.  \n\n", description= "See 'py super.py -h' for more info.")  
    subparser_buy_product.add_argument("-date", "-d", default=SYSTEM_DATE, type=str, action=ValidDate, help="format: 'YYYY-MM-DD'. ex: 2026-10-21 ") 

    # 11_SHOW_PROFIT: Create subparser "show_profit" with help text and add it to the container "command":
    subparser_show_cost = subparsers.add_parser("show_profit", help="   Goal: show profit in time range between start_date and end_date inclusive. \n   ex1: py super.py show_profit -sd 2023-09-01 -ed 2023-10-10 \n   start_date: 2023-09-01 \n   end_date: 2023-10-10 \n   result in terminal: \n   'Profit from start_date: 2023-09-01 to end_date: 2023-10-10 inclusive: Euro 27.9'  \n\n   ex2: py super.py show_profit -ed 2023-10-05 \n   start_date is start of financial  year of system_date. e.g. if system_date 23-06-08, then: 23-01-01.\n   end_date: 2023-10-05 \n   result in terminal: \n   'Profit from start_date: 2023-01-01 to end_date: 2023-10-05 inclusive: Euro 18.6'   \n\n   ex3: py super.py show_profit -sd 2023-07-01 \n   start_date: 2023-07-01 \n   end_date is by default system_date \n   result in terminal: \n   'Profit from start_date: 2023-07-01 to end_date: 2023-09-17 inclusive: Euro 9.9' \n   end_date has by default system_date.  \n\n   arg1: optional argument start_date in format 'YYYY-MM-DD'. ex: -sd 2023-09-01, or: -start_date 2023-09-01 \n   default value is january 1st of year from system_date: e.g. if system_date is 23-06-28, then default value is 23-01-01. \n   reason: often you want to know the profit of the current financial year until today inclusive. \n\n   arg2: optional argument end_date in format 'YYYY-MM-DD'. ex: -ed 2023-10-15, or: -end_date 2023-10-15 \n   default value is system_date, because often you want to know the cost of the current financial year until today  inclusive.  \n\n", description= "See 'py super.py -h' for more info.")
    #step: add the positional and optional arguments to 'subparser_show_profit':
    subparser_show_cost.add_argument("-start_date","-sd",default=START_DATE_OF_CURRENT_FINANCIAL_YEAR, type=str, action=ValidDate, help="format: 'YYYY-MM-DD'. ex: 2026-10-21 ")
    subparser_show_cost.add_argument("-end_date","-ed",default= SYSTEM_DATE, type=str, action=ValidDate, help="format: 'YYYY-MM-DD'. ex: 2026-10-28 ")

    # 12_SHOW_REVENUE: Create subparser "show_revenue" with help text and add it to the container "command":
    subparser_show_revenue = subparsers.add_parser("show_revenue", help="   Goal: show revenue in time range between start_date and end_date inclusive. \n   ex1: py super.py show_revenue -sd 2023-09-01 -ed 2023-10-10 \n   start_date: 2023-09-01 \n   end_date: 2023-10-10 \n   result in terminal: \n   'Revenue from start_date: 2023-09-01 to end_date: 2023-10-10 inclusive: Euro 27.9'  \n\n   ex2: py super.py show_revenue -ed 2023-10-05 \n   start_date is start of financial  year of system_date. e.g. if system_date 23-06-08, then: 23-01-01.\n   end_date: 2023-10-05 \n   result in terminal: \n   'Revenue from start_date: 2023-01-01 to end_date: 2023-10-05 inclusive: Euro 18.6'   \n\n   ex3: py super.py show_revenue -sd 2023-07-01 \n   start_date: 2023-07-01 \n   end_date is by default system_date \n   result in terminal: \n   'Revenue from start_date: 2023-07-01 to end_date: 2023-09-17 inclusive: Euro 9.9' \n   end_date has by default system_date.  \n\n   arg1: optional argument start_date in format 'YYYY-MM-DD'. ex: -sd 2023-09-01, or: -start_date 2023-09-01 \n   default value is january 1st of year from system_date: e.g. if system_date is 23-06-28, then default value is 23-01-01. \n   reason: often you want to know the revenue of the current financial year until today inclusive. \n\n   arg2: optional argument end_date in format 'YYYY-MM-DD'. ex: -ed 2023-10-15, or: -end_date 2023-10-15 \n   default value is system_date, because often you want to know the cost of the current financial year until today  inclusive.  \n\n", description= "See 'py super.py -h' for more info.")
    #step: add the positional and optional arguments to 'subparser_show_revenue':
    subparser_show_revenue.add_argument("-start_date","-sd",default=START_DATE_OF_CURRENT_FINANCIAL_YEAR, type=str, action=ValidDate, help="format: 'YYYY-MM-DD'. ex: 2026-10-21 ")
    subparser_show_revenue.add_argument("-end_date","-ed",default=SYSTEM_DATE, type=str, action=ValidDate, help="format: 'YYYY-MM-DD'. ex: 2026-10-28 ")

    # 13_SHOW_SALES_VOLUME: Create subparser "show_sales_volume" with help text and add it to the container "command":
    subparser_show_revenue = subparsers.add_parser("show_sales_volume", help="   Goal: show sales volume in time range between start_date and end_date inclusive. \n   ex1: py super.py show_sales_volume -sd 2023-09-01 -ed 2023-10-10 \n   start_date: 2023-09-01 \n   end_date: 2023-10-10 \n   result in terminal: \n   'Sales Volume from start_date: 2023-09-01 to end_date: 2023-10-10 inclusive: Euro 27.9'  \n\n   ex2: py super.py show_sales_volume -ed 2023-10-05 \n   start_date is start of financial  year of system_date. e.g. if system_date 23-06-08, then: 23-01-01.\n   end_date: 2023-10-05 \n   result in terminal: \n   'Sales volume from start_date: 2023-01-01 to end_date: 2023-10-05 inclusive: Euro 18.6'   \n\n   ex3: py super.py show_sales_volume -sd 2023-07-01 \n   start_date: 2023-07-01 \n   end_date is by default system_date \n   result in terminal: \n   'Sales volume from start_date: 2023-07-01 to end_date: 2023-09-17 inclusive: Euro 9.9' \n   end_date has by default system_date.  \n\n   arg1: optional argument start_date in format 'YYYY-MM-DD'. ex: -sd 2023-09-01, or: -start_date 2023-09-01 \n   default value is january 1st of year from system_date: e.g. if system_date is 23-06-28, then default value is 23-01-01. \n   reason: often you want to know the sales volume of the current financial year until today inclusive. \n\n   arg2: optional argument end_date in format 'YYYY-MM-DD'. ex: -ed 2023-10-15, or: -end_date 2023-10-15 \n   default value is system_date, because often you want to know the cost of the current financial year until today  inclusive.  \n\n", description= "See 'py super.py -h' for more info.")
    #step: add the positional and optional arguments to 'subparser_show_revenue':
    subparser_show_revenue.add_argument("-start_date","-sd",default=START_DATE_OF_CURRENT_FINANCIAL_YEAR, type=str, action=ValidDate, help="format: 'YYYY-MM-DD'. ex: 2026-10-21 ")
    subparser_show_revenue.add_argument("-end_date","-ed",default=SYSTEM_DATE, type=str, action=ValidDate, help="format: 'YYYY-MM-DD'. ex: 2026-10-28")

    # 14_SHOW_SOLD_CSV: Create subparser "show_sold_csv" with help text and add it to the container "command":
    subparser_show_sold_csv = subparsers.add_parser("show_sold_csv", help="   Goal: show all data from sold.csv in a table in the terminal. \n   ex: py super.py show_sold_csv \n   result: sold.csv is shown in the terminal as a table   \n\n", description= "See 'py super.py -h' for more info.") 

    # 15_SHOW_SYSTEM_DATE: Create subparser "show_system_date" with help text and add it to the container "command":
    subparser_show_system_date = subparsers.add_parser("show_system_date", help="   Goal: show SYSTEM_DATE (e.g. '2027-06-13') from system_date.txt in the terminal \n (...\superpy\data_used_in_superpy\system_date.txt). \n   ex: py super.py show_system_date \n   result: 'Superpy SYSTEM_DATE has value 2023-08-20'  \n\n", description= "See 'py super.py -h' for more info.") 

    # 16_TIME_TRAVEL: create subparser "time_travel" with help text and add it to the container "command":
    subparser_time_travel = subparsers.add_parser("time_travel", help="   Goal: change system_date by adding or subtracting nr of day(s) \n   ex1: py super.py time_travel 3.\n   nr_of_days: 3 \n   result: you travel with 3 days to the future. So if system_date is 2024-03-10, then \n   new date becomes 2024-03-13 in the future.\n\n   ex2: py super.py time_travel -3\n   nr_of_days: -3 \n   result: you travel with 3 days to the past. So if system date is 2024-03-10, \n   then new date becomes 2024-03-07 in the past.\n\n   arg1: positional argument days to add or subtract from system_date: e.g. 9, -8, etc.\n ", description= "See 'py super.py -h' for more info.") 
    #step: add the positional and optional arguments to  'subparser_time_travel': 
    subparser_time_travel.add_argument("nr_of_days", type=int, help="e.g. 3 == 3 days into the future, -2 == 2 days into the past") 

    args = parser.parse_args()

    # nr 1of16
    if args.command == "buy":
        path_to_id_with_highest_sequence_number = os.path.join(PATH_TO_DATA_DIRECTORY_INSIDE_PROJECT_SUPERPY, 'buy_id_counter.txt')
        id_of_row_in_csv_file_bought = increment_buy_id_counter_txt(path_to_id_with_highest_sequence_number) 

        path_to_csv_bought_input_file = os.path.join(PATH_TO_DATA_DIRECTORY_INSIDE_PROJECT_SUPERPY, 'bought.csv')
        path_to_csv_bought_output_file = path_to_csv_bought_input_file # but not the same in pytest.
        fn_execution_status = buy_product(args.product_name, args.price, args.buy_date, args.expiry_date, id_of_row_in_csv_file_bought, path_to_csv_bought_input_file, path_to_csv_bought_output_file) 
        # if not fn_execution_status == "date_entered_in_fn_in_wrong_format":
        show_extra_system_information("buy product and add to bought.csv", system_date_of_superpy, show_weekday_from_date) 
        print('---------------------------------------------------------------------------------------------------')                                                                                                                                                                                                                                                                           
        print(f" Status of: BOUGHT.CSV & SOLD.CSV:                                                                ")    
        print(f" 1of2: BOUGHT.CSV:                                                                                ")    
        show_csv_file_in_console_with_module_rich(PATH_TO_FILE_BOUGHT_CSV)
        print('---------------------------------------------------------------------------------------------------')
        print('                                                                                                   ')
        print(f" 2of2: SOLD.CSV:                                                                                  ")  
        path_to_csv_sold_file = get_path_to_file('data_used_in_superpy', 'sold.csv')
        show_csv_file_in_console_with_module_rich(path_to_csv_sold_file)

    # nr 2of16
    if args.command == "create_mock_data":
        print("create_mock_data:")  
        system_date_year = int(args.lower_boundary_year_of_time_interval_in_which_to_create_random_testdata)
        system_date_month = int(args.lower_boundary_month_of_time_interval_in_which_to_create_random_testdata)
        system_date_day = int(args.lower_boundary_day_of_time_interval_in_which_to_create_random_testdata)
        SYSTEM_DATE = date(system_date_year, system_date_month, system_date_day).strftime("%Y-%m-%d")
        system_date_in_the_middle_of_time_interval = calculate_middle_of_time_interval(
            SYSTEM_DATE, 
            args.upper_boundary_nr_of_months_to_add_to_calculate, 
            args.upper_boundary_nr_of_weeks_to_add_to_calculate, 
            args.upper_boundary_nr_of_days_to_add_to_calculate)
        
        path_to_file_system_datetxt = get_path_to_file('data_used_in_superpy', 'system_date.txt')
        set_system_date_to(system_date_in_the_middle_of_time_interval, path_to_file_system_datetxt)

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
            SUPERPY_PRODUCT_PRICES,
            PRODUCT_LIST_TO_CREATE_PRODUCT_RANGE,
            PATH_TO_FILE_BOUGHT_CSV,
            PATH_TO_FILE_SOLD_CSV,
            add_days_to_date,
            create_buy_id_for_each_row_in_mock_data,
            generate_random_buy_date_for_buy_transaction_in_future_in_time_interval
        )

        highest_buy_id_in_boughtcsv = get_highest_buy_id_from_boughtcsv(PATH_TO_FILE_BOUGHT_CSV)
        path_to_file_with_name_buy_id_counter = get_path_to_file("data_used_in_superpy", "buy_id_counter.txt")
        buy_id = set_buy_id_in_file_id_to_use_in_fn_to_buy_product_txt(highest_buy_id_in_boughtcsv, path_to_file_with_name_buy_id_counter)
        print(f"new_system_date: {buy_id}")
        '''
        suppose fn 'create_data_for_csv_files_bought_and_sold' has just created 132 rows of mock data for bought.csv 
        (the nr of rows in sold.csv depend on how many are deleted from these 132 rows by the script).
        That means that the nex buy_transaction to be added to bought.csv by the USER of the superpy-app, must have buy_id b_133. 
        For this to happen, in directory 'data_used_in_superpy': file 'buy_id_counter.txt' must now be set to buy_id 'b_132'.
        When creating this next buy_transaction, fn 'create_buy_id_that_increments_highest_buy_id_in_boughtcsv 
        will increment 'b_132' with 1, so this next transaction will show up in bought.csv as 'b_133'.
        '''  
        system_date_of_superpy = get_system_date( PATH_TO_FILE_WITH_SYSTEM_DATE) 
        show_extra_system_information(args.command, system_date_of_superpy, show_weekday_from_date)                                                                                                                                                                                                                                                                 
        print('---------------------------------------------------------------------------------------------------')        
        print(f" Status of: BOUGHT.CSV & SOLD.CSV:                                                                ")    
        print(f" 1of2: BOUGHT.CSV:                                                                                ")    
        
        show_csv_file_in_console_with_module_rich(PATH_TO_FILE_BOUGHT_CSV)
        print('---------------------------------------------------------------------------------------------------')
        print('                                                                                                   ')
        print(f" 2of2: SOLD.CSV:                                                                                  ")  
        show_csv_file_in_console_with_module_rich(PATH_TO_FILE_SOLD_CSV)

    # nr 3of16
    if args.command == "delete":
        print("delete:")
        create_data_for_csv_files_bought_and_sold(
            0, # this value 0 deletes all records. Values for other parameters are not relevant for this goal.
            2,9,3,3,2023,10,1,2,0,0,
            SUPERPY_PRODUCT_PRICES,
            PRODUCT_LIST_TO_CREATE_PRODUCT_RANGE,
            PATH_TO_FILE_BOUGHT_CSV,
            PATH_TO_FILE_SOLD_CSV,
            add_days_to_date,
            create_buy_id_for_each_row_in_mock_data,
            generate_random_buy_date_for_buy_transaction_in_future_in_time_interval
        )
        show_extra_system_information("delete all transactions from bought.csv and sold.csv", SYSTEM_DATE, show_weekday_from_date) 
        print('---------------------------------------------------------------------------------------------------')                                                                                                                                                                                                                                                                     
        print(f" Status of: BOUGHT.CSV & SOLD.CSV:                                                                ")    
        print(f" 1of2: BOUGHT.CSV:                                                                                ")    
        show_csv_file_in_console_with_module_rich(PATH_TO_FILE_BOUGHT_CSV)
        print('---------------------------------------------------------------------------------------------------')
        print('                                                                                                   ')
        print(f" 2of2: SOLD.CSV:                                                                                  ")  
        show_csv_file_in_console_with_module_rich(PATH_TO_FILE_SOLD_CSV)

        '''
        # postperation: with all data having been deleted from bought.csv and sold.csv, the next buy_id must be 
        reset to b_01 for the first buy_transaction to be added to bought.csv by the USER of the superpy-app:
        '''
        path_to_file_with_name_buy_id_counter = get_path_to_file("data_used_in_superpy", "buy_id_counter.txt")
        highest_buy_id_in_boughtcsv = "b_0"
        # pitfall: do not reset to b_01. This will be done at other point in the code.
        buy_id = set_buy_id_in_file_id_to_use_in_fn_to_buy_product_txt(highest_buy_id_in_boughtcsv, path_to_file_with_name_buy_id_counter)
        print(f"new_system_date: {buy_id}")

    # nr 4of16
    if args.command == "reset_system_date":     
        system_date_on_device_outside_of_Superpy = set_system_date_to(datetime.today().strftime('%Y-%m-%d'), PATH_TO_FILE_WITH_SYSTEM_DATE)
        show_extra_system_information("reset_system_time of Superpy to system time of host machine", system_date_on_device_outside_of_Superpy, show_weekday_from_date)  

    # nr 5of16
    if args.command == "sell":     
        path_to_csv_sold_input_file = os.path.join(PATH_TO_DATA_DIRECTORY_INSIDE_PROJECT_SUPERPY, 'sold.csv')
        path_to_csv_sold_output_file = path_to_csv_sold_input_file # but not the same in pytest.
        path_to_csv_bought_input_file = os.path.join(PATH_TO_DATA_DIRECTORY_INSIDE_PROJECT_SUPERPY, 'bought.csv')
        show_extra_system_information(args.command, SYSTEM_DATE, show_weekday_from_date)  
        print('---------------------------------------------------------------------------------------------------')

        if is_product_bought_with_product_name(args.product_name_or_buy_id):
            new_transaction_record = sell_product_by_product_name(args.product_name_or_buy_id, args.price, args.sell_date, calculate_inventory, path_to_csv_sold_input_file, path_to_csv_sold_output_file, path_to_csv_bought_input_file)
        else:
            new_transaction_record = sell_product_by_buy_id(args.product_name_or_buy_id, args.price, args.sell_date, path_to_csv_sold_input_file, path_to_csv_sold_output_file, path_to_csv_bought_input_file)

        if new_transaction_record == 'product_is_not_sold':
            print('---------------------------------------------------------------------------------------------------')
            print('                                                                                                   ')        
            print(f" Status of SOLD.CSV: the following transaction has NOT been added to SOLD.CSV:                     ")
            print(f" product_name: {args.product_name_or_buy_id}                                                      ")
            print(f" price: {args.price}                                                                              ")
            print(f" sell_date: {args.sell_date}                                                                      ") 
            print('                                                                                                   ') 
            print('---------------------------------------------------------------------------------------------------')       
        else:         
            print(f" Status: the following transaction has been added to SOLD.CSV below:                              ")
            show_last_added_sales_transaction_in_console_with_module_rich([[new_transaction_record[0], new_transaction_record[1], str(round(args.price,2)), args.sell_date]])    
            # left 2do: simplify nested list into list.                  
            print('---------------------------------------------------------------------------------------------------')
            print('                                                                                                   ')                                                                 
            print(f" Status of: SOLD.CSV & BOUGHT.CSV:                                                                ")    
            print(f" 1of2: SOLD.CSV:                                                                                  ")  
            path_to_csv_sold_file = get_path_to_file('data_used_in_superpy', 'sold.csv')
            show_csv_file_in_console_with_module_rich(path_to_csv_sold_file)
            print('---------------------------------------------------------------------------------------------------')
            print('                                                                                                   ')
            print(f" 2of2: BOUGHT.CSV:                                                                                ")    
            show_csv_file_in_console_with_module_rich(PATH_TO_FILE_BOUGHT_CSV)

    # nr 6of16
    if args.command == "set_system_date":
        new_system_date = set_system_date_to(args.new_system_date, PATH_TO_FILE_WITH_SYSTEM_DATE)
        show_extra_system_information(args.command, new_system_date, show_weekday_from_date)  

    # nr 7of16
    if args.command == "show_bought_csv":
        show_extra_system_information(args.command, SYSTEM_DATE, show_weekday_from_date)  
        print('---------------------------------------------------------------------------------------------------')
        print('                                                                                                   ')
        print(f" Contents of bought.csv: ")
        print('                                                                                                   ')        
        show_csv_file_in_console_with_module_rich(PATH_TO_FILE_BOUGHT_CSV)

    # nr 8of16
    if args.command == "show_cost":      
        cost = calculate_amount_in_interval(args.start_date, args.end_date, 'buy_date', 'buy_price', PATH_TO_FILE_BOUGHT_CSV)
        show_extra_system_information(args.command, SYSTEM_DATE, show_weekday_from_date)  
        print('---------------------------------------------------------------------------------------------------')
        print('                                                                                                   ')
        print(f"Cost from start_date: {args.start_date} to end_date: {args.end_date} inclusive: Euro {cost}")
        print('                                                                                                   ')
        print('---------------------------------------------------------------------------------------------------')

    # nr 9of16
    if args.command == "show_expired_products":
        expired_products = calculate_expired_products(args.date, PATH_TO_FILE_SOLD_CSV, PATH_TO_FILE_BOUGHT_CSV)
        if not expired_products == "date_entered_in_fn_in_wrong_format":
            show_extra_system_information(args.command, SYSTEM_DATE, show_weekday_from_date)  
            print('---------------------------------------------------------------------------------------------------')
            print('                                                                                                   ')
            print(f" Expired products on Superpy date: {args.date}: ")
            print('                                                                                                   ')
            show_selected_buy_transactions_in_console_with_module_rich(expired_products)

    # nr 10of16
    if args.command == "show_inventory":
        inventory = calculate_inventory(args.date, PATH_TO_FILE_SOLD_CSV, PATH_TO_FILE_BOUGHT_CSV)
        show_extra_system_information(args.command, SYSTEM_DATE, show_weekday_from_date)  
        print('---------------------------------------------------------------------------------------------------')
        print('                                                                                                   ')
        print(f" Inventory on Superpy date: {args.date}: ")
        print('                                                                                                   ')
        show_selected_buy_transactions_in_console_with_module_rich(inventory)

    # nr 11of16
    if args.command == "show_profit":
        path_to_csv_sold_file = get_path_to_file('data_used_in_superpy', "sold.csv")
        path_to_csv_bought_file = get_path_to_file('data_used_in_superpy', "bought.csv")
        profit = calculate_profit(args.start_date, args.end_date, path_to_csv_sold_file, path_to_csv_bought_file, calculate_amount_in_interval, calculate_amount_in_interval)
        show_extra_system_information(args.command, SYSTEM_DATE, show_weekday_from_date)  
        print('---------------------------------------------------------------------------------------------------')
        print('                                                                                                   ')
        print(f" Profit from start_date: {args.start_date} to end_date: {args.end_date} inclusive: Euro {profit}")
        print('                                                                                                   ')
        print('---------------------------------------------------------------------------------------------------')

    # nr 12of16
    if args.command == "show_revenue":
        revenue = calculate_amount_in_interval(args.start_date, args.end_date, "sell_date", "sell_price", PATH_TO_FILE_SOLD_CSV)
        console = Console()
        table = Table(show_header=True, header_style="bold magenta")
        table.add_column("Description")
        table.add_column("Value")
        table.add_row("Revenue", f"€ {revenue}")
        table.add_row("Revenue: start date", f"{args.start_date}")
        table.add_row("Revenue: end date (inclusive)", f"{args.end_date}")
        console.print(table)
        show_extra_system_information(args.command, SYSTEM_DATE, show_weekday_from_date)

        # continue here: 
        def display_revenue(revenue, start_date, end_date):
            '''
            # step: make nr of fn-arguments variable. 
            # step: the strings below (e.g. 'Revenue: start date') must also be fn-arguments.
            # step: each row in the table should be a list of 2 variables that belong together, e.g. Revenue (string) and revenue (variable)
            # step: so each combi of 2 vars must be stored as such in the fn-arguments, so it can be grabbed from there annd displayed on
            #       its own line in the table.
            # step: then make this fn generic, so it can be used in all other fn's that display a table with similar info.
            '''
            console = Console()
            table = Table(show_header=True, header_style="bold magenta")
            table.add_column("Description")
            table.add_column("Value")

            table.add_row("Revenue", f"€ {revenue}")
            table.add_row("Revenue: start date", f"{start_date}")
            table.add_row("Revenue: end date (inclusive)", f"{end_date}")

            console.print(table)

        display_revenue(revenue, args.start_date, args.end_date)

    # nr 13of16
    if args.command == "show_sales_volume":
        sales_volume = calculate_sales_volume(args.start_date, args.end_date, PATH_TO_FILE_SOLD_CSV)
        show_extra_system_information(args.command, SYSTEM_DATE, show_weekday_from_date)  
        print('---------------------------------------------------------------------------------------------------')                                                                                                                                                                                        
        print('                                                                                                   ')
        print(f" Sales volume from start_date: {args.start_date} to end_date: {args.end_date} inclusive: {sales_volume} products")
        print('                                                                                                   ')
        print('---------------------------------------------------------------------------------------------------')

    # nr 14of16
    if args.command == "show_sold_csv":
        show_extra_system_information(args.command, SYSTEM_DATE, show_weekday_from_date)                                                                                                                                                                                                                                                                        
        print(f"-------------------------------------------------------------------------------------------------")
        print(f" Status of: SOLD.CSV & BOUGHT.CSV:                                                                ")    
        print(f" 1of2: SOLD.CSV:                                                                                  ")  
        path_to_csv_sold_file = get_path_to_file('data_used_in_superpy', 'sold.csv')
        show_csv_file_in_console_with_module_rich(path_to_csv_sold_file)
        print('---------------------------------------------------------------------------------------------------')
        print('                                                                                                   ')
        print(f" 2of2: BOUGHT.CSV:                                                                                ")    
        show_csv_file_in_console_with_module_rich(PATH_TO_FILE_BOUGHT_CSV)

    # nr 15of16
    if args.command == "show_system_date":  
        system_date_of_superpy = get_system_date( PATH_TO_FILE_WITH_SYSTEM_DATE)
        show_extra_system_information(args.command, system_date_of_superpy, show_weekday_from_date)

    # nr 16of16
    if args.command == "time_travel":
        print("time_travel")
        new_system_date = time_travel(args.nr_of_days, PATH_TO_FILE_WITH_SYSTEM_DATE, PATH_TO_FILE_WITH_SYSTEM_DATE)                                                                                                                                                                                   
        show_extra_system_information(args.command, new_system_date, show_weekday_from_date)                       
if __name__ == "__main__":
    main()