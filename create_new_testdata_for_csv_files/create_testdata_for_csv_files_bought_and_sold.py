'''
    Goal: create testdata for bought.csv and sold.csv. --> Testdata has already been created with script in this file.

    manual:
        1. running the code will create testdata for bought.csv and sold.csv inside current directory 
           create_new_tesdata_for_csv_files.
           Parts of this created data are random, so the testdata will be different each time the code is run.
           But the pytest testcases need a frozen copy of the testdata to be able to run reliably.
        3. So I have created testdata and manually copied this data into directory csv_files_used_by_superpy. This 
           frozen copy is to be used to create pytest testcases for TDD-software-development.

        4. So if needed (e.g. if there is a reason to update the testdata), then this script can be run again 
           to create new testdata for bought.csv and sold.csv, without 
           affecting the current testdata.


           '''
 
'''

    design choices for bought.csv: 
        testdata is created for 60 days (day 1 to day 60 inclusive)
        products all expire after 5 days.
        products are bought on random days between day 1 and day 55 inclusive.

    design choices for sold.csv:
        sold.csv is copy of bought.csv, but with following modifications:
            -every 5th product is not sold (so will expire while time traveling)
            -each product is sold for 3 times the price it was bought for.
            -each product is sold 2 days after it was bought (supermarkets have fast stock turnover). 

    This script consists of parts:
    # part 1 of 2: create testdata for bought.csv
    # part 2 of 2: create testdata for sold.csv

'''



# Configuration settings to get other results in e.g. profit or revenue report, matplotlib graphs, etc.)
'''
    set nr of products in supermarket:
    This variable is an operand in fn product from module itertools.
    So more products leads to more rows in bought.csv and less products to less rows in bought.csv.
'''
nr_of_products_in_supermarket = 3

'''
    set nr of rows to delete from sold.csv:
    sold.csv is as a copy of bought.csv. After making the deepcopy, a few changes are made: e.g. make sell_price different (higher) than buy_price, but also delete some rows. Rows that are present in bought.csv, but not in sold.csv, will expire while time traveling.
    (e.g. if delete_every_nth_row = 2, then every 2nd row will be deleted)
    (e.g. if delete_every_nth_row = 3, then every 3rd row will be deleted)
'''
delete_every_nth_row = 2

# set nr of days between buying and selling a product:
number_of_days_between_buying_and_selling_a_product = 2

# set nr of days between buying a product and its expiry date:
nr_of_days_between_buying_a_product_and_its_expiry_date = 5

# set price margin for selling a product: 
# (e.g. if buying price is 3 euro and selling price is 12 euro, then margin is 4)
# (e.g. if buying price is 2 euro and selling price is 3 euro, then margin is 1.5)
price_margin_as_mulitplication_factor = 3

# timespan of application is 2 months:
'''
    (e.g. if today is 1 january 2021, then timespan is 1 january 2021 to 1 march 2021)
    to change the timespan, goto utils.py and adjust fn generate_random_date_in_future_in_time_interval_of_2_months()
    (there is no need to, just for future reference)
'''

import csv, os, random, sys
from itertools import product
from copy import deepcopy

# print(sys.path)
sys.path.append('c:\\dev\\pytWinc\\superpy')
sys.path.append('c:\\dev\\pytWinc\\superpy\\utils_superpy')
'''
    goal: solve ImportError: attempted relative import with no known parent package
    solution: add parent package to sys.path
    source: https://stackoverflow.com/questions/4383571/importing-files-from-different-folder

    analysis strange behaviour: I must append directory 'superpy' itself  to sys.path to 
    get rid of the error.
    I was expecting that "superpy\my_fns" must be added to sys.path instead.
    2do later: figure out why this is the case. 
'''

# print(sys.path) # ok
from utils_superpy.utils import generate_random_date_in_future_in_time_interval_of_2_months
from utils_superpy.utils import make_id_for_each_row_in_csv_file
from utils_superpy.utils import add_days_to_date
# print(make_id_for_each_row_in_csv_file('b', 1)()) 
csv_file_bought_id = make_id_for_each_row_in_csv_file('b', 1) 


print('part 1 of 2: create testdata for bought.csv: ')
# part 1 of 2: create testdata for bought.csv

#math highschool analogy: (5+2)*(3+4) == 5*3 + 5*4 + 2*3 + 2*4
supermarket_products = ['fish', 'rice', 'potatoes', 'quinoa', 'bread', 'carrots', 'chicken', 'beef', 'bulgur', 'tomatoes', 'lettuce', 'beans', 'cheese', 'apple', 'beetroot', 'kiwi', 'onions', 'eggs', 'banana', 'oats', 'milk', 'pasta']

# defensive coding: check if some products are in list more than once:
supermarket_products = list(set(supermarket_products))

products = random.sample(supermarket_products, nr_of_products_in_supermarket) # see config at start of file to change nr of products in supermarket.
# products = ['apple', 'banana', 'kiwi', 'beans', 'quinoa', 'oats', 'bulgur', 'rice', 'pasta', 'bread']
# amountOfUnits = [1, 2, 3, 4] # backlog: perhaps add this later.
pricePerUnit = [0.50, 1.10, 1.40, 2.50, 3.10, 4.00, 5.20]

boughtProducts = (list(product(products, pricePerUnit)))

products_with_bought_date = []
for product in boughtProducts:
    bought_date = generate_random_date_in_future_in_time_interval_of_2_months()
    # I want all data to stay in the range of 1 to 60.
    expiry_date = add_days_to_date(bought_date, nr_of_days_between_buying_a_product_and_its_expiry_date) # see config at start of file to set 2nd argument.
    products_with_bought_date.append(product + (bought_date, expiry_date)) 
    # note to self: tuple concatenation, if needed use comma after expiry_date.

# print(len(products_with_bought_date))

# now sort list with tuples on bought_date: (x[3] is the bought_date)
products_with_bought_date.sort(key=lambda x: x[3])
# note to self: sort is in-place, but sorted() returns a new list.
# print(products_with_bought_date) # status: ok (output: list with tuples)


# convert list with tuples into list with lists:
products_with_bought_date = [list(elem) for elem in products_with_bought_date]
# print(products_with_bought_date) # status: ok (output: list with lists)

# add id to each list in list:
for product_id, elem in enumerate(products_with_bought_date):
    # elem.insert(0, product_id) # status: ok 
    elem.insert(0, csv_file_bought_id())

print('products_with_bought_date: ')
print(products_with_bought_date)

# write list with lists to csv file:
path = os.getcwd()
# print(path)
'''
    do not create file directly in  directory csv_files_used_by_superpy. Otherwise
    testdata will be overwritten and pytest testcases will  need to be updated to
    reflect the new testdata.
'''
path_to_bought_csv = path + '\\create_new_testdata_for_csv_files\\bought.csv'
with open(path_to_bought_csv, 'w', newline='') as csvfile:    
    writer = csv.writer(csvfile)
    writer.writerow(['id', 'product', 'price', 'buy_date', 'expiry_date'])
    writer.writerows(products_with_bought_date) # note to self: writerows() expects a list of lists.

print('----------------------------------')
print('start of part 2 of 2: create testdata for sold.csv: ')
# part 2 of 2: create testdata for sold.csv

products_with_sold_date = deepcopy(products_with_bought_date)
# not to self: I need immutable copy here.
# print(products_with_sold_date) # ok

# modify the list with lists:
for row in products_with_sold_date:
    # replace b (as abbreviation of bought.csv) with s (as abbrivation of sold.csv) in primary key id.
    row[0] = row[0].replace('b', 's') 
    row.insert(1, row[0].replace('s', 'b'))
    # calculate price_sold: (price_sold = price_bought * 3)
    row[3] = round(row[3] * price_margin_as_mulitplication_factor,2) # see config at start of file to set 2nd argument.
    # set the sold_date to 2 days after bought_date:
    row[4] = add_days_to_date(row[4], number_of_days_between_buying_and_selling_a_product) # see config at start of file to set 2nd argument.
    



'''
    no need to sort the list on column date_sold, becaus that was already done in part 1 (on date_bought) and
    date_sold = date_bought + 2. (so they correlate in a linear fashion)
'''

# delete each nth list in list: (so each nth row will expire in sold.csv while time traveling to the future)
products_with_sold_date = [row for row in products_with_sold_date if int(row[0].split("_")[1]) % delete_every_nth_row != 0]   
# config variable delete_every_nth_row at beginning of this file.  
'''
see config at start of file to set variable delete_every_nth_row.

 explanation of 
 e.g. input is 'b_17'. b_17 means: row 17 in bought.csv == transaction nr 17 in bought.csv. b_17 is primary key in bought.csv.
 int(row[0].split("_")[1]) extracts 17 from b_17.
'''
# print(products_with_sold_date) # ok

print('products_with_sold_date: ')
print(products_with_sold_date)

path = os.getcwd()
#  print(path) # ok

path_to_sold_csv = path + '\\create_new_testdata_for_csv_files\\sold.csv'
with open(path_to_sold_csv, 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['id_sold', 'id_bought', 'product', 'price', 'sold_date', 'expiry_date'])
    writer.writerows(products_with_sold_date) # note to self: writerows() expects a list of lists.

