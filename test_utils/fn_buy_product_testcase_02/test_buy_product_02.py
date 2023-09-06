

import filecmp, os, sys
sys.path.append('c:\\dev\\pytWinc\\superpy')
sys.path.append('c:\\dev\\pytWinc\\superpy\\utils_superpy')
from utils_superpy.utils import buy_product

whereabouts_of_directory_of_testcase  = str(os.getcwd()) 
directory_of_testcase = "fn_buy_product_testcase_02" 
for root, dirs, files in os.walk(whereabouts_of_directory_of_testcase):
    for name in dirs:
        if name == directory_of_testcase: 
            path_to_directory_of_testcase = os.path.abspath(os.path.join(root, name))
            print(os.path.abspath(os.path.join(root, name)))
            break # break coz I only want first (one and supposedly only) result.



path_to_directory_that_contains_file_with_new_system_date = os.path.join(path_to_directory_of_testcase, 'actual_testresult') 
path_to_file_with_actual_testresult = os.path.join(path_to_directory_that_contains_file_with_new_system_date, 'bought.csv') # path to file 


path_to_test_input_file = os.path.join(path_to_directory_of_testcase, "test_input", 'input_file_for_testcase_02.csv') # path to file
path_to_file_with_expected_testresult = os.path.join(path_to_directory_of_testcase, "expected_testresult", 'expected_testresult_testcase_02.csv') 
def test_02_buy_product():
    filecmp.clear_cache()
    buy_product("orange", 0.75,"3333-04-22","3333-04-28", "b_301", path_to_test_input_file, path_to_file_with_actual_testresult)
    buy_product("cabbage", 1.20,"3333-04-23","3333-04-30", "b_302", path_to_file_with_actual_testresult, path_to_file_with_actual_testresult)
    # output of first fn call is input to second fn call.
    assert filecmp.cmp(path_to_file_with_actual_testresult, path_to_file_with_expected_testresult, shallow=False)
    filecmp.clear_cache()






