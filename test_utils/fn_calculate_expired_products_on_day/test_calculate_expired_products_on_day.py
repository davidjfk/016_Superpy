import filecmp, os, sys
sys.path.append('c:\\dev\\pytWinc\\superpy')
sys.path.append('c:\\dev\\pytWinc\\superpy\\utils_superpy')
from utils_superpy.utils import calculate_expired_products_on_day, get_path_to_directory_of_file

directory_of_testcase = "fn_calculate_expired_products_on_day" 
path_to_directory_of_testcase = get_path_to_directory_of_file(directory_of_testcase)

# input test files:
path_to_input_file_sold_test_01 = os.path.join(path_to_directory_of_testcase, "test_input", 'input_file_sold_for_testcase_01.csv') 
path_to_input_file_cost_test_01 = os.path.join(path_to_directory_of_testcase, "test_input", 'input_file_cost_for_testcase_01.csv') 

path_to_input_file_sold_test_02 = os.path.join(path_to_directory_of_testcase, "test_input", 'input_file_sold_for_testcase_02.csv') 
path_to_input_file_cost_test_02 = os.path.join(path_to_directory_of_testcase, "test_input", 'input_file_cost_for_testcase_02.csv') 



'''
about the data structure of expected testresult:
list of lists is a common and convenient (but not the only) way to create tables in Python.
This also applies to Rich.

So expected test results take the shape of a list with lists. 
'''


def test_01_calculate_expired_products_on_day_happy_flow():
    filecmp.clear_cache()
    date_on_which_to_calculate_expired_products = '2023-10-10'
    expected_test_result = [['b_3', 'kiwi', '5.2', '2023-09-19', '2023-09-29'], ['b_6', 'kiwi', '1.4', '2023-09-29', '2023-10-09']]
    actual_result = calculate_expired_products_on_day(date_on_which_to_calculate_expired_products, path_to_input_file_sold_test_01,
    path_to_input_file_cost_test_01)
    assert actual_result == expected_test_result


def test_02_calculate_expired_products_on_day_happy_flow():
    filecmp.clear_cache()
    date_on_which_to_calculate_expired_products = '2023-11-22'
    expected_test_result = [['b_2', 'oats', '1.1', '2023-10-05', '2023-10-20'], ['b_4', 'cheese', '3.1', '2023-10-14', '2023-10-29'], ['b_6', 'oats', '5.2', '2023-10-17', '2023-11-01'], ['b_8', 'banana', '1.1', '2023-10-19', '2023-11-03'], ['b_10', 'beetroot', '1.4', '2023-10-21', '2023-11-05'], ['b_12', 'rice', '3.1', '2023-10-21', '2023-11-05'], ['b_14', 'rice', '4.0', '2023-10-22', '2023-11-06'], ['b_16', 'tomato', '1.1', '2023-10-24', '2023-11-08'], ['b_18', 'beetroot', '2.5', '2023-10-27', '2023-11-11'], ['b_20', 'cheese', '1.1', '2023-10-28', '2023-11-12'], ['b_22', 'cheese', '4.0', '2023-10-30', '2023-11-14'], ['b_24', 'tomato', '3.1', '2023-10-30', '2023-11-14'], ['b_26', 'tomato', '2.5', '2023-10-31', '2023-11-15'], ['b_28', 'lettuce', '0.5', '2023-11-01', '2023-11-16'], ['b_30', 'lettuce', '4.0', '2023-11-02', '2023-11-17'], ['b_32', 'tomato', '5.2', '2023-11-03', '2023-11-18'], ['b_34', 'potato', '4.0', '2023-11-06', '2023-11-21']]
    actual_result = calculate_expired_products_on_day(date_on_which_to_calculate_expired_products, path_to_input_file_sold_test_02,
    path_to_input_file_cost_test_02)
    assert actual_result == expected_test_result

