import filecmp, os, sys
sys.path.append('c:\\dev\\pytWinc\\superpy')
sys.path.append('c:\\dev\\pytWinc\\superpy\\utils_superpy')
from utils_superpy.utils import calculate_revenue_in_time_range_between_start_date_and_end_date_inclusive, get_path_to_directory_of_file

directory_of_testcase = "fn_calculate_revenue_in_time_range_between_start_date_and_end_date_inclusive" 
path_to_directory_of_testcase = get_path_to_directory_of_file(directory_of_testcase)

# input test files:
path_to_input_file_test_01 = os.path.join(path_to_directory_of_testcase, "test_input", 'input_file_for_testcase_01.csv') 
path_to_input_file_test_02 = os.path.join(path_to_directory_of_testcase, "test_input", 'input_file_for_testcase_02.csv') 

def test_01_calculate_revenue_in_time_range_between_start_date_and_end_date_inclusive_happy_flow():
    filecmp.clear_cache()
    start_date = "2023-10-09"
    end_date = "2023-10-18"
    expected_test_result = 12.6
    actual_result = calculate_revenue_in_time_range_between_start_date_and_end_date_inclusive(start_date, end_date, path_to_input_file_test_01)
    assert actual_result == expected_test_result


def test_02_calculate_revenue_in_time_range_between_start_date_and_end_date_inclusive_happy_flow():
    filecmp.clear_cache()
    start_date = "2023-09-01"
    end_date = "2023-12-31"
    expected_test_result = 106.5
    actual_result = calculate_revenue_in_time_range_between_start_date_and_end_date_inclusive(start_date, end_date, path_to_input_file_test_02)
    assert actual_result == expected_test_result


