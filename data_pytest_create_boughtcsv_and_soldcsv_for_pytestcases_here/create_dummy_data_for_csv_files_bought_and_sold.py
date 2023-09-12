import os, sys


# Add path to directory 'superpy' to the PYTHONPATH environment variable:
# sys.path.append('c:\\dev\\pytWinc\\superpy') --> this code will break on another machine: absolute file path and backslashes.
'''
chicken-and-egg problem: 
    To make path to directory 'superpy' relative, I need to import fn get_path_to_directory_of_file from utils.py.
    To import fn get_path_to_directory_of_file from utils.py, I need to add path to directory 'superpy' to the PYTHONPATH environment variable.
'''
# solution for chicken-and-egg problem:
current_dir  = (os.getcwd()) # e.g. C:\dev\pytWinc\superpy\testdata
parent_directory_of_current_directory = os.path.abspath(os.path.join(current_dir, os.pardir)) # e.g. C:\dev\pytWinc\superpy
# (on every machine, the parent directory of current directory is the project directory superpy)
file_path_to_directory_superpy =  parent_directory_of_current_directory
sys.path.append(file_path_to_directory_superpy)

# the following 4 imported fns are arguments in fn create_data_for_csv_files_bought_and_sold() below.
from utils_superpy.utils import add_days_to_date, generate_random_date_in_future_in_time_interval
from utils_superpy.utils import get_path_to_directory_of_file, make_id_for_each_row_in_csv_file

from utils_superpy.utils import create_data_for_csv_files_bought_and_sold

def main():
    '''
        Option: I could put all variables below in a lookup-table / dictionary (e.g. config_variables = {},
        but that might make parding the arguments of fn create_data_for_csv_files_bought_and_sold() 
        more difficult. So I decided to leave the variables below as is.
    '''

    # before run fn create_data_for_csv_files_bought_and_sold below, overwrite the following 
    # config variables to your liking:
    nr_of_products_in_supermarket = 4
    '''
    set nr of products in supermarket:
    This variable is an operand in fn product from module itertools.
    So more products leads to more rows in bought.csv and less products to less rows in bought.csv.
    '''

    delete_every_nth_row = 2
    '''
    set nr of rows to delete from sold.csv:
    sold.csv is as a copy of bought.csv. After making the deepcopy, a few changes are made: 
    e.g. make sell_price different (higher) than buy_price, but also delete some rows. 
    Rows that are present in bought.csv, but not in sold.csv, will expire while time traveling.
    (e.g. if delete_every_nth_row = 2, then every 2nd row will be deleted)
    (e.g. if delete_every_nth_row = 3, then every 3rd row will be deleted)
    '''
    # set nr of days between buying and selling a product:
    number_of_days_between_buying_and_selling_a_product = 2

    # set nr of days between buying a product and its expiry date:
    nr_of_days_between_buying_a_product_and_its_expiry_date = 5

    # set price margin for selling a product: 
    # (e.g. if buying price is 3 euro and selling price is 12 euro, then margin is 4)
    # (e.g. if buying price is 2 euro and selling price is 3 euro, then margin is 1.5)
    price_margin_as_mulitplication_factor = 3

    # timespan of application is 2 months:
    '''
        (e.g. if today is 1 january 2021, then timespan is 1 january 2021 to 1 march 2021)
        to change the timespan, goto utils.py and adjust fn generate_random_date_in_future_in_time_interval_of_2_months()
        (there is no need to, just for future reference)
    '''

    # time_interval_in_which_to_create_random_testdata:
    lower_year_of_time_interval_in_which_to_create_random_testdata = 2023
    lower_month_of_time_interval_in_which_to_create_random_testdata = 10
    lower_week_of_time_interval_in_which_to_create_random_testdata = 1
    nr_of_months_to_add_to_calculate_upper_boundary = 2
    nr_of_weeks_to_add_to_calculate_upper_boundary = 0
    nr_of_days_to_add_to_calculate_upper_boundary = 0

    # set path to file bought.csv:
    path_to_directory_testdata = ''
    path_to_directory_testdata = get_path_to_directory_of_file('testdata')
    path_to_file_bought_csv = os.path.join(path_to_directory_testdata, 'bought.csv')

    # set path to file sold.csv:
    path_to_file_sold_csv = os.path.join(path_to_directory_testdata, 'sold.csv')

    create_data_for_csv_files_bought_and_sold(
        nr_of_products_in_supermarket,
        delete_every_nth_row,
        nr_of_days_between_buying_a_product_and_its_expiry_date,
        number_of_days_between_buying_and_selling_a_product,
        price_margin_as_mulitplication_factor,
        lower_year_of_time_interval_in_which_to_create_random_testdata,
        lower_month_of_time_interval_in_which_to_create_random_testdata,
        lower_week_of_time_interval_in_which_to_create_random_testdata,
        nr_of_months_to_add_to_calculate_upper_boundary,
        nr_of_weeks_to_add_to_calculate_upper_boundary,
        nr_of_days_to_add_to_calculate_upper_boundary,
        path_to_file_bought_csv,
        path_to_file_sold_csv,
        add_days_to_date,
        make_id_for_each_row_in_csv_file,
        generate_random_date_in_future_in_time_interval
    )

 

if __name__ == '__main__':
    main()