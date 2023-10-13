import csv, datetime, os, random, re, socket
from copy import deepcopy
from datetime import date, datetime, timedelta
from dateutil.relativedelta import relativedelta
from itertools import product
from rich.console import Console
from rich.table import Table
from typing import Callable

# LIST OF FUNCTIONS: (Ctrl+C, Ctrl+F to quickly go to fn):
# add_days_to_date()
# buy_product():
# calculate_expired_products():
# calculate_inventory():
# calculate_middle_of_time_interval():
# calculate_profit():
# calculate_revenue():
# calculate_sales_volume():
# create_buy_id_for_each_row_in_mock_data():
# create_buy_id_that_increments_highest_buy_id_in_boughtcsv():
# create_data_for_csv_files_bought_and_sold():
# find_product():
# generate_random_buy_date():
# generate_random_prices(): 
# get_dates_of_next_7_days():
# get_highest_buy_id_from_boughtcsv(path_to_csv_bought_file):
# get_path_to_directory_of_file(directory_of_file):
# get_path_to_file(directory_of_file, file_name_of_which_you_want_to_know_the_path):
# get_system_date():
# get_weekday_from_date():
# is_product_buy_id():  
# sell_product_by_buy_id():
# sell_product_by_product_name():
# set_buy_id_counter_txt():
# set_system_date_to():
# show_csv_file():
# show_superpy_system_info():
# show_selected_buy_transactions():
# travel_time():

def add_days_to_date(date_string: str, days_to_add: int) -> str:
    date = datetime.strptime(date_string, '%Y-%m-%d')
    new_date = date + timedelta(days= days_to_add)
    return new_date.strftime('%Y-%m-%d')

def buy_product(
        product_name: str, 
        price: float, 
        buy_date: str, 
        expiry_date: str, 
        id_of_row_in_csv_file_bought: str, 
        path_to_csv_bought_input_file: str, 
        path_to_csv_bought_output_file: str
) -> None:
    # Only when testing fn buy_product in pytest, input and output csv file are different.
    # E.g. 'Milk' and 'milk' must be stored as the same product. 
    product_name = product_name.lower() 

    # step: check if product has expired:
    if expiry_date != 'does not expire': 
        if datetime.strptime(buy_date, '%Y-%m-%d') > datetime.strptime(expiry_date, '%Y-%m-%d'):
            console = Console()
            # console.print()
            console.print(f"Warning: you have just bought product < {product_name} > with buy_date < {buy_date} > greater than\n its expiry_date < {expiry_date} >. " 
                        f"Are  you sure about this?",style="bold yellow")      
    try:
        with open(path_to_csv_bought_input_file, 'r', newline='') as file: 
            reader = csv.DictReader(file)
            rows = list(reader)
            file.seek(0)
    except FileNotFoundError:
        print(f"File '{path_to_csv_bought_input_file}' not found.")
    except PermissionError:
        print(f"You don't have permission to access '{path_to_csv_bought_input_file}'.")
    except UnicodeDecodeError:
        print(f"Invalid Unicode character found in '{path_to_csv_bought_input_file}'.")
    except csv.Error as e:
        print(f"Error while reading CSV file: {e}")
    try:
        with open(path_to_csv_bought_output_file, 'w', newline='') as file: 
            rows.append({'buy_id': id_of_row_in_csv_file_bought, 'product': product_name, 'buy_price': price, 'buy_date': buy_date, 'expiry_date': expiry_date}) 
            writer = csv.DictWriter(file, fieldnames= reader.fieldnames)
            writer.writeheader()
            writer.writerows(rows)
    except PermissionError:
        print(f"You don't have permission to write to '{path_to_csv_bought_output_file}'.")
    except csv.Error as e:
        print(f"Error while writing CSV file: {e}")   
    buy_transaction_status = "fn_buy_product_has_run_successfully"
    return buy_transaction_status

def calculate_amount(
        # goal: this is 1 generic fn to calculate cost or revenue. (but sales_volume is different)
        start_date: str, 
        end_date: str, 
        date_field_from_csv: str, # different field to calculate cost or revenue
        price_field_from_csv: str, # different field to calculate cost or revenue
        path_to_csv_file: str,

) -> float:
    start_date = datetime.strptime(str(start_date), '%Y-%m-%d')
    end_date = datetime.strptime(str(end_date), '%Y-%m-%d')
    amount = 0
    financial_amount_rounded = 0

    try:
        with open(path_to_csv_file, 'r', newline='') as file_object: 
            reader = csv.DictReader(file_object)
            for row in reader:
                date = row[date_field_from_csv]
                date = datetime.strptime(date, '%Y-%m-%d')
                if start_date <= date <= end_date:
                    amount += float(row[price_field_from_csv])
                    financial_amount_rounded = round(amount, 2)
        return financial_amount_rounded
    except FileNotFoundError:
        print(f"File '{path_to_csv_file}' not found.")
    except PermissionError:
        print(f"You don't have permission to access '{path_to_csv_file}'.")
    except UnicodeDecodeError:
        print(f"Invalid Unicode character found in '{path_to_csv_file}'.")
    except csv.Error as e:
        print(f"Error while reading CSV file: {e}")

def calculate_expired_products(
        date_on_which_to_calculate_expired_products: str, 
        path_to_csv_sold_file: str, 
        path_to_csv_bought_file: str
) -> list:
    date_on_which_to_calculate_expired_products = datetime.strptime(date_on_which_to_calculate_expired_products, '%Y-%m-%d').date()

    # sold.csv:
    sell_data = {}
    try:
        with open(path_to_csv_sold_file, 'r') as file_object:
            reader = csv.reader(file_object)
            next(reader)  
            for row in reader:
                sell_id, buy_id, sell_price, sell_date = row
                sell_data[buy_id] = sell_date if sell_date else None
    except FileNotFoundError:
        print(f"File '{path_to_csv_sold_file}' not found.")
    except PermissionError:
        print(f"You don't have permission to access '{path_to_csv_sold_file}'.")
    except UnicodeDecodeError:
        print(f"Invalid Unicode character found in '{path_to_csv_sold_file}'.")
    except csv.Error as e:
        print(f"Error while reading CSV file: {e}")

    # bought.csv:
    expired_products = []
    try:
        with open(path_to_csv_bought_file, 'r') as file_object:
            reader = csv.reader(file_object)
            next(reader)  
            for row in reader:
                # I have access to sold.csv and bought.csv:
                buy_id, product, buy_price, buy_date, expiry_date = row
                buy_date = datetime.strptime(buy_date, '%Y-%m-%d').date()
                '''
                about 'does not expire': 
                uc: if user buys a product via argparse cli ( calling fn buy_product) without setting expiry_date as a flag, then
                default value for expiry_date is 'does not expire'. Reason: supermarket also sells e.g. magazines, 
                light bulbs, etc. that do not expire)
                '''
                if expiry_date == 'does not expire':
                    if date_on_which_to_calculate_expired_products > buy_date and expiry_date == 'does not expire' and sell_data.get(buy_id) is None:
                        expired_products.append(row)
                else: 
                    expiry_date = datetime.strptime(expiry_date, '%Y-%m-%d').date() 
                    if date_on_which_to_calculate_expired_products > buy_date and date_on_which_to_calculate_expired_products > expiry_date and sell_data.get(buy_id) is None:
                        expired_products.append(row)             
                '''
                there is only 1 difference between  this fn and fn calculate_expired_products: 
                "<" in "date_on_which_to_calculate_products_in_inventory < expiry_date" above.

                in bought.csv: (by convention) buy_date is always set with either an expiry_date or 'does not expire'.

                about 'does not expire': 
                uc: if user buys a product via argparse cli (fn buy_product) without setting expiry_date, then
                default value for expiry_date is 'does not expire' (supermarket also sells e.g. magazines, light bulbs, etc. that do not expire)
                '''
    except FileNotFoundError:
        print(f"File '{path_to_csv_bought_file}' not found.")
    except PermissionError:
        print(f"You don't have permission to access '{path_to_csv_bought_file}'.")
    except UnicodeDecodeError:
        print(f"Invalid Unicode character found in '{path_to_csv_bought_file}'.")
    except csv.Error as e:
        print(f"Error while reading CSV file: {e}")
    return expired_products

def calculate_inventory(
        date_on_which_to_calculate_products_in_inventory: str, 
        path_to_csv_sold_file: str, 
        path_to_csv_bought_file: str
) -> list:
    # print(type(date_on_which_to_calculate_products_in_inventory)) # e.g. '2023-10-01' has datatype <class 'str'>
    date_on_which_to_calculate_products_in_inventory = datetime.strptime(date_on_which_to_calculate_products_in_inventory, '%Y-%m-%d').date()
    # print(type(date_on_which_to_calculate_products_in_inventory)) # e.g. '2023-10-01' now has datatype <class 'datetime.date'> and that is what I neeed. 

    # sold.csv:
    sell_data = {}
    try:
        with open(path_to_csv_sold_file, 'r') as file_object:
            reader = csv.reader(file_object)
            next(reader)  
            for row in reader:
                sell_id, buy_id, sell_price, sell_date = row
                sell_data[buy_id] = sell_date if sell_date else None
    except FileNotFoundError:
        print(f"File '{path_to_csv_sold_file}' not found.")
    except PermissionError:
        print(f"You don't have permission to access '{path_to_csv_sold_file}'.")
    except UnicodeDecodeError:
        print(f"Invalid Unicode character found in '{path_to_csv_sold_file}'.")
    except csv.Error as e:
        print(f"Error while reading CSV file: {e}")

        
    # bought.csv:
    products_in_inventory = []
    try:
        with open(path_to_csv_bought_file, 'r') as file_object:
            reader = csv.reader(file_object)
            next(reader)  
            for row in reader:
                # I have access to sold.csv and bought.csv:
                buy_id, product, buy_price, buy_date, expiry_date = row
                buy_date = datetime.strptime(buy_date, '%Y-%m-%d').date()
                '''
                about 'does not expire': 
                uc: if user buys a product via argparse cli ( calling fn buy_product) without setting expiry_date as a flag, then
                default value for expiry_date is 'does not expire'. Reason: supermarket also sells e.g. magazines, 
                light bulbs, etc. that do not expire)
                '''
                if expiry_date == 'does not expire':
                    if date_on_which_to_calculate_products_in_inventory > buy_date and expiry_date == 'does not expire' and sell_data.get(buy_id) is None:
                        products_in_inventory.append(row)
                else: 
                    expiry_date = datetime.strptime(expiry_date, '%Y-%m-%d').date() 
                    if date_on_which_to_calculate_products_in_inventory > buy_date and date_on_which_to_calculate_products_in_inventory < expiry_date and sell_data.get(buy_id) is None:
                        products_in_inventory.append(row) 
                '''
                there is only 1 difference between  this fn and fn calculate_expired_products: 
                "<" in "date_on_which_to_calculate_products_in_inventory < expiry_date" above.

                in bought.csv: (by convention) buy_date is always set with either an expiry_date or 'does not expire'.

                about 'does not expire': 
                uc: if user buys a product via argparse cli (fn buy_product) without setting expiry_date, then
                default value for expiry_date is 'does not expire' (supermarket also sells e.g. magazines, light bulbs, etc. that do not expire)
                '''
    except FileNotFoundError:
        print(f"File '{path_to_csv_bought_file}' not found.")
    except PermissionError:
        print(f"You don't have permission to access '{path_to_csv_bought_file}'.")
    except UnicodeDecodeError:
        print(f"Invalid Unicode character found in '{path_to_csv_bought_file}'.")
    except csv.Error as e:
        print(f"Error while reading CSV file: {e}")
    return products_in_inventory

def calculate_middle_of_time_interval(
        SYSTEM_DATE: str, 
        upper_boundary_nr_of_months_to_add_to_calculate: int, 
        upper_boundary_nr_of_weeks_to_add_to_calculate: int,
        upper_boundary_nr_of_days_to_add_to_calculate: int  
) -> str:
    '''
    GOAL: set system_date to the middle of the time interval in which to create random mock data for bought.csv
    and sold.csv.
    e.g. lower boundary: 2023-09-01, upper boundary: 2023-09-30, then system_date is set to 2023-09-15.
    Relevance: with  the system_date in the middle, you can immediately create a(ny) report using JUST the default arguments and 
    already see relevant results: e.g. << py super.py show_profit >>, << py super.py show_inventory >>, etc.
    ''' 
    system_date_as_object = datetime.strptime(SYSTEM_DATE, '%Y-%m-%d')
    lower_boundary_date_object = system_date_as_object # default value
    # print('lower_boundary_date_object: ', lower_boundary_date_object)

    upper_boundary_date_object = system_date_as_object + timedelta( weeks= upper_boundary_nr_of_weeks_to_add_to_calculate, days=upper_boundary_nr_of_days_to_add_to_calculate)
    # print('upper_boundary_date_object: ', upper_boundary_date_object)
    upper_boundary_date_object = upper_boundary_date_object + relativedelta(months=upper_boundary_nr_of_months_to_add_to_calculate)
    # print('upper_boundary_date_object: ', upper_boundary_date_object)

    time_interval_middle = lower_boundary_date_object + (upper_boundary_date_object - lower_boundary_date_object) / 2
    # print('time_interval_middle: ', time_interval_middle)
    SYSTEM_DATE = datetime.strftime(time_interval_middle, '%Y-%m-%d')
    # print('SYSTEM_DATE: ', SYSTEM_DATE)
    # print(type(SYSTEM_DATE))

    return SYSTEM_DATE

def calculate_profit(
        start_date: str, 
        end_date: str, 
        path_to_csv_sold_file: str, 
        path_to_csv_bought_file: str, 
        calculate_revenue: Callable[[str, str, str, str, str], float], 
        calculate_cost: Callable[[str, str, str, str, str], float]
) -> float:
    # So fn calculate_amount_in_interval is used to calculate cost and revenue.
    cost = calculate_cost(start_date, end_date, "buy_date", "buy_price", path_to_csv_bought_file)
    revenue = calculate_revenue(start_date, end_date, "sell_date", "sell_price", path_to_csv_sold_file)
    
    profit = round(revenue - cost,2)
    return profit

def calculate_sales_volume(
        start_date: str, 
        end_date: str, 
        path_to_csv_sold_file: str
    ) -> int:
    start_date = datetime.strptime(str(start_date), '%Y-%m-%d')
    end_date = datetime.strptime(str(end_date), '%Y-%m-%d')
    sales_volume = 0
    try:
        with open(path_to_csv_sold_file, 'r', newline='') as file_object: 
            reader = csv.DictReader(file_object)
            for row in reader:
                sell_date = row['sell_date']
                sell_date = datetime.strptime(sell_date, '%Y-%m-%d')
                if start_date <= sell_date <= end_date:
                    sales_volume += 1
    except FileNotFoundError:
        print(f"File '{path_to_csv_sold_file}' not found.")
    except PermissionError:
        print(f"You don't have permission to access '{path_to_csv_sold_file}'.")
    except UnicodeDecodeError:
        print(f"Invalid Unicode character found in '{path_to_csv_sold_file}'.")
    except csv.Error as e:
        print(f"Error while reading CSV file: {e}")

    return sales_volume

def create_buy_id_for_each_row_in_mock_data(
        csv_file_name_first_letter: str, 
        first_nr_in_range: int
) -> Callable[[], int]:
    count = first_nr_in_range
    count -= 1 # to start with 1, not 0
    def counter():
        nonlocal count
        count += 1
        if count < 10:
            return f"{csv_file_name_first_letter}_0{count}"
        return f"{csv_file_name_first_letter}_{count}"
    return counter

def create_data_for_csv_files_bought_and_sold(
        nr_of_products: int, 
        nr_of_prices: int,
        lowest_price_in_range: float,
        highest_price_in_range: float,
        delete_every_nth_row_in_soldcsv: int,
        shelf_life: int,
        turnover_time: int,
        markup: int,
        lower_boundary_year: int,
        lower_boundary_month: int,
        lower_boundary_day: int,
        upper_boundary_month: int,
        upper_boundary_week: int,
        upper_boundary_day: int,
        product_list_to_create_product_range: list,
        generate_random_prices: Callable[[float, float, int], list],
        path_to_file_bought_csv: str,
        path_to_file_sold_csv: str,
        add_days_to_date: int,
        create_buy_id_for_each_row_in_mock_data: Callable[[str, int], Callable[[], int]], 
        # reason: fn A is fn-argument in fn B == fn B(fn A). And B(fn A) is argument in fn C == fn C(B(fn A))
        generate_random_buy_date: Callable[[int, int, int, int, int, int], str]
) -> None:
    # PART 1 OF 2: create testdata for bought.csv: 
    if nr_of_products > len(product_list_to_create_product_range):
        print(f'Problem: nr_of_products to create mock data:', nr_of_products, 'exceeds nr of products in supermarket:', len(list((set(product_list_to_create_product_range)))))
        product_range = len(list((set(product_list_to_create_product_range))))
        print(f"Solution: product_range has been set to the maximum amount of products in file"
              f"product_range.py (...\\superpy\\superpy\\product_range.py). This is {len(list((set(product_list_to_create_product_range))))}. " 
              f"But if you need a higher product_range, then please add more products to product_range.py."
            )
    csv_file_bought_id = ''
    csv_file_bought_id = create_buy_id_for_each_row_in_mock_data('b', 1) 
    product_list_to_create_product_range = list(set(product_list_to_create_product_range))
    product_range = random.sample(product_list_to_create_product_range, nr_of_products)
    # E.g. 'Milk' and 'milk' must be stored as the same product: 
    product_range = [product.lower() for product in product_range]
    # problem: << py .\super.py sell soft drinks 3.33 >> --> solution: << py .\super.py sell soft_drinks 3.33 >>:
    product_range = [string.replace(' ', '_') if ' ' in string else string for string in product_range]
    price_range = generate_random_prices(lowest_price_in_range, highest_price_in_range, nr_of_prices)
    all_combinations_between_product_and_price = (list(product(product_range, price_range)))
    # add buy_date and expiry_date to each combi (each combi will become a row in bought.csv):
    products_with_bought_date = []
    for bought_product in all_combinations_between_product_and_price:
        bought_date = generate_random_buy_date(
            lower_boundary_year,
            lower_boundary_month,
            lower_boundary_day,
            upper_boundary_month,
            upper_boundary_week,
            upper_boundary_day)
        expiry_date = add_days_to_date(bought_date, shelf_life) 
        products_with_bought_date.append(bought_product + (bought_date, expiry_date)) 
    # x[3] is the bought_date:
    products_with_bought_date.sort(key=lambda x: x[3]) # list with tuples
    products_with_bought_date = [list(elem) for elem in products_with_bought_date] # list with lists
    # add id (b_01, b_02, b_03, etc.) to each list in list:
    for row_in_csv_file_bought in products_with_bought_date:
        row_in_csv_file_bought.insert(0, csv_file_bought_id())
    try:
        with open(path_to_file_bought_csv, 'w', newline='') as csvfile:    
            writer = csv.writer(csvfile)
            writer.writerow(['buy_id', 'product', 'buy_price', 'buy_date', 'expiry_date'])
            writer.writerows(products_with_bought_date) # writerows() expects a list of lists.
    except PermissionError:
        print(f"You don't have permission to write to '{path_to_file_bought_csv}'.")
    except csv.Error as e:
        print(f"Error while writing CSV file: {e}")

    # PART 2 OF 2: create testdata for sold.csv: 
    products_with_sold_date = deepcopy(products_with_bought_date)
    for row in products_with_sold_date: # products_with_sold_date is list with lists:
        buy_price = row[2] 
        sell_price = round(buy_price * markup,2)
        row[2] = sell_price # sell_price takes the place of buy_price in sold.csv
        # calculate sell_date:
        buy_date = row[3] # because sold.csv starts of as a deepcopy of bought.csv
        sold_date = add_days_to_date(buy_date, turnover_time) 
        row[3] = sold_date # sell_date takes the place of buy_date in sold.csv
        # delete product and expiry_date from sold.csv to avoid redundancy:
        del row[4] # expiry_date == row[4]
        del row[1] # product == row[1]
        # replace buy_id by sell_id: e.g. b_01 --> s_01, b_02 --> s_02, etc:
        buy_id_in_record_in_bought_csv = row[0] # e.g. b_28
        row.insert(1, buy_id_in_record_in_bought_csv) # e.g. b_28, so an exact copy of this immutable string.
        sell_id_of_record_in_sold_csv = row[0]
        sell_id_of_record_in_sold_csv = sell_id_of_record_in_sold_csv.replace('b', 's') # e.g. b_28 --> s_28
        row[0] = sell_id_of_record_in_sold_csv # e.g. s_28

    # delete each nth row in sold.csv (so each nth row will expire in sold.csv while time traveling to the future)
    products_with_sold_date = [row for row in products_with_sold_date if int(row[0].split("_")[1]) % 
        delete_every_nth_row_in_soldcsv != 0]   
    try:
        with open(path_to_file_sold_csv, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['sell_id', 'buy_id', 'sell_price', 'sell_date'])
            writer.writerows(products_with_sold_date) # note to self: writerows() expects a list of lists.
    except PermissionError:
        print(f"You don't have permission to write to '{path_to_file_sold_csv}'.")
    except csv.Error as e:
        print(f"Error while writing CSV file: {e}")

def find_product(list_with_transactions: list, product_name: str ) -> str or list:
    for buy_transaction_record in list_with_transactions:
        if buy_transaction_record[1] == product_name: 
            return buy_transaction_record
    return 'product_not_found' 

def generate_random_buy_date(
        interval_lower_boundary_year: int, 
        interval_lower_boundary_month: int, 
        interval_lower_boundary_day: int, 
        nr_of_months_added_to_calculate_upper_boundary: int, 
        nr_of_weeks_added_to_calculate_upper_boundary: int, 
        nr_of_days_added_to_calculate_upper_boundary: int
) -> str:     
    start_date = date(interval_lower_boundary_year, interval_lower_boundary_month, interval_lower_boundary_day)
    end_date = start_date + relativedelta(months=nr_of_months_added_to_calculate_upper_boundary)
    end_date = end_date + relativedelta(weeks=nr_of_weeks_added_to_calculate_upper_boundary)
    end_date = end_date + relativedelta(days=nr_of_days_added_to_calculate_upper_boundary)
    time_between_dates = end_date - start_date
    days_between_dates = time_between_dates.days
    random_number_of_days = random.randrange(days_between_dates)
    random_date = start_date + timedelta(days=random_number_of_days)
    return random_date.strftime('%Y-%m-%d')

def generate_random_prices(lowest_price: float, highest_price: float, nr_of_prices: int) -> list:
    return [round(random.uniform(lowest_price, highest_price), 2) for price in range(nr_of_prices)]

def get_dates_of_next_7_days(today: str) -> list:
    today_as_date_object = datetime.strptime(today, '%Y-%m-%d').date() 
    # Monday is 0, Sunday is 6, so add 1 for easier reading: 
    day_nr_of_week = (today_as_date_object.weekday() + 1 ) 
    if day_nr_of_week == 1:  # Monday
        monday = today_as_date_object + timedelta(days= 7)
        tuesday = today_as_date_object + timedelta(days= 1)
        wednesday = today_as_date_object + timedelta(days= 2)
        thursday = today_as_date_object + timedelta(days= 3)
        friday = today_as_date_object + timedelta(days= 4)
        saturday = today_as_date_object + timedelta(days= 5)
        sunday = today_as_date_object + timedelta(days= 6)
    if day_nr_of_week == 2: # Tuesday
        monday = today_as_date_object + timedelta(days= 6)
        tuesday = today_as_date_object + timedelta(days= 7)
        wednesday = today_as_date_object + timedelta(days= 1)
        thursday = today_as_date_object + timedelta(days= 2)
        friday = today_as_date_object + timedelta(days= 3)
        saturday = today_as_date_object + timedelta(days= 4)
        sunday = today_as_date_object + timedelta(days= 5)
    if day_nr_of_week == 3: # Wednesday
        monday = today_as_date_object + timedelta(days= 5)
        tuesday = today_as_date_object + timedelta(days= 6)
        wednesday = today_as_date_object + timedelta(days= 7)
        thursday = today_as_date_object + timedelta(days= 1)
        friday = today_as_date_object + timedelta(days= 2)
        saturday = today_as_date_object + timedelta(days= 3)
        sunday = today_as_date_object + timedelta(days= 4)
    if day_nr_of_week == 4: # Thursday
        monday = today_as_date_object + timedelta(days= 4)
        tuesday = today_as_date_object + timedelta(days= 5)
        wednesday = today_as_date_object + timedelta(days= 6)
        thursday = today_as_date_object + timedelta(days= 7)
        friday = today_as_date_object + timedelta(days= 1)
        saturday = today_as_date_object + timedelta(days= 2)
        sunday = today_as_date_object + timedelta(days= 3)
    if day_nr_of_week == 5: # Friday
        monday = today_as_date_object + timedelta(days= 3)
        tuesday = today_as_date_object + timedelta(days= 4)
        wednesday = today_as_date_object + timedelta(days= 5)
        thursday = today_as_date_object + timedelta(days= 6)
        friday = today_as_date_object + timedelta(days= 7)
        saturday = today_as_date_object + timedelta(days= 1)
        sunday = today_as_date_object + timedelta(days= 2)
    if day_nr_of_week == 6: # Saturday
        monday = today_as_date_object + timedelta(days= 2)
        tuesday = today_as_date_object + timedelta(days= 3)
        wednesday = today_as_date_object + timedelta(days= 4)
        thursday = today_as_date_object + timedelta(days= 5)
        friday = today_as_date_object + timedelta(days= 6)
        saturday = today_as_date_object + timedelta(days= 7)
        sunday = today_as_date_object + timedelta(days= 1)
    if day_nr_of_week == 7: # Sunday
        monday = today_as_date_object + timedelta(days= 1)
        tuesday = today_as_date_object + timedelta(days= 2)
        wednesday = today_as_date_object + timedelta(days= 3)
        thursday = today_as_date_object + timedelta(days= 4)
        friday = today_as_date_object + timedelta(days= 5)
        saturday = today_as_date_object + timedelta(days= 6)
        sunday = today_as_date_object + timedelta(days= 7)
    dates_of_next_7_days = [monday, tuesday, wednesday, thursday, friday, saturday, sunday]
    dates_of_next_7_days_as_strings = []
    for day in dates_of_next_7_days:
        day = day.strftime('%Y-%m-%d')
        dates_of_next_7_days_as_strings.append(day)
    return dates_of_next_7_days_as_strings

def get_highest_buy_id_from_boughtcsv(path_to_csv_bought_file: str) -> str:
    highest_buy_id = 'b_0' 
    try: 
        with open(path_to_csv_bought_file, 'r') as file_object:
            reader = csv.reader(file_object)
            next(reader) # skip header row
            for row in reader:
                csv_column_1 = row[0] # ex: b_1, or: b_2, or: b_3, etc
                if int(csv_column_1.split('_')[1]) > int(highest_buy_id.split('_')[1]):
                    highest_buy_id = csv_column_1
    except FileNotFoundError:
        print(f"File '{path_to_csv_bought_file}' not found.")
    except PermissionError:
        print(f"You don't have permission to access '{path_to_csv_bought_file}'.")
    except UnicodeDecodeError:
        print(f"Invalid Unicode character found in '{path_to_csv_bought_file}'.")
    except csv.Error as e:
        print(f"Error while reading CSV file: {e}")
    return highest_buy_id

def get_path_to_directory_of_file(directory_of_file: str) -> str: # rule: directory_of_file must be unique inside project superpy.
    whereabouts_of_directory_of_file  = str(os.getcwd()) 
    path_to_directory_of_this_file = ''
    for root, dirs, files in os.walk(whereabouts_of_directory_of_file):
        for name in dirs:
            if name == directory_of_file: 
                path_to_directory_of_this_file = os.path.abspath(os.path.join(root, name))
                break 
    return path_to_directory_of_this_file

def get_path_to_file(directory_of_file: str, file_name_of_which_you_want_to_know_the_path: str) -> str: # rule: directory_of_file must be unique inside project superpy.
    whereabouts_of_directory_of_file  = str(os.getcwd()) 
    path_to_directory_of_this_file = ''
    for root, dirs, files in os.walk(whereabouts_of_directory_of_file):
        for name in dirs:
            if name == directory_of_file: 
                path_to_directory_of_this_file = os.path.abspath(os.path.join(root, name))
                break 
    path_to_file = os.path.join(path_to_directory_of_this_file, file_name_of_which_you_want_to_know_the_path ) # path to file 
    return path_to_file

def get_system_date(path_to_system_date: str) -> datetime:
    try:
        with open(path_to_system_date, 'r', newline='') as file:
            system_date = file.read()
    except FileNotFoundError:
        print(f"File '{path_to_system_date}' not found.")
    except PermissionError:
        print(f"You don't have permission to access '{path_to_system_date}'.")
    except UnicodeDecodeError:
        print(f"Invalid Unicode character found in '{path_to_system_date}'.")
    except IOError as e:
        print(f"Error while reading file: {e}")
    return system_date

def get_weekday_from_date(date: str) -> str:
    date_object = datetime.strptime(date, '%Y-%m-%d')
    day_of_week = date_object.strftime('%A')
    return day_of_week

def increment_buy_id_counter_txt(path_to_id_with_highest_sequence_number: str) -> str:
    try:
        with open(path_to_id_with_highest_sequence_number, 'r', newline='') as file:
            last_id_used_in_fn_buy_product =file.read()
            id_parts = last_id_used_in_fn_buy_product.split("_") # e.g. ['b', '323']
            new_buy_id_counter = int(id_parts[1]) + 1
            # Transaction ids are sorted alphabetically, not numerically: e.g. b_10 is sorted before b_2, etc., so I need:  
            if new_buy_id_counter < 10:
                new_buy_id_counter = "b_0" + str(new_buy_id_counter)
            else:
                new_buy_id_counter = "b_" + str(new_buy_id_counter)
            file.seek(0)
    except FileNotFoundError:
        print(f"File '{path_to_id_with_highest_sequence_number}' not found.")
    except PermissionError:
        print(f"You don't have permission to access '{path_to_id_with_highest_sequence_number}'.")
    except UnicodeDecodeError:
        print(f"Invalid Unicode character found in '{path_to_id_with_highest_sequence_number}'.")
    except IOError as e:
        print(f"Error while reading file: {e}")
    try:
        with open(path_to_id_with_highest_sequence_number, 'w', newline='') as file: 
            file.write(new_buy_id_counter)
    except PermissionError:
        print(f"You don't have permission to write to '{path_to_id_with_highest_sequence_number}'.")
    except IOError as e:
        print(f"Error while writing file: {e}")
    return new_buy_id_counter

def is_product_bought_with_product_name(product_descriptor: str) -> bool:  
    pattern = r'^[bB]_\d{2,}$'
    '''
        e.g. b_01, B_02, b_03, (...) B_1079, etc....all return True
        e.g. apple, quinoa, bulgur, etc...all return False
        [bB]_ matches exactly 'b_' or 'B_' --> internally in Superpy only lowercase 'b_' is used.
    '''
    return not bool(re.match(pattern, product_descriptor))

def sell_product_by_buy_id(bought_product_id: str, 
                sell_price: float, 
                sell_date: str, 
                path_to_csv_sold_input_file: str, 
                path_to_csv_sold_output_file: str,
                path_to_csv_bought_file: str
) -> str:
    bought_product_id = bought_product_id.lower() # input can be e.g. B_01 or b_01, but internally in Superpy only b_01 is used.
    try: # error check 1of3: check if product exists in bought.csv:
        with open(path_to_csv_bought_file, 'r', newline='') as file: 
            is_bought_product_id_in_bought_csv = False
            reader = csv.DictReader(file)
            rows = list(reader)
            for row in rows:
                if row['buy_id'] == bought_product_id:
                    is_bought_product_id_in_bought_csv = True
            if not is_bought_product_id_in_bought_csv:
                console = Console()
                console.print(f"Warning: You are trying to sell a product with a buy_id << {bought_product_id} >> that " 
                    f"does NOT exist in bought.csv. So this sales transaction is aborted.",style="bold red")
                return 'product_is_not_sold' # this aborts the sales transaction          
    except FileNotFoundError:
        print(f"File '{path_to_csv_bought_file}' not found.")
    except PermissionError:
        print(f"You don't have permission to access '{path_to_csv_bought_file}'.")
    except UnicodeDecodeError:
        print(f"Invalid Unicode character found in '{path_to_csv_bought_file}'.")
    except csv.Error as e:
        print(f"Error while reading CSV file: {e}")
    try: # error check 2of3: check if product has already been sold:
        with open(path_to_csv_sold_input_file, 'r', newline='') as file: 
            '''
            Goal: check if product has already been sold: 
            Business rule: each product has a unique buy_id (e.g. b_01, b_02, ...).
            Business rule: each product is sold by its buy_id.
            So, if bought_product_id is already in sold.csv, then raise error:
            '''
            reader = csv.DictReader(file)
            rows = list(reader)
            for row in rows:
                if row['buy_id'] == bought_product_id:
                    console = Console()
                    console.print(f"Warning: You are trying to sell product with buy_id << {bought_product_id} >> that " 
                        f"has already been sold. So this sales transaction is aborted!",style="bold red")
                    return 'product_is_not_sold' # this aborts the sales transaction
            file.seek(0)
            sold_product_id = bought_product_id.replace('b', 's')
    except FileNotFoundError:
        print(f"File '{path_to_csv_sold_input_file}' not found.")
    except PermissionError:
        print(f"You don't have permission to access '{path_to_csv_sold_input_file}'.")
    except UnicodeDecodeError:
        print(f"Invalid Unicode character found in '{path_to_csv_sold_input_file}'.")
    except csv.Error as e:
        print(f"Error while reading CSV file: {e}")
    try: # error check 3of3: check if product has expired: 
        with open(path_to_csv_bought_file, 'r', newline='') as file:
            reader_bought_csv = csv.DictReader(file)
            for reader_bought_row in reader_bought_csv:
                    if reader_bought_row['buy_id'] == bought_product_id:
                        expiry_date = reader_bought_row['expiry_date']
                        if expiry_date != 'does not expire': 
                            if expiry_date < sell_date:
                                console = Console()
                                console.print(f"Warning: You have  just sold an expired product with buy_id << {bought_product_id} >>." 
                                    f" Please check if this is what you want.",style="bold yellow")
    except FileNotFoundError:
        print(f"File not found.")
    except PermissionError:
        print(f"You don't have permission to access the file.")
    except UnicodeDecodeError:
        print(f"Invalid Unicode character found in the file.")
    except csv.Error as e:
        print(f"Error while reading CSV file: {e}")
    try: # create sell transaction in sold.csv:           
        with open(path_to_csv_sold_output_file, 'w', newline='') as file: 
            rows.append({'sell_id': sold_product_id, 'buy_id': bought_product_id, 'sell_price': sell_price, 'sell_date': sell_date}) 
            writer = csv.DictWriter(file, fieldnames= reader.fieldnames)
            writer.writeheader()
            # sort rows by sell_id (== first column in sold.csv):
            sorted_rows = sorted(rows, key=lambda row: row['sell_id'])
            writer.writerows(sorted_rows)
    except PermissionError:
        print(f"You don't have permission to write to '{path_to_csv_sold_output_file}'.")
    except csv.Error as e:
        print(f"Error while writing CSV file: {e}")

    return [sold_product_id, bought_product_id, sell_price, sell_date] # used to show data in console in table with module rich (see fn sell_product() in super.py)

def sell_product_by_product_name(product_name, sell_price,  sell_date, calculate_inventory, calculate_expired_products, find_product, path_to_csv_sold_input_file, path_to_csv_sold_output_file, path_to_csv_bought_file):
    inventory = calculate_inventory(sell_date, path_to_csv_sold_input_file, path_to_csv_bought_file) #list with transactions as lists
    buy_transaction_record_in_inventory = None
    buy_transaction_record_in_inventory = find_product(inventory, product_name) # returns buy_transaction or 'product_not_found'
    inventory_product_list = [] 
    inventory_product_list = [sublist[1] for sublist in inventory]
    inventory_product_list = list(set(inventory_product_list))
    expired_products = calculate_expired_products(sell_date, path_to_csv_sold_input_file, path_to_csv_bought_file) #list with transactions as lists
    buy_transaction_record_in_expired_products = None
    buy_transaction_record_in_expired_products = find_product(expired_products, product_name) # returns buy_transaction or 'product_not_found'
    expired_products_list = [] 
    expired_products_list = [sublist[1] for sublist in expired_products]
    expired_products_list = list(set(expired_products_list))
    sold_product_id = '' 
    bought_product_id = '' 

    if buy_transaction_record_in_inventory == 'product_not_found':
        console = Console()
        console.print(f"Product < {product_name} > is not in the inventory on sell_date: {sell_date}.",style="bold red")
        console.print(f"Inventory on {sell_date}: {inventory_product_list}.",style="bold green")
        console.print() 

    if buy_transaction_record_in_inventory == 'product_not_found' and buy_transaction_record_in_expired_products == 'product_not_found':
        console = Console()
        console.print(f"Product < {product_name} > is not in the list with expired products on sell_date: {sell_date}.",style="bold red")
        console.print(f"Expired products on {sell_date}: {expired_products_list}.",style="bold green")  
        console.print() 

    if buy_transaction_record_in_inventory == 'product_not_found' and buy_transaction_record_in_expired_products == 'product_not_found':
        products_in_bought_csv = []
        try: # check if product is in the product range altogether: 
            with open(path_to_csv_bought_file, 'r', newline='') as file: 
                reader = csv.DictReader(file)
                rows = list(reader)
                for row in rows:
                    products_in_bought_csv.append(row['product'])
                file.seek(0)
        except FileNotFoundError:
            print(f"File '{path_to_csv_bought_file}' not found.")
        except PermissionError:
            print(f"You don't have permission to access '{path_to_csv_bought_file}'.")
        except UnicodeDecodeError:
            print(f"Invalid Unicode character found in '{path_to_csv_bought_file}'.")
        except csv.Error as e:
            print(f"Error while reading CSV file: {e}")
        unique_products_in_bought_csv = list(set(products_in_bought_csv))
        if product_name in unique_products_in_bought_csv:
            console = Console()
            console.print()
            console.print(f"* Product < {product_name} > is in the Superpy product range.",style="bold green") 
            console.print(f"To provide a quick alternative to the client, check if there is a similar product in the\n"
                f" Superpy product range:",style="bold green")
            console.print(f"{unique_products_in_bought_csv}.", style="bold green")
        if product_name not in unique_products_in_bought_csv:
            console = Console()
            console.print()
            console.print(f"Product < {product_name} > is not in the product range of Superpy at all. ",style="bold red")
            console.print(f"To provide a quick alternative to the client, check if there is a similar product in the \n"
                f"Superpy product range: \n",style="bold green")
            console.print(f"{unique_products_in_bought_csv}.", style="bold green")
        if buy_transaction_record_in_inventory == 'product_not_found' and buy_transaction_record_in_expired_products == 'product_not_found':
            console = Console()
            console.print()
            console.print("The following transaction has NOT been added to SOLD.CSV:", style="bold red")

        if buy_transaction_record_in_inventory == 'product_not_found' or buy_transaction_record_in_expired_products == 'product_not_found':
            return 'product_is_not_sold' 

    if not buy_transaction_record_in_inventory == 'product_not_found' or not buy_transaction_record_in_expired_products == 'product_not_found':   
        # happy flow for customer: product is in inventory or list with expired_products on that date, so it can be sold.    
        if buy_transaction_record_in_inventory != 'product_not_found':
            bought_product_id = buy_transaction_record_in_inventory[0]
            buy_price = buy_transaction_record_in_inventory[2]
            expiry_date = buy_transaction_record_in_inventory[4]  

            console = Console()
            console.print(f"Product < {product_name} > is in the inventory on sell_date: {sell_date}.",style="bold green")
            console.print(f"Inventory on {sell_date}: {inventory_product_list}.",style="bold green")  
            console.print() 

        elif buy_transaction_record_in_inventory == 'product_not_found' and buy_transaction_record_in_expired_products != 'product_not_found':
            bought_product_id = buy_transaction_record_in_expired_products[0]
            buy_price = buy_transaction_record_in_expired_products[2]
            expiry_date = buy_transaction_record_in_expired_products[4]

            console = Console()
            console.print(f"Product < {product_name} > is in the list with expired products on sell_date: {sell_date}.",style="bold green")
            console.print(f"Expired products on {sell_date}: {expired_products_list}.",style="bold green")  
            console.print() 
        else:
            console = Console()
            console.print('Error: Cannot find transaction_record that can be sold inside fn sell_product_by_product_name() in utils.py.', style="bold red")
        sold_product_id = '' 
        try: # create sell transaction in sold.csv:
            with open(path_to_csv_sold_input_file, 'r', newline='') as file: 
                reader = csv.DictReader(file)
                rows = list(reader)
                file.seek(0)           
                sold_product_id = bought_product_id.replace('b', 's')
        except FileNotFoundError:
            print(f"File '{path_to_csv_sold_input_file}' not found.")
        except PermissionError:
            print(f"You don't have permission to access '{path_to_csv_sold_input_file}'.")
        except UnicodeDecodeError:
            print(f"Invalid Unicode character found in '{path_to_csv_sold_input_file}'.")
        except csv.Error as e:
            print(f"Error while reading CSV file: {e}")
        try:            
            with open(path_to_csv_sold_output_file, 'w', newline='') as file: 
                rows.append({'sell_id': sold_product_id, 'buy_id': bought_product_id, 'sell_price': sell_price, 'sell_date': sell_date}) 
                writer = csv.DictWriter(file, fieldnames= reader.fieldnames)
                writer.writeheader()
                sorted_rows = sorted(rows, key=lambda row: row['sell_id'])
                writer.writerows(sorted_rows)
        except PermissionError:
            print(f"You don't have permission to write to '{path_to_csv_sold_output_file}'.")
        except csv.Error as e:
            print(f"Error while writing CSV file: {e}")
        if expiry_date != 'does not expire': 
            if datetime.strptime(sell_date, '%Y-%m-%d') > datetime.strptime(expiry_date, '%Y-%m-%d'):
                console = Console()
                console.print(f"Warning: you have just sold product < {product_name} > with sell_date < {sell_date} > greater than\n its expiry_date < {expiry_date} >. " 
                            f"Are  you sure about this?",style="bold yellow")
        if float(sell_price) < float(buy_price):
            console = Console()
            console.print()
            console.print(f"Warning: you have just sold product < {product_name} > with sell_date < {sell_date} > and sell_id\n < {sold_product_id} > at a loss of € < {round(float(buy_price) - sell_price,2)} >. "
                        f"Are  you sure about this?",style="bold yellow")
    return [sold_product_id, bought_product_id, sell_price, sell_date]  

def set_buy_id_counter_txt(buy_id: str, path_to_buy_id_file: str) -> str:
    if buy_id == None: # read: if bought.csv is empty
        buy_id = 'b_00' 
    try:
        with open(path_to_buy_id_file, 'w', newline='') as file:
            file.write(buy_id)
    except PermissionError:
        print(f"You don't have permission to write to '{path_to_buy_id_file}'.")
    except IOError as e:
        print(f"Error while writing file: {e}")
    return buy_id

def set_system_date_to(system_date: str, path_to_system_date: str) -> datetime:
    try:
        with open(path_to_system_date, 'w', newline='') as file:
            file.write(system_date)
    except PermissionError:
        print(f"You don't have permission to write to '{path_to_system_date}'.")
    except IOError as e:
        print(f"Error while writing file: {e}")
    return system_date

def show_header(list: list):
    console = Console()
    table = Table(show_header=False)
    for information in list:
        table.add_row(str(information))
    console.print(table)

def show_csv_file(path_to_csv_file: str) -> None:
    console = Console()
    table = Table(show_header=True, header_style="bold magenta")
    try:
        with open(path_to_csv_file, 'r') as file:
            csv_reader = csv.reader(file)
            header = next(csv_reader)  
            for column in header:
                
                if column == 'product':
                    table.add_column(column, style="dim", width=50)
                else: 
                    table.add_column(column)
            for row in reversed(list(csv_reader)):
                table.add_row(*row)
    except FileNotFoundError:
        print(f"File '{path_to_csv_file}' not found.")
    except PermissionError:
        print(f"You don't have permission to access '{path_to_csv_file}'.")
    except UnicodeDecodeError:
        print(f"Invalid Unicode character found in '{path_to_csv_file}'.")
    except csv.Error as e:
        print(f"Error while reading CSV file: {e}")
    console.print(table)

def show_superpy_logistic_info(description, list_of_lists: list):
    console = Console()
    table = Table(show_header=True, header_style="bold magenta")
    table.add_column(description)
    table.add_column("Value")
    for list in list_of_lists:
        table.add_row(str(list[0]), str(list[1]))
    console.print(table)

def show_superpy_system_info(current_action_in_superpy, system_date, get_weekday_from_date):
    console = Console() 
    table = Table(show_header=True, header_style="bold magenta")
    table.add_column("Description")
    table.add_column("Value")
    table.add_row("Superpy SYSTEM_DATE", f"{system_date} ({get_weekday_from_date(system_date)})")
    table.add_row("Host machine date", f"{datetime.now().date()} ({get_weekday_from_date(datetime.now().date().strftime('%Y-%m-%d'))})")
    table.add_row("Current action", current_action_in_superpy)
    table.add_row("Host machine", socket.gethostname())
    console.print(table)

def show_selected_buy_transactions(list: list) -> Table: # input is list with lists.
    rich_table = Table(show_header=True, header_style="bold magenta")
    rich_table.add_column('buy_id', style="dim", width=12)
    rich_table.add_column('product', style="dim", width=50)
    rich_table.add_column('buy_price €', style="dim", width=12)
    rich_table.add_column('buy_date', style="dim", width=12)
    rich_table.add_column('expiry_date', style="dim", width=12)
    for row in list:
        rich_table.add_row(*row)
    console = Console()
    console.print(rich_table)
    return rich_table

def travel_time(
        nr_of_days_to_travel: int, 
        path_to_input_file: str, 
        path_to_output_file: str
    ) -> str:
    try:
        with open(path_to_input_file, 'r', newline='') as file:
            current_system_date = file.readline().split(',')[0]
            file.seek(0)
    except FileNotFoundError:
        print(f"File '{path_to_input_file}' not found.")
    except PermissionError:
        print(f"You don't have permission to access '{path_to_input_file}'.")
    except UnicodeDecodeError:
        print(f"Invalid Unicode character found in '{path_to_input_file}'.")
    except IOError as e:
        print(f"Error while reading file: {e}")
    try:
        with open(path_to_output_file, 'w', newline='') as file:
            new_system_date = add_days_to_date(current_system_date, nr_of_days_to_travel)
            file.write(new_system_date)
    except PermissionError:
        print(f"You don't have permission to write to '{path_to_output_file}'.")
    except IOError as e:
        print(f"Error while writing file: {e}")  
    return new_system_date