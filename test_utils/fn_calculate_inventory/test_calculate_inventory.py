import filecmp, os, sys
sys.path.append('c:\\dev\\pytWinc\\superpy')
sys.path.append('c:\\dev\\pytWinc\\superpy\\utils_superpy')
from utils.utils import calculate_inventory, get_path_to_directory_of_file

directory_of_testcase = "fn_calculate_inventory" 
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

So expected test results take the shape of a list with lists. This has worked
while testing fn calculate_expired_products_on_day.
'''


def test_01_calculate_inventory_happy_flow():
    filecmp.clear_cache()
    date_on_which_to_calculate_inventory = '2024-05-21'
    expected_test_result = [['b_3', 'candle', '3.1', '2024-01-11', 'does not expire'], ['b_6', 'book', '0.5', '2024-01-15', 'does not expire'], ['b_39', 'skeelers', '1.1', '2024-04-20', 'does not expire'], ['b_45', 'shoes', '1.4', '2024-04-30', 'does not expire'], ['b_48', 'fish', '2.5', '2024-05-08', '2024-05-23'], ['b_51', 'kiwi', '0.5', '2024-05-15', '2024-05-30'], ['b_54', 'onion', '1.1', '2024-05-21', '2024-06-05']]
    actual_result = calculate_inventory(date_on_which_to_calculate_inventory, path_to_input_file_sold_test_01,
    path_to_input_file_cost_test_01)
    assert actual_result == expected_test_result


def test_02_calculate_inventory_happy_flow():
    filecmp.clear_cache()
    date_on_which_to_calculate_inventory = '2023-11-15'
    expected_test_result = [['b_6', 'garbage_bag', '5.2', '2023-10-17', 'does not expire'], ['b_26', 'tomato', '2.5', '2023-10-31', '2023-11-15'], ['b_28', 'lettuce', '0.5', '2023-11-01', '2023-11-16'], ['b_30', 'lettuce', '4.0', '2023-11-02', '2023-11-17'], ['b_32', 'tomato', '5.2', '2023-11-03', '2023-11-18'], ['b_34', 'lightbulb', '4.0', '2023-11-06', 'does not expire'], ['b_36', 'tomato', '4.0', '2023-11-07', '2023-11-22'], ['b_38', 'rice', '0.5', '2023-11-08', '2023-11-23'], ['b_40', 'cheese', '1.4', '2023-11-09', '2023-11-24'], ['b_42', 'book', '5.2', '2023-11-11', 'does not expire'], 
    ['b_44', 'oats', '0.5', '2023-11-14', '2023-11-29']]
    actual_result = calculate_inventory(date_on_which_to_calculate_inventory, path_to_input_file_sold_test_02,
    path_to_input_file_cost_test_02)
    assert actual_result == expected_test_result

