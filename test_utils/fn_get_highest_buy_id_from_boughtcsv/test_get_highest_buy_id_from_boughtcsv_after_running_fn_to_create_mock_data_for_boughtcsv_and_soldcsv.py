import filecmp, os, sys
sys.path.append('c:\\dev\\pytWinc\\superpy')
sys.path.append('c:\\dev\\pytWinc\\superpy\\utils_superpy')
from utils.utils import get_highest_buy_id_from_boughtcsv, get_path_to_directory_of_file

directory_of_testcase = "fn_get_highest_buy_id_from_boughtcsv" 
path_to_directory_of_testcase = get_path_to_directory_of_file(directory_of_testcase)

# input test files:
path_to_input_file_test_01 = os.path.join(path_to_directory_of_testcase, "test_input", 'input_file_for_testcase_01.csv') 
path_to_input_file_test_02 = os.path.join(path_to_directory_of_testcase, "test_input", 'input_file_for_testcase_02.csv') 
path_to_input_file_test_03 = os.path.join(path_to_directory_of_testcase, "test_input", 'input_file_for_testcase_03.csv') 
path_to_input_file_test_04 = os.path.join(path_to_directory_of_testcase, "test_input", 'input_file_for_testcase_04.csv') 

def test_01_get_highest_buy_id_from_boughtcsv_happy_flow():
    filecmp.clear_cache()
    expected_test_result = 'b_63'
    actual_result = get_highest_buy_id_from_boughtcsv( path_to_input_file_test_01)
    assert actual_result == expected_test_result


def test_02_get_highest_buy_id_from_boughtcsv_happy_flow():
    filecmp.clear_cache()
    expected_test_result = 'b_280' 
    actual_result = get_highest_buy_id_from_boughtcsv(path_to_input_file_test_02)
    assert actual_result == expected_test_result

def test_03_get_highest_buy_id_from_boughtcsv_happy_flow():
    filecmp.clear_cache()
    expected_test_result = 'b_279' # off by 1 error
    actual_result = get_highest_buy_id_from_boughtcsv(path_to_input_file_test_03)
    assert not actual_result == expected_test_result

def test_04_get_highest_buy_id_from_boughtcsv_happy_flow():
    filecmp.clear_cache()
    expected_test_result = 'b_281' # off by 1 error
    actual_result = get_highest_buy_id_from_boughtcsv(path_to_input_file_test_04)
    assert not actual_result == expected_test_result