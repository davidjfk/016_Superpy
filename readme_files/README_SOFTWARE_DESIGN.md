
# ANALYSIS

1. definitions:
    profit == total revenue minus total expenses
    revenue == average sales price * number of units sold.

    date == date object == calendar day.
    Format of calender day: the date object with string representation in format: '%Y-%m-%d'. 

    time range == a range of days between 1 (or higher) and 60 (or lower) inclusive. So 
                    maximum time range is 60 days and minimum time range is 1 day.

    record == transaction ==  line of text (i.e. the "transaction" ) in bought.csv or sold.csv that depicts 
                    the act of buying or selling products by the supermarket.  


    2 types of data:
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

    Argparse: 
    Application has 2 types of argparse-arguments (abbreviated as "actions"):

    a. actions that change state: buy, sell, setting the date (e.g. yesterday)
        This is the "model layer".

    b. actions that show (but do not modify) (part of or the entire) state on a certain moment: inventory, report 
        This is the "view layer".



# DESIGN

1.  various:
    The time horizon of the superpy app is (arbitrarily) 60 days (counting days starts at 1).

2. create erd to connect tables bought.csv and sold.csv . (done)
    As part of this determine the columns in each table. 

    3 tables: bought.csv , sold.csv , system_date.txt

    design choice: these tables are not connected via primary nor foreign keys.

    - The fields that connect the tables: 
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

    - practical considerations about connecting sold.csv and bought.csv:
        design choice: in sold.csv a foreign key to bought.csv is NOT needed.

        In a real-life supermarket most products (e.g. an apple, packet of milk, loaf of bread) only have a barcode, 
        but you cannot trace (a product on the shelves or) a sold product (in sold.csv) back to a transaction on bought.csv 
        (i.e. the transaction when this e.g. apple was bought by the supermarket).
    
        Suppose in the supermarket in the vegetable department in a fruit-display-container there are apples  mixed together 
        from 3 transactions in bought.csv and a client (by coincidence) selects apples from all 3 transactions in bought.csv. 
        When (s)he buys these apples the resulting transaction in sold.csv would need 
        to contain 3 foreign keys to the bought.csv file.

        There are a few supermarket products that could be traced back to the transaction in bought.csv:
        e.g. medication, eggs, magazines. But also these products can be sold without tracing them back.
        QED: no foreign key in sold.csv pointing to bought.csv

        Check if products are in inventory before selling them:
        Prior to selling a product (e.g. 10 apples) on a certain date (e.g. day 17) (in day range 1 to 60 inclusive), first check if there 
        are enough apples in the enventory that day. So inside the sell_product fn there is no check if there is enough inventory 
        of producttype apple.
        It is management responsibility to ensure (with fn calculate_inventory in combination with timetraveling) that there are always 
        products for a particular sale of products (e.g. 10 apples) to take place. 
        See point 10 'prevent selling sold out products' below at end of this document, that automates this check. 



    - practical consideration  about the field ID in tables bought.csv and sold.csv:
        The field ID is calculated dynamically. So if I delete a record from  bought.csv or sold.csv, then 
        the (some) other records could  get another dynamically created ID that is different from the ID before
        the delete action was executed. 
        There is no requirement about the persistency of IDs, so I assume that is not a problem. 
    
    - practical considerations about SYSTEM_DATE.csv:
        Variable system_current_date is a configurable / changeable and completely independent entity that 
        can be used to timetravel. By timetraveling the products of individual transactions in the table
        bought.csv expire, depending on the timedelta between system_current_date and the expiry_date of each
        individual transaction.  


3. Create fn update_csv_file to update data in a given csv file
    (status: done)
    This code serves as a baseline / template to create additional fns to CRUD csv-data.
    - read data (part of fn update_csv_file)
    - write data (part of fn update_csv_file)
    - append data ()  --> 2do.

4.  Create for following use cases the fn-signature (i.e. fn-name, fn-arguments, type of fn-arguments, return-variable, type of returned-var):    

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
        def timetravel(nr_of_days_to_set_system_date_to_future_or_past):

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
        def buy_product(productType, amountOfUnits, pricePerUnit, boughtDate, expiryDate):
        
        shell command plus argparse arguments:
        py s.py buy apple 9 4.50 16 20 

    - sell product (and add to sold.csv)
 
        pyt fn:
        def sell_product(productType, amountOfUnits, pricePerUnit, sellDate):
        
        shell command plus argparse arguments:
        py s.py sell apple 9 13.50 18 

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

        (skip this)

    - report revenue in time range

        pyt fn:
        def calculate_revenue(system_date, productType):
        productType will be positional argument.
        
        shell command plus argparse arguments:
        py s.py calc_revenue 18 
        py s.py calc_revenue 18 --productType apple

    - report profit in time range

        pyt fn:
        def calculate_profit(system_date, productType):
        productType will be positional argument.
        
        shell command plus argparse arguments:
        py s.py calc_profit 18 
        py s.py calc_profit 18 --productType apple    

    - delete product (e.g. an expired one)
        This is not a requirement. So only implement if there is time left. 

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

5.  create the argparse user interface:
    in argparse assign a subparser to each use case from step 3.  
    make choices about positional vs optional arguments, etc.
    Goal: make sure the superpy-app is easy and  intuitive to use.
    The argparse-code itself will be created later on. 

    status: done. See section  4. above.

6.  Create testdata
     generate automated testdata in bought.csv and sold.csv 
      (erd in previous step must be ready before creating testdata)
    
    The testdata is necessary to work in a TDD-fashion. 

    The testdata is very specific, so I prefer to create it myself, rather than 
    to create it on e.g. mockaroo.com

    table bought.csv:
        Use built-in fn enumerate to dynamically create values for the columns ID.

        Use permutations-fn from itertools library to create testdata for fields productType, 
        pricePerUnit and amountOfUnits in table bought.csv

        boughtDate for each buying transaction gets a value in day range 1 to 55 inclusive. 
        expiryDate is 5 days after boughtDate.

    table sold.csv:
        sold.csv is a copy of bought.csv
        Each 5th bought product will expire.
        The other products will be sold for 3 times the price it was bought for.        
        soldDate is 1 day after boughtDate.


7.  Implement each use case in its own iteration
    Perform the following steps iteratively for each use case from step 4. above. E.g.:
    a. take the first use case: buy_product (each use case already has a fn-signature at this point)
    b. create testfn test_buy_product (with testdat from previous step). (goal is to do TDD)
        Once completed, all testcases in the testfn are supposed to fail, because the 
        fn-body is still empty at this point. 

    c. implement fn-body (i.e. "code that does stuff") of fn-signature buy_product
    d. create argparse code that runs fn buy_product
    e. write code until all testcases pass. 

    e. take the next use case from step 4: use case sell_product
        (repeat the steps above)
        etc.




8. display the output (e.g. report profit) to pyt module tabulate 
    (more info: https://analyticsindiamag.com/beginners-guide-to-tabulate-python-tool-for-creating-nicely-formatted-tables/#:~:text=Tabulate%20is%20an%20open%2Dsource,for%20all%20types%20of%20formatting)

    
9. display the output (e.g. report profit) to pyt module matplotlib

10. prevent selling sold out products:
    Inside fn sell_product check if products are available (so you don't end up selling a product that is not there).
    Implementation: On a system_date (e.g. day 53) inside fn sell_product where you want to sell 
    e.g. 11 oranges, call fn calculte_inventory and check if the 10 oranges are available on day 53. 






