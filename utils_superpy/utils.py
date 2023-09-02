
# list of imports:
import os
import datetime
import random
from datetime import date, datetime, timedelta


# list of functions:
# add_days_to_date(date_string, days_to_add)
# generate_random_date_in_future_in_time_interval_of_2_months()
# make_id_for_each_row_in_csv_file(csv_file_name_first_letter, first_nr_in_range):
# set_system_date_to(system_date, path_to_system_date, system_date_file='system_date.txt'): (created in TDD fashion)




# time_travel_to_date(date_to_travel_to) (2do)

def add_days_to_date(date_string, days_to_add):
    date = datetime.strptime(date_string, '%Y-%m-%d')
    new_date = date + timedelta(days= days_to_add)
    print(new_date)
    return new_date.strftime('%Y-%m-%d')

def generate_random_date_in_future_in_time_interval_of_2_months():
    today = date(3333, 3, 1)
    start_date = today.replace(day=1)
    end_date = start_date.replace(month=start_date.month+2)
    time_between_dates = end_date - start_date
    days_between_dates = time_between_dates.days
    random_number_of_days = random.randrange(days_between_dates)
    random_date = start_date + timedelta(days=random_number_of_days)
    return random_date.strftime('%Y-%m-%d')


def make_id_for_each_row_in_csv_file(csv_file_name_first_letter, first_nr_in_range):
    ''' 
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
        jsComp: no kw nonlocal in javascript.      
        '''
        count += 1
        return f"{csv_file_name_first_letter}_{count}"
    return counter


def set_system_date_to(system_date, path_to_system_date, system_date_file='system_date.txt'):
    # system_date is datetime object, ex: '2020-01-01'
    print('inside set_system_date_to()')
    print(path_to_system_date)
    
    # defensive programming: (over-engineering here?)
    if not os.path.exists(path_to_system_date):
        os.makedirs(path_to_system_date)
    
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
        path_to_directory_that_contains_file_with_new_system_date, 
        path_to_directory_that_contains_file_with_current_system_date = "production_env", 
        system_date_input_file='system_date.txt', 
        system_date_output_file='system_date.txt'
    ):
    '''
    When using this fn, you need a value for the first 2 arguments ONLY.
    When testing this fn, you need a value for the first 4 arguments.
    Fn-argument 5 has default value to use for both. It is an argument
    only to prevent fn-side-effects. 

    All variables are strings, except nr_of_days_to_travel, which is int.
    '''
    # nr of days is int, ex: 1
    print('inside time_travel_system_date_with_nr_of_days()') 
    print(f'path_to_system_date_output', path_to_directory_that_contains_file_with_new_system_date)
    print(f'path_to_directory_that_contains_file_with_current_system_date', path_to_directory_that_contains_file_with_current_system_date)

    # defensive programming: (over-engineering here?)
    if not os.path.exists(path_to_directory_that_contains_file_with_new_system_date):
        os.makedirs(path_to_directory_that_contains_file_with_new_system_date)

    try:
        # read current system date from file:
        if path_to_directory_that_contains_file_with_current_system_date == "production_env": 
            print('production env:')
            path_to_directory_that_contains_file_with_current_system_date = path_to_directory_that_contains_file_with_new_system_date
        else:
            print('pytest "test" env:')
            print(path_to_directory_that_contains_file_with_current_system_date)
        # else: ... path_to_directory_that_contains_file_with_current_system_date points to a directory inside directory test_utils with a pytest testcase. 

        with open(os.path.join(path_to_directory_that_contains_file_with_current_system_date, system_date_input_file), 'r', newline='') as file:
            # read current system date from file: the  only contents should be a date in format YYYY-MM-DD:
            current_system_date = file.readline().split(',')[0]
            print('current_system_date: ', current_system_date)
            file.seek(0)

        # write new system date to file:
        with open(os.path.join(path_to_directory_that_contains_file_with_new_system_date, system_date_output_file), 'w', newline='') as file:
            new_system_date = add_days_to_date(current_system_date, nr_of_days_to_travel)
            file.write(new_system_date)
            print('new_system_date: ', new_system_date)

    except IOError:
        print("Error: File is already / still open. Plz investigate.")
        # file.close()
        print("status: File has been closed (as a work-around). But error must still be investigated.")
        # with open(os.path.join(path_to_system_date_output, system_date_file), 'w', newline='') as file:
        #     file.write(current_system_date)

    # returning new_system_date for testing purposes only (returned value is not used in the code)    
    return new_system_date


   























import os
print(os.getcwd())

import site 
print(site.getsitepackages())



