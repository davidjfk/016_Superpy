

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


          
actual_testresult_path = os.path.join(path_to_directory_of_testcase, 'actual_testresult_directory')
actual_testresult = os.path.join(actual_testresult_path, 'system_date.txt')

expected_testresult = os.path.join(path_to_directory_of_testcase,  'expected_testresult_system_date.txt') 


def test_time_travel_to_the_future():
    filecmp.clear_cache()
    time_travel_system_date_with_nr_of_days(5, actual_testresult_path, path_to_directory_of_testcase)
    assert filecmp.cmp(actual_testresult, expected_testresult, shallow=False)

def test_time_travel_to_the_future_actual_result_not_same_as_expected_result():
    filecmp.clear_cache()
    time_travel_system_date_with_nr_of_days(4, actual_testresult_path, path_to_directory_of_testcase)
    assert not filecmp.cmp(actual_testresult, expected_testresult, shallow=False)

# def test_time_travel_to_the_future():
#     filecmp.clear_cache()
#     time_travel_system_date_with_nr_of_days('reset_data_of_previous_testrun_with_this_string', actual_testresult_path)
#     time_travel_system_date_with_nr_of_days('20', actual_testresult_path)
#     assert not filecmp.cmp(actual_testresult, expected_testresult, shallow=False)



