
# INTRO
    This doc contains an analysis-part and a design-part.

    The analysis-part helps me to understand things.
    The overal / "grand" design, consisting of the steps 1-13, helps me to get 
    things done, while providing an overview.
    Step 7 contains the main use cases (ucs).
    Step 10 is a manual of how to implement the ucs of step 7 in a TDD manner.

    Steps 11, 12 and 13 are functionality (e.g. show data in matplotlib) that will not be 
    implemented with TDD.

    The first uc of step 7, set_system_date_to, is used as a touchstone to modify 
    and validate the TDD way of implementing the remaining ucs of step 7. 
    
# ANALYSIS

1. # definitions:
    profit == total revenue minus total expenses
    revenue == sum of each individual product * sales price of that product. --> each product is bought and sold 1 at a 
    time, so revenue == sum of all sales prices of all sold proudcts. 
        remark: so this definition deviates from the general definition of revenue: "average sales price * number of units sold".

    date == date object == calendar day.
    Format of calender day: the date object with string representation in format: '%Y-%m-%d'. 

    time range == a range of days between 1 (or higher) and 60 (or lower) inclusive. So 
                    maximum time range is 60 days and minimum time range is 1 day.

    record == transaction ==  line of text (i.e. the "transaction" ) in bought.csv or sold.csv that depicts 
                    the act of buying or selling a product (1 in each transaction) by the supermarket.  

    system_date == ('the day that is today'). This date will be saved
    in file 'system_date.txt'

    # 2 types of data:
    stateful data ('the model layer'): bought products, sold products, system-date.

    "derived" data ('the view layer'): inventory 
            Inventory == sold products minus bought products in a time range.
            This time range starts at the first day that products were bought or sold.
            This time range ends at system_date.txt

    To avoid redundancy in the csv-files, inventory (and any other derived data) will be calculated dynamically.
    The requirement 'Exporting selections of data to CSV files;' is about being able to export a report of 
    the inventory of a certain time range into a csv-file. 

    # Argparse: 
    Application has 2 types of argparse-arguments (abbreviated as "actions"):

    a. actions that change state: buy, sell, setting the date (e.g. yesterday)
        This is the "model layer".

    b. actions that show (but do not modify) (part of or the entire) state on a certain moment: inventory, report 
        This is the "view layer".

    # Thinking of how to connect csv-tables bought.csv and sold.csv

    -- design idea 1: bought.csv and sold.csv not connected via primary and foreign keys 
        (tldr; bad idea for practical coding reasons).

        The supermarket strictly uses logistic principle FIFO (first in first out).

        The fields that connect the tables: 
        The tables bought.csv and  sold.csv share the field 'productType'. 
        Field 'productType' is nor a primary key nor a foreign key.

        In table SYSTEM_DATE.txt the field system_current_date matches
        the date field 'boughtDate' in table BOUGHT.csv and 'soldDate' in table SOLD.csv.
        These date fields are nor primary key nor foreign key.

        design choice: the(se aforementioned) fields 'productType', 'system_current_date' and 
        'expiryDate' are used to combine these tables to generate the data required by the use cases
        in the 'list of use cases' further below.
        So although I have created an erd, the tables in the erd are not relational in the sense that 
        they are not connected to one another via primary and foreign keys (nor do they adhere to the other
        Codd's rules https://www.tutorialspoint.com/dbms/dbms_codds_rules.htm ).

        In a real-life supermarket most products (e.g. an apple, packet of milk, loaf of bread) only have a barcode, 
        but you cannot trace (a product on the shelves nor) a sold product (in sold.csv) back to a transaction on bought.csv 
        (i.e. the transaction when this e.g. apple was bought by the supermarket).
    
        Suppose in the supermarket in the vegetable department in a fruit-display-container there are apples  mixed together 
        from 3 transactions in bought.csv and a client (by coincidence) selects apples from all 3 transactions in bought.csv. 
        When the client buys these apples the resulting transaction in sold.csv would need 
        to contain 3 foreign keys to the bought.csv file.
        Getting back to the logistic principle FIFO: e.g. the oldest milk is presented at the front of the shelf and the
        milk with longer longevity is placed at the back of the shelf (just like  in a real supermarket). Same with e.g. the
        fruit: inside a fruit-display-container the oldest fruit (with a lower id on bought.csv) on top and fruit 
        from a later transaction (with a higher id on bought.csv) (again, this is also how things go in real supermarket). 
        This FIFO-mechanismm is important to be able to calculate which products have expired at a certain system_date.

        There are a few supermarket products that could be traced back to the transaction in bought.csv:
        e.g. medication, eggs, magazines. But also these products can be sold without tracing them back.
        QED: no foreign key in sold.csv pointing to bought.csv

        Caveat / challenge: how to calculate the expiry date for each product type on a certain system_date?
        Ex: 
        Up until day 20 I have bought 100 apples and sold 80 apples. Now I must check if some of the 20 apples
        in store have expired:
        a. slice day 1-20 out of bought.csv
        b. filter only the apples from bought.csv
        c. reverse the list with bought apples (reversed()) . result looks something like this:
            20,banana,5,3.1,20,25
            19,banana,6,2.5,18,23
            18,banana,3,1.25,17,22
            14,banana,3,2.5,14,19
            12,banana,6,1.25,13,17
        d. see entity_relationship_diagram to interpret this data.
        e. loop thru the data to determine which ones have expired.
        f. expected result: the following products have expired:
            14,banana,3,2.5,14,19  --> all 3 bananas have expired.
            12,banana,6,1.25,13,17 --> 3 out of 6 bananas have expired. The other 3 had already been sold.
        
        Now repeat this for all other products.
        QED: a lot of work as a consequence / toil of disconnecting bought.csv from sold.csv in the erd.


    -- design idea 2: use primary and foreign key to connect bought.csv and sold.csv (my choice)
        
        I connect each transaction  in sold.csv via a foreign key in sold.csv to a primary key
        in bought.csv 

        That makes it practical for the supermarket to sell products in the same amount they were bought in. 
        ex:
        'buy-transaction' (A) in bought.csv is connected to 'sell-transaction' (B) in sold.csv . 
        Now if A contains 10 apples, then B contains 10 apples too. 
        Suppose in B I only sell 5 apples, then there are 5 apples in A still unsold. This means that 
        calculating the expiry date does not only involve checking if A has been sold in B, but also
        if A has ENTIRELY been sold in B. Also calculating inventory, turnover and profit will be more work.
    
        So to keep it simple, I assume that the supermarket will sell products in the amounts they were 
        bought in.
        
        To simplify this further, I assume that the supermarket will buy and sell products in 
        amounts of ONE at a time, because this will make calculating inventory, turnover and profit easier. 
        
        So A and B are about 1 product at a time.

        This seems ok according to the example code in winc assignment:
        $ python super.py sell --product-name orange --price 2
        OK
        analysis: 1 orange is sold at a certain price. 
        Furthermore the use of primary and foreign keys to connect bought.csv and sold.csv is suggested
        in winc assignment. 
        So I can do this as well:
        $ python super.py buy --product-name orange --price 2
        OK
        analysis: 1 orange is bought at a certain price. 
        Both transactions are connected via primary and foreign key. 

        Benefit: the supermarket can buy any type of product. E.g.
        py s.py buy apple 0.20
        py s.py buy quinoa 1.20 
        etc.

        Benefit: for each new buy or sell transaction I can set the price manually. E.g.
        py s.py buy apple 0.20  (system generates id, e.g. b_194, for appended row in bought.csv)


        py.s.py sell s_194 0.50   --> so I refer to the transaction where I bought the apple: e.g. take b_194, then
                replace the 'b' by 's'. 

        The profit is delta between b_194 and s_194. So here  profit is  0.30 euro.

        Another ex:
        py s.py buy quinoa 1.20  --> system generates id 'b_188'
        py s.py sell s_188 0.70
        
        (loss: 0.50 euro --> perhaps quinoa is on sale  to attract  customers)

        If you try to sell product that does not exist, e.g. there is no buy-transaction with id b_1004, then 
        the following argparse command will raise an exception:
        
        py.s.py sell s_1004 0.50 


# DESIGN

1.  various:
    The time horizon of the superpy app is (arbitrarily) 60 days (counting days starts at 1).


    To keep it simple I sell 1 product of a productType in 1 transaction, just like in the example code:
        $ python super.py sell --product-name orange --price 2
        OK
    If I would buy e.g. buy 15 products in 1 transaction and then sell 7 products from this transaction, then I need a 
    book keeping mechanism to book the remaining 8 products in store. I do not want to go  down that rabbit hole.


2. create erd to connect tables bought.csv and sold.csv . (done)
    This erd contains 3 tables: bought.csv , sold.csv , system_date.txt --> see project directory 'entity relationship diagram'.

    bought.csv and sold.csv connect via primary and foreign keys. 
    Each buy-transaction buys 1 product.
    Each sell-transaction sells 1 product.

    Previous chapter analysis explains why.

3. inventory management:
    It is management responsibility to ensure (with fn calculate_inventory in combination with timetraveling) that there are always 
    products for a particular sale of products (e.g. 10 apples) to take place. 
        
    Inside the sell_product fn there will also be a check if there is enough inventory (here: of productType apple)
    to sell the product. -->  See 'give error when trying to sell a product that is not in stock:' below at end of this document, where that feature will be implemented. 
        

4. field ID in tables bought.csv and sold.csv:
    Each ID must be unique.
    Each ID must work like a counter.
    Each ID must specify its identity (i.e. tell id in  bought.csv apart from id in sold.csv).
    Each ID must be brief, because selling a product will look like this:

    py s.py s_8 5.30
    This means:
    py = python
    s = vsCode superpy project = abbreviation of superpy. 
        Superpy is command line tool and an argparse argument while using this tool.
        So for the sake of brevity / pleasant user experience I have named the superpy-project itself 's'. 
    
    s_8 means: as a supermarket employee I sell the product b_8. b_8 is transaction on row
        8 in bought.csv.
    5.30 == the price in euros.

    ex: 
    first buy_transaction gets id b_1 ( == bought_1 )
    second buy_transaction gets id b_2
    etc.

    idem for sold.csv:
        s_1 ( == sold_1)
        s_2
        etc.
    
    implement with closure (status: in progress)
    (random nr of 3 digits is not unique enough)
    (module uuid creates unwieldy long unique identifiers)
    
5. SYSTEM_DATE.csv:
   practical considerations about SYSTEM_DATE.csv:
    Variable system_current_date is a configurable / changeable and completely independent entity that 
    can be used to timetravel. By timetraveling the products of individual transactions in the table
    bought.csv expire, depending on the timedelta between system_current_date and the expiry_date of each
    individual transaction.  


6. Create fn update_csv_file to update data in a given csv file
    (status: done)
    This code serves as a baseline / template to create additional fns to CRUD csv-data.
    - read data (part of fn update_csv_file)
    - write data (part of fn update_csv_file)
    - append data ()  --> 2do.

7.  List with fn signatures and argparse-command signatures:
    Create for following use cases the fn-signature (i.e. fn-name, fn-arguments, type of fn-arguments, return-variable, type of returned-var):    

    - general remark: subparsers will be used to implement the following use cases. 
      Use cases that do not require a range, must be ready before starting with use cases
      that require a range.


    - uc 01: set the system_date in time range
        This creates a baseline to timetravel ('back to the future, yeah, here I come')

        Order of events: 
        A value for date object (e.g. day 16) is a prerequisite for buying and selling products
        and all subsequent use cases below.

        pyt fn:
        def set_system_date_to(system_date):

        (super.py abbreviated as s.py so less repetitive typing)
        shell command plus argparse arguments: 
        py .\main.py set_date 2020-02-25   (status: works)
       


    
    - uc 02: timetravel in time range.
        example code: $ python super.py --advance-time 2

        To 'advance' means to move forward in purposeful way. But this superpy-app can also timetravel to 
        the past. So I use 'timetravel' as a verb instead of 'advance'.  
        Implement Argparse argument 'timetravel' inside a subparsers with a positional argument. 
        (use timedelta from module datetime to implement)

        pyt fn: 
        def time_travel(nr_of_days_to_set_system_date_to_future_or_past):

        shell command plus argparse arguments:
        (super.py abbreviated as s.py so less repetitive typing)
        py .\main.py time_travel -2 
        legenda:
        positive nr: to the future. e.g. 7 is 7 days to the future
        negative nr: to the past. e.g. -4 is 4 days to the past  
        
        Order of events:
        The ability to timetravel must be in place in order to implement any use case that requires
        the presence of a range (e.g. report profit in day range 17 to 43 inclusive). 



    - uc 03: buy product (and add to bought.csv) 

        pyt fn:
        def buy_product(productType, pricePerUnit, buy_date, expiryDate):
        
        shell command plus argparse arguments:
        py s.py buy apple 4.50 16 20 

        design:
        2 options:
        option 1:
        add var buy_date explicitly (see code ex above)

        option 2:
        goto the date (e.g. 24-02-09) on which you want to buy a product with fns
        set_system_date_to and/or time_travel. Then use that day  as system_date
        on which you buy that product.

        choice: option 1 seems to be more user-friendly.


        Rule: each id in buy.csv (e.g. b_08) and sell.csv (e.g. s_08) MUST be unique.

        There are 2 different SOURCES that create ids in the application:
        SOURCE OF IDS 1OF2: script create_testdata_for_csv_files_bought_and_sold creates ids.
        3 use cases:
        1. start the production application with real-looking data.
        2. create input files for testcases.
        3. create expected testresult for testcases.

        SOURCE OF IDS 2OF2: the application user and/or pytest user buys and sells products and by doing so also 
        makes the app create ids.
        2 use cases:
        1. as a supermarket-logistics-employee-user of superpy create new data in the production application .
        2. as pytest create the file with the actual testresult. 


        To avoid source 1 and 2 accidentally create a buy or sell record with the 
        same id, I stick to the following convention:
        testdata id range: b_01 until b_299 included.
        testdata id range: s_01 until s_299 included.
        To create testdata this range is big enough.

        id range for supermarket-user and/or pytest-user of application: b_300 and higher.
        id range for supermarket-user and/or pytest-user of application: s_300 and higher.

        fn make_id_for_each_row_in_csv_file must be able to accommodate these 2 ranges
        in such a way that "id clashes" between testdata-generated-by-script on the one hand and on the other hand data created by supermarket-user and/or pytest-"engine"-user will be avoided. 
        (2do implement this in branch_05_uc_buy_product)

        About the user-friendliness of the id:
        When user sells a product via commandline, then id of bought product (e.g. b_128) must be entered.
        When a user deletes a product via commandline, then id of bought product (e.g. b_79) must be entered.

        So to keep things user-friendly, an id should not be too lengthy:

            import uuid
            unique_id = uuid.uuid4()
            print(unique_id)   
            output: e.g.: d7fbc5c8-8772-4629-9aad-6af354964341

            It would be very user-unfriendly to type in such an id when deleting e.g. a product with such an id.


    - uc 04: sell product (and add to sold.csv)
 
        pyt fn:
        def sell_product(productType, pricePerUnit, sellDate):
        
        shell command plus argparse arguments:
        py s.py sell apple 13.50 18 

    - uc 05: calculate inventory on day x (in range 1 to 60 inclusive)

        pyt fn:
        def calculate_inventory(system_date, productType):
        productType will be positional argument.
        
        shell command plus argparse arguments:
        py s.py show_inventory 18 
        py s.py show_inventory 18 --productType apple

    - uc 06: calculate expired products on day x (in range 1 to 60 inclusive)

        pyt fn:
        def calculate_expired_products(system_date, productType):
        productType will be positional argument.
        
        shell command plus argparse arguments:
        py s.py show_expired 18 
        py s.py show_expired 18 --productType apple

    - uc 07: calculate sales of number of products (Dutch: afzet). 
        --> serves as input to calculate revenue 
        (maybe skip this one, because same products (e.g. apples) can (and will) be bought 
        at different prices. In that case calculating an average sales price
        would be pointless)

        (probably skip this)

    - uc 08: report revenue in time range

        pyt fn:
        def calculate_revenue(system_date, productType):
        productType will be positional argument.
        
        shell command plus argparse arguments:
        py s.py calc_revenue 18 
        py s.py calc_revenue 18 --productType apple (implement if time left)

    - uc 09: report profit in time range

        pyt fn:
        def calculate_profit(system_date, productType):
        productType will be positional argument.
        
        shell command plus argparse arguments:
        py s.py calc_profit 18 
        py s.py calc_profit 18 --productType apple (implement if time left)   

    - uc 10: delete product (e.g. an expired one)
        (This is not a requirement. So only implement if there is time left. )

        First read uc 03 above. Uc 03 states:
        Rule: each id in buy.csv (e.g. b_08) and sell.csv (e.g. s_08) MUST be unique.

        In addition to this: After deleting a record (e.g. b_131 apple 0.50, 24-03-04, 24-03-04).
        an id (here: b_131) should not be reused.

        pyt fn:
        def delete_row_in_csv_file_bought(id):
        
        shell command plus argparse arguments:
        py s.py del_bought 43 
        legenda: delete row from BOUGHT.csv with id 43
    
        pyt fn:
        def delete_row_in_csv_file_sold(id):
        
        shell command plus argparse arguments:
        py s.py del_sold 43  
        legenda: delete row from SOLD.csv with id 18. 

        
        design / implementation issues / choices: 
        1. For each bought product that I want to delete (e.g. milk has expired / is out of date ), I must first check if
        the product has not already been sold.
        If it has been sold, then this product cannot be removed (not without 'cooking the books').

        2. a product can be deleted if it has expired, but also if it has not yet expired.

8.  create the argparse user interface:
    in argparse assign a subparser to each use case from step 7.  
    make choices about positional vs optional arguments, etc.
    Goal: make sure the superpy-app is easy and  intuitive to use.
    The argparse-code itself will be created later on. 

    status: done. Argparse-UI has been added to step 7 above.

9.  Create testdata in script create_testdata_for_csv_files_bought_and_sold.py 
    (erd in previous step must be ready before creating testdata)
    
    The testdata is necessary to work in a TDD-fashion. 
    This script can make custom testdata to test each fn from section 
    'List with fn signatures and argparse-command signatures:' above individually. 

    The testdata is very specific. Imho: quicker to create testdata myself, rather than 
    to create it on e.g. mockaroo.com and tweak it subsequently.

    table bought.csv:
        Use built-in fn enumerate to dynamically create values for the columns ID.

        Use product-fn from itertools library to create testdata for fields productType and 
        pricePerUnit in table bought.csv

        buy_date for each buying transaction gets a value in day range 1 to 55 inclusive. 
        expiryDate is 5 days after buy_date.

    table sold.csv:
        sold.csv is a copy of bought.csv
        For each row in  sold.csv a foreign key refers to primary key in bought.csv
        Each 5th bought product will expire.
        The other products will be sold for 3 times the price they were (each individually) bought for.        
        sold_date is 2 days after buy_date.

    status: done

10. coding methodology for each uc: implement each use case in its own TDD-iteration
    Perform the following steps iteratively for each use case from chapter 'List with fn signatures and argparse-command signatures' above. 
    Workflow: 
    a. take the first use case: set_system_date_to . Each use case at this point already has:
       - fn-signature. 
       - signature to call fn with argparse
    b. in utils.py create fn set_system_date_to with return pass as fn-body.
    c. in test_utils.py create a directory fn__test_set_system_date_to. This directory will
        contain testdata, actual results, expected result, etc. By experimenting I 
        have figured out what exactly I need in this directory for each testcase.
    
    d.  if a fn modifies only a system_date.txt (e.g. set_system_date_to), then script
        create_testdata_for_csv_files_bought_and_sold.py need not provide any data.
        elif a fn modifies bought.csv or sold.csv, then the script does need to 
        provide data.

    e.  At this point all testcases will fail, because the fn-body of the "fn under test"
        is still empty at this point. 



    f. in utils.py implement fn-body (i.e. "code that does stuff") of 
        fn-signature set_system_date_to. The code is ready as soon as all testcases pass.
        Then call this fn from main.py and check if it sets the system_date correctly.
       
    g. in main.py create argparse code that calls fn set_system_date_to . Testing the 
        argparse interface itself e.g. with a bash script is out of scope.


    h. take the next use case from step 4: uc time travel in time range
        (repeat the steps above)

    i. about os.getcwd():
        When using the superpy application via argparse, then  data is always stored inside folder data_directory inside project superpy.
        So os.getcwd() is static (i.e. always the same) when I run main.py from the command line.
        By comparison: when I run pytest, os.getcwd() is dynamic, i.e. different for each directory that 
        contains 1 [or more] testcases to test a fn from utils.py: ex of such a directory: fn_set_system_date_testcase_01

    j. during the (iterative) coding of a uc (e.g. calculate_profit) all testcases for this uc, 
        together will all testcases for all the already implemented ucs  (i.e. the regression test)
        can be tested inside project superpy via the cli with the default command 'pytest'. 
        

        I will use the first uc, set_system_date_to, as a proof of concept to implement, adjust and polish my intended TDD methodology. 
        Then I use the resulting TDD methodology to implement the remaining ucs. 
        If needed I make adjustments to the TDD methodology on-the-fly.


        bird's-eye view: For TDD of each uc I need 6 "things" / deliverables: 
        I. fn that performs some data manipulation in system_date.txt, bought.csv or sold.csv. Each fn will be
            developed with TDD. Each fn will be invoked via argparse-cli. The argparse-cli development
            itself is out of scope for TDD.
        II. test-fn in pytest
        III. fn-input (not all are used in each fn): 
            - some data (e.g. a string system_date, a product to buy, a product to sell, etc.) --> mandatory fn-parameter.
            - file path (to system_date.txt, bought.csv or sold.csv). --> 1 of 3 is mandatory fn-parameter.

            - a file system_date.txt is also a fn-input, but only if the goal is to update file system_date.txt.
              a file bought.csv or sold.csv (not both at the same time) is also fn-input, but only if the goal 
                is to update bought.csv or sold.csv (with either a bought or sold product).
              --> 1 of 3 file types is mandatory fn-parameter.
            
            Script 'create_testdata_for_csv_files_bought_and_sold' creates testdata for each fn individually.

            filepath is fn-input, because I want the fn-output of (e.g. fn set_system_date_to) when running pytest testcase 
            to be stored in a testdirectory test_utils, but the same fn-output in "live production" in directory data_directory. ("structure follows strategy")

            file is fn-input to make the fn pure. Otherwise fn has side-effect(s).

        IV. actual_testresult == csv-file or txt-file --> created by running the fn from step 1.
        V. expected_testresult = csv-file or txt-file --> created manually upfront.
        VI. fn to compare two files: see filecmp.cmp from standard library for this. file.cmp takes 
            actual_testresult and expected_testresult as its parameters.

            ex:
            import filecmp
            def test_set_system_date_to():
                filecmp.clear_cache()
                set_system_date_to('2020-01-01')
                assert filecmp.cmp(actual_test_result_inside_file, expected_path_to_system_date)
                
                'expected_path_to_system_date' points to a txt-file that contains '2020-01-01' (if
                this test is supposed to pass). 


11. give error when trying to sell a product that is not in stock:  

    $ python super.py sell --product-name orange --price 2
    ERROR: Product not in stock.

    how2 implement:
    Inside fn sell_product check if products are available (so you don't end up selling a product that is not there).
    Implementation: On a system_date (e.g. day 53) inside fn sell_product where you want to sell an orange, call fn calculte_inventory and check if an orange is in stock on day 53 that can be sold.   


12. display the output (e.g. report profit) to pyt module tabulate 
    (more info: https://analyticsindiamag.com/beginners-guide-to-tabulate-python-tool-for-creating-nicely-formatted-tables/#:~:text=Tabulate%20is%20an%20open%2Dsource,for%20all%20types%20of%20formatting)

    
13. display the output (e.g. report profit) to pyt module matplotlib








