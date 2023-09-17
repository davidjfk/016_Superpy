import filecmp, os, sys
sys.path.append('c:\\dev\\pytWinc\\superpy')
sys.path.append('c:\\dev\\pytWinc\\superpy\\utils_superpy')
from utils_superpy.utils import calculate_profit_in_time_range_between_start_date_and_end_date_inclusive
from utils_superpy.utils import calculate_revenue_in_time_range_between_start_date_and_end_date_inclusive
from utils_superpy.utils import calculate_cost_in_time_range_between_start_date_and_end_date_inclusive
from utils_superpy.utils import get_path_to_directory_of_file

directory_of_testcase = "fn_calculate_profit_in_time_range_between_start_date_and_end_date_inclusive" 
path_to_directory_of_testcase = get_path_to_directory_of_file(directory_of_testcase)

# input test files:
path_to_input_file_revenue_test_01 = os.path.join(path_to_directory_of_testcase, "test_input", 'input_file_revenue_for_testcase_01.csv') 
path_to_input_file_cost_test_01 = os.path.join(path_to_directory_of_testcase, "test_input", 'input_file_cost_for_testcase_01.csv') 

path_to_input_file_revenue_test_02 = os.path.join(path_to_directory_of_testcase, "test_input", 'input_file_revenue_for_testcase_02.csv') 
path_to_input_file_cost_test_02 = os.path.join(path_to_directory_of_testcase, "test_input", 'input_file_cost_for_testcase_02.csv') 


def test_01_calculate_profit_in_time_range_between_start_date_and_end_date_inclusive_happy_flow():
    filecmp.clear_cache()
    start_date = "2023-10-05"
    end_date = "2023-10-25"
    expected_test_result = 37.2 # revenue: 78 ,  cost: 40.8  --> profit: 78 - 40.8 = 37.2
    actual_result = calculate_profit_in_time_range_between_start_date_and_end_date_inclusive(
        start_date, 
        end_date, 
        path_to_input_file_revenue_test_01,
        path_to_input_file_cost_test_01,
        calculate_revenue_in_time_range_between_start_date_and_end_date_inclusive=calculate_revenue_in_time_range_between_start_date_and_end_date_inclusive,
        calculate_cost_in_time_range_between_start_date_and_end_date_inclusive=calculate_cost_in_time_range_between_start_date_and_end_date_inclusive
        )
    assert actual_result == expected_test_result


def test_02_calculate_profit_in_time_range_between_start_date_and_end_date_inclusive_happy_flow():
    filecmp.clear_cache()
    start_date = "2023-10-14"
    end_date = "2023-10-26"
    expected_test_result = -2.7 # revenue: 49 , cost: 51.7 --> profit: 49 - 51.7 = -2.7
    actual_result = calculate_profit_in_time_range_between_start_date_and_end_date_inclusive(
        start_date, 
        end_date, 
        path_to_input_file_revenue_test_02,
        path_to_input_file_cost_test_02,
        calculate_revenue_in_time_range_between_start_date_and_end_date_inclusive=calculate_revenue_in_time_range_between_start_date_and_end_date_inclusive,
        calculate_cost_in_time_range_between_start_date_and_end_date_inclusive=calculate_cost_in_time_range_between_start_date_and_end_date_inclusive
        )
    assert actual_result == expected_test_result


