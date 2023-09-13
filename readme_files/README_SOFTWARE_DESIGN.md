


# INTRO
    To create application super.py I do the following:
    1. create ERD
    2. create fn to quickly create testdata for  bought.csv and sold.csv
    3. define the ucs to implement (e.g. buy_product, sell_product, etc.)
    4. define a workflow to implement each uc with Test Driven Development (TDD): in
       iteration first create testcases for a uc and then make testcases pass
       by developing the functionality. 
       Then the next iteration: create testcases for next uc and then make
       testcases pass by developing the functionality. 
       etc.



# TABLE OF CONTENTS:

# ANALYSIS
1. # DEFINITIONS

# DESIGN
1. # CREATE datamodel / ERD (entity relationship diagram)  
2. # CREATE FUNCTION create_testdata_for_csv_files_bought_and_sold.py 
3. # USE CASES (UCS):
        uc 01: set the system_date in time range
        uc 02: timetravel in time range.
        uc 03: buy product (and add to bought.csv) 
        uc 04: sell product (and add to sold.csv)
        uc 05: cancel_buy_transaction (cruD: Delete part 1)
        uc 06: cancel_sell_transaction (cruD: Delete part 2)
        uc 07: update_buy_transaction
        uc 08: update_sell_transaction

        uc 09 fill bought.csv and sold.csv with mock data via argparse cli.

        uc 10: calculate inventory on date
        uc 11: report expired products in time range between start_date and end_date inclusive
        uc 12: report sales of number of products (Dutch: afzet) in time range between start_date and end_date inclusive
        uc 13: report costs in time range between start_date and end_date inclusive
        uc 14: report revenue in time range between start_date and end_date inclusive
        uc 15: report profit in time range between start_date and end_date inclusive
4. # MVC: model, view, controller  
5. # TASKS (not UCS )
6. # TDD: CODING STEPS TO IMPLEMENT EACH EACH UC
7. # IMPLEMENTATION ORDER OF UCS and TASKS (mandatory and optional)





# ANALYSIS

1. # DEFINITIONS:

    date == calendar day == date object with string representation in format: '%Y-%m-%d', e.g. '2025-10-15'. --> 
        system_date is a date with a special purpose. See system_date below. 


    inventory == list of items, goods, or materials that a business or individual has in stock in a certain time_interval.
                 inventory depends on the system_date (see def of system_date below).
    

    markup is the amount of money a business adds to the cost of a product or service in order to make a profit.
        In super.py markup is calculated as a factor:
        cost-of-product   markup   sell_price
            1               3         3
            2               3         6
            3               3         9
            2.5             2         5
        (used in fn create_data_for_csv_files_bought_and_sold() )


    product_range == product_assortment == the amount of different products in a shop .
        e.g. ['apple', 'cabbage', 'beetroot'], or e.g. ['coffee', 'potato', 'orange']
        product_range is an operand in fn product from module itertools.
        So more products in product_range lead to more rows in bought.csv.
        (used in fn create_data_for_csv_files_bought_and_sold() )


    profit == total revenue minus total expenses in a certain time_interval
        ex: time_interval == from 23-09-12 until 23-12-15 (included)
        revenue    expenses     profit
        115.500     80.000      35.500
   

    record == transaction ==  line of text (i.e. the "transaction" ) in bought.csv or sold.csv that depicts 
                    the act of buying or selling a product (1 in each transaction) by the supermarket.  

    revenue == sum of each individual product * sales price of that product in a certain time_interval. 
        --> each product is bought and sold 1-unit-at-a-time, so revenue == sum of all sales prices of all sold proudcts
        in a certain time_interval. 
        So this definition deviates from the general definition of revenue: "average sales price * number of units sold".

    shelf_life == shelf_time == number of days between buying a product and its expiry_date.
        ex: buy an apple:
        buy_date    expiry_date     shelf_life
        23-09-12     23-09-19         7
        23-09-12     23-09-20         8
        (used in fn create_data_for_csv_files_bought_and_sold() )


     
    system_date is a date (see def of date above) that is perceived as "today" in the system. system_date is saved
        in file 'system_date.txt' in directory data_directory. 
        If you buy a product without explicitly setting a buy_date, then system_date will be used instead as default value. 
        Same for selling a product. 
        Variable system_date is a configurable can be used to timetravel. 


    time_interval == amount of time (e.g. 3 days, or 4 months and 2 weeks, etc.) between lower boundary and  
        higher boundary.
        (used in fn create_data_for_csv_files_bought_and_sold() )   


    "to report" == to calculate (e.g. inventory, see def above) + display the output of the calculation (e.g. in
        rich and/or matplotlib). The verb 'report' is used in the following ucs:
        uc 10: calculate inventory on date
        uc 11: report expired products in time range between start_date and end_date inclusive:
        uc 12: report sales of number of products (Dutch: afzet) in time range between start_date and end_date inclusive: 
        uc 13: report costs in time range between start_date and end_date inclusive:
        uc 14: report revenue in time range between start_date and end_date inclusive:
        uc 15: report profit in time range between start_date and end_date inclusive:


    turnover time == inventory turnover == the number of days between buying and selling a product  
        ex: sell an apple:
        buy_date    sell_date     turnover_time
        23-09-12     23-09-14         2
        23-09-12     23-09-15         3
        (used in fn create_data_for_csv_files_bought_and_sold() )



# DESIGN

1. # CREATE datamodel / ERD (entity relationship diagram)
    Goal: decide about how to connect csv-tables bought.csv and sold.csv.
    -- design idea 1: bought.csv and sold.csv not connected via primary and foreign keys 
        (tldr; bad idea for practical coding reasons).

        The supermarket strictly uses logistic principle FIFO (first in first out).

        The fields that connect the tables: 
        The tables bought.csv and  sold.csv share the field 'product_type'. 
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
        but you cannot trace (a product on the shelves nor) a sold product (in sold.csv) back to a transaction in bought.csv 
        (i.e. the transaction when this e.g. apple was bought by the supermarket).
    
        Suppose in the supermarket in the vegetable department in a fruit-display-container there are apples  mixed together 
        from 3 transactions in bought.csv and a client (by coincidence) selects apples from all 3 transactions in bought.csv,
        but not all apples from all 3 transactions. 
        When the client buys these apples the resulting transaction in sold.csv would need 
        to contain 3 foreign keys to the bought.csv file. Furthermore, some of the apples in all 3 transactions in bought.csv have now 
        been  sold, but not all of them...so how to account for this?
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
            id,product,amount,price,buy_date,expiry_date
            20,banana,5,3.1,20,25
            19,banana,6,2.5,18,23
            18,banana,3,1.25,17,22
            14,banana,3,2.5,14,19
            12,banana,6,1.25,13,17
        d. see entity_relationship_diagram (erd_superpy_old) to interpret this data.
        e. loop thru the data to determine which ones have expired.
        f. expected result: the following products have expired:
            14,banana,3,2.5,14,19  --> all 3 bananas have expired.
            12,banana,6,1.25,13,17 --> 3 out of 6 bananas have expired. The other 3 had already been sold.
        
        Now repeat this for all other products.
        QED: a lot of work / toil as a consequence of disconnecting bought.csv from sold.csv in the erd.


    -- design idea 2: use primary and foreign key to connect bought.csv and sold.csv (my choice)
        Winc assignment suggests the use of primary and foreign keys to connect bought.csv and sold.csv. 
        I connect each transaction  in sold.csv via a foreign key in sold.csv to a primary key
        in bought.csv 

        Rule: supermarket sells products in the same amount they were bought at.
            That makes it practical for the supermarket to sell products in the same amount they were bought at. 
            ex 1:
            'buy-transaction' (A) in bought.csv is connected to 'sell-transaction' (B) in sold.csv . 
            Now if A contains 10 apples, then B contains 10 apples too. 
            Suppose in B I only sell 5 apples, then there are 5 apples in A still unsold. This means that 
            calculating the expiry date does not only involve checking if A has been sold in B, but also
            if A has ENTIRELY been sold in B. Also calculating inventory, turnover and profit will be more work.
            So to keep it simple, I assume that the supermarket will sell products in the amounts they were 
            bought in.  
            ex 2:
            If I would buy e.g. buy 15 products in 1 transaction and then sell 7 products from this transaction, then 
            I need a book keeping mechanism to book the remaining 8 products in store. 
            I do not want to go  down that "accounting" rabbit hole.

        Rule: supermarket buys and sells products in the amount of 1 at a time.
            To simplify this further, I assume that the supermarket will buy and sell products in 
            amounts of ONE at a time, because this will make calculating inventory, turnover and profit easier. 
            
            So A and B are about 1 product at a time.

            This seems ok according to the example code in winc assignment:
            $ python super.py sell --product-name orange --price 2
            OK
            analysis: 1 orange is sold at a certain price. 
        
            So I can do this as well:
            $ python super.py buy --product-name orange --price 2
            OK
            analysis: 1 orange is bought at a certain price. 
            Both transactions are connected via primary and foreign key. 

            another ex: 
            $ python super.py sell --product-name orange --price 2
            OK
   
        Rule: field ID in tables bought.csv and sold.csv must comply with the following:
            Each ID must be unique.
            Each ID must work like a counter.
            Each ID must specify its identity (i.e. tell id in  bought.csv apart from id in sold.csv).
            Each ID must be brief, because selling a product will look like this:

            py super.py sell s_8 5.30
            This means:
            py = python
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


        Rule: you can buy any type of product. 
            ex:
            py super.py buy apple 0.20 --> super.py generates id, e.g. b_190, for appended row in bought.csv
            py super.py buy quinoa 1.20 --> super.py generates id, e.g. b_191, for appended row in bought.csv
            etc.

        Rule: for each new buy transaction you can manually set the price:
            py super.py buy apple 0.20  --> super.py generates id, e.g. b_194, for appended row in bought.csv

            Rule: for each new sell transaction you can manually set the price:
            py.super.py sell s_194 0.50   --> so I refer to the transaction where I bought the apple: e.g. take b_194, then
                    replace the 'b' by 's'. 

            The profit is delta between b_194 and s_194. So here  profit is  0.30 euro.

            Another ex:
            py super.py buy quinoa 1.20  --> system generates id 'b_188'
            py super.py sell s_188 0.70
            
            (loss: 0.50 euro --> perhaps quinoa is on sale  to attract  customers)



    The  erd contains 3 tables: bought.csv , sold.csv , system_date.txt.
    First read chapter analysis --> paragraph 'datamodel / erd' above.
    I use tool mermaid to create erd. 
    See created 'erd_superpy.png' in project directory 'entity relationship diagram'.

    bought.csv and sold.csv connect via primary and foreign keys. 
    The primary and foreign keys are ids. 
    ex:
    if b_108 is primary key in bought.csv that belongs to a record that indicates the purchas of a product, then s_108 becomes
    the primary key in sold.csv when this product is sold.
    For this transaction in sold.csv b_108 is added  as foreign key to bought.csv. 

    Each buy-transaction buys 1 product.
    Each sell-transaction sells 1 product.



2.  # CREATE FUNCTION create_testdata_for_csv_files_bought_and_sold() 
    precondition: ERD (see prev par) must be ready before creating script.

    Fn create_data_for_csv_files_bought_and_sold() has 2 purposes:
    1. provide pytest testcases (path: (...)superpy\dir test_utils) with testdata, both input as well
        as expected output to test a fn.

        This data is created in directory: (...)\superpy\data_pytest_create_boughtcsv_and_soldcsv_for_pytestcases_here
        with script 'create_testdata_for_csv_files_bought_and_sold.py'. The created files bought.csv and  sold.csv
        are then moved to the relevant testcases inside directory (...)\superpy\test_utils. 

    2. provide application superpy with start data. In file super.py (path: (...)superpy\super.py)
        via argparse subparser ('generate_mock_data' or something similar) superpy-user can fill
        the application with data.

    The scope here is to get this fn to work. Then in  'uc 09 fill bought.csv and sold.csv with mock data via argprse cli'
    the goal is to call this fn via argparse cli.

    The script by default creates random transactions in bought.csv and sold.csv 

    Fn create_testdata_for_csv_files_bought_and_sold() has the following configurable options:
        product_range
        delete_every_nth_row,
        shelf_life,
        turnover_time,
        markup,
        lower_boundary_year_of_time_interval_in_which_to_create_random_testdata,
        lower_boundary_month_of_time_interval_in_which_to_create_random_testdata,
        lower_boundary_week_of_time_interval_in_which_to_create_random_testdata,
        upper_boundary_nr_of_months_to_add_to_calculate,
        upper_boundary_nr_of_weeks_to_add_to_calculate,
        upper_boundary_nr_of_days_to_add_to_calculate,
        path_to_file_bought_csv,
        path_to_file_sold_csv,
        add_days_to_date,
        create_id_for_each_row_in_boughtcsv_while_script_generates_this_boughtcsv,
        generate_random_buy_date_for_buy_transaction_in_future_in_time_interval

        Inside this fn there is a long list with products from which to randomly select products
        to generate testdata. If needed, this list can also become a configurable fn-parameter.


    table bought.csv:
        Each row in bought.csv has an automatically generated unique primary key (e.g. b_1, b_2, etc.)

        Use product-fn from itertools library to create testdata by returning Cartesian product of 
        the provided  iterables product and price (so 2 iterables in total).
 
        math highschool analogy: (5+2)*(3+4) == 5*3 + 5*4 + 2*3 + 2*4:
        (5+2)*(3+4) == 5*3 + 5*4 + 2*3 + 2*4 == (5,2)*(3,4) == (5,3) + (5,4) + (2,3) + (2,4)
        While reading this, suppose 5 and 3 are products and 2 and 4 are price_per_unit.
        Then 2 products and 2 price_per_unit result in 4 combinations == 4 bought products == 4 rows in bought.csv.
        Then 4 products and 3 price_per_unit result in 12 combinations == 12 bought products == 12 rows in bought.csv.


        Add columns buy_date and expiry_date

        Ex of bought.csv: 
        id,product,price,buy_date,expiry_date
        b_1,eggs,0.5,2023-10-01,2023-10-06
        b_2,eggs,1.1,2023-10-01,2023-10-06
        b_3,eggs,1.4,2023-10-02,2023-10-07
        b_4,kiwi,1.1,2023-10-03,2023-10-08
        b_5,lettuce,1.1,2023-10-11,2023-10-16
        b_6,lettuce,1.4,2023-10-13,2023-10-18
        b_7,lettuce,2.5,2023-10-16,2023-10-21
        b_8,fish,4.0,2023-10-16,2023-10-21
        b_9,lettuce,3.1,2023-10-17,2023-10-22


    table sold.csv:
        sold.csv is a deepcopy of bought.csv
        For each row in  sold.csv a foreign key refers to primary key in bought.csv
        Each 'nth' (e.g. 3rd) bought product will expire.
        The other products will be sold for "n" (e.g. 4) times the price they were (each individually) bought for.        
        sold_date is "t" (e.g. 5) days after buy_date.

        Ex of bought.csv sample: 
        id_sold,id_bought,product,price,sold_date,expiry_date
        b_1,s_1,eggs,1.5,2023-10-03,2023-10-06
        b_3,s_3,eggs,4.2,2023-10-04,2023-10-07
        b_5,s_5,lettuce,3.3,2023-10-13,2023-10-16
        b_7,s_7,lettuce,7.5,2023-10-18,2023-10-21
        b_9,s_9,lettuce,9.3,2023-10-19,2023-10-22
        b_11,s_11,eggs,9.3,2023-10-21,2023-10-24
        b_13,s_13,kiwi,12.0,2023-10-26,2023-10-29
        b_15,s_15,kiwi,7.5,2023-10-29,2023-11-01
        b_17,s_17,lettuce,12.0,2023-10-30,2023-11-02



3.  # USE CASES
   - intro
        If a uc is about implementing a fn, then in the uc the following 2 signatures are provided:
        1. fn-signature (e.g. buy_product(product, price, buy_date, expiry_date))
        2. argparse-command signature (e.g. py main.py product, price, buy_date, expiry_date) 
        
        To ensure good user experience / usability of the superpy-cli-app, the
        arparse user interface gets attention in an early stage, before any code is written. 

        Each fn will be implemented with its own argparse-subparser.  

        As far as possible, upfront choices are made about positional vs optional arguments, etc., 
        so the superpy-app will become easy and  intuitive to use.

        While creating the fn- and arparse-signatures, I check if they are compatible with the created ERD.


    - uc 01: set the system_date in time range
        This creates a baseline to timetravel ('back to the future, yeah, here I come')

        Order of events: 
        A value for date object (e.g. day 16) is a prerequisite for buying and selling products
        and all subsequent use cases below.

        pyt fn:
        def set_system_date_to(system_date):

        
        shell command plus argparse arguments: 
        py super.py set_date 2020-02-25   (status: works)
       
        About the name 'super.py': 
        Abbreviating super.py to e.g. s.py does not mean less typing in the command line:
        To enter s.py you:
        1. type 's'
        2. kb TAB triggers auto completion.
        3. kb SPACE

        To enter super.py you do exactly the same. So I use the more descriptive super.py instead of "s.py".


    
    - uc 02: timetravel in time range.
        example code: $ py main.py time_travel 2

        To 'advance' means to move forward in purposeful way. But this superpy-app can also timetravel to 
        the past. So I use 'timetravel' as a verb instead of 'advance'.  
        Implement Argparse argument 'timetravel' inside a subparsers with a positional argument. 
        (use timedelta from module datetime to implement)

        pyt fn: 
        def time_travel(nr_of_days_to_set_system_date_to_future_or_past):

        shell command plus argparse arguments:
        (super.py abbreviated as s.py so less repetitive typing)
        py super.py time_travel -2 
        legenda:
        positive nr: to the future. e.g. 7 is 7 days to the future
        negative nr: to the past. e.g. -4 is 4 days to the past  
        
        Order of events:
        The ability to timetravel must be in place in order to implement any use case that requires
        the presence of a range (e.g. report profit in day range 17 to 43 inclusive). 



    - uc 03: buy product (and add to bought.csv) 

        pyt fn:
        def buy_product(product_type, price_per_unit, buy_date, expiryDate):
        
        shell command plus argparse arguments:
        py super.py buy apple 4.50 23-09-07 23-09-20 

        design:
        fn-parameter buy_date in argparse is optional argument with default value 'system_date'.
        The current value for 'system_date' will be fetched dynamically from file 'system_date.txt' in
        diretory 'data_directory'.

        Rule 1: each id in buy.csv (e.g. b_08) and sell.csv (e.g. s_08) MUST be unique.
        Rule 2: an id (e.g. b_08 or s_08) can only be used once. purchasing and selling is the heart of the 
        superpy application.  So each purchase and sale must be traceable.

        There are 2 different SOURCES that create ids in the application (each record in bought.csv and
        sold.csv starts with an id):
        SOURCE OF IDS 1OF2: script create_testdata_for_csv_files_bought_and_sold creates ids.
        3 use cases for this script:
        1. start the production application with real-looking data.
        2. create input files for testcases.
        3. create expected testresult for testcases.
        The script use fn make_id_for_each_row_in_csv_file() from file  utils.py.

        SOURCE OF IDS 2OF2: the application user and/or pytest-"engine"-user buys and sells products and by doing so also makes the superpy-app create ids.
        2 use cases:
        1. as a supermarket-logistics-employee-user of superpy create new data in the production application .
        2. as pytest create the file with the actual testresult. 
        superpy-app keeps track of the next-id-to-use in file id_to_use_in_fn_buy_product.txt in directory data_directory.

        To avoid source 1 and 2 accidentally create a buy or sell record with the 
        same id, I stick to the following convention:

        SOURCE OF IDS 1OF2:
        testdata id range: b_01 until b_299 included.
        testdata id range: s_01 until s_299 included.
        For the 3 ucs above this range is big enough.

        SOURCE OF IDS 2OF2:
        id range for supermarket-user and/or pytest-user of application: b_300 and higher.
        id range for supermarket-user and/or pytest-user of application: s_300 and higher.

        fn make_id_for_each_row_in_csv_file must be able to accommodate these 2 ranges
        in such a way that "id clashes" will be avoided between both sources of IDs. 


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
        Rule 1: each id in buy.csv (e.g. b_08) and sell.csv (e.g. s_08) MUST be unique.
        Rule 2: a primary key id in sold.csv can only be created if there is a primary key in
            bought.csv with the same nr. examples:

            create s_17 based on b_17.
            Reason: not possible to sell a product that has not been bought.

        Rule 3: a product can only be sold once. 
            e.g. if b_17 in bought.csv has been sold, then a record s_17 in sold.csv exists. If so,
            then b_17 cannot be sold a second time ("you cannot have your cake and eat it too")

        pyt fn:
        def sell_product(product_type, price_per_unit, sell_date):
        product_type is positional parameter.
        price_per_unit is positional parameter.
        sell_date is optional argument with 'system_date' as default value.
        
        shell command plus argparse arguments:
        py super.py sell apple 4.50 23-09-10  --> taking 23-09-10 as sell_date
        py super.py sell apple 4.50  --> taking system_date as default sell_date.

        Rule 4: error if you If you try to sell product that has not been bought (so is not in the inventory)
            ex: there is no buy-transaction with id b_1004, then 
            the following argparse command will raise an exception:
            
            py.super.py sell s_1004 0.50 
            output:
            ERROR: Product not in stock.


    - uc 05: cancel_buy_transaction (cruD: Delete part 1)
        
        Rule 1: a bought product can be sold if it has not yet been sold. (exception: see rule 4)
        Rule 2: a bought product cannot be deleted if it has already been sold.

        Rule 3: After cancelling (== deleting) a record from bought.csv (e.g. b_131 apple 0.50, 24-03-04, 24-03-14).
        an id (here: b_131) should not be reused.

        pyt fn:
        def cancel_buy(id):
        
        shell command plus argparse arguments:
        py super.py cancel_buy b_131 
        legenda: delete row from BOUGHT.csv with id b_131

        Rule 4: after cancelling a sold transaction (see next uc: cancel_sell_transaction) (e.g. s_179), the 
            buy_transaction (here: b_179) can  now also be cancelled. 
    
    - uc 06: cancel_sell_transaction (cruD: Delete part 2)
        
        Rule 1: a sale (i.e. the sales transaction) of a product can  be undone / cancelled. 
        Rule 2: also the sales transaction of an  expired  product can be cancelled: it does 
            not matter if product has expired for the act of cancelling.

        Rule 3: After cancelling (== deleting) a record from sold.csv (e.g. s_131 apple 1.50, 24-03-06, 24-03-14).
        an id (here: s_131) should not be reused.

        pyt fn:
        def cancel_sell(id):
        
        shell command plus argparse arguments:
        py super.py cancel_sell s_131 
        legenda: delete row from SOLD.csv with id s_131
        (maybe abbreviate 'cancel_sell' to 'cs')
        
        design / implementation issues / choices: 
        1. For each bought product that I want to delete (e.g. milk has expired / is out of date ), I must first check if
            the product has already been sold.
            If it has been sold, then this product cannot be removed (not without 'cooking the books').

        2. a product can be deleted if it has expired, but also if it has not yet expired.

        (implement only if there is time left)        

    - uc 07: update_buy_transaction

        update_buy_transaction = cancel_buy_transaction (uc 05) + buy_product (uc 03)
        So to update you first do cancel_buy_transaction (uc 05) and then buy the same product
        with the updated information (uc 03)     
        
        update can be handy to correct info. E.g. if you enter a bought product into super.py with e.g.
        incorrect buy_date and/or expiry_date, then the combination of uc 05 and uc 03 allows you 
        to correct the data.

        So in uc 07 the same business rules apply as in uc 05 and uc 03.

        Nothing to do here.
        

    - uc 08: update_sell_transaction

        update_sell_transaction = cancel_sell_transaction (uc 06) + buy_product (uc 04)
        So to update you first do cancel_buy_transaction (uc 06) and then buy the same product
        with the updated information (uc 04)     
        
        update can be handy to correct info. E.g. if you enter a sold product into super.py with e.g.
        incorrect sell_date and/or sell_price, then the combination of uc 06 and uc 04 allows you 
        to correct the data.

        So in uc 08 the same business rules apply as in uc 06 and uc 04.

        Nothing to do here.



    - uc 09: fill bought.csv and sold.csv with mock data

        goal: call fn def create_data_for_csv_files_bought_and_sold() in utils.py from argparse interface
              to quickly create specific (test) application data.
              Feature: this will overwrite all data in both bought.csv as well as sold.csv, that
              has been added to both files. 
              2 scenarios:
              1. there is no data or not enough in both files, but you want to e.g. calculate inventory, turnover, 
                profit (etc.) over a certain period with  certain quantity and composition of data.
              2. current data in  both  files has become too cluttered and you need a reset.


        pyt-fn: (status: working )
            def create_data_for_csv_files_bought_and_sold(
                product_range
                delete_every_nth_row_in_soldcsv_so_every_nth_row_in_boughtcsv_can_expire_when_time_travelling,
                shelf_life,
                turnover_time,
                markup,
                lower_boundary_year_of_time_interval_in_which_to_create_random_testdata,
                lower_boundary_month_of_time_interval_in_which_to_create_random_testdata,
                lower_boundary_week_of_time_interval_in_which_to_create_random_testdata,
                upper_boundary_nr_of_months_to_add_to_calculate,
                upper_boundary_nr_of_weeks_to_add_to_calculate,
                upper_boundary_nr_of_days_to_add_to_calculate,
                path_to_file_bought_csv,
                path_to_file_sold_csv,
                add_days_to_date,
                create_id_for_each_row_in_boughtcsv_while_script_generates_this_boughtcsv,
                generate_random_buy_date_for_buy_transaction_in_future_in_time_interval
            ):     

        shell command plus argparse arguments:
        All arguments in this fn are optional arguments with a default value:
    
       
        py super.py create_data -product_range 5       default value: 3
        (2 flags for the same parameter: -pr, -product_range)

        py super.py create_data -delete_every_nth_row 5       default value: 3
        (2 flags for the same parameter: -del_row,  -delete_every_nth_row)

        fn creates data for bought.csv. Then to create sold.csv a deepcopy is made from
        bought.csv . Then rows are deleted from sold.csv (e.g. every 3rd row).
        By time travelling to the future these bought_products (e.g. every 3rd row)
        will expire. 

        py super.py create_data -shelf_life 4       default value: 2
        (2 flags for the same parameter: -sl, -shelf_life)

        py super.py create_data -turnover_time 4       default value: 2
        (2 flags for the same parameter: -tt, -turnover_time)

        py super.py create_data -markup 2       default value: 3
        (2 flags for the same parameter: -mu, -markup)

        py super.py create_data -lby 2024       default value: 2023
        (2 flags for the same parameter: -lby, -lower_boundary_year)

        py super.py create_data -lbm 11       default value: 10
        (2 flags for the same parameter: -lbm, -lower_boundary_month)       

        py super.py create_data -lbw 2       default value: 4
        (2 flags for the same parameter: -lbw, -lower_boundary_week)   

        py super.py create_data -uby 1       default value: 0
        (2 flags for the same parameter: -uby, -upper_boundary_year)

        py super.py create_data -ubm 1       default value: 0
        (2 flags for the same parameter: -ubm, -upper_boundary_month)       

        py super.py create_data -ubw 2       default value: 4
        (2 flags for the same parameter: -ubw, -upper_boundary_week)   

        The remaining fn-arguments are NOT supposed to be changed via argparse-cli: 
            path_to_file_bought_csv,
            path_to_file_sold_csv,
            add_days_to_date,
            create_id_for_each_row_in_boughtcsv_while_script_generates_this_boughtcsv,
            generate_random_buy_date_for_buy_transaction_in_future_in_time_interval


    - uc 10: calculate inventory on date

        When calculating inventory something special is happening:
        The inventory is calculated as the state at the end of a time range, just
        like when calculating profit, revenue, costs, expired products, etc. 
        
        But unlike when  calculating profit, revenue, etc., as a super.py-user 
        you CANNOT choose the lower boundary of the time range yourself. Instead, the lower 
        boundary is ALWAYS the date on which the first product has been bought.
        ex: 
        week 1: buy 300 tins of beans 
        week 2: buy 300 tins of beans
        week 3: sell 300 tins of beans 
        suppose you look at the inventory of week 2 and 3 (and ignore the inventory of week 1)
        then the inventory at the end of week 3 would be: 0 tins of beans...but this is nonsense, because
        you still have 300 tins of beans from week 1.
        qed: lower boundary of time range is the date on which you (have) bought the first product. 



        It is management responsibility to ensure that there are always 
        products available to sell at any given system_date. 
        
        pyt fn:
        def calculate_inventory(product_type, start_date, end_date):
        product_type is optional argument with "all products" as default value.
        start_date is positional argument.
        end_date is optional argument with 'system_date' as default value.
                
        shell command plus argparse arguments:
        optional argument with 'system_date' as default value. 
        py super.py inventory -p apple 230909  --> setting an end_date. "give me inventory of apples on 23-09-09". 
        py super.py inventory -p coconut --> "give me inventory of coconut on system_date".  
        py super.py inventory --> "give me inventory of all products on system_date".  

        (-p is flag for 'product_type')

        perhaps shorten inventory to inv.

        result is shown in a table:
        column 1: product_type
        column 2: nr of products unsold and not yet expired.

        e.g. 
        py s.py inventory 230909 
        output:
        product_type    inventory:  
        apple           3
        pear            5
        etc.

        ex 2:
        py s.py inventory -p apple 230909 
        product_type   id       purchase_price  buy_date        expire_date  
        apple          b_5          0.20        2023-09-05      2323-09-20
        apple          b_12         0.25        2023-09-07      2323-09-22
        apple          b_100        0.50        2023-09-09      2323-09-24

        This info is necessary before you can decide to sell a product (e.g. sell b_5 as s_5) 
        for a certain price (e.g. 0.40 would be profitable but selling for 0.20 is acceptable if 
        b_5 is about to expire)


    - uc 11: calculate expired products in time range between start_date and end_date inclusive

        pyt fn:
        def calculate_expired_products(product_type, start_date, end_date):
        product_type is optional argument with "all products" as default value.
        start_date is positional argument.
        end_date is optional argument with 'system_date' as default value.
                
        shell command plus argparse arguments:
        py super.py expired 230709 230909 
        py super.py expired -p apple  230709 230909
        py super.py expired 230709  
        (-p is flag for 'product_type')

        Perhaps shorten expired to exp.
        
        (implement if time left) 

        (2 flags: calculate_expired , ce)

    - uc 12: calculate sales of number of products (Dutch: afzet) in time range between 
        start_date and end_date inclusive 
        --> also serves as input to calculate revenue 

        pyt fn:
        def calculate_sales_number(product_type, start_date, end_date):
        product_type is optional argument with "all products" as default value.
        start_date is positional argument.
        end_date is optional argument with 'system_date' as default value.

        shell command plus argparse arguments:
        py super.py sales_nr 230709 230909 
        py super.py sales_nr -p apple  230709 230909
        py super.py sales_nr 230709  
        (-p is flag for 'product_type')
        
        (implement if time left) 

    - uc 13: report costs in time range between start_date and end_date inclusive
        --> also serves as input to calculate revenue 

        pyt fn:
        def calculate_costs(product_type, start_date, end_date):
        product_type is optional argument with "all products" as default value.
        start_date is positional argument.
        end_date is optional argument with 'system_date' as default value.

        shell command plus argparse arguments:
        py super.py cost 230709 230909 
        py super.py cost -p apple  230709 230909
        py super.py cost 230709  
        (-p is flag for 'product_type')
        
        (implement if time left) 

    - uc 14: report revenue in time range between start_date and end_date inclusive

        pyt fn:
        def calculate_revenue(product_type, start_date, end_date):
        start_date is positional argument.
        end_date is optional argument with 'system_date' as default value.
        product_type is optional argument with "all products" as default value.
        

        shell command plus argparse arguments:
        py super.py revenue 230709 230909 
        py super.py revenue -p apple  230709 230909 
        py super.py revenue 230709 
        (-p is flag for 'product_type')
        
        (implement if time left)

    - uc 15: report profit in time range between start_date and end_date inclusive

        pyt fn:
        def calculate_profit(product_type, start_date, end_date):
        start_date is positional argument.
        end_date is optional argument with 'system_date' as default value.
        product_type is optional argument with "all products" as default value.
        
        shell command plus argparse arguments:
        py super.py profit 230709 230909 
        py super.py profit -p apple  230709 230909
        py super.py profit 230709  
        (-p is flag for 'product_type')
        
        (implement if time left) 

 




4. # MVC: model, view, controller 

    Looking at the ucs from previous chapter 3 from a bird's-eye view:

    MODEL LAYER (MVC-model):
        The following ucs are in the Model layer (MVC-model) because they change state:
        uc 01: set the system_date in time range
        uc 02: timetravel in time range.
        uc 03: buy product (and add to bought.csv) 
        uc 04: sell product (and add to sold.csv)
        uc 05: cancel_buy_transaction (cruD: Delete part 1)
        uc 06: cancel_sell_transaction (cruD: Delete part 2)
        uc 07: update_buy_transaction
        uc 08: update_sell_transaction

        They combine all CUD-operations (create, update, delete) that are allowed (within 
        the constraints of the rules in these ucs) on system_date.txt, bought.csv and sold.csv .
        These are the basic operations that must be in place before moving on
        with the following ucs (imho). 

        Uc 09 creates realistic mock data via argparse interface, so as a super.py-user you do not have 
        to start with entering a whole bunch of buy- and sell-records, before you can e.g. calculate
        the inventory, costs, turnover and/or profit over a certain period in the upcoming ucs.
        Uc 09 is also are in the Model layer (MVC-model) because it changes state.

    MODEL / VIEW LAYER (MVC-model):
        The following ucs are partly in the View layer and partly in the Model layer (MVC-model) of the application, 
        because if you change change system_date, then the produced reports (in e.g. rich and matplotlib) will also change
        uc 10: calculate inventory on date
        uc 11: report expired products in time range between start_date and end_date inclusive
        uc 12: report sales of number of products (Dutch: afzet) in time range between start_date and end_date inclusive
        uc 13: report costs in time range between start_date and end_date inclusive
        uc 14: report revenue in time range between start_date and end_date inclusive
        uc 15: report profit in time range between start_date and end_date inclusive

        "to report" == to calculate (e.g. inventory) + display the output of the calculation in tool 'rich' and 'matplotlib'.
        calculation-part is model.
        display-part is view.
        I have selected tool 'rich' instead of tool 'tabulate' because of the better rating on 
        https://www.libhunt.com/compare-python-tabulate-vs-rich (especially with regard to amount of stars)
        
    CONTROLLER LAYER (MVC-model):   
        The argparse cli in super.py ( (...)\superpy\super.py) acts as the controller between MODEL and VIEW. 

5. # TASKS (not UCS )
    - task 01: connect id-range of script 'create_testdata_for_csv_files_bought_and_sold' with id-range of 
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

        (not a requirement, so implement only if time left) 

    - task 01: write report (16 instead of uc 16 because this is not a uc)
        Please include a short, 300-word report that highlights three technical elements of your implementation that you find notable.    
        Explain what problem they solve and why you chose to implement them in this way.   
        Include this in your repository as a report.md file.

        Our tips regarding the report:

        You may consider using Markdown for your report.

        Markdown is a markup language you can use for styling your plain text. It is widely used in programming, so it could be a good choice, but it is not required.
        To assist your explanation you may use code snippets.    

        (this is a mandatory requirement)



6. # TDD: CODING STEPS TO IMPLEMENT EACH EACH UC
    coding methodology for each uc: implement each use case in its own TDD-iteration
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


7. # IMPLEMENTATION ORDER OF UCS and TASKS (mandatory and optional)
    I first implement the mandatory requirements about super.py from Winc Academy. If time left / permits,
    I will implement the rest as well.

    Develop all use cases (ucs) with TDD ( == non-trivial feature 1). See previous chapter 6 for explanation 
    of TDD-metholodogy. The code for each use case (uc) can be found in (...)\superpy\test_utils\"name of uc"
    "name of uc" can be e.g. "fn_buy_product_testcases". 

    - Mandatory Winc Academy Requirements: 2 implement first:
    uc 01: set the system_date in time range
    uc 02: timetravel in time range.
    uc 03: buy product (and add to bought.csv) 
    uc 04: sell product (and add to sold.csv)

    uc 09 fill bought.csv and sold.csv with mock data via argparse cli. ( == non-trivial feature 2)

    uc 14: report revenue in time range between start_date and end_date inclusive
    uc 15: report profit in time range between start_date and end_date inclusive        

    uc 14 and 15 display output in Rich ( == non-trivial feature 3)



    - extra optional features: 2 implement next (if time permits):
    uc 05: cancel_buy_transaction (cruD: Delete part 1)
    uc 06: cancel_sell_transaction (cruD: Delete part 2)
    uc 07: update_buy_transaction
    uc 08: update_sell_transaction
    
    uc 10: calculate inventory on date
    uc 11: report expired products in time range between start_date and end_date inclusive
    uc 12: report sales of number of products (Dutch: afzet) in time range between start_date and end_date inclusive
    uc 13: report costs in time range between start_date and end_date inclusive

    uc 14 and 15 display output in Matplotlib ( == non-trivial feature 4)






