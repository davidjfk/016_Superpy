Important !!  
Please read this document in Open Preview: Ctrl+Shift+V, or Right-click  
'README_REPORT.md' in the vsCode Explorer and then select the first option 'Open Preview'.

## Table of contents

- [Intro](#intro)
- [Topic 1: Write data to csv in a testable manner](#topic-1-write-data-to-csv-in-a-testable-manner)
- [Topic 2: Run pytest with control over cwd](#topic-2-run-pytest-with-control-over-cwd)
- [Topic 3: Add path to directory 'superpy' to PYTHONPATH environment variable](#topic-3-add-path-to-directory-superpy-to-pythonpath-environment-variable)
- [Topic 4: Connect bought.csv and sold.csv with primary and foreign keys](#topic-4-connect-boughtcsv-and-soldcsv-with-primary-and-foreign-keys)

# Intro
[Table of contents](#table-of-contents)

Goal: Please include a short, 300-word report that highlights three technical elements   
of your implementation that you find notable.
Explain what problem they solve and why you chose to implement them in this way.
- You may consider using Markdown for your report.
- To assist your explanation you may use code snippets.
- Our tips regarding the report:
- You may consider using Markdown for your report.
- Markdown is a markup language you can use for styling your plain text. It is widely used  
    in programming, so it could be a good choice, but it is not required.
- To assist your explanation you may use code snippets.    

<br/><br/>

# Topic 1: Write data to csv in a testable manner
[Table of contents](#table-of-contents)

- Problem: how can fn buy_product and fn sell_product  
    (see (...\superpy\utils_superpy\utils.py)) be be called in:  
    1. Superpy (see ...\superpy\utils_superpy\utils\)
    2. Pytest (see ...\superpy\test_utils\).

- Initial solution: (code snippets below are from  both fns)
```python 
    with open(path_to_csv_bought_output_file, 'a', newline='') as file:
        row = [id_of_row_in_csv_file_bought,product,price,buy_date,expiry_date]
        writer = csv.writer(file)
        writer.writerow(row)
```
- Problem: in append-mode: data gets added to the file with actual testresult. 
    So after each testrun the file with actual testresult gets longer and longer.  
    So 1st time you run pytest testcases, they will pass. But 2nd time   
    you run pytest (and 3rd, etc.) the same testcases will fail.  

- Solution: 

```python 
    with open(path_to_csv_bought_output_file, 'w', newline='') as file: 
        rows.append({'buy_id': id_of_row_in_csv_file_bought, 'product': product, 'buy_price': price, 'buy_date': buy_date, 'expiry_date': expiry_date}) 
        writer = csv.DictWriter(file, fieldnames= reader.fieldnames)
        writer.writeheader()
        writer.writerows(rows)
```

-  In pytest the actual testresult from the previous testrun is completely overwritten.   
    At the ame time in Superpy a transaction (buy or sell) still gets appended to csv file (bought.csv or sold.csv).  

- Alternative solution 1: prior to testrun, empty data file with actual result (that still contains output from previous testrun) 
- Alternative solution 2: use a fixture instead.
    

# Topic 2: Run pytest with control over cwd
[Table of contents](#table-of-contents)

- Goal 1: in pytest to run regression tests
- problem: being in the "wrong" cwd when you run  pytest, resulted in storing the actual-test-result-files  
    in a wrong directory. Not only do these testcases fail, but also superpy file structure got cluttered   
    with actual-result-files stored in the wrong location.

- solution: create 2 fns that help to point to the correct location to store the actual test results.
  <br/>
  This works as follows:  
  * 1of3: when cwd points to following directories and I run pytest:
    1. (...\superpy), 
    2. (...\superpy\test_utils)  
    then the actual result is stored in the correct directory of the pytest testcase 
    (ex: (...\superpy\test_utils\fn_buy_product_testcases) ).

  * 2of3: when I am in the directory of a fn and  run pytest:
    ex:  
    step 1: goto "cd into"  (...\superpy\test_utils\fn_buy_product_testcases)
    step 2: run pytest  
    result: only pytest testcases inside fn_buy_product_testcases are run.

  * 3of3: when cwd points to another directory inside superpy, then pytest does not run any testcases.  
    ex: 
    step 1: goto "cd into"  (...\superpy\test_utils\data_used_in_superpy)
    step 2: run pytest
    result: no testcases are run.
```python

def get_path_to_directory_of_file(directory_of_file):
    # rule1: directory_of_file must be unique inside project superpy.
    whereabouts_of_directory_of_file  = str(os.getcwd()) 
    path_to_directory_of_this_file = '' # prevent UnboundLocalError
    for root, dirs, files in os.walk(whereabouts_of_directory_of_file):
        for name in dirs:
            if name == directory_of_file: 
                path_to_directory_of_this_file = os.path.abspath(os.path.join(root, name))
                break # if rule1 above has been followed, then you can stop searching here to save time.
    return path_to_directory_of_this_file


def get_path_to_file(directory_of_file, file_name_of_which_you_want_to_know_the_path):
    # rule1: directory_of_file must be unique inside project superpy.
    whereabouts_of_directory_of_file  = str(os.getcwd()) 
    path_to_directory_of_this_file = '' # prevent UnboundLocalError
    for root, dirs, files in os.walk(whereabouts_of_directory_of_file):
        for name in dirs:
            if name == directory_of_file: 
                path_to_directory_of_this_file = os.path.abspath(os.path.join(root, name))
                break # if rule1 above has been followed, then you can stop searching here to save time.
    path_to_file = os.path.join(path_to_directory_of_this_file, file_name_of_which_you_want_to_know_the_path ) # path to file 
    return path_to_file

```
    I let both fns start with os.getcwd(). Otherwise, python will start looking everywhere  
    on the filesystem and performance becomes a bottleneck.

<br/><br/>

# Topic 3: Add path to directory 'superpy' to PYTHONPATH environment variable 

[Table of contents](#table-of-contents)

During development inside directory Superpy, I had a subdirectory 'pytest_testdata_factory'.  
Inside this subdirectory there was a script 'produce_testdata_for_csv_files_bought_and_sold.py'. This script called fn 'create_data_for_csv_files_bought_and_sold()' from ...\superpy\utils.utils.py.


step: to get this script  to work, add path to directory 'superpy' to the PYTHONPATH environment variable:
```
sys.path.append('c:\\dev\\pytWinc\\superpy') 
```
* problem: this code will break on another machine: absolute file path and backslashes.

Chicken-and-egg problem while trying to solve this problem: 
- To make path to directory 'superpy' relative, I need to import fn  
  get_path_to_directory_of_file from utils.py.
- To import fn get_path_to_directory_of_file from utils.py, I need to add path to  
  directory 'superpy' to the PYTHONPATH environment variable.

Solution:
```
current_dir  = (os.getcwd()) # e.g. C:\dev\pytWinc\superpy\testdata

parent_directory_of_current_directory = os.path.abspath(os.path.join(current_dir, os.pardir)) # e.g. C:\dev\pytWinc\superpy
```
- On every machine that runs Superpy, the parent directory of current directory is the project directory superpy
```
file_path_to_directory_superpy =  parent_directory_of_current_directory
sys.path.append(file_path_to_directory_superpy)
```
So now I can import everything I need:  
```
from utils.utils import add_days_to_date
from utils.utils import generate_random_buy_date_for_buy_transaction_in_future_in_time_interval
from utils.utils import create_buy_id_for_each_row_in_boughtcsv_as_part_of_mockdata_that_is_being_created
from utils.utils import get_path_to_directory_of_file
from utils.utils import create_data_for_csv_files_bought_and_sold

```
Alternative solution: copy-past the code from fn get_path_to_directory_of_file
into the script. 

<br/><br/>

# Topic 4: Connect bought.csv and sold.csv with primary and foreign keys
[Table of contents](#table-of-contents)

* (only if previous 3 topics are not enough, then plz read this topic 4)

- General problem: how to connect bought.csv and sold.csv, as if they are a relational database together?
- Multiple subproblems need to be addressed:
- problem 1: There are 2 ways to create buy-transactions:  
  1. fn create_data_for_csv_files_bought_and_sold() that creates mock data (1 up to a 1000 or more buy transactions at a time),
  2. fn buy_product that buys 1 product at a time.   
    How to create buy_ids for both options? 
- problem 2: how 2 automatically assign a buy_id to each created MOCK buy-transaction? If script creates  358 buy-transactions, then  
    each buy-transaction in the mock data must get a unique buy_id (b_1, b_2, b_3, etc.)
- problem 3: how 2 automatically assign a buy_id to each buy-transaction (not mock data)that is added 1 at a time, while the Superpy-user  
    does other stuff in the mean time: e.g. sell products, show reports of costs, revenue, sales volume, profit, etc.
- problem 4: how does the option to delete all data in bought.csv and sold.csv (i.e. 'py super.py delete') have effect  
    on which buy_id to issue next for the next buy-transaction?
- problem 5: how to make sure that the buy_ids of a script creating mock-buy-transactions and users creating buy-transactions still  
    connect to each other? ex: script creates 131 buy-transactions (b_1, b_2, ... b_131), then user creates buy-transaction and  
    superpy creates and assigns b_132 to this transaction.
- problem 6: in fn sell_product implement following rules:
    - 1: product does  not exist, so you cannot sell  it.
    - 2: product has already been sold, so you cannot sell it again.
    - 3: product has expired, then sell product and notify user.  
        (just for fun I have implemented also the following rules:)
    - 4: if product is sold at a loss (i.e. sell_price < buy_price), then sell the product and notify user.
    - 5: By default product is sold by its name: e.g. 'py super.py apple 0.49 -s 2403-06-07'. But if product name is very long  
    e.g. "Cold-Pressed Extra Virgin Olive Oil with Lemon and Garlic", then Superpy user also has the option to sell the product  
    by its buy_id (before selling anything first check the inventory: py super.py show_inventory 2403-06-07'):  
    e.g. 'py super.py b_45' (assuming that this product has buy_id b_45 and it is sold on system_date)

 
<br/><br/>

1. problem-1-solution: 2 fns that can both create a buy_ids:

    ```python
        def create_mock_data_for_csv_files_bought_and_sold("a lot of parameters"):
            pass

        def buy_product("a lot of parameters"):
            pass
    ```    
    The first fn makes use of a closure to create a serial id for each transaction in bought.csv.  
    The seconds fn makes use of a buy_id_count.txt to save the system_date in a persistent way.  
    This is the core with around it a multitude of fns to make bought.csv and sold.csv work together 
    like a relational database. 


2. problem-2-solution:
        Inside fn create_data_for_csv_files_bought_and_sold() the following fn creates a buy_id for each  
        buy-transaction. Because this fn create_data_for_csv_files_bought_and_sold()   
        overwrites the current contents of both bought.csv as well as sold.csv, 
        the first issued buy-id by fn   
        create_id_for_each_row_in_boughtcsv_while_script_generates_this_boughtcsv()  
        will ALWAYS be b_1, the next b_2, etc. Internally fn  
        create_id_for_each_row_in_boughtcsv_while_script_generates_this_boughtcsv()
        makes use of a closure to implement this. 

    ```python
    def create_buy_id_for_each_row_in_boughtcsv_as_part_of_mockdata_that_is_being_created(csv_file_name_first_letter, first_nr_in_range):
        pass
    ```

3. problem-3-solution:
        The last issued buy_id is persistently stored in file 'buy_id_counter.txt'  
        (...\superpy\data_used_in_superpy\buy_id_counter.txt)  
        The following fn gets the value from this txt-file (e.g. b_163), increments it with 1, and then  
        feeds the incremented nr (b_164)  into the buy-fn above as argument 'id_of_row_in_csv_file_bought':

    ```python
    def create_buy_id_that_increments_highest_buy_id_in_boughtcsv(path_to_id_with_highest_sequence_number):
        pass
    ```

4. problem-4-solution:

        ```
        py super.py delete
        ```
        result: bought.csv and sold.csv are now empty. You can now (again) create buy-transaction(s) in one
        of the 2 ways as described above.

        Call the following fn with product-range of 0 (== 'no products'):
    ```python
    def create_data_for_csv_files_bought_and_sold("a lot of parameters"):
        pass
    ```
        This means the fn will overwrite bought.csv and sold.csv with just the header-row, but without
        any buy-transactions, nor sell-transactions.


5.  problem-5-solution:
        connect id-range of fn 'create_data_for_csv_files_bought_and_sold' with id-range of  
        buy-transactions that are manually added.  
 
        If script creates e.g. 167 buy_transactions (b_1 - b_167), and super.py-user then creates a few  
        buy_transactions, then the buy_transaction_counter should continue at b_168, b_169, etc.   


        Goal of this task: connect the 2 ranges, nomatter how many buy_transactions the script creates.  
        So in ex above, the super.py-user manually creates a buy_transaction that gets assigned b_168 (intead  
        of b_300).  
        If script creates 17 buy_transactions (b_1 - b_17), then user creates its first buy_transaction with  
        b_18 assigned to it, and so on.

        ex: 
        step 1: 
    ```python
        py super.py create_mock_data -pr 9   (-pr == product_range)
    ```
        result: 64 lines of mock buy-transactions are created in bought.csv, so buy_ids: b_1, b_2 (...) b_64
        are taken.

        step 2:
    ```python
        py super.py buy apple 1.43 -s 2023-10-01 -e 2023-10-25    (-sd == start_date, exd == expiry_date)
    ```
        expected result: super.py assigns buy_id b_65 to this transaction (but NOT b_1)


        When doing this:
    ```python
        py super.py create_mock_data -pr 9   (-pr == product_range)
    ```
        then 3 things happen (triggered by this argparse cli command):

        step 1: call fn:
    ```python
    def create_data_for_csv_files_bought_and_sold("a lot of parameters"):
        pass
    ```
        This fn will - as explained above - overwrite all previous data in bought.csv and sold.csv, and then
        any created buy-transactions will start with b_01, then b_02 and so on.

        status: after having done this, superpy does not know the id of the last buy-transaction.  
        But superpy needs to know, because a(ny) next buy-transaction
        by the superpy-user also needs a unique buy_id. That is why the next fn will  
        get the  highest buy_id from  bought.csv:

        step 2: call fn: (after_running_fn_to_create_mock_data_for_boughtcsv_and_soldcsv)
    ```python
    def get_highest_buy_id_from_boughtcsv(path_to_csv_bought_file):
        pass

    ```
        status: now this highest buy_id must be made persistent, so it can be used to calculate the 
        next buy_id for the next buy-transaction.

        step 3: call fn:

    ```python
    def set_buy_id_in_file_id_to_use_in_fn_to_buy_product_txt(buy_id, path_to_buy_id_file):
        pass
    ```
        As described above in 'challenge-2-solution':
        The last issued buy_id is persistently stored in file buy_id_counter.txt
        (...\superpy\data_used_in_superpy\buy_id_counter.txt)

        fn set_buy_id_in_file_id_to_use_in_fn_to_buy_product_txt(buy_id, path_to_buy_id_file) 
        initializes the value in file 'buy_id_counter.txt'.
        ex1: if 65 rows of mock buy-transactions have been created, then b_65 is stored in this txt-file.
        ex2: if 18 rows of mock buy-transactions have been created, then b_18 is stored in this txt-file.

        status: bought.csv and sold.csv have been filled with data. If a superpy-user now buys a product,
        then the buy-transaction  must be b_66 (in ex1 above), or b_19 (in ex2 above).

        The solution for challenge 2 further above, explains the implementation of assigning b_66 (when
        previous buy_id is b_65) or e.g. b_19 (when previous buy_id is b_18).

6. problem-6-solution: reset buy_id_counter (...\superpy\data_used_in_superpy\buy_id_counter.txt) after  
    creating and then deleting mock_data. Solved in branch_16_uc_create_readme_files_part3.

7. problem-7-solution: implement the rules 1 at a time:
    - 1of3: product does  not exist, so you cannot sell  it.
    - 2of3: product has already been sold, so you cannot sell it again.
    - 3of3: product has expired, so you cannot sell it. 
    - Solved in branch_16_uc_create_readme_files_part3.


<br/><br/>


