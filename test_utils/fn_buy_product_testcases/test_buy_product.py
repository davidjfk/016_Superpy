import filecmp, os, sys
sys.path.append('c:\\dev\\pytWinc\\superpy')
sys.path.append('c:\\dev\\pytWinc\\superpy\\utils_superpy')
from utils.utils import buy_product, get_path_to_directory_of_file

directory_of_testcase = "fn_buy_product_testcases" 
path_to_directory_of_testcase = get_path_to_directory_of_file(directory_of_testcase)

# input test files:
path_to_input_file_test_01 = os.path.join(path_to_directory_of_testcase, "test_input", 'input_file_for_testcase_01.csv') 
path_to_input_file_test_02 = os.path.join(path_to_directory_of_testcase, "test_input", 'input_file_for_testcase_02.csv') 

# actual results:
path_to_actual_testresults_directory = os.path.join(path_to_directory_of_testcase, 'actual_testresults') 
path_to_file_with_actual_result_test_01 = os.path.join(path_to_actual_testresults_directory, 'actual_result_test_01.csv')
path_to_file_with_actual_result_test_02 = os.path.join(path_to_actual_testresults_directory, 'actual_result_test_02.csv')

# expected results:
path_to_file_with_expected_result_01 = os.path.join(path_to_directory_of_testcase, "expected_testresults",  'expected_result_test_01.csv') 
path_to_file_with_expected_result_02 = os.path.join(path_to_directory_of_testcase, "expected_testresults",  'expected_result_test_02.csv') 


def test_01_buy_product():
    filecmp.clear_cache()
    buy_product("apple", 0.25,"3333-03-07","3333-03-17", "b_301", path_to_input_file_test_01, path_to_file_with_actual_result_test_01)
    assert filecmp.cmp(path_to_file_with_actual_result_test_01, path_to_file_with_expected_result_01, shallow=False)


def test_02_buy_product():
    filecmp.clear_cache()
    buy_product("orange", 0.75,"3333-04-22","3333-04-28", "b_301", path_to_input_file_test_02, path_to_file_with_actual_result_test_02)
    buy_product("cabbage", 1.20,"3333-04-23","3333-04-30", "b_302", path_to_file_with_actual_result_test_02, path_to_file_with_actual_result_test_02)
    # output of first fn call is input to second fn call.
    assert filecmp.cmp(path_to_file_with_actual_result_test_02, path_to_file_with_expected_result_02, shallow=False)