

import filecmp, os, sys
sys.path.append('c:\\dev\\pytWinc\\superpy')
sys.path.append('c:\\dev\\pytWinc\\superpy\\utils_superpy')
from utils_superpy.utils import time_travel_system_date_with_nr_of_days

whereabouts_of_directory_of_testcase  = str(os.getcwd()) 
directory_of_testcase = "fn_time_travel_system_date_with_nr_of_days_testcase_01" 
for root, dirs, files in os.walk(whereabouts_of_directory_of_testcase):
    for name in dirs:
        if name == directory_of_testcase: 
            path_to_directory_of_testcase = os.path.abspath(os.path.join(root, name))
            print(os.path.abspath(os.path.join(root, name)))
            break # break coz I only want first (one and supposedly only) result.

# make dynamic (i.e. each testcase its own file with its own data):
# by (my) convention, I put the files with the current system dates in the directory of the testcase.
path_to_directory_that_contains_file_with_current_system_date = path_to_directory_of_testcase 

path_to_directory_that_contains_file_with_new_system_date = os.path.join(path_to_directory_that_contains_file_with_current_system_date, 'actual_testresult') # path to directory
actual_testresult = os.path.join(path_to_directory_that_contains_file_with_new_system_date, 'system_date.txt') # path to file 



# make dynamic (i.e. each testcase its own file with its own data):
expected_testresult = os.path.join(path_to_directory_of_testcase,  'expected_testresult_system_date.txt') 


def test_01_time_travel_to_the_future():
    filecmp.clear_cache()
    time_travel_system_date_with_nr_of_days(5, path_to_directory_that_contains_file_with_new_system_date, path_to_directory_that_contains_file_with_current_system_date, "system_date_input_for_test01.txt")
    assert filecmp.cmp(actual_testresult, expected_testresult, shallow=False)

def test_02_time_travel_to_the_future_actual_result_not_same_as_expected_result():
    filecmp.clear_cache()
    time_travel_system_date_with_nr_of_days(4, path_to_directory_that_contains_file_with_new_system_date, path_to_directory_that_contains_file_with_current_system_date, "system_date_input_for_test02.txt")
    assert not filecmp.cmp(actual_testresult, expected_testresult, shallow=False)


def test_03_time_travel_to_the_future_actual_result_not_same_as_expected_result():
    filecmp.clear_cache()
    time_travel_system_date_with_nr_of_days(16, path_to_directory_that_contains_file_with_new_system_date, path_to_directory_that_contains_file_with_current_system_date, "system_date_input_for_test03.txt")
    assert filecmp.cmp(actual_testresult, expected_testresult, shallow=False)



