import filecmp, os, sys
sys.path.append('c:\\dev\\pytWinc\\superpy')
sys.path.append('c:\\dev\\pytWinc\\superpy\\utils_superpy')
from utils.utils import sell_product_by_buy_id, get_path_to_directory_of_file

directory_of_testcase = "fn_sell_product_with_buy_id_testcases" 
path_to_directory_of_testcase = get_path_to_directory_of_file(directory_of_testcase)

# input test files:
path_to_file_bought_csv_test_01 = os.path.join(path_to_directory_of_testcase, "test_input", 'path_to_file_bought_csv_test_01.csv') 
path_to_file_sold_csv_test_01 = os.path.join(path_to_directory_of_testcase, "test_input", 'path_to_file_sold_csv_test_01.csv') 

path_to_file_bought_csv_test_02 = os.path.join(path_to_directory_of_testcase, "test_input", 'path_to_file_bought_csv_test_02.csv') 
path_to_file_sold_csv_test_02 = os.path.join(path_to_directory_of_testcase, "test_input", 'path_to_file_sold_csv_test_02.csv') 

# actual results:
path_to_actual_testresults_directory = os.path.join(path_to_directory_of_testcase, 'actual_testresults') 
path_to_file_with_actual_result_test_01 = os.path.join(path_to_actual_testresults_directory, 'actual_result_test_01.csv')
path_to_file_with_actual_result_test_02 = os.path.join(path_to_actual_testresults_directory, 'actual_result_test_02.csv')

# expected results:
path_to_file_with_expected_result_01 = os.path.join(path_to_directory_of_testcase, "expected_testresults",  'expected_result_test_01.csv') 
path_to_file_with_expected_result_02 = os.path.join(path_to_directory_of_testcase, "expected_testresults",  'expected_result_test_02.csv') 


def test_01_sell_1_product_happy_flow():
    filecmp.clear_cache()
    sell_product_by_buy_id("b_2", 4.6,"2023-10-10", path_to_file_sold_csv_test_01, path_to_file_with_actual_result_test_01, path_to_file_bought_csv_test_01)
    assert filecmp.cmp(path_to_file_with_actual_result_test_01, path_to_file_with_expected_result_01, shallow=False)


def test_02_sell_2_products_happy_flow():
    filecmp.clear_cache()
    sell_product_by_buy_id("b_1", 7.5,"2023-10-06", path_to_file_sold_csv_test_02, path_to_file_with_actual_result_test_02, path_to_file_bought_csv_test_02)
    sell_product_by_buy_id("b_3", 15.6,"2023-10-14", path_to_file_with_actual_result_test_02, path_to_file_with_actual_result_test_02, path_to_file_bought_csv_test_02)
    # actual result of first sell_product() call is input for second sell_product() call
    assert filecmp.cmp(path_to_file_with_actual_result_test_02, path_to_file_with_expected_result_02, shallow=False)