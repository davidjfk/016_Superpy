import filecmp, os, sys
sys.path.append('c:\\dev\\pytWinc\\superpy')
sys.path.append('c:\\dev\\pytWinc\\superpy\\utils_superpy')
from utils.utils import get_path_to_directory_of_file, set_system_date_to

directory_of_testcase = "fn_set_system_date_testcases" 
path_to_directory_of_testcase = get_path_to_directory_of_file(directory_of_testcase)     

# actual results:
path_to_actual_testresults_directory = os.path.join(path_to_directory_of_testcase, 'actual_testresults')
path_to_file_with_actual_result_test_01 = os.path.join(path_to_actual_testresults_directory, 'actual_result_test_01.txt')
path_to_file_with_actual_result_test_02 = os.path.join(path_to_actual_testresults_directory, 'actual_result_test_02.txt')

# expected results:
path_to_expected_testresults_directory = os.path.join(path_to_directory_of_testcase, 'expected_testresults')
path_to_file_with_expected_result_01 = os.path.join(path_to_expected_testresults_directory,  'expected_result_test_01.txt')           
path_to_file_with_expected_result_02 = os.path.join(path_to_expected_testresults_directory,  'expected_result_test_02.txt')  

def test_01_set_system_date_to_a_value_equal_to_exected_testresult():
    filecmp.clear_cache()
    set_system_date_to('reset_data_of_previous_testrun_with_this_string', path_to_file_with_actual_result_test_01)
    set_system_date_to('2024-11-03', path_to_file_with_actual_result_test_01)
    assert filecmp.cmp(path_to_file_with_actual_result_test_01, path_to_file_with_expected_result_01, shallow=False)

def test_02_set_system_date_to_a_value_NOT_equal_to_exected_testresult():
    filecmp.clear_cache()
    set_system_date_to('reset_data_of_previous_testrun_with_this_string', path_to_file_with_actual_result_test_02)
    set_system_date_to('2020-01-02', path_to_file_with_actual_result_test_02)
    assert not filecmp.cmp(path_to_file_with_actual_result_test_02, path_to_file_with_expected_result_02, shallow=False)