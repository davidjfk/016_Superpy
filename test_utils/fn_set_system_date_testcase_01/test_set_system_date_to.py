'''
    With os.walk() I can run pytest from anywhere inside project superpy, irrespective of my
    current working directory. 
    The cwd can be different each time I run pytest.  So without os.walk() syntax, as a consequence, 
    the actual result gets stored in a different directory each time I run pytest with a different 
    cwd. This messed up grabbing the file with the actual result (being txt-file system_data.txt or
    csv-file bought.csv or sold.csv, depending on the fn under test) as input for the file comparison
    with the file with the expected result.
    But with the current solution, the actual result is always stored in the directory of the testcase
    (e.g. fn_set_system_date_testcase_01.), nomatter what the cwd is :).  

'''

import filecmp, os, sys
sys.path.append('c:\\dev\\pytWinc\\superpy')
sys.path.append('c:\\dev\\pytWinc\\superpy\\utils_superpy')
from utils_superpy.utils import set_system_date_to

whereabouts_of_directory_of_testcase  = str(os.getcwd()) 
# is a lot faster than starting at "/" and walking the whole tree.

directory_of_testcase = "fn_set_system_date_testcase_01" 
'''
    pitfall: target_file_directory MUST have unique name. It serves as my anchor to create the path
    to the directory with the actual test result (being txt-file system_data.txt or 
    csv-file bought.csv or sold.csv, depending on the fn under test). 

    naming convention: function name + "_testcase_" + testcase_number.
    "fn_set_system_date_testcase_01"
    "fn_set_system_date_testcase_02", etc. 

    1 testcase can contain 1 or more tests. Below it is more practical to have 
    1 testcase with 2 tests.
'''

for root, dirs, files in os.walk(whereabouts_of_directory_of_testcase):
    for name in dirs:
        if name == directory_of_testcase: 
            path_to_directory_of_testcase = os.path.abspath(os.path.join(root, name))
            print(os.path.abspath(os.path.join(root, name)))
            break # break coz I only want first (one and supposedly only) result.

expected_testresult = os.path.join(path_to_directory_of_testcase,  'expected_testresult_system_date.txt')           
actual_testresult_directory = os.path.join(path_to_directory_of_testcase, 'actual_testresult_directory')
actual_testresult = os.path.join(actual_testresult_directory, 'system_date.txt')

def test_set_system_date_to_a_value_equal_to_exected_testresult():
    filecmp.clear_cache()
    set_system_date_to('reset_data_of_previous_testrun_with_this_string', actual_testresult_directory)
    set_system_date_to('2020-01-01', actual_testresult_directory)
    assert filecmp.cmp(actual_testresult, expected_testresult, shallow=False)
    
def test_set_system_date_to_a_value_NOT_equal_to_exected_testresult():
    filecmp.clear_cache()
    set_system_date_to('reset_data_of_previous_testrun_with_this_string', actual_testresult_directory)
    set_system_date_to('2020-01-02', actual_testresult_directory)
    assert not filecmp.cmp(actual_testresult, expected_testresult, shallow=False)





