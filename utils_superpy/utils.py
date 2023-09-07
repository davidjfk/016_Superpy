
# list of imports:
import os, sys, csv
import datetime
import random
from datetime import date, datetime, timedelta


# list of functions:
# add_days_to_date(date_string, days_to_add)
# buy_product(product,price,buy_date,expiry_date,id_of_row_in_csv_file_bought,path_to_csv_bought_input_file,path_to_csv_bought_output_file):
# create_id_with_unused_highest_sequence_nr_to_buy_product(path_to_id_with_highest_sequence_number):
# generate_random_date_in_future_in_time_interval_of_2_months()
# get_path_to_file(directory_of_file, file_name_of_which_you_want_to_know_the_path):
# make_id_for_each_row_in_csv_file(csv_file_name_first_letter, first_nr_in_range):
# set_system_date_to(system_date, path_to_system_date, system_date_file='system_date.txt'): (created in TDD fashion)
# time_travel_system_date_with_nr_of_days(nr_of_days_to_travel, path_to_input_file, path_to_output_file):


def add_days_to_date(date_string, days_to_add):
    date = datetime.strptime(date_string, '%Y-%m-%d')
    new_date = date + timedelta(days= days_to_add)
    print(new_date)
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
        rows.append({'id': id_of_row_in_csv_file_bought, 'product': product, 'price': price, 'buy_date': buy_date, 'expiry_date': expiry_date}) 
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

def create_id_with_unused_highest_sequence_nr_to_buy_product(path_to_id_with_highest_sequence_number):
    # uc: provide input for fn buy_product in directory utils.py
    # no other use cases. 
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

def generate_random_date_in_future_in_time_interval_of_2_months():
    today = date(3333, 3, 1)
    start_date = today.replace(day=1)
    end_date = start_date.replace(month=start_date.month+2)
    time_between_dates = end_date - start_date
    days_between_dates = time_between_dates.days
    random_number_of_days = random.randrange(days_between_dates)
    random_date = start_date + timedelta(days=random_number_of_days)
    return random_date.strftime('%Y-%m-%d')

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
    for root, dirs, files in os.walk(whereabouts_of_directory_of_file):
        for name in dirs:
            if name == directory_of_file: 
                path_to_directory_of_this_file = os.path.abspath(os.path.join(root, name))
                print(os.path.abspath(os.path.join(root, name)))
                break # break coz I only want first (one and supposedly only) result.
    return path_to_directory_of_this_file


def get_path_to_file(directory_of_file, file_name_of_which_you_want_to_know_the_path):
    whereabouts_of_directory_of_file  = str(os.getcwd()) 
    path_to_directory_of_this_file = ''
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
    print(path_to_system_date)
    try:
        with open(path_to_system_date, 'r', newline='') as file:
            system_date = file.read()
            print(system_date)
    except IOError:
        print("fn get_system_date: trying to get system_date. Plz investigate error.")
    return system_date

def make_id_for_each_row_in_csv_file(csv_file_name_first_letter, first_nr_in_range):
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



