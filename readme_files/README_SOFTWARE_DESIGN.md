
# ANALYSIS

1. # definitions:
    profit == total revenue minus total expenses
    revenue == average sales price * number of units sold.

    date == date object == calendar day.
    Format of calender day: the date object with string representation in format: '%Y-%m-%d'. 

    time range == a range of days between 1 (or higher) and 60 (or lower) inclusive. So 
                    maximum time range is 60 days and minimum time range is 1 day.

    record == transaction ==  line of text (i.e. the "transaction" ) in bought.csv or sold.csv that depicts 
                    the act of buying or selling products by the supermarket.  


    # 2 types of data:
    "original" data: bought products, sold products, system-date.
        system_date == ('the day that is today'). This date will be saved
        in file 'system_date.txt'

    "derived" data: inventory 
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
        the date field 'expiryDate' in table BOUGHT.csv and 'expiryDate' in table SOLD.csv.
        These date fields are nor primary key nor foreign key.

        design choice: the(se aforementioned) fields 'productType', 'system_current_date' and 
        'expiryDate' are used to combine these tables to generate the data required by the use cases
        in the 'list of use cases' further below.
        So although I have created an erd, the tables in the erd are not relational in the sense that 
        they are not connected to one another via primary and foreign keys (nor do they adhere to the other
        Codd's rules https://www.tutorialspoint.com/dbms/dbms_codds_rules.htm ).

        In a real-life supermarket most products (e.g. an apple, packet of milk, loaf of bread) only have a barcode, 
        but you cannot trace (a product on the shelves or) a sold product (in sold.csv) back to a transaction on bought.csv 
        (i.e. the transaction when this e.g. apple was bought by the supermarket).
    
        Suppose in the supermarket in the vegetable department in a fruit-display-container there are apples  mixed together 
        from 3 transactions in bought.csv and a client (by coincidence) selects apples from all 3 transactions in bought.csv. 
        When (s)he buys these apples the resulting transaction in sold.csv would need 
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
        QED: a lot of work for disconnecting bought.csv from sold.csv in the erd.


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

    - set the date in time range. 
        This creates a baseline to timetravel ('back to the future, yeah, here I come')

        Order of events: 
        A value for date object (e.g. day 16) is a prerequisite for buying and selling products
        and all subsequent use cases below.

        pyt fn:
        def set_the_date_in_time_range(system_date):

        (super.py abbreviated as s.py so less repetitive typing)
        shell command plus argparse arguments: 
        py s.py set_date 4   


    
    - timetravel in time range.

        example code: $ python super.py --advance-time 2

        To 'advance' means to move forward in purposeful way. But this superpy-app can also timetravel to 
        the past. So I use 'timetravel' as a verb instead of 'advance'.  
        Implement Argparse argument 'timetravel' inside a subparsers with a positional argument. 
        (use timedelta from module datetime to implement)


        pyt fn: 
        def time_travel(nr_of_days_to_set_system_date_to_future_or_past):

        shell command plus argparse arguments:
        (super.py abbreviated as s.py so less repetitive typing)
        py s.py time_travel -2 
        legenda:
        positive nr: to the future
        negative nr: to the past  


        Order of events:
        The ability to timetravel must be in place in order to implement any use case that requires
        the presence of a range (e.g. report profit in day range 17 to 43 inclusive). 


    

    - buy product (and add to bought.csv) 

        pyt fn:
        def buy_product(productType, pricePerUnit, buy_date, expiryDate):
        
        shell command plus argparse arguments:
        py s.py buy apple 4.50 16 20 

    - sell product (and add to sold.csv)
 
        pyt fn:
        def sell_product(productType, pricePerUnit, sellDate):
        
        shell command plus argparse arguments:
        py s.py sell apple 13.50 18 

    - calculate inventory on day x (in range 1 to 60 inclusive)

        pyt fn:
        def calculate_inventory(system_date, productType):
        productType will be positional argument.
        
        shell command plus argparse arguments:
        py s.py show_inventory 18 
        py s.py show_inventory 18 --productType apple

    - calculate expired products on day x (in range 1 to 60 inclusive)

        pyt fn:
        def calculate_expired_products(system_date, productType):
        productType will be positional argument.
        
        shell command plus argparse arguments:
        py s.py show_expired 18 
        py s.py show_expired 18 --productType apple

    - calculate sales of number of products (Dutch: afzet). 
        --> serves as input to calculate revenue 
        (maybe skip this one, because same products (e.g. apples) can (and will) be bought 
        at different prices. In that case calculating an average sales price
        would be pointless)

        (probably skip this)

    - report revenue in time range

        pyt fn:
        def calculate_revenue(system_date, productType):
        productType will be positional argument.
        
        shell command plus argparse arguments:
        py s.py calc_revenue 18 
        py s.py calc_revenue 18 --productType apple (implement if time left)

    - report profit in time range

        pyt fn:
        def calculate_profit(system_date, productType):
        productType will be positional argument.
        
        shell command plus argparse arguments:
        py s.py calc_profit 18 
        py s.py calc_profit 18 --productType apple (implement if time left)   

    - delete product (e.g. an expired one)
        (This is not a requirement. So only implement if there is time left. )

        The combination of timetravel, delete and buy and/or sell would make
        it possible to update and correct data. A system does not feel
        complete without this feature. 

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

8.  create the argparse user interface:
    in argparse assign a subparser to each use case from step 3.  
    make choices about positional vs optional arguments, etc.
    Goal: make sure the superpy-app is easy and  intuitive to use.
    The argparse-code itself will be created later on. 

    status: done. See section  7. above.

9.  Create testdata in script create_testdata_for_csv_files_bought_and_sold.py
     generate automated testdata in bought.csv and sold.csv 
      (erd in previous step must be ready before creating testdata)
    
    The testdata is necessary to work in a TDD-fashion. 

    The testdata is very specific, so I prefer to create it myself, rather than 
    to create it on e.g. mockaroo.com

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
        The other products will be sold for 3 times the price it was bought for.        
        sold_date is 2 days after buy_date.


10. Implement each use case in its own TDD-iteration
    Perform the following steps iteratively for each use case from chapter 'List with fn signatures and argparse-command signatures' above. 
    Workflow: 
    a. take the first use case: buy_product (each use case already has a fn-signature at this point)
    b. in utils.py create fn buy_product with return "foo" as fn-body.
    c. in test_utils.py create testfn test_buy_product. For input and output of testfn use testdata generated by script create_testdata_for_csv_files_bought_and_sold.py .
        Once completed, all testcases in the testfn are supposed to fail, because the 
        fn-body is still empty at this point. 

    c. in utils.py implement fn-body (i.e. "code that does stuff") of fn-signature buy_product
    d. in main.py create argparse code that calls fn buy_product
    e. in utils.py crud code until all testcases in test_buy_product pass. 

    e. take the next use case from step 4: use case sell_product
        (repeat the steps above)
        etc.




11. display the output (e.g. report profit) to pyt module tabulate 
    (more info: https://analyticsindiamag.com/beginners-guide-to-tabulate-python-tool-for-creating-nicely-formatted-tables/#:~:text=Tabulate%20is%20an%20open%2Dsource,for%20all%20types%20of%20formatting)

    
12. display the output (e.g. report profit) to pyt module matplotlib

13. give error when trying to sell a product that is not in stock:  

    $ python super.py sell --product-name orange --price 2
    ERROR: Product not in stock.

    how2 implement:
    Inside fn sell_product check if products are available (so you don't end up selling a product that is not there).
    Implementation: On a system_date (e.g. day 53) inside fn sell_product where you want to sell an orange, call fn calculte_inventory and check if an orange is in stock on day 53 that can be sold.






