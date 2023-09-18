
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



# list of functions:
# add_days_to_date(date_string, days_to_add)
# buy_product(product,price,buy_date,expiry_date,id_of_row_in_csv_file_bought,path_to_csv_bought_input_file,path_to_csv_bought_output_file):
# calculate_cost_in_time_range_between_start_date_and_end_date_inclusive(start_date, end_date, path_to_csv_bought_file):
# calculate_profit_in_time_range_between_start_date_and_end_date_inclusive(start_date, end_date, path_to_csv_sold_file, path_to_csv_bought_file, calculate_revenue_in_time_range_between_start_date_and_end_date_inclusive, calculate_cost_in_time_range_between_start_date_and_end_date_inclusive):
# calculate_revenue_in_time_range_between_start_date_and_end_date_inclusive(start_date, end_date, path_to_csv_sold_file):
# create_data_for_csv_files_bought_and_sold("long list of parameters")
# create_id_for_each_row_in_boughtcsv_while_script_generates_boughtcsv(path_to_id_with_highest_sequence_number)
# create_id_with_unused_highest_sequence_nr_to_buy_product_as_superpy_user(path_to_id_with_highest_sequence_number):
# generate_random_date_in_future_in_time_interval_of_2_months()
# get_highest_buy_id_after_running_script_to_create_mock_data_for_boughtcsv_and_soldcsv(path_to_csv_bought_file)
# get_path_to_file(directory_of_file, file_name_of_which_you_want_to_know_the_path):
# set_buy_id_after_running_script_to_create_mock_data_for_boughtcsv_and_soldcsv(buy_id, path_to_buy_id_file)
# set_system_date_to(system_date, path_to_system_date, system_date_file='system_date.txt'): (created in TDD fashion)
# show_csv_file_in_console_with_module_rich(path_to_csv_file):
# time_travel_system_date_with_nr_of_days(nr_of_days_to_travel, path_to_input_file, path_to_output_file):


def add_days_to_date(date_string, days_to_add):
    date = datetime.strptime(date_string, '%Y-%m-%d')
    new_date = date + timedelta(days= days_to_add)
    '''
    This is a helper fn used as fn-argument in following fns:
    - create_data_for_csv_files_bought_and_sold()
    - time_travel_system_date_with_nr_of_days()
    
    pitfall:
    new_date = date.replace(day=date.day+days_to_add) 
    problem: if date.day+days_to_add > nr of days in month, then you get an error (e.g. 31+1=32, but no month has 32 days).
    solution: use timedelta() instead of replace().
    '''
    return new_date.strftime('%Y-%m-%d')


def buy_product(product,
                price,
                buy_date,
                expiry_date, 
                id_of_row_in_csv_file_bought,
                path_to_csv_bought_input_file,  
                path_to_csv_bought_output_file
                ):
    '''
    About the input_file and output_file:
    when using superpy as user, input and output csv file are the same.
    Only when testing fn buy_product in pytest, input and output csv file are different.
    reason: when testing fn buy_product in pytest, I want to keep the csv-file with testdata intact.
    '''
    with open(path_to_csv_bought_input_file, 'r', newline='') as file: 
        #r+ == read and write. This makes the code below more compact. 
        # newline='' is necessary to avoid empty lines in csv-file.
        print('var file is an iterator obj:')
        print(file) # <_io.TextIOWrapper name='test_file.csv' mode='r+' encoding='cp1252'>
        print(type(file)) # <class '_io.TextIOWrapper'>
        # file is an iterator with strings as elements. (!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!)
        
        print('-----------------------------------')
        reader = csv.DictReader(file)
        print('var reader is an iterator obj:')
        print(reader) # <csv.DictReader object at 0x000002579966D600>
        print(type(reader)) # <class 'csv.DictReader'>
        # reader is an iterator with dictionaries as elements. (!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!)
        # an: so at this point you are still working with an iterator, not with a list.

        print('-----------------------------------')
        print('var reader.fieldnames is a list:')   
        print(reader.fieldnames) 
        print(type(reader.fieldnames)) # <class 'list'>

        print('-----------------------------------')
        print('list stuff:')
        print('convert iterator with dictionaries into list with dictionaries: ')
        rows = list(reader)
        # rows is a list with dictionaries as elements.

        # print(rows)
        print('type of rows:')
        print(type(rows))
        file.seek(0)

    # choose between option 1 and 2 (COMMENT OUT THE UNUSED OPTION)
    # option1of2: this alternative in write-mode works as well (but is more verbose and misuses write-mode):
    with open(path_to_csv_bought_output_file, 'w', newline='') as file: 
        rows.append({'buy_id': id_of_row_in_csv_file_bought, 'product': product, 'buy_price': price, 'buy_date': buy_date, 'expiry_date': expiry_date}) 
        writer = csv.DictWriter(file, fieldnames= reader.fieldnames)
        # Dictwriter is a class. writer is its instanciated obj.
        writer.writeheader()
        writer.writerows(rows)
        '''
            in this alternative rows is a list with dictionaries. 
            Apparently writerows() expects a list with dictionnaries to be passed as argument,
            in order to update csv-file test_file.csv.        
        '''

    # option 2of2: 
    '''
    problem with this alternative in append-mode: data gets added to the file with actual testresult. 
    So after each testrun the file with actual testresult gets longer and longer. So 2nd time 
    you run pytest (and 3rd, etc.) the testcases will fail! Solution: as postperation remove the 
    data that has been added to the actual testresult file during the testrun....I don't like this solution.
    '''
    # with open(path_to_csv_bought_output_file, 'a', newline='') as file:
    #     row = [id_of_row_in_csv_file_bought,product,price,buy_date,expiry_date]
    #     writer = csv.writer(file)
    #     writer.writerow(row)


# def calculate_revenue_in_time_range_between_start_date_and_end_date_inclusive(start_date, end_date, path_to_input_file):
#     pass

def calculate_cost_in_time_range_between_start_date_and_end_date_inclusive(start_date, end_date, path_to_csv_bought_file):
    '''
    Goal of fn: calculate cost in time range between start_date and end_date inclusive.
    hardcoded variables in fn: buy_date, buy_price.
    These variables refer to column names in bought.csv. 
    (for now no need to make them dynamic, i.e. no need to turn them into fn-parameters)
    
    ex of start_date: '2023-09-01'
    ex of end_date: '2023-12-21'
    '''
    # print('start_date:')
    start_date = datetime.strptime(str(start_date), '%Y-%m-%d')
    # print(start_date)
    # print('end_date:')
    end_date = datetime.strptime(str(end_date), '%Y-%m-%d')
    # print(end_date)
    cost = 0
    cost_rounded = 0
    with open(path_to_csv_bought_file, 'r', newline='') as file: 
        reader = csv.DictReader(file)
        for row in reader:
            print('row:')
            print(row)
            sell_date = row['buy_date']
            sell_date = datetime.strptime(sell_date, '%Y-%m-%d')
            if start_date <= sell_date <= end_date:
                # print(revenue)
                cost += float(row['buy_price'])
                cost_rounded = round(cost, 2)
    return cost_rounded

def calculate_profit_in_time_range_between_start_date_and_end_date_inclusive(start_date, end_date, path_to_csv_sold_file, path_to_csv_bought_file, calculate_revenue_in_time_range_between_start_date_and_end_date_inclusive, calculate_cost_in_time_range_between_start_date_and_end_date_inclusive):
    cost = calculate_cost_in_time_range_between_start_date_and_end_date_inclusive(start_date, end_date, path_to_csv_bought_file)
    revenue = calculate_revenue_in_time_range_between_start_date_and_end_date_inclusive(start_date, end_date, path_to_csv_sold_file)
    profit = round(revenue - cost,2)
    return profit

def calculate_sales_volume(start_date, end_date, path_to_csv_sold_file):
    pass


def calculate_revenue_in_time_range_between_start_date_and_end_date_inclusive(start_date, end_date, path_to_csv_sold_file):
    '''
    Goal of fn: calculate revenue in time range between start_date and end_date inclusive.
    hardcoded variables in fn: sell_date, sell_price .
    These variables refer to column names in sold.csv. 
    (for now no need to make them dynamic, i.e. no need to turn them into fn-parameters)
    
    ex of start_date: '2023-09-01'
    ex of end_date: '2023-12-21'
    '''
    # print('start_date:')
    start_date = datetime.strptime(str(start_date), '%Y-%m-%d')
    # print(start_date)
    # print('end_date:')
    end_date = datetime.strptime(str(end_date), '%Y-%m-%d')
    # print(end_date)

    revenue = 0
    revenue_rounded = 0
    with open(path_to_csv_sold_file, 'r', newline='') as file: 
        reader = csv.DictReader(file)
        for row in reader:
            # print('row:')
            # print(row)
            sell_date = row['sell_date']
            sell_date = datetime.strptime(sell_date, '%Y-%m-%d')
            if start_date <= sell_date <= end_date:
                # print(revenue)
                revenue += float(row['sell_price'])
                revenue_rounded = round(revenue, 2)
    return revenue_rounded


def create_data_for_csv_files_bought_and_sold(
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
):
    '''
        Goal: create testdata for bought.csv and sold.csv. 
        # part 1 of 2: create testdata for bought.csv
        # part 2 of 2: create testdata for sold.csv

        fn-parameters are not in a lookup-table / dictionary (e.g. config_variables = {} ), 
        because it could make parsing with argparse cli more difficult (not sure).

        This fn cannot be tested with pytest, because I use random.sample() in this fn.
    
    '''
    # PART 1 OF 2: create testdata for bought.csv: 
    # step 1: create id for each bought product: (e.g. b_1, b_2, b_3, etc):
    csv_file_bought_id = ''
    csv_file_bought_id = create_id_for_each_row_in_boughtcsv_while_script_generates_this_boughtcsv('b', 1) 

    # step 2: create list with products that are sold in supermarket:
    # rule: each product can only appear once in supermarket_products:    
    supermarket_products = list(set(['fish', 'rice', 'potato', 'quinoa', 'bread', 'carrot', 'chicken', 'beef', 'bulgur','tomato', 'lettuce', 'beans', 'cheese', 'apple', 'beetroot', 'kiwi', 'onion', 'eggs', 'banana', 'oats', 'milk', 'pasta']))
   
    # step 3: create random list with products that are sold in supermarket:
    # product = '' # prevent UnboundLocalError: local variable 'product' referenced before assignment
    products = random.sample(supermarket_products, product_range)
    

    price_per_unit = [0.50, 1.10, 1.40, 2.50, 3.10, 4.00, 5.20]

    # step 4: generate all possible combinations of products and price_per_unit:
    bought_products = (list(product(products, price_per_unit)))
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
    with open(path_to_file_bought_csv, 'w', newline='') as csvfile:    
        writer = csv.writer(csvfile)
        writer.writerow(['buy_id', 'product', 'buy_price', 'buy_date', 'expiry_date'])
        writer.writerows(products_with_bought_date) 
        # writerows() expects a list of lists.


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
    with open(path_to_file_sold_csv, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['sell_id', 'buy_id', 'sell_price', 'sell_date'])
        writer.writerows(products_with_sold_date) # note to self: writerows() expects a list of lists.

def create_id_for_each_row_in_boughtcsv_while_script_generates_this_boughtcsv(csv_file_name_first_letter, first_nr_in_range):
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
        '''
        note to self: nonlocal is keyword that allows 
        you to assign to variables in outer 
        (but non-global) scope.  
        jsComp: in javascript no kw nonlocal (nor a need to use such a kw in this situation).      
        '''
        count += 1
        return f"{csv_file_name_first_letter}_{count}"
    return counter

def create_id_with_unused_highest_sequence_nr_to_buy_product_as_superpy_user(path_to_id_with_highest_sequence_number):
    # uc: provide input for fn buy_product in directory utils.py
    # no other use cases. 

    '''
    The first buy_id that is used by superpy-user is generated by fn set_buy_id_in_file_id_to_use_in_fn_buy_product() in directory utils.py.
    
    '''

    '''
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

            id_parts = last_id_used_in_fn_buy_product.split("_")
            new_id_to_use_in_fn_buy_product = int(id_parts[1]) + 1
            new_id_to_use_in_fn_buy_product = "b_" + str(new_id_to_use_in_fn_buy_product)
            # print(new_id_to_use_in_fn_buy_product)
            file.seek(0)
        with open(path_to_id_with_highest_sequence_number, 'w', newline='') as file: 
            print(new_id_to_use_in_fn_buy_product)  
            file.write(new_id_to_use_in_fn_buy_product)
    except IOError:
        print("Error in fn create_id_with_unused_highest_sequence_nr()")
    return new_id_to_use_in_fn_buy_product





def generate_random_buy_date_for_buy_transaction_in_future_in_time_interval(interval_lower_boundary_year, 
                                                    interval_lower_boundary_month, 
                                                    interval_lower_boundary_day, 
                                                    nr_of_months_added_to_calculate_upper_boundary,
                                                    nr_of_weeks_added_to_calculate_upper_boundary,
                                                    nr_of_days_added_to_calculate_upper_boundary
                                                    ):
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


def get_highest_buy_id_after_running_script_to_create_mock_data_for_boughtcsv_and_soldcsv(path_to_csv_bought_file):
    '''
    At any moment in superpy-app via argparse cli a script can run that adds 
    new mock data to bought.csv and sold.csv. 
    At any moment in superpy-app via argparse cli a script can run to delete all
    data from bought.csv and sold.csv.
    see py super.py -h for more info.

    Next, a superpy-app user may want to buy a product (or more products). Before
    adding a new row to bought.csv, the fn below will check what the highest buy_id
    is in bought.csv. Then it will increment that buy_id with one.

    
    Code below expects first column in bought.csv to be buy_id with format 
    b_1, b_2, b_3, etc.  
    '''
    highest_buy_id = 'b_0' 
    with open(path_to_csv_bought_file, 'r') as file_object:
        reader = csv.reader(file_object)
        next(reader) # skip header row
        for row in reader:
            csv_column_1 = row[0] # ex: b_1, or: b_2, or: b_3, etc
            if int(csv_column_1.split('_')[1]) > int(highest_buy_id.split('_')[1]):
                highest_buy_id = csv_column_1
    return highest_buy_id


def get_path_to_directory_of_file(directory_of_file):
    # rule: directory_of_file must be unique inside project superpy.
    '''
        With os.walk() I can run pytest from anywhere inside project superpy, irrespective of my
        current working directory. 
        The cwd can be different each time I run pytest.  So without os.walk() syntax, as a consequence, 
        the actual result gets stored in a different directory each time I run pytest with a different 
        cwd. This messed up grabbing the file with the actual result (being txt-file system_data.txt or
        csv-file bought.csv or sold.csv, depending on the fn under test) as input for the file comparison
        with the file with the expected result.
        But with the current solution, the actual result is always stored in the directory of the testcase
        (e.g. fn_set_system_date_testcase_01.), nomatter what the cwd is :).  
    '''
    whereabouts_of_directory_of_file  = str(os.getcwd()) 
    path_to_directory_of_this_file = '' # prevent UnboundLocalError
    for root, dirs, files in os.walk(whereabouts_of_directory_of_file):
        for name in dirs:
            if name == directory_of_file: 
                path_to_directory_of_this_file = os.path.abspath(os.path.join(root, name))
                # print(os.path.abspath(os.path.join(root, name)))
                break # break coz I only want first (one and supposedly only) result.
    return path_to_directory_of_this_file


def get_path_to_file(directory_of_file, file_name_of_which_you_want_to_know_the_path):
    whereabouts_of_directory_of_file  = str(os.getcwd()) 
    path_to_directory_of_this_file = '' # prevent UnboundLocalError
    for root, dirs, files in os.walk(whereabouts_of_directory_of_file):
        for name in dirs:
            if name == directory_of_file: 
                path_to_directory_of_this_file = os.path.abspath(os.path.join(root, name))
                # print(os.path.abspath(os.path.join(root, name)))
                break # break coz I only want first (one and supposedly only) result.
    # print('path_to_directory_of_this_file:')
    # print(path_to_directory_of_this_file)
    path_to_file = os.path.join(path_to_directory_of_this_file, file_name_of_which_you_want_to_know_the_path ) # path to file 
    # print('path_to_file')
    # print(path_to_file)
    return path_to_file

def get_system_date(path_to_system_date):
    # system_date is datetime object, ex: '2020-01-01'
    # print(path_to_system_date)
    try:
        with open(path_to_system_date, 'r', newline='') as file:
            system_date = file.read()
            # print(system_date)
    except IOError:
        print("fn get_system_date: trying to get system_date. Plz investigate error.")
    return system_date

def sell_product(bought_product_id, 
                 price, 
                 sell_date, 
                 path_to_csv_bought_input_file, 
                 path_to_csv_bought_output_file):

    # more info: see comments in fn buy_product()
    '''
    About the input_file and output_file:
    when using superpy as user, input and output csv file are the same.
    Only when testing fn buy_product in pytest, input and output csv file are different.
    reason: when testing fn buy_product in pytest, I want to keep the csv-file with testdata intact.
    '''
    with open(path_to_csv_bought_input_file, 'r', newline='') as file: 
        #r+ == read and write. This makes the code below more compact. 
        # newline='' is necessary to avoid empty lines in csv-file.
        print('var file is an iterator obj:')
        print(file) # <_io.TextIOWrapper name='test_file.csv' mode='r+' encoding='cp1252'>
        print(type(file)) # <class '_io.TextIOWrapper'>
        # file is an iterator with strings as elements. (!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!)
        
        print('-----------------------------------')
        reader = csv.DictReader(file)
        print('var reader is an iterator obj:')
        print(reader) # <csv.DictReader object at 0x000002579966D600>
        print(type(reader)) # <class 'csv.DictReader'>
        # reader is an iterator with dictionaries as elements. (!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!)
        # an: so at this point you are still working with an iterator, not with a list.

        print('-----------------------------------')
        print('var reader.fieldnames is a list:')   
        print(reader.fieldnames) 
        print(type(reader.fieldnames)) # <class 'list'>

        print('-----------------------------------')
        print('list stuff:')
        print('convert iterator with dictionaries into list with dictionaries: ')
        rows = list(reader)
        # rows is a list with dictionaries as elements.

        # print(rows)
        print('type of rows:')
        print(type(rows))
        file.seek(0)

        # create sold_product_id:
        sold_product_id = bought_product_id.replace('b', 's')
    # choose between option 1 and 2 (COMMENT OUT THE UNUSED OPTION)
    # option1of2: this alternative in write-mode works
    with open(path_to_csv_bought_output_file, 'w', newline='') as file: 
        rows.append({'sell_id': sold_product_id, 'buy_id': bought_product_id, 'sell_price': price, 'sell_date': sell_date}) 
        writer = csv.DictWriter(file, fieldnames= reader.fieldnames)
        # Dictwriter is a class. writer is its instanciated obj.
        writer.writeheader()
        writer.writerows(rows)
        '''
            in this alternative rows is a list with dictionaries. 
            Apparently writerows() expects a list with dictionnaries to be passed as argument,
            in order to update csv-file test_file.csv.        
        '''

    # option 2of2: 
    '''
    problem with this alternative in append-mode: data gets added to the file with actual testresult. 
    So after each testrun the file with actual testresult gets longer and longer. So 2nd time 
    you run pytest (and 3rd, etc.) the testcases will fail! Solution: as postperation remove the 
    data that has been added to the actual testresult file during the testrun....I don't like this solution.
    '''
    # with open(path_to_csv_bought_output_file, 'a', newline='') as file:
    #     row = [id_of_row_in_csv_file_bought,product,price,buy_date,expiry_date]
    #     writer = csv.writer(file)
    #     writer.writerow(row)


def set_buy_id_after_running_script_to_create_mock_data_for_boughtcsv_and_soldcsv(buy_id, path_to_buy_id_file):
    # location of file: (...superpy\data_used_in_superpy\id_to_use_in_fn_buy_product.txt)
    # ex of buy_id: b_1, or: b_2, or: b_3, etc
    if buy_id == None: # if bought.csv is empty
        buy_id = 'b_1'
    try:
        with open(path_to_buy_id_file, 'w', newline='') as file:
            file.write(buy_id)
    except IOError:
        print("Inside fn set_system_date_to() --> Plz investigate IOError.  ")
    return buy_id

def set_system_date_to(system_date, path_to_system_date):
    # system_date is datetime object, ex: '2020-01-01'
    try:
        with open(path_to_system_date, 'w', newline='') as file:
            file.write(system_date)
    except IOError:
        print("Inside fn set_system_date_to() --> Plz investigate IOError.  ")
    return system_date

def set_system_date_to_OLD__DO_NOT_USE(system_date, path_to_system_date, system_date_file='system_date.txt'):
    # system_date is datetime object, ex: '2020-01-01'
    print('inside set_system_date_to()')
    print(path_to_system_date)
    
    # defensive programming: (over-engineering here?)
    # if not os.path.exists(path_to_system_date):
    #     os.makedirs(path_to_system_date)
    try:
        with open(os.path.join(path_to_system_date, system_date_file), 'w', newline='') as file:
            file.write(system_date)
            print('inside try')
    except IOError:
        print("Error: File is already / still open. Plz investigate.")
        file.close()
        print("status: File has been closed (as a work-around). But error must still be investigated.")
        with open(os.path.join(path_to_system_date, system_date_file), 'w', newline='') as file:
            file.write(system_date)
    return system_date

def show_csv_file_in_console_with_module_rich(path_to_csv_file):
    console = Console()
    table = Table(show_header=True, header_style="bold magenta")
    with open(path_to_csv_file, 'r') as file:
        csv_reader = csv.reader(file)
        header = next(csv_reader)  
        for column in header:
            table.add_column(column)
        for row in csv_reader:
            table.add_row(*row)
    console.print(table)

def time_travel_system_date_with_nr_of_days(
        nr_of_days_to_travel, 
        path_to_input_file, 
        path_to_output_file
    ):
    try:
        with open(path_to_input_file, 'r', newline='') as file:
            # read current system date from file in format YYYY-MM-DD. This
            # should be the only contents of the file. 
            current_system_date = file.readline().split(',')[0]
            print('current_system_date: ', current_system_date)
            file.seek(0)

        with open(path_to_output_file, 'w', newline='') as file:
            new_system_date = add_days_to_date(current_system_date, nr_of_days_to_travel)
            file.write(new_system_date)
            print('new_system_date: ', new_system_date)

    except IOError:
        print("Error: File is already / still open. Plz investigate.")
        file.close()
        print("status: File has been closed (as a work-around). But error must still be investigated.")
        with open(os.path.join(path_to_output_file), 'w', newline='') as file:
            file.write(current_system_date)
    # returning new_system_date for testing purposes only (returned value is not used in the code)    
    return new_system_date































import os
print(os.getcwd())

import site 
print(site.getsitepackages())



