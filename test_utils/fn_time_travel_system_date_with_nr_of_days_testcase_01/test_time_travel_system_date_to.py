

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


# path_to_file_with_actual_testresult is the SAME var for all testcases: (I can reuse this location)
path_to_directory_that_contains_file_with_new_system_date = os.path.join(path_to_directory_of_testcase, 'actual_testresult') 
path_to_file_with_actual_testresult = os.path.join(path_to_directory_that_contains_file_with_new_system_date, 'system_date.txt') # path to file 



path_to_test_input_file1 = os.path.join(path_to_directory_of_testcase, "test_input", 'system_date_input_for_test01.txt') # path to file
'''
    weird: somehow pytest cannot run 3 testcases below together, if all 3 testcases use the same var
    'path_to_test_input_file' eventhough in each testcase this var points to a different file... not sure why.
    work-around: each testcase gets its own unique name. 
'''
path_to_file_with_expected_testresult = os.path.join(path_to_directory_of_testcase, "expected_testresult",  'expected_testresult_system_date_testcase_01.txt') 

def test_01_time_travel_to_the_future():
    filecmp.clear_cache()
    time_travel_system_date_with_nr_of_days(5, path_to_test_input_file1, path_to_file_with_actual_testresult)
    assert filecmp.cmp(path_to_file_with_actual_testresult, path_to_file_with_expected_testresult, shallow=False)
    filecmp.clear_cache()




path_to_test_input_file2 = os.path.join(path_to_directory_of_testcase, "test_input", 'system_date_input_for_test02.txt') # path to file
path_to_file_with_expected_testresult = os.path.join(path_to_directory_of_testcase, "expected_testresult", 'expected_testresult_system_date_testcase_02.txt') 

def test_02_time_travel_to_the_future_actual_result_not_same_as_expected_result():
    filecmp.clear_cache()
    time_travel_system_date_with_nr_of_days(4, path_to_test_input_file2, path_to_file_with_actual_testresult)
    assert not filecmp.cmp(path_to_file_with_actual_testresult, path_to_file_with_expected_testresult, shallow=False)
    filecmp.clear_cache()



path_to_test_input_file3 = os.path.join(path_to_directory_of_testcase, "test_input", 'system_date_input_for_test03.txt') # path to file
path_to_file_with_expected_testresult = os.path.join(path_to_directory_of_testcase, "expected_testresult", 'expected_testresult_system_date_testcase_03.txt') 

def test_03_time_travel_to_the_future_actual_result_not_same_as_expected_result():
    filecmp.clear_cache()
    time_travel_system_date_with_nr_of_days(7, path_to_test_input_file3, path_to_file_with_actual_testresult)
    assert filecmp.cmp(path_to_file_with_actual_testresult, path_to_file_with_expected_testresult, shallow=False)
    filecmp.clear_cache()



