

import filecmp, os, sys
sys.path.append('c:\\dev\\pytWinc\\superpy')
sys.path.append('c:\\dev\\pytWinc\\superpy\\utils_superpy')
from utils_superpy.utils import buy_product

whereabouts_of_directory_of_testcase  = str(os.getcwd()) 
directory_of_testcase = "fn_buy_product_testcase_01" 
for root, dirs, files in os.walk(whereabouts_of_directory_of_testcase):
    for name in dirs:
        if name == directory_of_testcase: 
            path_to_directory_of_testcase = os.path.abspath(os.path.join(root, name))
            print(os.path.abspath(os.path.join(root, name)))
            break # break coz I only want first (one and supposedly only) result.


# path_to_file_with_actual_testresult is the SAME var for all testcases: (I can reuse this location)
path_to_directory_that_contains_file_with_new_system_date = os.path.join(path_to_directory_of_testcase, 'actual_testresult') 
path_to_file_with_actual_testresult = os.path.join(path_to_directory_that_contains_file_with_new_system_date, 'bought.csv') # path to file 


path_to_test_input_file1 = os.path.join(path_to_directory_of_testcase, "test_input", 'input_file_for_testcase_01.csv') # path to file
path_to_file_with_expected_testresult = os.path.join(path_to_directory_of_testcase, "expected_testresult",  'expected_testresult_testcase_01.csv') 
def test_01_buy_product():
    filecmp.clear_cache()
    buy_product("apple", 0.25,"3333-03-07","3333-04-17", path_to_test_input_file2, path_to_file_with_actual_testresult)
    assert filecmp.cmp(path_to_file_with_actual_testresult, path_to_file_with_expected_testresult, shallow=False)
    filecmp.clear_cache()



path_to_test_input_file2 = os.path.join(path_to_directory_of_testcase, "test_input", 'input_file_for_testcase_02.csv') # path to file
path_to_file_with_expected_testresult = os.path.join(path_to_directory_of_testcase, "expected_testresult", 'expected_testresult_testcase_02.csv') 
def test_02_buy_product():
    filecmp.clear_cache()
    buy_product("orange", 0.75,"3333-04-22","3333-04-28", path_to_test_input_file2, path_to_file_with_actual_testresult)
    buy_product("cabbage", 1.20,"3333-04-23","3333-04-30", path_to_test_input_file2, path_to_file_with_actual_testresult)
    assert filecmp.cmp(path_to_file_with_actual_testresult, path_to_file_with_expected_testresult, shallow=False)
    filecmp.clear_cache()

#2adjust: buy 2 products and then do an assert.



