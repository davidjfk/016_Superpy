import os, sys
'''
# step: to get this script  to work, add path to directory 'superpy' to the PYTHONPATH environment variable:
# sys.path.append('c:\\dev\\pytWinc\\superpy') --> caveat: this code will break on another machine: absolute file path and backslashes.

chicken-and-egg problem while trying to solve this caveat: 
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
from utils.utils import add_days_to_date
from utils.utils import generate_random_buy_date_for_buy_transaction_in_future_in_time_interval
from utils.utils import create_buy_id_for_each_row_in_boughtcsv_as_part_of_mockdata_that_is_being_created
from utils.utils import get_path_to_directory_of_file

from utils.utils import create_data_for_csv_files_bought_and_sold


from data_used_in_superpy.product_prices import superpy_product_prices
from data_used_in_superpy.product_range import superpy_product_range


def main():
    
    # CONFIGURATION:
    # to create testdata for bought.csv and sold.csv configure following variables to your liking:
    product_range = 9
    # see produt_range definition in README_SOFTWARE_DESIGN.md --> ch definitions. 

    delete_every_nth_row_in_soldcsv_so_every_nth_row_in_boughtcsv_can_expire_when_time_travelling = 3

    shelf_life = 15
    # see shelf_life definition in README_SOFTWARE_DESIGN.md --> ch definitions.

    turnover_time = 4
    # see turnover_time definition in README_SOFTWARE_DESIGN.md --> ch definitions.
    
    markup = 5
    # see markup definition in README_SOFTWARE_DESIGN.md --> ch definitions.

    # see time_interval definition in README_SOFTWARE_DESIGN.md --> ch definitions:
    lower_boundary_year_of_time_interval_in_which_to_create_random_testdata = 2024
    lower_boundary_month_of_time_interval_in_which_to_create_random_testdata = 1
    lower_boundary_week_of_time_interval_in_which_to_create_random_testdata = 1
    upper_boundary_nr_of_months_to_add_to_calculate = 6
    upper_boundary_nr_of_weeks_to_add_to_calculate = 0
    upper_boundary_nr_of_days_to_add_to_calculate = 0
    # <end of CONFIGURATION>



    # pitfall / warning: as a Superpy-user, plz do NOT assign other values to the following variables:
    # set path to file bought.csv:
    path_to_directory_testdata = ''
    path_to_directory_testdata = get_path_to_directory_of_file('testdata')
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
        superpy_product_prices,
        superpy_product_range,
        path_to_file_bought_csv,
        path_to_file_sold_csv,
        add_days_to_date,
        create_buy_id_for_each_row_in_boughtcsv_as_part_of_mockdata_that_is_being_created,
        generate_random_buy_date_for_buy_transaction_in_future_in_time_interval
    )

if __name__ == '__main__':
    main()