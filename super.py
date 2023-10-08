# Do not change these lines.
__winc_id__ = "a2bc36ea784242e4989deb157d527ba0"
__human_name__ = "superpy"
# Your code below this line.
import textwrap
import argparse, os, sys, socket, csv
from datetime import date, datetime, timedelta
from dateutil.relativedelta import relativedelta
from rich.console import Console
from rich.table import Table

sys.path.append('c:\\dev\\pytWinc\\superpy')
sys.path.append('c:\\dev\\pytWinc\\superpy\\utils_superpy')
from utils.utils import * # import ALL functions from utils.py (all of them are used in super.py )
SUPERPY_PRODUCT_PRICES = '' # prevent UnboundLocalError
PRODUCT_LIST_TO_CREATE_PRODUCT_RANGE = '' # prevent UnboundLocalError
from data_used_in_superpy.product_prices import superpy_product_prices as SUPERPY_PRODUCT_PRICES
from data_used_in_superpy.product_list_to_create_product_range import product_list_to_create_product_range as PRODUCT_LIST_TO_CREATE_PRODUCT_RANGE
from data_used_in_superpy import helptekst_subparsers 

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
    UPPER_BOUNDARY_NR_OF_MONTHS = 0
    UPPER_BOUNDARY_NR_OF_WEEKS = 4
    UPPER_BOUNDARY_NR_OF_DAYS = 0
    '''
    SYSTEM_DATE sets / assigns the default values of following 3 variables in the argparse subparser 'create_mock_data':
        lower_boundary_year_of_time_interval_in_which_to_create_random_testdata 
        lower_boundary_month_of_time_interval_in_which_to_create_random_testdata 
        lower_boundary_week_of_time_interval_in_which_to_create_random_testdata 

        So update their default values by updating SYSTEM_DATE:
        e.g.: py super.py set_system_date 2030-10-11  
    '''

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
    HEADER_1OF2_BOUGHT_CSV = ["Status of: BOUGHT.CSV & SOLD.CSV:","1of2: BOUGHT.CSV:"]
    HEADER_2of2_SOLD_CSV = ["2of2: SOLD.CSV:"]
    HEADER_1OF2_SOLD_CSV = ["Status of: SOLD.CSV & BOUGHT.CSV:","1of2: SOLD.CSV:"]
    HEADER_2of2_BOUGHT_CSV = ["2of2: BOUGHT.CSV:"]
    year = int(SYSTEM_DATE[:4]) 
    start_date_of_current_financial_year_unformatted = date(year, 1, 1) # e.g. 2023-01-01
    START_DATE_OF_CURRENT_FINANCIAL_YEAR = start_date_of_current_financial_year_unformatted.strftime('%Y-%m-%d') # e.g. 2023-01-01 
    today = SYSTEM_DATE # e.g. 2023-10-11
    TOMORROW = add_days_to_date(today, 1)
    OVERMORROW = add_days_to_date(today, 2) 
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
    subparsers = parser.add_subparsers(dest="command", help='Commands: \n buy\n create_mock_data\n delete\n sell\n set_date\n show_bought_csv\n show_cost\n show_expired_products\n show_inventory\n show_profit\n show_revenue\n show_sales_volume\n show_sold_csv\n travel_time\n\n')

    subparser_buy_product = subparsers.add_parser("buy", help=helptekst_subparsers.buy, description= helptekst_subparsers.description_tekst_general)  
    subparser_buy_product.add_argument("product_name", type=str, help="E.g. apple, quinoa, bulgur, linseed, soft cheeese, etc.") 
    subparser_buy_product.add_argument("price", type=float, help="E.g. 1.20 == 1 euro and 20 cents. 0.2 == 0.20 == 20 cents.") 
    subparser_buy_product.add_argument("-buy_date", "-b", default= SYSTEM_DATE, type=str, action=ValidDate, help=helptekst_subparsers.valid_date_format) 
    subparser_buy_product.add_argument("-expiry_date", "-e", default="does not expire", type=str, action=ValidDate, help=helptekst_subparsers.valid_date_format) 

    subparser_create_mock_data = subparsers.add_parser("create_mock_data", help=helptekst_subparsers.create_mock_data, description= helptekst_subparsers.description_tekst_general)
    subparser_create_mock_data.add_argument("-product_range", "-pr", default=PRODUCT_RANGE, type=int, help="Product_range == the amount of different products in Superpy: choose between 1 and 50. ") 
    subparser_create_mock_data.add_argument("-delete_every_nth_row", "-denr", default=DELETE_EVERY_NTH_ROW_IN_SOLDCSV, type=int, help="Delete every nth row in sold.csv, so there are less rows in sold.csv than in bought.csv, so bought products expire while time travelling. ") 
    subparser_create_mock_data.add_argument("-shelf_life", "-sl", default=SHELF_LIFE, type=int, help="Number of days between buying a product and its expiry_date. E.g. 10 means 10 days ") 
    subparser_create_mock_data.add_argument("-turnover_time", "-tt", default=TURNOVER_TIME, type=int, help="Number of days between buying and selling a product. E.g. 3 means 3 days ")
    subparser_create_mock_data.add_argument("-markup", "-mu", default=MARKUP, type=float, help="factor between buy_price and sell_price. E.g. 3 means 3 times the buy_price. ")
    default_year = int(SYSTEM_DATE[:4])
    default_month = int(SYSTEM_DATE[5:7])
    default_day = int(SYSTEM_DATE[8:])
    subparser_create_mock_data.add_argument("-lower_boundary_year","-lby", default=default_year, type=int, help="lower boundary year of time_interval in which to create mock data: e.g. 2023 is the year.")
    subparser_create_mock_data.add_argument("-lower_boundary_month","-lbm", default=default_month, type=int, help="lower boundary_month of time interval in which to create mock data: e.g. 10 means October.")
    subparser_create_mock_data.add_argument("-lower_boundary_day","-lbd", default=default_day, type=int, help="lower boundary day of time interval in which to create mock data: e.g. 11 means 11th of the month.")
    subparser_create_mock_data.add_argument("-upper_boundary_month","-ubm", default=UPPER_BOUNDARY_NR_OF_MONTHS, type=int, help="upper_boundary_nr_of_months_to_add_to_calculate: e.g. 4 means 4 months.")
    subparser_create_mock_data.add_argument("-upper_boundary_week","-ubw", default=UPPER_BOUNDARY_NR_OF_WEEKS, type=int, help="upper_boundary_nr_of_weeks_to_add_to_calculate: e.g. 2 means 2 weeks.")
    subparser_create_mock_data.add_argument("-upper_boundary_day", "-ubd", default=UPPER_BOUNDARY_NR_OF_DAYS, type=int, help="upper_boundary_nr_of_days_to_add_to_calculate: e.g. 5 means 5 days.")

    subparsers.add_parser("delete", help=helptekst_subparsers.delete, description=helptekst_subparsers.description_tekst_general )

    subparsers.add_parser("reset_system_date", help=helptekst_subparsers.reset_system_date, description= helptekst_subparsers.description_tekst_general)

    subparser_sell_product = subparsers.add_parser("sell", help=helptekst_subparsers.sell, description= helptekst_subparsers.description_tekst_general)
    subparser_sell_product.add_argument("product_name_or_buy_id", type=str, help="E.g. of product name: apple, quinoa, bulgur, linseed, soft cheeese, etc. E.g. of product buy_id: b_01, b_02 (...), b_103, etc.") 
    subparser_sell_product.add_argument("price", type=float, help="e.g. 1.20 means 1 euro and 20 cents. 0.2 or 0.20 means 20 cents.") 
    subparser_sell_product.add_argument("-sell_date", "-s", default= SYSTEM_DATE, type=str, action=ValidDate, help=helptekst_subparsers.valid_date_format) 
    
    subparser_set_date = subparsers.add_parser("set_system_date", help =helptekst_subparsers.set_system_date , description= helptekst_subparsers.description_tekst_general)
    subparser_set_date.add_argument("new_system_date", type=str, action=ValidDate, help=helptekst_subparsers.valid_date_format) 

    subparsers.add_parser("show_bought_csv", help=helptekst_subparsers.show_bought_csv, description= helptekst_subparsers.description_tekst_general)   

    subparser_show_cost = subparsers.add_parser("show_cost", help=helptekst_subparsers.show_cost, description= helptekst_subparsers.description_tekst_general)
    subparser_show_cost.add_argument("-start_date","-sd",default=START_DATE_OF_CURRENT_FINANCIAL_YEAR, type=str, action=ValidDate, help=helptekst_subparsers.valid_date_format)
    subparser_show_cost.add_argument("-end_date","-ed",default=SYSTEM_DATE, type=str, action=ValidDate, help=helptekst_subparsers.valid_date_format)

    subparser_buy_product = subparsers.add_parser("show_expired_products", help=helptekst_subparsers.show_expired_products, description= helptekst_subparsers.description_tekst_general) 
    subparser_buy_product.add_argument("-date", "-d", default=SYSTEM_DATE, type=str, action=ValidDate, help=helptekst_subparsers.valid_date_format) 

    subparser_buy_product = subparsers.add_parser("show_inventory", help=helptekst_subparsers.show_inventory, description= helptekst_subparsers.description_tekst_general)  
    subparser_buy_product.add_argument("-date", "-d", default=SYSTEM_DATE, type=str, action=ValidDate, help=helptekst_subparsers.valid_date_format) 

    subparser_show_cost = subparsers.add_parser("show_profit", help=helptekst_subparsers.show_profit, description= helptekst_subparsers.description_tekst_general)
    subparser_show_cost.add_argument("-start_date","-sd",default=START_DATE_OF_CURRENT_FINANCIAL_YEAR, type=str, action=ValidDate, help=helptekst_subparsers.valid_date_format)
    subparser_show_cost.add_argument("-end_date","-ed",default= SYSTEM_DATE, type=str, action=ValidDate, help=helptekst_subparsers.valid_date_format)

    subparser_show_revenue = subparsers.add_parser("show_revenue", help=helptekst_subparsers.show_revenue, description= helptekst_subparsers.description_tekst_general)
    subparser_show_revenue.add_argument("-start_date","-sd",default=START_DATE_OF_CURRENT_FINANCIAL_YEAR, type=str, action=ValidDate, help=helptekst_subparsers.valid_date_format)
    subparser_show_revenue.add_argument("-end_date","-ed",default=SYSTEM_DATE, type=str, action=ValidDate, help=helptekst_subparsers.valid_date_format)

    subparser_show_revenue = subparsers.add_parser("show_sales_volume", help=helptekst_subparsers.show_sales_volume, description= helptekst_subparsers.description_tekst_general)
    subparser_show_revenue.add_argument("-start_date","-sd",default=START_DATE_OF_CURRENT_FINANCIAL_YEAR, type=str, action=ValidDate, help=helptekst_subparsers.valid_date_format)
    subparser_show_revenue.add_argument("-end_date","-ed",default=SYSTEM_DATE, type=str, action=ValidDate, help=helptekst_subparsers.valid_date_format)

    subparsers.add_parser("show_sold_csv", help=helptekst_subparsers.show_sold_csv, description= helptekst_subparsers.description_tekst_general) 

    subparsers.add_parser("show_system_date", help=helptekst_subparsers.show_system_date, description= helptekst_subparsers.description_tekst_general) 

    subparser_travel_time = subparsers.add_parser("travel_time", help=helptekst_subparsers.travel_time_help_tekst, description= helptekst_subparsers.description_tekst_general) 
    subparser_travel_time.add_argument("nr_of_days", type=int, help="E.g. 3 == 3 days into the future. E.g. -2 == 2 days into the past") 

    args = parser.parse_args()

    if args.command == "buy":
        path_to_id_with_highest_sequence_number = os.path.join(PATH_TO_DATA_DIRECTORY_INSIDE_PROJECT_SUPERPY, 'buy_id_counter.txt')
        id_of_row_in_csv_file_bought = increment_buy_id_counter_txt(path_to_id_with_highest_sequence_number) 
        path_to_csv_bought_input_file = os.path.join(PATH_TO_DATA_DIRECTORY_INSIDE_PROJECT_SUPERPY, 'bought.csv')
        path_to_csv_bought_output_file = path_to_csv_bought_input_file # but not the same in pytest.
        buy_product(args.product_name, args.price, args.buy_date, args.expiry_date, id_of_row_in_csv_file_bought, path_to_csv_bought_input_file, path_to_csv_bought_output_file) 
        show_superpy_system_info("buy product and add to bought.csv", SYSTEM_DATE, get_weekday_from_date) 
        show_header(HEADER_1OF2_BOUGHT_CSV)
        show_csv_file(PATH_TO_FILE_BOUGHT_CSV)
        show_header(HEADER_2of2_SOLD_CSV)  
        show_csv_file(PATH_TO_FILE_SOLD_CSV)
    if args.command == "create_mock_data": 
        system_date_year = int(args.lower_boundary_year)
        system_date_month = int(args.lower_boundary_month)
        system_date_day = int(args.lower_boundary_day)
        SYSTEM_DATE = date(system_date_year, system_date_month, system_date_day).strftime("%Y-%m-%d")
        system_date_in_the_middle_of_time_interval = calculate_middle_of_time_interval(
            SYSTEM_DATE, 
            args.upper_boundary_month, 
            args.upper_boundary_week, 
            args.upper_boundary_day)
        path_to_file_system_datetxt = get_path_to_file('data_used_in_superpy', 'system_date.txt')
        set_system_date_to(system_date_in_the_middle_of_time_interval, path_to_file_system_datetxt)
        create_data_for_csv_files_bought_and_sold(
            args.product_range,
            args.delete_every_nth_row,
            args.shelf_life,
            args.turnover_time,
            args.markup,
            args.lower_boundary_year,
            args.lower_boundary_month,
            args.lower_boundary_day,
            args.upper_boundary_month,
            args.upper_boundary_week,
            args.upper_boundary_day,
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
        system_date_of_superpy = get_system_date( PATH_TO_FILE_WITH_SYSTEM_DATE) 
        show_superpy_system_info(args.command, system_date_of_superpy, get_weekday_from_date)
        show_header(HEADER_1OF2_BOUGHT_CSV)
        show_csv_file(PATH_TO_FILE_BOUGHT_CSV)
        show_header(HEADER_2of2_SOLD_CSV) 
        show_csv_file(PATH_TO_FILE_SOLD_CSV)
    if args.command == "delete":
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
        show_superpy_system_info("Delete all transactions from bought.csv and sold.csv", SYSTEM_DATE, get_weekday_from_date) 
        show_header(HEADER_1OF2_BOUGHT_CSV)  
        show_csv_file(PATH_TO_FILE_BOUGHT_CSV)
        show_header(HEADER_2of2_SOLD_CSV)                                                                                     
        show_csv_file(PATH_TO_FILE_SOLD_CSV)
        path_to_file_with_name_buy_id_counter = get_path_to_file("data_used_in_superpy", "buy_id_counter.txt")
        highest_buy_id_in_boughtcsv = "b_0" # pitfall: do not reset to b_01. This will be done at other point in the code.
        buy_id = set_buy_id_in_file_id_to_use_in_fn_to_buy_product_txt(highest_buy_id_in_boughtcsv, path_to_file_with_name_buy_id_counter)
        print(f"new_system_date: {buy_id}")
    if args.command == "reset_system_date":     
        system_date_on_device_outside_of_Superpy = set_system_date_to(datetime.today().strftime('%Y-%m-%d'), PATH_TO_FILE_WITH_SYSTEM_DATE)
        show_superpy_system_info("Reset_system_time of Superpy to system time of host machine", system_date_on_device_outside_of_Superpy, get_weekday_from_date)  
    if args.command == "sell":     
        path_to_csv_sold_input_file = os.path.join(PATH_TO_DATA_DIRECTORY_INSIDE_PROJECT_SUPERPY, 'sold.csv')
        path_to_csv_sold_output_file = path_to_csv_sold_input_file # but not the same in pytest.
        path_to_csv_bought_input_file = os.path.join(PATH_TO_DATA_DIRECTORY_INSIDE_PROJECT_SUPERPY, 'bought.csv')
        show_superpy_system_info(args.command, SYSTEM_DATE, get_weekday_from_date)  
        if is_product_bought_with_product_name(args.product_name_or_buy_id):
            new_transaction_record = sell_product_by_product_name(args.product_name_or_buy_id, args.price, args.sell_date, calculate_inventory, calculate_expired_products, path_to_csv_sold_input_file, path_to_csv_sold_output_file, path_to_csv_bought_input_file)
        else:
            new_transaction_record = sell_product_by_buy_id(args.product_name_or_buy_id, args.price, args.sell_date, path_to_csv_sold_input_file, path_to_csv_sold_output_file, path_to_csv_bought_input_file)
        if new_transaction_record == 'product_is_not_sold':
            sell_abort_details = [["Product name", args.product_name_or_buy_id],["Price:  ", args.price],[ "Attempted sell date", args.sell_date]]
            show_superpy_logistic_info('Aborted sales transaction:', sell_abort_details)   
        else:         
            latest_sales_transaction_in_sold_csv_info = [["sell_id", new_transaction_record[0]],['buy_id', new_transaction_record[1]],[ 'sell_price €', str(round(args.price,2)),[ 'sell_date', args.sell_date]]]
            show_superpy_logistic_info("Status: the following\ntransaction has been added\nto SOLD.CSV below: ", latest_sales_transaction_in_sold_csv_info) 
            show_header(HEADER_1OF2_SOLD_CSV)                   
            show_csv_file(PATH_TO_FILE_SOLD_CSV)
            show_header(HEADER_2of2_BOUGHT_CSV)                                                                                 
            show_csv_file(PATH_TO_FILE_BOUGHT_CSV)
    if args.command == "set_system_date":
        new_system_date = set_system_date_to(args.new_system_date, PATH_TO_FILE_WITH_SYSTEM_DATE)
        show_superpy_system_info(args.command, new_system_date, get_weekday_from_date)  
    if args.command == "show_bought_csv":
        show_superpy_system_info(args.command, SYSTEM_DATE, get_weekday_from_date)
        show_header(HEADER_1OF2_BOUGHT_CSV)
        show_csv_file(PATH_TO_FILE_SOLD_CSV)
        show_header(HEADER_2of2_SOLD_CSV)  
        show_csv_file(PATH_TO_FILE_BOUGHT_CSV)
    if args.command == "show_cost":      
        cost = calculate_amount_in_interval(args.start_date, args.end_date, 'buy_date', 'buy_price', PATH_TO_FILE_BOUGHT_CSV) 
        show_cost_info = [["Cost: €", cost],["Cost: start date:  ", args.start_date],[ "Cost: end date (inclusive):", args.end_date]]
        show_superpy_logistic_info('Cost calculation', show_cost_info)  
        show_superpy_system_info(args.command, SYSTEM_DATE, get_weekday_from_date)
    if args.command == "show_expired_products":
        expired_products = calculate_expired_products(args.date, PATH_TO_FILE_SOLD_CSV, PATH_TO_FILE_BOUGHT_CSV)
        if not expired_products == "date_entered_in_fn_in_wrong_format":
            expired_products_info = [["Expired products on SYSTEM_DATE:", args.date]]
            show_superpy_logistic_info('Expired products', expired_products_info) 
            show_selected_buy_transactions(expired_products)
            show_superpy_system_info(args.command, SYSTEM_DATE, get_weekday_from_date)
    if args.command == "show_inventory":
        inventory = calculate_inventory(args.date, PATH_TO_FILE_SOLD_CSV, PATH_TO_FILE_BOUGHT_CSV)
        inventory_info = [["Inventory on SYSTEM_DATE:", args.date]]
        show_superpy_logistic_info('Inventory', inventory_info)
        show_selected_buy_transactions(inventory)
        show_superpy_system_info(args.command, SYSTEM_DATE, get_weekday_from_date) 
    if args.command == "show_profit":
        path_to_csv_sold_file = get_path_to_file('data_used_in_superpy', "sold.csv")
        path_to_csv_bought_file = get_path_to_file('data_used_in_superpy', "bought.csv")
        profit = calculate_profit(args.start_date, args.end_date, path_to_csv_sold_file, path_to_csv_bought_file, calculate_amount_in_interval, calculate_amount_in_interval)
        profit_info = [["Profit: €", profit],["Profit: start date:  ", args.start_date],[ "Profit: end date (inclusive):", args.end_date]]
        show_superpy_logistic_info('Profit calculation', profit_info)         
        show_superpy_system_info(args.command, SYSTEM_DATE, get_weekday_from_date) 
    if args.command == "show_revenue":
        revenue = calculate_amount_in_interval(args.start_date, args.end_date, "sell_date", "sell_price", PATH_TO_FILE_SOLD_CSV)     
        revenue_info = [["Revenue: €", revenue],["Revenue: start date:  ", args.start_date],[ "Revenue: end date (inclusive):", args.end_date]]
        show_superpy_logistic_info('Revenue calculation', revenue_info)   
        show_superpy_system_info(args.command, SYSTEM_DATE, get_weekday_from_date)
    if args.command == "show_sales_volume":
        sales_volume = calculate_sales_volume(args.start_date, args.end_date, PATH_TO_FILE_SOLD_CSV)
        sales_volume_info = [["Sales volume: number of products:", sales_volume],["Sales volume: start date:  ", args.start_date],[ "Sales volume: end date (inclusive):", args.end_date]]
        show_superpy_logistic_info('Sales volume calculation', sales_volume_info) 
        show_superpy_system_info(args.command, SYSTEM_DATE, get_weekday_from_date)  
    if args.command == "show_sold_csv":
        show_superpy_system_info(args.command, SYSTEM_DATE, get_weekday_from_date)
        show_header(HEADER_1OF2_SOLD_CSV)
        show_csv_file(PATH_TO_FILE_SOLD_CSV)
        show_header(HEADER_2of2_BOUGHT_CSV)  
        show_csv_file(PATH_TO_FILE_BOUGHT_CSV)
    if args.command == "show_system_date":  
        system_date_of_superpy = get_system_date( PATH_TO_FILE_WITH_SYSTEM_DATE)
        show_superpy_system_info(args.command, system_date_of_superpy, get_weekday_from_date)
    if args.command == "travel_time":
        print("travel_time")
        new_system_date = travel_time(args.nr_of_days, PATH_TO_FILE_WITH_SYSTEM_DATE, PATH_TO_FILE_WITH_SYSTEM_DATE)                                                                                                                         
        show_superpy_system_info(args.command, new_system_date, get_weekday_from_date)                       
if __name__ == "__main__":
    main()