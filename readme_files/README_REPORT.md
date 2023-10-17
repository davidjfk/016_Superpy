Important !!  
Please read this document in Open Preview: Ctrl+Shift+V, or Right-click  
'README_REPORT.md' in the vsCode Explorer and then select the first option 'Open Preview'.

## Table of contents

- [Intro](#intro)
- [Topic 1: Create fn that also takes files as input and output and is testable in pytest](#topic-1-create-fn-that-also-takes-files-as-input-and-output-and-is-testable-in-pytest)
- [Topic 2: Write data to csv in a testable manner](#topic-2-write-data-to-csv-in-a-testable-manner)
- [Topic 3: Run pytest with control over cwd](#topic-3-run-pytest-with-control-over-cwd)
- [Topic 4: Add path to directory 'superpy' to PYTHONPATH environment variable](#topic-4-add-path-to-directory-superpy-to-pythonpath-environment-variable)
- [Topic 5: Connect bought.csv and sold.csv with primary and foreign keys](#topic-5-connect-boughtcsv-and-soldcsv-with-primary-and-foreign-keys)

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

# Topic 1: Create fn that also takes files as input and output and is testable in pytest
[Table of contents](#table-of-contents)

- Problem: How to create fns in utils.py in such  way that they are testable and Superpy user can call them. 

* solution: I described what both "use cases" of a fn require:


| "Use cases" of a fn in utils.py |  | Input | Actual Output | Expected Output |
|----------|-----------|-------|---------------|-----------------|
| 1of2: Run pytest testcase ( pytest ) | | | | |
| | | value | file | file |
| | | file |  |  |
| 2of2: As Superpy user call fn  (e.g. py super.py buy apple 1.11 ) | | |  file  | NA |
| | | value | file  |

- This helped me realize that to test 1 fn I need a folder with (up to) 3 "buckets" / subfolders: 
  1. test_input
  2. actual_testresults
  3. expected_testresults
* e.g. in test_utils (...\superpy\test_utils) directory 'fn_buy_product_testcases' and  its subfolders.


- Also each fn  (e.g. buy_product) must have a fn-argument to target each of these "buckets",  
  in order
    to make the  fn testable in a pytest regression testset.

- In addition to that, adding a filepath  (e.g. to bought.csv) as fn-argument, simplified the code.  
  Before that I inserted a partial path, a directory name and file name into a fn and connected  
  the pieces inside the fn. This both violated single responsibility principle and  
  as well as made the code more difficult to read.  

<br/><br/>


# Topic 2: Write data to csv in a testable manner
[Table of contents](#table-of-contents)

- Intro:
    Some of the fns write data to csv, e.g. buy_product() and sell_product(),  
    see (...\superpy\utils_superpy\utils.py) and are tested in pytest, see  
    (...\superpy\test_utils\).

- Problem: how to write data to csv in a testable manner?

- Initial solution: (code snippets below are from  both fns)
```python 
    with open(path_to_csv_bought_output_file, 'a', newline='') as file:
        row = [id_of_row_in_csv_file_bought,product,price,buy_date,expiry_date]
        writer = csv.writer(file)
        writer.writerow(row)
```
- Problem: in append-mode: data gets added to the file with actual testresult  
    (== 1 of the "buckets" in previous topic 1 above). 
    So after each testrun the file with actual testresult gets longer and longer.  
    So 1st time you run pytest testcases, they will pass. But 2nd time   
    you run pytest (and 3rd, etc.) the same testcases will fail.  

- Final solution: 

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
<br />    
<br />    

# Topic 3: Run pytest with control over cwd
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
    e.g. (...\superpy\test_utils\fn_buy_product_testcases) .

  * 2of3: when I am inside superpy in a directory that tests a fn (e.g. fn_buy_product_testcases) and  run pytest:
    ex:  
    step 1: goto "cd into"  (...\superpy\test_utils\fn_buy_product_testcases)
    step 2: run pytest  
    result: only pytest testcases inside fn_buy_product_testcases are run.

  * 3of3: when cwd points to another directory inside superpy, then pytest does not run any testcases.  
    ex: 
    step 1: goto "cd into"  (...\superpy\test_utils\data_used_in_superpy)
    step 2: run pytest
    result: no testcases are run.
```py

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

# Topic 4: Add path to directory 'superpy' to PYTHONPATH environment variable 

[Table of contents](#table-of-contents)

During development inside directory Superpy, I had a subdirectory 'pytest_testdata_factory'.  
Inside this subdirectory there was a script 'produce_testdata_for_csv_files_bought_and_sold.py'.  
This script called fn 'create_data_for_csv_files_bought_and_sold()' from ...\superpy\utils.utils.py.


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



# Topic 5: Connect bought.csv and sold.csv with primary and foreign keys
[Table of contents](#table-of-contents)

- General problem: how to connect bought.csv and sold.csv, as if they are a relational database together?  

1. sub-problem 1: How to create a buy_id for each bought product, given that there are 2 ways to create buy-transactions? 
    - A whole bunch of mock data in bought.csv and sold.csv. If script creates  358 buy-transactions, then  
    each buy-transaction in the mock data must get a unique buy_id (b_1, b_2, b_3, etc.)
    - As a superpy-user buy or sell 1 product at a time.  
     <br/>

2. sub-problem 2: how to make sure that the buy_ids of a script creating mock-buy-transactions and users creating buy-transactions still  
    connect to each other? ex: script creates 131 buy-transactions (b_1, b_2, ... b_131), then user creates buy-transaction and  
    superpy creates and assigns b_132 to this transaction.  
    <br/>

3. sub-problem 3: how to connect bought products to sold product in such a way that buy_id is primary key in bought.csv and at  
    at the same time foreign key in sold.csv?

4. sub-problem 4: how to reset the last issued  buy_id (e.g. b_359) to b_00, when all transactions in bought.csv and sold.csv  
    have been deleted?
 
<br/><br/>

1. problem-1-solution: create a fn for each way to create a buy-transaction. Each fn creates its own buy_id(s):

    ```python
        def create_data_for_csv_files_bought_and_sold("a lot of parameters"):
            pass

        def buy_product("a lot of parameters"):
            pass
    ``` 

    - fn create_data_for_csv_files_bought_and_sold():
  
        This fn makes use of a closure to create a serial buy_id for each transaction in bought.csv  
        (1 up to infinity buy and sell transactions at a time). This fn always starts to count at b_01, b_02, etc.  
        This work is done in fn:

        ```py 
            def create_buy_id_for_each_row_in_mock_data():
        ``` 
        Suppose 358 transactions  have been added to bought.csv, then  
        as a next step the highest buy_id (e.g. b_358)  is added to buy_id_count.txt with fn:

        ```py 
            def set_buy_id_counter_txt(highest_buy_id_in_boughtcsv, path_to_file_with_name_buy_id_counter)
        ```
    

    - fn buy_product():

        Fn buy_product creates 1 bought product in bought.csv at a time.  

        First it needs to know the last issued / lag buy_id (e.g. b_358) in bought.csv. The following  
        fn does that:  

        ```py
            def get_highest_buy_id_from_boughtcsv(path_to_csv_bought_file):
        ```

        Then a serial buy_id is needed (e.g. b_359) for a new buy_transaction that is about to be  
        added to bought.csv:

        ```py 
            def create_buy_id_that_increments_highest_buy_id_in_boughtcsv():
        ```
        Furthermore the lag buy_id in buy_id_count.txt is updated with value b_359 with fn:

        ```py
            def increment_buy_id_counter_txt(path_to_id_with_highest_sequence_number) 
        
        ```

    Now the cycle can repeat itself. Suppose another buy_transaction is added to bought.csv, then first  
    b_359 is read from buy_id_count.txt. After that b_360 is written to buy_id_count.txt and b_360 will  
    be the buy_id of the latest bought product in bought.csv. And so on. 


    It also uses buy_id_count.txt to save the lag / highest buy_id (e.g. b_358) in a persistent way.  

    <br />
    <br />

2. problem-2-solution:
    First read problem-1-solution.  
    So there are 2 fns ("ways") to create buy-transactions. Both fns are generating buy_id(s)...

    For both fns there is one single source of truth with the last issued buy_id for a buy-transaction, this  
    is buy_id_count.txt (...\superpy\data_used_in_superpy\buy_id_counter.txt). Both fns use this single  
    source of truth and keep it up-to-date.

    <br />
    <br />

3. problem-3-solution:
    First read problem-1-solution.  
    So there are 2 fns ("ways") to create buy-transactions. Both fns are generating buy_id(s)...

    - fn create_data_for_csv_files_bought_and_sold():
        Suppose 20 buy-transactions are added to bought.csv: b_01 (...) b_20:

        ```py
            py super.py create_mock_data -denr 2 -hp 9.99 -lp 0.09 -mu 3 -nopro 5 -nopri 4 -sl 10 -tt 3 -lby 2029 -lbm 1 -lbd 1 -ubm 0 -ubw 0 -ubd 3 
            py show_bought_csv
        
        ```
        For each created buy-transaction in bought.csv, a sell-transaction is created in sold.csv.  
        Delete every nth row '-denr' with value of 2 deletes every second row in sold.csv. The  
        remaining 10 sell-transactions remain part of sold.csv:

        ```py
            py super.py show_sold_csv
        ```

        Each sold product in sold.csv has a sell_id as primary key that matches to a buy_id in bought.csv as follows:  
        s_01 --> b_01, s_02 --> b_02, s_03 --> b_03, etc.
        The matching buy_id (b_01, b_02, b_03, etc.) is added to sold.csv as foreign key.


    - fn buy_product():

        A product can  be sold by name  or by buy_id: (first run previous 3 superpy-commands above)

        ```py
            py super.py show_inventory -d 2029-01-02
        ```

        Now either sell a product (with short name) like this:

        ```py
            py super.py sell bananas 3.45 -s 2029-01-02
        ```

        Or a product (wit a long name, e.g. prebiotic_probiotic_organic_greek_yogurt ) like this:

        ```py
            py super.py sell b_11 4.55 -s 2029-01-02
        ```

        Either way, if the buy_id is b_xx, then the sell_id as primary key in sold.csv becomes s_xx. Examples:  
        b_01 --> s_01 , b_02 --> s_02, b_03 --> s_03, etc. 
        The matching buy_id (b_01, b_02, b_03, etc.) is added to sold.csv as foreign key.

    <br />
    <br />

4. problem-4-solution:

    ```py 
        py super.py delete
    ```
    result: all transactions have been removed from bought.csv and sold.csv are now empty.  
    This resets the last issued buy_id (e.g. b_359) to b_00.  

    This is implemented by calling the following fn with a nr of products '-nopro' of 0:

    ```python
    def create_data_for_csv_files_bought_and_sold("a lot of parameters"):
        pass
    ```
        
    Now you can continue with a clean slate: if you now buy a product, then it will get buy_id b_01, the 2nd  
    product b_02, and so on. 

<br/><br/>


