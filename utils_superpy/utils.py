
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
    new_date = date + timedelta(days=days_to_add)
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
    pass

























import os
print(os.getcwd())

import site 
print(site.getsitepackages())



