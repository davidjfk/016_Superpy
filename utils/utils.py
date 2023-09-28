
# list of imports:
import os, sys, csv
import datetime
import random
from datetime import date, datetime, timedelta
from dateutil.relativedelta import relativedelta
from rich.table import Table
from rich.console import Console

# only used in fn create_data_for_csv_files_bought_and_sold():
from itertools import product
from copy import deepcopy
from typing import Callable

# LIST OF FUNCTIONS:
# add_days_to_date(date_string, days_to_add)

# buy_product(product, price, buy_date, expiry_date, id_of_row_in_csv_file_bought, path_to_csv_bought_input_file, path_to_csv_bought_output_file):

# calculate_cost_in_time_range_between_start_date_and_end_date_inclusive(start_date, end_date, path_to_csv_bought_file):

# calculate_expired_products_on_day(date_on_which_to_calculate_expired_products, path_to_csv_sold_file, path_to_csv_bought_file):

# calculate_inventory_on_day(date_on_which_to_calculate_products_in_inventory, path_to_csv_sold_file, path_to_csv_bought_file):

# calculate_middle_of_time_interval(SYSTEM_DATE: str, upper_boundary_nr_of_months_to_add_to_calculate: int, upper_boundary_nr_of_weeks_to_add_to_calculate: int,upper_boundary_nr_of_days_to_add_to_calculate: int  ) -> str:

# calculate_profit_in_time_range_between_start_date_and_end_date_inclusive(start_date, end_date, path_to_csv_sold_file, path_to_csv_bought_file, calculate_revenue_in_time_range_between_start_date_and_end_date_inclusive, calculate_cost_in_time_range_between_start_date_and_end_date_inclusive):

# calculate_revenue_in_time_range_between_start_date_and_end_date_inclusive(start_date, end_date, path_to_csv_sold_file):

# calculate_sales_volume_in_time_range_between_start_date_and_end_date_inclusive(start_date, end_date, path_to_csv_sold_file):

# create_buy_id_for_each_row_in_boughtcsv_as_part_of_mockdata_that_is_being_created(csv_file_name_first_letter, first_nr_in_range):

# create_buy_id_that_increments_highest_buy_id_in_boughtcsv(path_to_id_with_highest_sequence_number):

# create_data_for_csv_files_bought_and_sold(product_range, delete_every_nth_row_in_soldcsv_so_every_nth_row_in_boughtcsv_can_expire_when_time_travelling, shelf_life, turnover_time, markup, lower_boundary_year_of_time_interval_in_which_to_create_random_testdata, lower_boundary_month_of_time_interval_in_which_to_create_random_testdata, lower_boundary_week_of_time_interval_in_which_to_create_random_testdata, upper_boundary_nr_of_months_to_add_to_calculate, upper_boundary_nr_of_weeks_to_add_to_calculate, upper_boundary_nr_of_days_to_add_to_calculate, path_to_file_bought_csv, path_to_file_sold_csv, add_days_to_date, create_id_for_each_row_in_boughtcsv_while_script_generates_this_boughtcsv, generate_random_buy_date_for_buy_transaction_in_future_in_time_interval):

# generate_random_buy_date_for_buy_transaction_in_future_in_time_interval(interval_lower_boundary_year,            interval_lower_boundary_month, interval_lower_boundary_day, nr_of_months_added_to_calculate_upper_boundary,            nr_of_weeks_added_to_calculate_upper_boundary, nr_of_days_added_to_calculate_upper_boundary):

# get_dates_of_next_7_days(today: str) -> list:

# get_highest_buy_id_from_boughtcsv(path_to_csv_bought_file):

# get_path_to_directory_of_file(directory_of_file):

# get_path_to_file(directory_of_file, file_name_of_which_you_want_to_know_the_path):

# get_system_date(path_to_system_date):

# sell_product(bought_product_id, price, sell_date, path_to_csv_bought_input_file, path_to_csv_bought_output_file):

# set_buy_id_in_file_id_to_use_in_fn_to_buy_product_txt_after_running_fn_to_create_mock_data_for_boughtcsv_and_soldcsv(buy_id, path_to_buy_id_file):

# set_system_date_to(system_date, path_to_system_date):

# show_list_with_nested_lists_in_console_with_module_rich(list):

# show_csv_file_in_console_with_module_rich(path_to_csv_file):

# time_travel_system_date_with_nr_of_days(nr_of_days_to_travel, path_to_input_file, path_to_output_file):

# show_weekday_from_date(date: str) -> str:

def add_days_to_date(date_string: str, days_to_add: int) -> str:
    date = datetime.strptime(date_string, '%Y-%m-%d')
    new_date = date + timedelta(days= days_to_add)
    '''
    This is a helper fn used as fn-argument in following fns:
    - create_data_for_csv_files_bought_and_sold()
    - time_travel_system_date_with_nr_of_days()
    
    '''
    return new_date.strftime('%Y-%m-%d')


def buy_product(
        product: str, 
        price: float, 
        buy_date: str, 
        expiry_date: str, 
        id_of_row_in_csv_file_bought: str, 
        path_to_csv_bought_input_file: str, 
        path_to_csv_bought_output_file: str
) -> None:
    '''
    About the input_file and output_file:
    when using superpy as user, input and output csv file are the same.
    Only when testing fn buy_product in pytest, input and output csv file are different.
    reason: when testing fn buy_product in pytest, I want to keep the csv-file with testdata intact.
    '''
    try:
        with open(path_to_csv_bought_input_file, 'r', newline='') as file: 
            reader = csv.DictReader(file)
            rows = list(reader)
            print('type of rows:')
            print(type(rows))
            file.seek(0)
    except FileNotFoundError:
        print(f"File '{path_to_csv_bought_input_file}' not found.")
    except PermissionError:
        print(f"You don't have permission to access '{path_to_csv_bought_input_file}'.")
    except UnicodeDecodeError:
        print(f"Invalid Unicode character found in '{path_to_csv_bought_input_file}'.")
    except csv.Error as e:
        print(f"Error while reading CSV file: {e}")

    try:
        with open(path_to_csv_bought_output_file, 'w', newline='') as file: 
            rows.append({'buy_id': id_of_row_in_csv_file_bought, 'product': product, 'buy_price': price, 'buy_date': buy_date, 'expiry_date': expiry_date}) 
            writer = csv.DictWriter(file, fieldnames= reader.fieldnames)
            writer.writeheader()
            writer.writerows(rows)
    except PermissionError:
        print(f"You don't have permission to write to '{path_to_csv_bought_output_file}'.")
    except csv.Error as e:
        print(f"Error while writing CSV file: {e}")   


def calculate_cost_in_time_range_between_start_date_and_end_date_inclusive(
        start_date: str, 
        end_date: str, 
        path_to_csv_bought_file: str
) -> float:
    '''
    Goal of fn: calculate cost in time range between start_date and end_date inclusive.
    hardcoded variables in fn: buy_date, buy_price.
    These variables refer to column names in bought.csv. 
    (for now no need to make them dynamic, i.e. no need to turn them into fn-parameters)
    
    ex of start_date: '2023-09-01'
    ex of end_date: '2023-12-21'
    '''
    start_date = datetime.strptime(str(start_date), '%Y-%m-%d')
    end_date = datetime.strptime(str(end_date), '%Y-%m-%d')
    cost = 0
    cost_rounded = 0

    try:
        with open(path_to_csv_bought_file, 'r', newline='') as file_object: 
            reader = csv.DictReader(file_object)
            for row in reader:
                sell_date = row['buy_date']
                sell_date = datetime.strptime(sell_date, '%Y-%m-%d')
                if start_date <= sell_date <= end_date:
                    cost += float(row['buy_price'])
                    cost_rounded = round(cost, 2)
        return cost_rounded
    except FileNotFoundError:
        print(f"File '{path_to_csv_bought_file}' not found.")
    except PermissionError:
        print(f"You don't have permission to access '{path_to_csv_bought_file}'.")
    except UnicodeDecodeError:
        print(f"Invalid Unicode character found in '{path_to_csv_bought_file}'.")
    except csv.Error as e:
        print(f"Error while reading CSV file: {e}")


def calculate_expired_products_on_day(
        date_on_which_to_calculate_expired_products: str, 
        path_to_csv_sold_file: str, 
        path_to_csv_bought_file: str
) -> list:
    # print(type(date_on_which_to_calculate_expired_products)) # e.g. '2023-10-01' has datatype <class 'str'>
    date_on_which_to_calculate_expired_products = datetime.strptime(date_on_which_to_calculate_expired_products, '%Y-%m-%d').date()
    # print(type(date_on_which_to_calculate_expired_products)) # e.g. '2023-10-01' now has datatype <class 'datetime.date'> and that is what I neeed. 

    # sold.csv:
    sell_data = {}
    try:
        with open(path_to_csv_sold_file, 'r') as file_object:
            reader = csv.reader(file_object)
            next(reader)  
            for row in reader:
                sell_id, buy_id, sell_price, sell_date = row
                sell_data[buy_id] = sell_date if sell_date else None
    except FileNotFoundError:
        print(f"File '{path_to_csv_sold_file}' not found.")
    except PermissionError:
        print(f"You don't have permission to access '{path_to_csv_sold_file}'.")
    except UnicodeDecodeError:
        print(f"Invalid Unicode character found in '{path_to_csv_sold_file}'.")
    except csv.Error as e:
        print(f"Error while reading CSV file: {e}")

    # bought.csv:
    expired_products = []
    try:
        with open(path_to_csv_bought_file, 'r') as file_object:
            reader = csv.reader(file_object)
            next(reader)  
            for row in reader:
                # I have access to sold.csv and bought.csv:
                buy_id, product, buy_price, buy_date, expiry_date = row
                buy_date = datetime.strptime(buy_date, '%Y-%m-%d').date()
                '''
                about 'does not expire': 
                uc: if user buys a product via argparse cli ( calling fn buy_product) without setting expiry_date as a flag, then
                default value for expiry_date is 'does not expire'. Reason: supermarket also sells e.g. magazines, 
                light bulbs, etc. that do not expire)
                '''
                if expiry_date == 'does not expire':
                    if date_on_which_to_calculate_expired_products > buy_date and expiry_date == 'does not expire' and sell_data.get(buy_id) is None:
                        expired_products.append(row)
                else: 
                    expiry_date = datetime.strptime(expiry_date, '%Y-%m-%d').date() 
                    if date_on_which_to_calculate_expired_products > buy_date and date_on_which_to_calculate_expired_products > expiry_date and sell_data.get(buy_id) is None:
                        expired_products.append(row)             
                '''
                there is only 1 difference between  this fn and fn calculate_expired_products_on_day: 
                "<" in "date_on_which_to_calculate_products_in_inventory < expiry_date" above.

                in bought.csv: (by convention) buy_date is always set with either an expiry_date or 'does not expire'.

                about 'does not expire': 
                uc: if user buys a product via argparse cli (fn buy_product) without setting expiry_date, then
                default value for expiry_date is 'does not expire' (supermarket also sells e.g. magazines, light bulbs, etc. that do not expire)
                '''
    except FileNotFoundError:
        print(f"File '{path_to_csv_bought_file}' not found.")
    except PermissionError:
        print(f"You don't have permission to access '{path_to_csv_bought_file}'.")
    except UnicodeDecodeError:
        print(f"Invalid Unicode character found in '{path_to_csv_bought_file}'.")
    except csv.Error as e:
        print(f"Error while reading CSV file: {e}")
    return expired_products



def calculate_inventory_on_day(
        date_on_which_to_calculate_products_in_inventory: str, 
        path_to_csv_sold_file: str, 
        path_to_csv_bought_file: str
) -> list:
    # print(type(date_on_which_to_calculate_products_in_inventory)) # e.g. '2023-10-01' has datatype <class 'str'>
    date_on_which_to_calculate_products_in_inventory = datetime.strptime(date_on_which_to_calculate_products_in_inventory, '%Y-%m-%d').date()
    # print(type(date_on_which_to_calculate_products_in_inventory)) # e.g. '2023-10-01' now has datatype <class 'datetime.date'> and that is what I neeed. 

    # sold.csv:
    sell_data = {}
    try:
        with open(path_to_csv_sold_file, 'r') as file_object:
            reader = csv.reader(file_object)
            next(reader)  
            for row in reader:
                sell_id, buy_id, sell_price, sell_date = row
                sell_data[buy_id] = sell_date if sell_date else None
    except FileNotFoundError:
        print(f"File '{path_to_csv_sold_file}' not found.")
    except PermissionError:
        print(f"You don't have permission to access '{path_to_csv_sold_file}'.")
    except UnicodeDecodeError:
        print(f"Invalid Unicode character found in '{path_to_csv_sold_file}'.")
    except csv.Error as e:
        print(f"Error while reading CSV file: {e}")

        
    # bought.csv:
    products_in_inventory = []
    try:
        with open(path_to_csv_bought_file, 'r') as file_object:
            reader = csv.reader(file_object)
            next(reader)  
            for row in reader:
                # I have access to sold.csv and bought.csv:
                buy_id, product, buy_price, buy_date, expiry_date = row
                buy_date = datetime.strptime(buy_date, '%Y-%m-%d').date()
                '''
                about 'does not expire': 
                uc: if user buys a product via argparse cli ( calling fn buy_product) without setting expiry_date as a flag, then
                default value for expiry_date is 'does not expire'. Reason: supermarket also sells e.g. magazines, 
                light bulbs, etc. that do not expire)
                '''
                if expiry_date == 'does not expire':
                    if date_on_which_to_calculate_products_in_inventory > buy_date and expiry_date == 'does not expire' and sell_data.get(buy_id) is None:
                        products_in_inventory.append(row)
                else: 
                    expiry_date = datetime.strptime(expiry_date, '%Y-%m-%d').date() 
                    if date_on_which_to_calculate_products_in_inventory > buy_date and date_on_which_to_calculate_products_in_inventory < expiry_date and sell_data.get(buy_id) is None:
                        products_in_inventory.append(row) 
                '''
                there is only 1 difference between  this fn and fn calculate_expired_products_on_day: 
                "<" in "date_on_which_to_calculate_products_in_inventory < expiry_date" above.

                in bought.csv: (by convention) buy_date is always set with either an expiry_date or 'does not expire'.

                about 'does not expire': 
                uc: if user buys a product via argparse cli (fn buy_product) without setting expiry_date, then
                default value for expiry_date is 'does not expire' (supermarket also sells e.g. magazines, light bulbs, etc. that do not expire)
                '''
    except FileNotFoundError:
        print(f"File '{path_to_csv_bought_file}' not found.")
    except PermissionError:
        print(f"You don't have permission to access '{path_to_csv_bought_file}'.")
    except UnicodeDecodeError:
        print(f"Invalid Unicode character found in '{path_to_csv_bought_file}'.")
    except csv.Error as e:
        print(f"Error while reading CSV file: {e}")
    return products_in_inventory


def calculate_middle_of_time_interval(
        SYSTEM_DATE: str, 
        upper_boundary_nr_of_months_to_add_to_calculate: int, 
        upper_boundary_nr_of_weeks_to_add_to_calculate: int,
        upper_boundary_nr_of_days_to_add_to_calculate: int  
) -> str:

    system_date_as_object = datetime.strptime(SYSTEM_DATE, '%Y-%m-%d')
    lower_boundary_date_object = system_date_as_object # default value
    # print('lower_boundary_date_object: ', lower_boundary_date_object)

    upper_boundary_date_object = system_date_as_object + timedelta( weeks= upper_boundary_nr_of_weeks_to_add_to_calculate, days=upper_boundary_nr_of_days_to_add_to_calculate)
    # print('upper_boundary_date_object: ', upper_boundary_date_object)
    upper_boundary_date_object = upper_boundary_date_object + relativedelta(months=upper_boundary_nr_of_months_to_add_to_calculate)
    # print('upper_boundary_date_object: ', upper_boundary_date_object)

    time_interval_middle = lower_boundary_date_object + (upper_boundary_date_object - lower_boundary_date_object) / 2
    # print('time_interval_middle: ', time_interval_middle)
    SYSTEM_DATE = datetime.strftime(time_interval_middle, '%Y-%m-%d')
    # print('SYSTEM_DATE: ', SYSTEM_DATE)
    # print(type(SYSTEM_DATE))

    return SYSTEM_DATE


def calculate_profit_in_time_range_between_start_date_and_end_date_inclusive(
        start_date: str, 
        end_date: str, 
        path_to_csv_sold_file: str, 
        path_to_csv_bought_file: str, 
        calculate_revenue_in_time_range_between_start_date_and_end_date_inclusive: Callable[[str, str, str], float], 
        calculate_cost_in_time_range_between_start_date_and_end_date_inclusive: Callable[[str, str, str], float]
) -> float:
    cost = calculate_cost_in_time_range_between_start_date_and_end_date_inclusive(start_date, end_date, path_to_csv_bought_file)
    revenue = calculate_revenue_in_time_range_between_start_date_and_end_date_inclusive(start_date, end_date, path_to_csv_sold_file)
    profit = round(revenue - cost,2)
    return profit


def calculate_sales_volume_in_time_range_between_start_date_and_end_date_inclusive(
        start_date: str, 
        end_date: str, 
        path_to_csv_sold_file: str
    ) -> int:
    '''
    Goal of fn: calculate sales volume in time range between start_date and end_date inclusive.
    hardcoded variables in fn: sell_date, sell_price .
    These variables refer to column names in sold.csv. 
    (for now no need to make them dynamic, i.e. no need to turn them into fn-parameters)

    ex of start_date: '2023-09-01'
    ex of end_date: '2023-12-21'
    '''
    start_date = datetime.strptime(str(start_date), '%Y-%m-%d')
    end_date = datetime.strptime(str(end_date), '%Y-%m-%d')
    sales_volume = 0
    try:
        with open(path_to_csv_sold_file, 'r', newline='') as file_object: 
            reader = csv.DictReader(file_object)
            for row in reader:
                sell_date = row['sell_date']
                sell_date = datetime.strptime(sell_date, '%Y-%m-%d')
                if start_date <= sell_date <= end_date:
                    sales_volume += 1
    except FileNotFoundError:
        print(f"File '{path_to_csv_sold_file}' not found.")
    except PermissionError:
        print(f"You don't have permission to access '{path_to_csv_sold_file}'.")
    except UnicodeDecodeError:
        print(f"Invalid Unicode character found in '{path_to_csv_sold_file}'.")
    except csv.Error as e:
        print(f"Error while reading CSV file: {e}")

    return sales_volume


def calculate_revenue_in_time_range_between_start_date_and_end_date_inclusive(
        start_date: str, 
        end_date: str, 
        path_to_csv_sold_file: str
) -> float:
    '''
    Goal of fn: calculate revenue in time range between start_date and end_date inclusive.
    hardcoded variables in fn: sell_date, sell_price .
    These variables refer to column names in sold.csv. 
    (for now no need to make them dynamic, i.e. no need to turn them into fn-parameters)
    
    ex of start_date: '2023-09-01'
    ex of end_date: '2023-12-21'
    '''
    start_date = datetime.strptime(str(start_date), '%Y-%m-%d')
    end_date = datetime.strptime(str(end_date), '%Y-%m-%d')

    revenue = 0
    revenue_rounded = 0
    try:
        with open(path_to_csv_sold_file, 'r', newline='') as file: 
            reader = csv.DictReader(file)
            for row in reader:
                sell_date = row['sell_date']
                sell_date = datetime.strptime(sell_date, '%Y-%m-%d')
                if start_date <= sell_date <= end_date:
                    revenue += float(row['sell_price'])
                    revenue_rounded = round(revenue, 2)
        return revenue_rounded
    except FileNotFoundError:
        print(f"File '{path_to_csv_sold_file}' not found.")
    except PermissionError:
        print(f"You don't have permission to access '{path_to_csv_sold_file}'.")
    except UnicodeDecodeError:
        print(f"Invalid Unicode character found in '{path_to_csv_sold_file}'.")
    except csv.Error as e:
        print(f"Error while reading CSV file: {e}")


def create_buy_id_for_each_row_in_boughtcsv_as_part_of_mockdata_that_is_being_created(
        csv_file_name_first_letter: str, 
        first_nr_in_range: int
) -> Callable[[], int]:
    ''' 
    scope: only used by script create_testdata_for_csv_files_bought_and_sold.py.
    e.g. "b" is abbreviation of 'bought.csv'. This 'b' will be part of 
    argparse argument, so needs to be concise for pleasant user 
    experience.    
    '''
    count = first_nr_in_range
    count -= 1 # to start with 1, not 0
    def counter():
        nonlocal count
        count += 1

        if count < 10:
            return f"{csv_file_name_first_letter}_0{count}"
        return f"{csv_file_name_first_letter}_{count}"
    return counter


def create_buy_id_that_increments_highest_buy_id_in_boughtcsv(path_to_id_with_highest_sequence_number: str) -> str:
    '''
    Goal: use output of this fn to create a buy_id as input for fn buy_product, so fn buy_product can create a next buy-transaction.
    Context: this fn is  only used in super.py.
    More info about how this fn fits into  the bigger picture, see: README_REPORT.md --> '# Technical element 2: create primary 
    and foreign keys to connect bought.csv and sold.csv 

    I run superpy via the command line in argparse.
    So state of last id that was used in fn buy_product() is unknown (e.g. b_323), given
    that I buy products and delete products (records) from bought.csv. 
    I do not want to reuse an id that was used before (e.g. that belonged to a product
    that was deleted).
    So I save the state of the id (e.g. b_351) that was used last in fn buy_product() in a txt-file.

    The products that are bought by superpy-user and/or pytest-"testengine" user  start
    at id b_300 and count up from there.
    The range id_1 to id_299 is reserved for script 'create_testdata_for_csv_files_bought_and_sold'
    in directory create_new_testdata_for_csv_files.

    '''
    print('path_to_id_with_highest_sequence_number')
    print(path_to_id_with_highest_sequence_number)
    # new_id_to_use_in_fn_buy_product = ''
    try:
        with open(path_to_id_with_highest_sequence_number, 'r', newline='') as file:
            last_id_used_in_fn_buy_product =file.read()

            id_parts = last_id_used_in_fn_buy_product.split("_") # e.g. ['b', '323']
            new_id_to_use_in_fn_buy_product = int(id_parts[1]) + 1
            '''
            b_1 (...) b_9 must be created as b_01 (...) b_09.
            reason: 
            In this the ids of the transactions in sold.csv are created by replacing the 'b' in the buy_id with an 's'.
            So the ids of the transactions in sold.csv are s_1 (...) s_9, and s_10 (...) s_99, and s_100 (...) s_999, etc.
            But this is a problem, because the ids of the transactions in sold.csv are sorted alphabetically, not numerically.
            So s_10 is sorted before s_2, and s_100 is sorted before s_3, etc.
            So I need to create b_01 (...) b_09, so that s_01 (...) s_09 can be created.
            '''
            if new_id_to_use_in_fn_buy_product < 10:
                new_id_to_use_in_fn_buy_product = "b_0" + str(new_id_to_use_in_fn_buy_product)
            else:
                new_id_to_use_in_fn_buy_product = "b_" + str(new_id_to_use_in_fn_buy_product)
            file.seek(0)
    except FileNotFoundError:
        print(f"File '{path_to_id_with_highest_sequence_number}' not found.")
    except PermissionError:
        print(f"You don't have permission to access '{path_to_id_with_highest_sequence_number}'.")
    except UnicodeDecodeError:
        print(f"Invalid Unicode character found in '{path_to_id_with_highest_sequence_number}'.")
    except IOError as e:
        print(f"Error while reading file: {e}")

    try:
        with open(path_to_id_with_highest_sequence_number, 'w', newline='') as file: 
            print(new_id_to_use_in_fn_buy_product)  
            file.write(new_id_to_use_in_fn_buy_product)
    except PermissionError:
        print(f"You don't have permission to write to '{path_to_id_with_highest_sequence_number}'.")
    except IOError as e:
        print(f"Error while writing file: {e}")

    return new_id_to_use_in_fn_buy_product


def create_data_for_csv_files_bought_and_sold(
        product_range: int, 
        delete_every_nth_row_in_soldcsv_so_every_nth_row_in_boughtcsv_can_expire_when_time_travelling: int,
        shelf_life: int,
        turnover_time: int,
        markup: int,
        lower_boundary_year_of_time_interval_in_which_to_create_random_testdata: int,
        lower_boundary_month_of_time_interval_in_which_to_create_random_testdata: int,
        lower_boundary_week_of_time_interval_in_which_to_create_random_testdata: int,
        upper_boundary_nr_of_months_to_add_to_calculate: int,
        upper_boundary_nr_of_weeks_to_add_to_calculate: int,
        upper_boundary_nr_of_days_to_add_to_calculate: int,
        superpy_product_prices: list,
        superpy_product_range: list,
        path_to_file_bought_csv: str,
        path_to_file_sold_csv: str,
        add_days_to_date: int,
        create_buy_id_for_each_row_in_boughtcsv_as_part_of_mockdata_that_is_being_created: Callable[[str, int], Callable[[], int]], 
        # reason: fn A is fn-argument in fn B == fn B(fn A). And B(fn A) is argument in fn C == fn C(B(fn A))
        generate_random_buy_date_for_buy_transaction_in_future_in_time_interval: Callable[[int, int, int, int, int, int], str]
) -> None:
    '''
        Goal: create testdata for bought.csv and sold.csv. 
        # part 1 of 2: create testdata for bought.csv
        # part 2 of 2: create testdata for sold.csv

        fn-parameters are not in a lookup-table / dictionary (e.g. config_variables = {} ), 
        because it could make parsing with argparse cli more difficult (not sure).

        This fn cannot be tested with pytest, because I use random.sample() in this fn.

        backlog idea: add fn-arg price_range (implement same way as product_range). 
            Edge case to test while implementing this backlog feature:
            1. create mock_data with product_range and price_range of 1
            2. result: less than 10 transactions in bought.csv
            3. now check if fn create_buy_id_that_increments_highest_buy_id_in_boughtcsv() still
            works as expected: i.e. can handle an input of e.g. b_9 and return b_10.
            Up until now the lowest input into  this fn has been  b_12, b_13 etc. 
    '''
    # PART 1 OF 2: create testdata for bought.csv: 

    # step 1: check if product_range does not exceed nr of products in supermarket (i.e. imported superpy_product_range):

    if product_range > len(superpy_product_range):
        raise ValueError('''product_range cannot exceed nr of products in supermarket. 
                         Plz specify a lower value for product_range. 
                         See README_USAGE_GUIDE.md ffor more information.''')


    # step 2: create id for each bought product: (e.g. b_1, b_2, b_3, etc):
    csv_file_bought_id = ''
    csv_file_bought_id = create_buy_id_for_each_row_in_boughtcsv_as_part_of_mockdata_that_is_being_created('b', 1) 

    superpy_product_range = list(set(superpy_product_range))
    # step 3: create random list with products that are sold in supermarket:
    # product = '' # prevent UnboundLocalError: local variable 'product' referenced before assignment
    products = random.sample(superpy_product_range, product_range)
    
    # step 4: generate all possible combinations of products and price_per_unit:
    bought_products = (list(product(products, superpy_product_prices)))
    '''
        math highschool analogy: (5+2)*(3+4) == 5*3 + 5*4 + 2*3 + 2*4:
        (5+2)*(3+4) == 5*3 + 5*4 + 2*3 + 2*4 == (5,2)*(3,4) == (5,3) + (5,4) + (2,3) + (2,4)
        While reading this, suppose 5 and 3 are products and 2 and 4 are price_per_unit.
        Then 2 products and 2 price_per_unit result in 4 combinations == 4 bought products == 4 rows in bought.csv.
        Then 4 products and 3 price_per_unit result in 12 combinations == 12 bought products == 12 rows in bought.csv.
    '''

    # step 5: generate buy_date and expiry_date for each product:
    products_with_bought_date = []
    for bought_product in bought_products:
        bought_date = generate_random_buy_date_for_buy_transaction_in_future_in_time_interval(
            lower_boundary_year_of_time_interval_in_which_to_create_random_testdata,
            lower_boundary_month_of_time_interval_in_which_to_create_random_testdata,
            lower_boundary_week_of_time_interval_in_which_to_create_random_testdata,
            upper_boundary_nr_of_months_to_add_to_calculate,
            upper_boundary_nr_of_weeks_to_add_to_calculate,
            upper_boundary_nr_of_days_to_add_to_calculate)

        expiry_date = add_days_to_date(bought_date, shelf_life) 
        products_with_bought_date.append(bought_product + (bought_date, expiry_date)) 

    # step 6: sort list with tuples on bought_date: (x[3] is the bought_date)
    products_with_bought_date.sort(key=lambda x: x[3])

    # step 7: convert list with tuples into list with lists:
    products_with_bought_date = [list(elem) for elem in products_with_bought_date]
    # print(products_with_bought_date) # status: ok (output: list with lists)

    # step 8: add id (b_1, b_2, b_3, etc.) to each list in list:
    for row_in_csv_file_bought in products_with_bought_date:
        row_in_csv_file_bought.insert(0, csv_file_bought_id())

    # step 9: save data to bought.csv:
    try:
        with open(path_to_file_bought_csv, 'w', newline='') as csvfile:    
            writer = csv.writer(csvfile)
            writer.writerow(['buy_id', 'product', 'buy_price', 'buy_date', 'expiry_date'])
            writer.writerows(products_with_bought_date) 
            # writerows() expects a list of lists.
    except PermissionError:
        print(f"You don't have permission to write to '{path_to_file_bought_csv}'.")
    except csv.Error as e:
        print(f"Error while writing CSV file: {e}")

    # PART 2 OF 2: create testdata for sold.csv: 

    # step 1: make a deepcopy of bought.csv:
    products_with_sold_date = deepcopy(products_with_bought_date)
    # deepcopy() is needed to prevent that changes to products_with_sold_date also affect products_with_bought_date.

    # step 2: make changes to deepcopy of bought.csv:
    for row in products_with_sold_date:
        # products_with_sold_date is list with lists:

        buy_price = row[2] # price_of_sold_product is float
        sell_price = round(buy_price * markup,2)
        row[2] = sell_price # sell_price takes the place of buy_price in sold.csv

        # calculate sell_date:
        buy_date = row[3] # because sold.csv starts of as a deepcopy of bought.csv
        sold_date = add_days_to_date(buy_date, turnover_time) 
        row[3] = sold_date # sell_date takes the place of buy_date in sold.csv

        # delete expiry_date from sold.csv to avoid redundancy:
        # expiry_date = row[4] 
        del row[4] 

        # delete product from sold.csv to avoid redundancy:
        # product = row[1]
        del row[1]

        # replace buy_id by sell_id: e.g. b_1 --> s_1, b_2 --> s_2, etc:
        buy_id_in_record_in_bought_csv = row[0] # e.g. b_28
        row.insert(1, buy_id_in_record_in_bought_csv) # e.g. b_28, so an exact copy of this immutable string.

        sell_id_of_record_in_sold_csv = row[0]
        sell_id_of_record_in_sold_csv = sell_id_of_record_in_sold_csv.replace('b', 's') # e.g. b_28 --> s_28
        row[0] = sell_id_of_record_in_sold_csv # e.g. s_28

    # step 3: delete each nth list in list: (so each nth row will expire in sold.csv while time traveling to the future)
    products_with_sold_date = [row for row in products_with_sold_date if int(row[0].split("_")[1]) % 
        delete_every_nth_row_in_soldcsv_so_every_nth_row_in_boughtcsv_can_expire_when_time_travelling != 0]   
    '''
    About 'deleting each nth list in list': this sets nr of rows to delete from sold.csv:
    sold.csv is as a copy of bought.csv. After making the deepcopy, a few changes are made: 
    e.g. make sell_price different (higher) than buy_price, but also delete some rows. 
    Rows that are present in bought.csv, but not in sold.csv, will expire while time traveling.
    (e.g. if delete_every_nth_row_in_soldcsv_so_every_nth_row_in_boughtcsv_can_expire_when_time_travelling = 2, then every 2nd row will be deleted)
    (e.g. if delete_every_nth_row_in_soldcsv_so_every_nth_row_in_boughtcsv_can_expire_when_time_travelling = 3, then every 3rd row will be deleted)

    ex: e.g. input is 'b_17'. b_17 means: row 17 in bought.csv == transaction nr 17 in bought.csv. 
    b_17 is primary key in bought.csv.
    int(row[0].split("_")[1]) extracts 17 from b_17.
    The code bit "% delete_every_nth_row_in_soldcsv_so_every_nth_row_in_boughtcsv_can_expire_when_time_travelling != 0" means: if 17 % 2 != 0, then keep row 17 in bought.csv.
    17 % 2 != 0, so row 17 is kept in bought.csv.
    '''

    # step 4: save data to sold.csv:
    try:
        with open(path_to_file_sold_csv, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['sell_id', 'buy_id', 'sell_price', 'sell_date'])
            writer.writerows(products_with_sold_date) # note to self: writerows() expects a list of lists.
    except PermissionError:
        print(f"You don't have permission to write to '{path_to_file_sold_csv}'.")
    except csv.Error as e:
        print(f"Error while writing CSV file: {e}")


def generate_random_buy_date_for_buy_transaction_in_future_in_time_interval(
        interval_lower_boundary_year: int, 
        interval_lower_boundary_month: int, 
        interval_lower_boundary_day: int, 
        nr_of_months_added_to_calculate_upper_boundary: int, 
        nr_of_weeks_added_to_calculate_upper_boundary: int, 
        nr_of_days_added_to_calculate_upper_boundary: int
) -> str:     
    '''
    alternative setup for fn-arguments: system_date in format '%Y-%m-%d' for lower boundary and another one for upper boundary.
    '''
    start_date = date(interval_lower_boundary_year, interval_lower_boundary_month, interval_lower_boundary_day)
    end_date = start_date + relativedelta(months=nr_of_months_added_to_calculate_upper_boundary)
    end_date = end_date + relativedelta(weeks=nr_of_weeks_added_to_calculate_upper_boundary)
    end_date = end_date + relativedelta(days=nr_of_days_added_to_calculate_upper_boundary)
    time_between_dates = end_date - start_date
    days_between_dates = time_between_dates.days
    random_number_of_days = random.randrange(days_between_dates)
    random_date = start_date + timedelta(days=random_number_of_days)
    return random_date.strftime('%Y-%m-%d')

def get_dates_of_next_7_days(today: str) -> list:
    '''
    uc: as a Superpy user I want to have intuitive 
    UI: e.g.
    'py super.py buy apple 1.10 next_monday 
    instead of e.g.:
    'py super.py buy apple 1.10 2021-09-25'
    '''
    today_as_date_object = datetime.strptime(today, '%Y-%m-%d').date()
    # print(f'today_as_date_object: {today_as_date_object}')
    
    day_of_week = (today_as_date_object.weekday() + 1 ) 
    # Monday is 0, Sunday is 6, so add 1 for easier reading.
    # print(f'day_of_week: {day_of_week}')
    '''
    My code below is bit of a long stretch, but I do not
    know how to make it shorter. 
    '''
    if day_of_week == 1:  # Monday
        monday = today_as_date_object + timedelta(days= 7)
        tuesday = today_as_date_object + timedelta(days= 1)
        wednesday = today_as_date_object + timedelta(days= 2)
        thursday = today_as_date_object + timedelta(days= 3)
        friday = today_as_date_object + timedelta(days= 4)
        saturday = today_as_date_object + timedelta(days= 5)
        sunday = today_as_date_object + timedelta(days= 6)
    if day_of_week == 2: # Tuesday
        monday = today_as_date_object + timedelta(days= 6)
        tuesday = today_as_date_object + timedelta(days= 7)
        wednesday = today_as_date_object + timedelta(days= 1)
        thursday = today_as_date_object + timedelta(days= 2)
        friday = today_as_date_object + timedelta(days= 3)
        saturday = today_as_date_object + timedelta(days= 4)
        sunday = today_as_date_object + timedelta(days= 5)
    if day_of_week == 3: # Wednesday
        monday = today_as_date_object + timedelta(days= 5)
        tuesday = today_as_date_object + timedelta(days= 6)
        wednesday = today_as_date_object + timedelta(days= 7)
        thursday = today_as_date_object + timedelta(days= 1)
        friday = today_as_date_object + timedelta(days= 2)
        saturday = today_as_date_object + timedelta(days= 3)
        sunday = today_as_date_object + timedelta(days= 4)
    if day_of_week == 4: # Thursday
        monday = today_as_date_object + timedelta(days= 4)
        tuesday = today_as_date_object + timedelta(days= 5)
        wednesday = today_as_date_object + timedelta(days= 6)
        thursday = today_as_date_object + timedelta(days= 7)
        friday = today_as_date_object + timedelta(days= 1)
        saturday = today_as_date_object + timedelta(days= 2)
        sunday = today_as_date_object + timedelta(days= 3)
    if day_of_week == 5: # Friday
        monday = today_as_date_object + timedelta(days= 3)
        tuesday = today_as_date_object + timedelta(days= 4)
        wednesday = today_as_date_object + timedelta(days= 5)
        thursday = today_as_date_object + timedelta(days= 6)
        friday = today_as_date_object + timedelta(days= 7)
        saturday = today_as_date_object + timedelta(days= 1)
        sunday = today_as_date_object + timedelta(days= 2)
    if day_of_week == 6: # Saturday
        monday = today_as_date_object + timedelta(days= 2)
        tuesday = today_as_date_object + timedelta(days= 3)
        wednesday = today_as_date_object + timedelta(days= 4)
        thursday = today_as_date_object + timedelta(days= 5)
        friday = today_as_date_object + timedelta(days= 6)
        saturday = today_as_date_object + timedelta(days= 7)
        sunday = today_as_date_object + timedelta(days= 1)
    if day_of_week == 7: # Sunday
        monday = today_as_date_object + timedelta(days= 1)
        tuesday = today_as_date_object + timedelta(days= 2)
        wednesday = today_as_date_object + timedelta(days= 3)
        thursday = today_as_date_object + timedelta(days= 4)
        friday = today_as_date_object + timedelta(days= 5)
        saturday = today_as_date_object + timedelta(days= 6)
        sunday = today_as_date_object + timedelta(days= 7)

    dates_of_next_7_days = [monday, tuesday, wednesday, thursday, friday, saturday, sunday]

    dates_of_next_7_days_as_strings = []
    for day in dates_of_next_7_days:
        day = day.strftime('%Y-%m-%d')
        dates_of_next_7_days_as_strings.append(day)

    return dates_of_next_7_days_as_strings

def get_highest_buy_id_from_boughtcsv(path_to_csv_bought_file: str) -> str:
    '''
    Goal: use output of this fn to create a buy_id for the next buy-transaction.
    Context: this fn is  only used in super.py: after the mockdata has been created for bought.csv and sold.csv, but before you
    start using super.py via the command line in argparse to e.g.  buy a product,  you call this fn.
    More info about how this fn fits into  the bigger picture, see: README_REPORT.md --> '# Technical element 2: create primary 
    and foreign keys to connect bought.csv and sold.csv 
 
    Code below expects first column in bought.csv to be buy_id with format 
    b_1, b_2, b_3, etc.  
    '''
    highest_buy_id = 'b_0' 
    try: 
        with open(path_to_csv_bought_file, 'r') as file_object:
            reader = csv.reader(file_object)
            next(reader) # skip header row
            for row in reader:
                csv_column_1 = row[0] # ex: b_1, or: b_2, or: b_3, etc
                if int(csv_column_1.split('_')[1]) > int(highest_buy_id.split('_')[1]):
                    highest_buy_id = csv_column_1
    except FileNotFoundError:
        print(f"File '{path_to_csv_bought_file}' not found.")
    except PermissionError:
        print(f"You don't have permission to access '{path_to_csv_bought_file}'.")
    except UnicodeDecodeError:
        print(f"Invalid Unicode character found in '{path_to_csv_bought_file}'.")
    except csv.Error as e:
        print(f"Error while reading CSV file: {e}")
    return highest_buy_id


def get_path_to_directory_of_file(directory_of_file: str) -> str:
    # rule1: directory_of_file must be unique inside project superpy.
    whereabouts_of_directory_of_file  = str(os.getcwd()) 
    path_to_directory_of_this_file = '' # prevent UnboundLocalError
    for root, dirs, files in os.walk(whereabouts_of_directory_of_file):
        for name in dirs:
            if name == directory_of_file: 
                path_to_directory_of_this_file = os.path.abspath(os.path.join(root, name))
                break # if rule1 above has been followed, then you can stop searching here to save time.
    return path_to_directory_of_this_file


def get_path_to_file(directory_of_file: str, file_name_of_which_you_want_to_know_the_path: str) -> str:
    # rule1: directory_of_file must be unique inside project superpy.
    whereabouts_of_directory_of_file  = str(os.getcwd()) 
    path_to_directory_of_this_file = '' # prevent UnboundLocalError
    for root, dirs, files in os.walk(whereabouts_of_directory_of_file):
        for name in dirs:
            if name == directory_of_file: 
                path_to_directory_of_this_file = os.path.abspath(os.path.join(root, name))
                break # if rule1 above has been followed, then you can stop searching here to save time.
    path_to_file = os.path.join(path_to_directory_of_this_file, file_name_of_which_you_want_to_know_the_path ) # path to file 
    return path_to_file

def get_system_date(path_to_system_date: str) -> str:
    # fn-output: system_date is datetime object, ex: '2020-01-01'
    try:
        with open(path_to_system_date, 'r', newline='') as file:
            system_date = file.read()
    except FileNotFoundError:
        print(f"File '{path_to_system_date}' not found.")
    except PermissionError:
        print(f"You don't have permission to access '{path_to_system_date}'.")
    except UnicodeDecodeError:
        print(f"Invalid Unicode character found in '{path_to_system_date}'.")
    except IOError as e:
        print(f"Error while reading file: {e}")
    return system_date


def sell_product(bought_product_id: str, 
                 price: float, 
                 sell_date: str, 
                 path_to_csv_bought_input_file: str, 
                 path_to_csv_bought_output_file: str
) -> None:
    '''
    About the input_file and output_file:
    when using superpy as user, input and output csv file are the same.
    Only when testing fn buy_product in pytest, input and output csv file are different.
    reason: when testing fn buy_product in pytest, I want to keep the csv-file with testdata intact.
    '''
    try: 
        with open(path_to_csv_bought_input_file, 'r', newline='') as file: 
            reader = csv.DictReader(file)
            rows = list(reader)
            file.seek(0)
            sold_product_id = bought_product_id.replace('b', 's')
    except FileNotFoundError:
        print(f"File '{path_to_csv_bought_input_file}' not found.")
    except PermissionError:
        print(f"You don't have permission to access '{path_to_csv_bought_input_file}'.")
    except UnicodeDecodeError:
        print(f"Invalid Unicode character found in '{path_to_csv_bought_input_file}'.")
    except csv.Error as e:
        print(f"Error while reading CSV file: {e}")
    try:            
        with open(path_to_csv_bought_output_file, 'w', newline='') as file: 
            rows.append({'sell_id': sold_product_id, 'buy_id': bought_product_id, 'sell_price': price, 'sell_date': sell_date}) 
            writer = csv.DictWriter(file, fieldnames= reader.fieldnames)
            writer.writeheader()
            # sort rows by sell_id (== first column in sold.csv):
            sorted_rows = sorted(rows, key=lambda row: row['sell_id'])
            writer.writerows(sorted_rows)
    except PermissionError:
        print(f"You don't have permission to write to '{path_to_csv_bought_output_file}'.")
    except csv.Error as e:
        print(f"Error while writing CSV file: {e}")


def set_buy_id_in_file_id_to_use_in_fn_to_buy_product_txt_after_running_fn_to_create_mock_data_for_boughtcsv_and_soldcsv(buy_id: str, path_to_buy_id_file: str) -> str:
    '''
    # pitfall: read first part of fn-name 'file_id_to_use_in_fn_to_buy_product_txt' as a reference to a file. 
    # arg1: ex of buy_id: b_1, or: b_2, or: b_3, etc
    # arg2: location of file: (...superpy\\data_used_in_superpy\\id_to_use_in_fn_buy_product.txt)
    
    Context: this fn is  only used in file super.py.
    More info about how this fn fits into  the bigger picture, see: README_REPORT.md --> '# Technical element 2: create primary 
    and foreign keys to connect bought.csv and sold.csv 
    '''
    if buy_id == None: # if bought.csv is empty
        buy_id = 'b_00' 
        '''
        # pitfall: at this point in the code you can fill out b_00 or b_0. It does not matter.
        Later, in fn create_buy_id_that_increments_highest_buy_id_in_boughtcsv(), b_00 will be converted to b_1.
        '''
        


    try:
        with open(path_to_buy_id_file, 'w', newline='') as file:
            file.write(buy_id)
    except PermissionError:
        print(f"You don't have permission to write to '{path_to_buy_id_file}'.")
    except IOError as e:
        print(f"Error while writing file: {e}")
    return buy_id


def set_system_date_to(system_date: str, path_to_system_date: str) -> str:
    # system_date is datetime object, ex: '2020-01-01'
    try:
        with open(path_to_system_date, 'w', newline='') as file:
            file.write(system_date)
    except PermissionError:
        print(f"You don't have permission to write to '{path_to_system_date}'.")
    except IOError as e:
        print(f"Error while writing file: {e}")
    return system_date


def show_list_with_nested_lists_in_console_with_module_rich(list: list) -> Table: # more precise: input is list with lists.
    rich_table = Table(show_header=True, header_style="bold magenta")
    # (future reference: column names hardcoded. Currently no need
    # to make dynamic).
    rich_table.add_column('buy_id', style="dim", width=12)
    rich_table.add_column('product', style="dim", width=12)
    rich_table.add_column('buy_price', style="dim", width=12)
    rich_table.add_column('buy_date', style="dim", width=12)
    rich_table.add_column('expiry_date', style="dim", width=12)
    for row in list:
        rich_table.add_row(*row)
    console = Console()
    console.print(rich_table)
    return rich_table


def show_csv_file_in_console_with_module_rich(path_to_csv_file: str) -> None:
    console = Console()
    table = Table(show_header=True, header_style="bold magenta")
    try:
        with open(path_to_csv_file, 'r') as file:
            csv_reader = csv.reader(file)
            header = next(csv_reader)  
            for column in header:
                table.add_column(column)
            for row in reversed(list(csv_reader)):
                table.add_row(*row)
    except FileNotFoundError:
        print(f"File '{path_to_csv_file}' not found.")
    except PermissionError:
        print(f"You don't have permission to access '{path_to_csv_file}'.")
    except UnicodeDecodeError:
        print(f"Invalid Unicode character found in '{path_to_csv_file}'.")
    except csv.Error as e:
        print(f"Error while reading CSV file: {e}")
    console.print(table)


def time_travel_system_date_with_nr_of_days(
        nr_of_days_to_travel: int, 
        path_to_input_file: str, 
        path_to_output_file: str
    ) -> str:
    try:
        with open(path_to_input_file, 'r', newline='') as file:
            # read current system date from file in format YYYY-MM-DD (e.g. '2025-03-14). This
            # should be the only contents of the file. 
            current_system_date = file.readline().split(',')[0]
            print('current_system_date: ', current_system_date)
            file.seek(0)
    except FileNotFoundError:
        print(f"File '{path_to_input_file}' not found.")
    except PermissionError:
        print(f"You don't have permission to access '{path_to_input_file}'.")
    except UnicodeDecodeError:
        print(f"Invalid Unicode character found in '{path_to_input_file}'.")
    except IOError as e:
        print(f"Error while reading file: {e}")

    try:
        with open(path_to_output_file, 'w', newline='') as file:
            new_system_date = add_days_to_date(current_system_date, nr_of_days_to_travel)
            file.write(new_system_date)
            print('new_system_date: ', new_system_date)
    except PermissionError:
        print(f"You don't have permission to write to '{path_to_output_file}'.")
    except IOError as e:
        print(f"Error while writing file: {e}")
    # returning new_system_date for testing purposes only (returned value is not used in the code)    
    return new_system_date

def show_weekday_from_date(date: str) -> str:
    date_object = datetime.strptime(date, '%Y-%m-%d')
    day_of_week = date_object.strftime('%A')
    return day_of_week