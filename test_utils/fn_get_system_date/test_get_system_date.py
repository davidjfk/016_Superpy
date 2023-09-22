import filecmp, os, sys
sys.path.append('c:\\dev\\pytWinc\\superpy')
sys.path.append('c:\\dev\\pytWinc\\superpy\\utils_superpy')
from utils_superpy.utils import get_system_date, get_path_to_directory_of_file

directory_of_testcase = "fn_get_system_date" 
path_to_directory_of_testcase = get_path_to_directory_of_file(directory_of_testcase)

# input test files:
path_to_input_file_test_01 = os.path.join(path_to_directory_of_testcase, "test_input", 'input_file_for_testcase_01.txt') 
path_to_input_file_test_02 = os.path.join(path_to_directory_of_testcase, "test_input", 'input_file_for_testcase_02.txt') 

def test_01_calculate_sales_volume_in_time_range_between_start_date_and_end_date_inclusive_happy_flow():
    filecmp.clear_cache()
    expected_test_result = '2024-10-31'
    actual_result = get_system_date( path_to_input_file_test_01)
    assert actual_result == expected_test_result


def test_02_calculate_sales_volume_in_time_range_between_start_date_and_end_date_inclusive_happy_flow():
    filecmp.clear_cache()
    expected_test_result = '2025-11-26' 
    actual_result = get_system_date(path_to_input_file_test_02)
    assert actual_result == expected_test_result

