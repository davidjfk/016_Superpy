



## Table of contents
<!-- <a name="#table-of-contents" style="visibility: hidden;"></a> -->
- [Intro](#intro)
- [Topic 1: Write data to csv in a testable manner](#topic-1-write-data-to-csv-in-a-testable-manner)
- [Topic 2: Create primary and foreign keys to connect bought.csv and sold.csv](#topic-2-create-primary-and-foreign-keys-to-connect-boughtcsv-and-soldcsv)
- [Topic 3: Run pytest with control over cwd](#topic-3-run-pytest-with-control-over-cwd)

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

- goal: write data to csv
- scope: fn buy_product and fn sell_product (see (...\superpy\utils_superpy\utils.py))
- uc: these 2 fns are used in 2 ways: 
    a. in app superpy (see ...\superpy\utils_superpy\utils\)
    b. in pytest (see ...\superpy\test_utils\).
- requirement: fns must be testable in pytest in easy way.

- initial solution:

```python 
    with open(path_to_csv_bought_output_file, 'a', newline='') as file:
        row = [id_of_row_in_csv_file_bought,product,price,buy_date,expiry_date]
        writer = csv.writer(file)
        writer.writerow(row)
```
- problem: in append-mode: data gets added to the file with actual testresult. 
    So after each testrun the file with actual testresult gets longer and longer.  
    So 1st time you run pytest testcases, they will pass. But 2nd time   
    you run pytest (and 3rd, etc.) the same testcases will fail!  

- solution: 

```python 
    with open(path_to_csv_bought_output_file, 'w', newline='') as file: 
        rows.append({'buy_id': id_of_row_in_csv_file_bought, 'product': product, 'buy_price': price, 'buy_date': buy_date, 'expiry_date': expiry_date}) 
        writer = csv.DictWriter(file, fieldnames= reader.fieldnames)
        writer.writeheader()
        writer.writerows(rows)
```

- advantage: in pytest the actual testresult from the previous testrun is completely overwritten.   
    in superpy a transaction (buy or sell) still gets appended to csv file (bought.csv or sold.csv).  
    

- alternative solution: use tmp_path fixture as a test preparation to remove the data that has been added  
    to the actual testresult file during the previous testrun.  
    Because I had  issues with running pytest in such a way that I had control over the cwd (see technical element 3 below),   
    I did not like any solution  that involveD os.remove() or any other options to delete files or directories. 
    But now, with the cwd-issue solved, I will try to use fixtures in my next python project. 
    

<br/><br/>
# Topic 2: Create primary and foreign keys to connect bought.csv and sold.csv
[Table of contents](#table-of-contents)

- goal: connect bought.csv and sold.csv with primary and foreign keys
- 5 problems to solve: 
- problem 1: 2 options to create buy-transactions: script-that-creates-mock-data and as-a-user. how to create buy_ids for both options? 
- problem 2: how 2 automatically assign a buy_id to each created MOCK buy-transaction? If script creates  150 buy-transactions, then  
    each buy-transaction must get a unique buy_id (b_1, b_2, b_3, etc.)
- problem 3: same problem, but this time for superpy-user buying  products 1 at a time and  doing other stuff in the  
    mean time: e.g. sell products, show reports of costs, revenue, sales volume, profit, etc.
- problem 4: how does the option to delete all data in bought.csv and sold.csv have effect on which buy_id to issue next for the  
    next buy-transaction?
- problem 5: how to make sure that the buy_ids of a script creating mock-buy-transactions and users creating buy-transactions still  
    connect to each other? ex: script creates 131 buy-transactions (b_1, b_2, ... b_131), then user creates buy-transaction and superpy
    creates and assigns b_132 to this transaction.

Solutions:
- problem-1-solution: there are 2 options to create buy-transactions in superpy:
        option 1of2 to create buy-transaction: 
            py super.py create_mock_data 
                --> bought.csv and sold.csv are filled with mockdata that has
                    been created with 11 optional arguments with default values.
            py super.py create_mock_data -product_range 3 -del_row 2 -shelf_life 10 -markup 4 -lower_boundary_year 2024 
                    --> bought.csv and sold.csv are filled with mockdata that has
                    been created with 5 optional values, and 6 optional values with a default value.       
            
            result  /rule: all previous data in bought.csv and sold.csv are overwritten, including any data 
                    that has been created by option 1 above.
            result: superpy creates buy_id (b_1, b_2, b_3, etc.) for each buy-transaction.

        option 2of2 to create buy-transaction:
            py super.py buy apple 1.75 -sd 23-09-15 -exd 23-09-27 
                --> buy_date is 23-09-15 . expiry_date is 23-09-27
            py super.py buy pear 3.00 
                --> default buy_date is system_date and default expiry_date is 'does not expire'

            result: superpy creates buy_id (b_1, b_2, b_3, etc.) for each buy-transaction.

        So 2 functions must be created that can both create buy_ids:

    ```python
        def buy_product(product, price, buy_date, expiry_date, id_of_row_in_csv_file_bought, path_to_csv_bought_input_file, path_to_csv_bought_output_file):
            pass

        def create_data_for_csv_files_bought_and_sold("a lot of parameters"):
            pass
    ```    



- problem-2-solution:
        Inside fn create_data_for_csv_files_bought_and_sold() the following fn creates a buy_id for each
        buy-transaction. Because this fn create_data_for_csv_files_bought_and_sold() 
        overwrites the current contents of both bought.csv as well as sold.csv, 
        the first issued buy-id by fn create_id_for_each_row_in_boughtcsv_while_script_generates_this_boughtcsv()
        will ALWAYS be b_1, the next b_2, etc. Internally fn create_id_for_each_row_in_boughtcsv_while_script_generates_this_boughtcsv()
        makes use of a closure to implement this. 

    ```python
    def create_buy_id_for_each_row_in_boughtcsv_as_part_of_mockdata_that_is_being_created(csv_file_name_first_letter, first_nr_in_range):
        pass
    ```

- problem-3-solution:
        The last issued buy_id is persistently stored in file 'buy_id_counter.txt'
        (...\superpy\data_used_in_superpy\buy_id_counter.txt)
        The following fn gets the value from this txt-file (e.g. b_163), increments it with 1, and then
        feeds the incremented nr (b_164)  into the buy-fn above as argument 'id_of_row_in_csv_file_bought':

    ```python
    def create_buy_id_that_increments_highest_buy_id_in_boughtcsv(path_to_id_with_highest_sequence_number):
        pass
    ```

- problem-4-solution:

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


- problem-5-solution:
        connect id-range of fn 'produce_testdata_for_csv_files_bought_and_sold' with id-range of  
        buy-transactions that are manually added.  

        Currently id-range id_1 to id_299 are served for this script and range id_300 and beyond are  
        reserved for buy_transactions that are added by super.py-user.  
        If script creates e.g. 167 buy_transactions (b_1 - b_167), and super.py-user then creates a few  
        buy_transactions (starting at b_300), then currently there is a gap between the 2 ranges.  


        Goal of this task: connect the 2 ranges, nomatter how many buy_transactions the script creates.  
        So in ex above, the super.py-user manually creates a buy_transaction that gets assigned b_168 (intead  
        of b_300).  
        If script creates 17 buy_transactions (b_1 - b_17), then user creates its first buy_transaction with  
        b_18 assigned to it, and so on.

        ex: 
        step 1: 
        ```
            py super.py create_mock_data -pr 9   (-pr == product_range)
        ```
        result: 64 lines of mock buy-transactions are created in bought.csv, so buy_ids: b_1, b_2 (...) b_64
        are taken.

        step 2:
        ```
            py super.py buy apple -sd 2023-10-01 -exd 2023-10-25    (-sd == start_date, exd == expiry_date)
        ```
        expected result: super.py assigns buy_id b_65 to this transaction (but NOT b_1)


        When doing this:
        ```
            py super.py create_mock_data -pr 9   (-pr == product_range)
        ```
        then 3 things happen (triggered by this argparse cli command):

        step 1: call fn:
    ```python
    def create_data_for_csv_files_bought_and_sold("a lot of parameters"):
        pass
    ```
        This fn will - as explained above - overwrite all previous data in bought.csv and sold.csv, and then
        any created buy-transactions will start with b_1, then b_2 and so on.

        status: after having done this, superpy does not know the id of the last buy-transaction. But superpy needs to know, because a(ny) next buy-transaction
        by the superpy-user also needs a unique buy_id. That is why the next fn will get the  highest buy_id from  bought.csv:

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

        fn set_buy_id_after_running_script_to_create_mock_data_for_boughtcsv_and_soldcsv(buy_id, path_to_buy_id_file) 
        initializes the value in file 'buy_id_counter.txt'.
        ex1: if 65 rows of mock buy-transactions have been created, then b_65 is stored in this txt-file.
        ex2: if 18 rows of mock buy-transactions have been created, then b_18 is stored in this txt-file.

        status: bought.csv and sold.csv have been filled with data. If a superpy-user now buys a product,
        then the buy-transaction  must be b_66 (in ex1 above), or b_19 (in ex2 above).

        The solution for challenge 2 further above, explains the implementation of assigning b_66 (when
        previous buy_id is b_65) or e.g. b_19 (when previous buy_id is b_18).


<br/><br/>
# Topic 3: Run pytest with control over cwd
[Table of contents](#table-of-contents)

- Goal 1: in pytest to run regression tests
- problem: pytest looks at the cwd to determine where to look for where to read and/or write
    * test input files
    * actual test result files
    * expected test result files  
  
        In addition to that, each fn-to-test has its own directory with these files and its own testscript.  
        Being in the "wrong" directory when you run  pytest, results in storing the actual-test-result-files  
        in a wrong directory.  
        Not only do these testcases fail, but also superpy file structure gets cluttered with  
        actual-result-files stored in the wrong location.


- solution: my 2 fns below solve the problem as follows:
  <br/>
        1of3: when cwd points to following directories and I run pytest:
        a. (...\superpy), 
        b. (...\superpy\test_utils)
        then the actual result is stored in the correct directory of the pytest testcase 
        (ex: (...\superpy\test_utils\fn_buy_product_testcases) ).

        2of3: when I am in the directory of a fn and  run pytest:
        ex: 
        step 1: goto "cd into"  (...\superpy\test_utils\fn_buy_product_testcases)
        step 2: run pytest
        result: only pytest testcases inside fn_buy_product_testcases are run.

        3of3: when cwd points to another directory inside superpy, then pytest does not run any testcases.
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
Both fn start with os.getcwd(). Otherwise, python will start looking everywhere on the filesystem and performance
becomes a bottleneck.
