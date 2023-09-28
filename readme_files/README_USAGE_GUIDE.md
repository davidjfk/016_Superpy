## Table of contents
- [Intro](#intro)
- [Argparse commands and arguments](#argparse-commands-and-arguments)
  - [Buy Product](#buy-product)
  - [Create mock data](#create-mock-data)
  - [Delete](#delete)
  - [Reset system date](#reset-system-date)
  - [Sell product](#sell-product)
  - [Set system date](#set-system-date)
  - [Show bought.csv](#show-boughtcsv)
  - [Show cost](#show-cost)
  - [SHOW\_EXPIRED\_PRODUCTS](#show_expired_products)
  - [Show inventory](#show-inventory)
  - [Show profit](#show-profit)
  - [Show revenue](#show-revenue)
  - [Show sales volume](#show-sales-volume)
  - [Show sold.csv](#show-soldcsv)
  - [Time travel](#time-travel)
- [USE CASES](#use-cases)
  - [intro](#intro-1)
  - [UC: get familiar with the data](#uc-get-familiar-with-the-data)
  - [UC: buy and sell a few products](#uc-buy-and-sell-a-few-products)
  - [UC: show all management reports](#uc-show-all-management-reports)
  - [UC: create\_mock\_date and add buy and sell transactions](#uc-create_mock_date-and-add-buy-and-sell-transactions)
  - [UC: buy products in all syntax-variations](#uc-buy-products-in-all-syntax-variations)
  - [UC: sell products in all syntax-variations](#uc-sell-products-in-all-syntax-variations)
  - [UC: time travel to the future and past](#uc-time-travel-to-the-future-and-past)
  - [UC: make profit](#uc-make-profit)
  - [UC: make loss](#uc-make-loss)
  - [UC: inventory "versus" expired products...let's time\_travel](#uc-inventory-versus-expired-productslets-time_travel)
  - [UC: show reports from start of financial year](#uc-show-reports-from-start-of-financial-year)
- [INSTALLATION](#installation)
- [DEFINITIONS](#definitions)
- [LOCATION OF IMPORTANT DIRECTORIES AND FILES](#location-of-important-directories-and-files)
- [DATA-MODEL](#data-model)
- [Testing the application in pytest](#testing-the-application-in-pytest)
  - [1of2: run regression testcases:](#1of2-run-regression-testcases)
  - [2of2: create testdata for additional testcases:](#2of2-create-testdata-for-additional-testcases)
- [Trouble shooting](#trouble-shooting)
- [FAQ](#faq)
- [Support](#support)

<br/>

# Intro
[Table of contents](#table-of-contents)

- ARGPARSE-COMMANDS-AND-ARGUMENTS
- USE-CASES
- INSTALLATION
- DEFINITIONS
- LOCATION-OF-IMPORTANT-DIRECTORIES-AND-FILES
- DATA-MODEL
- TESTING-THE-APPLICATION-IN-**PYTEST**
- TROUBLE-SHOOTING
- FAQ
- SUPPORT 

<br/>

Application Superpy can be used to buy and sell products. In addition to that  
all kinds of reports can be created: revenue, cost,  profit, inventory, expired_products, etc.  
Moreover, Superpy allows for setting and updating the system_date and  
time travelling to the past and future.  

The target group of this usage guide consists of Winc Academy students.  
Winc students are familiar with python, vsCode 
and running applications via argparse cli.


This is a hands-on document to get you, the Superpy user, up to speed with using Superpy  
as quickly as possible. So the first 2 chapters of this manual are about:
1. ARGPARSE-COMMANDS-AND-ARGUMENTS. --> the commands and arguments are the building  
    blocks of the workflows in the second chapter of this user manual.  
    Comprehensive info about all argparse commands and arguments is also available via:

```python
py super.py -h
```
2. WORKFLOWS --> workflows in Superpy are the meat of the matter for each
    Superpy user: workflows support and execute (parts of) business processes.  
    Business processes create value for the customer and generate return on investment for
    the supermarket chain using the Superpy-application. 
   
To learn Superpy faster, the following supporting features can be used via the cli:
1. quickly create mock data for bought.csv and sold.csv 
2. quickly delete all data in bought.csv and sold.csv 
3. quickly show current system_date in the console
4. quickly reset system_date
5. quickly show current contents of bought.csv in the console 
6. quickly show current contents of sold.csv in the console 
7. many commands use default values, so you can first try this:
```python
py super.py buy newspaper 0.29 

```
- explanation: buy_date (== -bd) has default value system_date (can be e.g. 2025-11-23).
- explanation: expiry_date (== -expd) has default value 'no expiry date'
and then try this:
```python
py super.py buy apple 0.29 -b tomorrow -e next_tuesday

```  
- explanation: buy_date (== -b) is tomorrow. Tomorrow == system_date "plus 1 day" (can be e.g. 2025-11-24).
- explanation: expiry_date (== -e) is next_tuesday. If system_date is e.g. 2025-11-23 on a Friday,  
    then next_tuesday is  2025-11-27.  

- remark: you can use 'py' or 'python' to run a scrip in the Superpy cli. 
<br/>
<br/>
- another ex: first try:
```python
py super.py create_mock_data  
```
<br/>

- explanation: create_mock_data with default values.  
- and  then try e.g. this:
```python
    py super.py create_mock_data  -product_range 24 -delete_every_nth_row 3 -shelf_life 100  
                                    -turnover_time 100 -markup 100 -lower_boundary_year 2023 
                                    -lower_boundary_month 9 -lower_boundary_day 18 
                                    -upper_boundary_month 3 -upper_boundary_week 3 
                                    -upper_boundary_day 3
```
- explanation: see next chapter argparse-commands-and-arguments. 
<br/>
<br/>
<br/>





# Argparse commands and arguments
[Table of contents](#table-of-contents)
<br/>


|Nr | Superpy functionality                             | Goal                                                        |
|---|---------------------------------------------------|-------------------------------------------------------------|
|1  | [Buy Product](#buy-product)                       | buy 1 product and add this product to bought.csv            | 
|2  | [Create mock data](#create-mock-data)             | fill bought.csv and sold.csv with mockdata.                 |
|3  | [Delete](#delete)                                 | delete all transaction records in bought.csv and sold.csv   |
|4  | [Reset system date](#reset-system-date)           | reset to current date on device Superpy is running on       |
|5  | [Sell Product](#sell-product)                     | buy 1 product and add this product to bought.csv            |
|6  | [Set system date](#set-system-date)               | set system_date  in system_date.txt                         |
|7  | [Show bought.csv](#show-bought.csv)               | show contents of bought.csv as a table                      |
|8  | [Show cost](#show-cost)                           | calculate and display cost of a time interval               |
|9  | [Show expired products](#show-expired-products)   | calculate and display expired products on a date            | 
|10 | [Show inventory](#show-inventory)                 | calculate and display inventory on a date                   |
|11 | [Show profit](#show-profit)                       | calculate and display profit of a time interval             |
|12 | [Show revenue](#show-revenue)                     | calculate and display revenue of a time interval            |
|13 | [Show sales volume](#show-sales-volume)           | calculate and display sales volume of a time interval       |
|14 | [Show sold.csv](#show-sold.csv)                   | show contents of bought.csv as a table                      |
|15 | [Show system date](#show-system-date)             | show system date from system_date.txt                       |
|16 | [Time_travel] (#time-travel)                      | change the system_date by adding or subtracing a nr of days |

<br/>

-   The Superpy argparse commands and arguments are like little building blocks, pieces of lego   
    with functionality so to speak.  
    Each one of them is explained comprehensively in this chapter, see the  following  table.

    Of each argparse command we  want to know the following:
    1. what does it do? (e.g. buy product, show sales volume, etc.)
    2. how can we use this functionality?

    In the next chapter these pieces of lego will be put together to create workflows,  
    like buying and selling products and then show all kinds of reports about profit,  
    inventory,  expired products, etc. 

<br /> 
<br /> 
<br />

## Buy Product
quick links: 
-  [Table of contents](#table-of-contents)
-  [Argparse commands and arguments](#argparse-commands-and-arguments)
<br/><br/>

Goal: buy product and add to file bought.csv 
- ex1: 

```
    py super.py buy apple 1.75 -b 23-09-15 -e 23-09-27 
```

-   product: apple,  price: &euro; 1.75, buy_date: 23-09-15, expiry_date: 23-09-27     

- ex2: 
```
    py super.py buy linseed 3.00 -e 23-09-28 
```
-   product: linseed, price: &euro; 3.00, buy_date: system_date as default, expiry_date: 23-09-28   

- ex3: 
```
    py super.py buy cabbage 0.73 
```
-   product: cabbage, price: &euro; 0.73, buy_date: system_date as default, expiry_date:  'does not expire' as default 
<br/>
- arg1: positional argument product: e.g. apple, potato, milk
- arg2: positional argument price, in euros: e.g. 1.24, 0.3, 0.35   
- arg3: optional argument -buy_date, -b (ex: 2023-09-15) with default value system_date 
- arg4: optional argument -expiry_date, -e (ex: 2023-10-03) with default value 'does not expire' 
<br/>
- arg with date value can be entered in format YYYY-MM-DD: e.g. 2029-02-03 , or as a word (exhaustive list):  
    today, tomorrow, overmorrow, yesterday, next_monday (...) next_sunday.

<br /> 
<br /> 
<br /> 

## Create mock data

quick links: 
-  [Table of contents](#table-of-contents)
-  [Argparse commands and arguments](#argparse-commands-and-arguments)
<br/><br/>


Goal: create mock data for bought.csv and sold.csv
- Of 8 arguments the default values can be changed in (...\superpy\super.py --> goto section 'CONFIGURATION' at start of main.py())
- Quick summary: 
- Mock data are created in a time interval (e.g. 2024-02-03 until 2024-04-03 inclusive). The system_date is automatically  
    set to the middle of the time interval: this is handy and practical when creating the reports: show_inventory, show_expired_products,    
    show profit, etc.
- All 11 arguments are optional, so you can do this:
```
    py super.py create_mock_data
```
-   result: bought.csv and sold.csv are filled with mockdata that has been created with default values. 
<br/>
<br/>

- arg1: product_range
    - flags: -pr, -product_range
    - product_range == product_assortment == the amount of different products in Superpy.
    - minimum value: 1 (generates 8 transactions in bought.csv) 
    - maximum value: 40 (generates 280 transactions in bought.csv)
    - ex1:
    ```
    py super.py create_mock_data -pr 3
    ```
    - product_range: 3 random products: e.g. 'apple', 'cabbage' and 'beetroot' as input to create mock data
    <br />
    - ex2:
    ```
    py super.py create_mock_data -pr 2
    ```
    - product_range: 2 random products: e.g. 'coffee' and 'potato' as input to create mock data.

<br />
<br/>

- arg2: delete_every_nth_row
    - delete_every_nth_row == delete every nth row in sold.csv
    - Purpose: deleting rows makes them expire while time travelling:
    - after creating mock data for bought.csv, a copy is made to create sold.csv.
    - Then rows are deleted from sold.csv (e.g. every 3rd row).
    - By time travelling to the future these bought_products (e.g. every 3rd row) will expire.
    - flags: -denr, -delete_every_nth_row

    - ex1:
    ```
    py super.py create_mock_data -denr 3
    ```
    - delete_every_nth_row: 3 
    
<br />
<br/>

- arg3: shelf_life
    - shelf_life == shelf_time == number of days between buying a product and its expiry_date
    - flags: -sl, -shelf_life

    - ex1:
    ```
    py super.py create_mock_data -del_row 3
    ```
    - shelf_life: 10 days
    - result: a bought product will expire after 10 days.
<br />
<br/>

- arg4: turnover_time
    - turnover_time == inventory turnover == the number of days between buying a product in bought.csv  
        and selling a product in sold.csv.
    - flags: -turnover_time, -tt

    - ex1:
    ```
    py super.py create_mock_data -tt 4
    ```
    - turnover_time: 4 days
    - result: a bought product will expire after 10 days.
<br />
<br/>

- arg5: markup
    - markup = the amount of money a business adds to the cost of a product or service in order to make a profit.
    - In super.py markup is calculated as a factor: ex: if buy_price is 3 euro and sell_price is 4 euro,  
        then markup is 4/3 = 1.33 . 
    - flags: -mu, -markup

    - ex1:
    ```
    py super.py create_mock_data -mu 3
    ```
    - markup: factor 3
    - result: if buy_price in bought.csv is 3 euro, then sell_price will be 9 euro in sold.csv.
<br />
<br/>

- arg6: lower_boundary_year
    - lower_boundary_year == lower_boundary_year_of_time_interval_in_which_to_create_random_testdata.
    - flags: -lby, -lower_boundary_year 

    - ex1:
    ```
    py super.py create_mock_data -lby 2024
    ```
    - lower_boundary_year: 2024

<br />
<br/>

- arg7: lower_boundary_month
    - lower_boundary_month == lower_boundary_month_of_time_interval_in_which_to_create_random_testdata.
    - flags: -lbm, -lower_boundary_month 

    - ex1:
    ```
    py super.py create_mock_data -lbm 10
    ```
    - lower_boundary_month: October

<br />
<br/>

- arg8: lower_boundary_day
    - lower_boundary_day == lower_boundary_day_of_time_interval_in_which_to_create_random_testdata.
    - flags: -lbd, -lower_boundary_day 

    - ex1:
    ```
    py super.py create_mock_data -lbd 15
    ```
    - lower_boundary_day: 15th day of  the  month

<br />
<br/>

- arg9: nr_of_months_to_calculate_upper_boundary_month
    - flags: -ubmnr, -upper_boundary_month_nr

    - ex1:
    ```
    py super.py create_mock_data -ubmnr 3
    ```
    - nr_of_months_to_calculate_upper_boundary_month: 3 months
    - result: upper boundary month of time interval in which to create data is 3 months in the future

<br />
<br/>

- arg10: nr_of_weeks_to_calculate_upper_boundary_week
    - flags: -ubwnr, -upper_boundary_weeknr

    - ex1:
    ```
    py super.py create_mock_data -ubwnr 8
    ```
    - nr_of_weeks_to_calculate_upper_boundary_month: 3 weeks
    - result: upper boundary week of time interval in which to create data is 8 weeks in the future

<br />
<br/>

- arg11: nr_of_days_to_calculate_upper_boundary_day
    - flags: -ubwnr, -upper_boundary_weeknr

    - ex1:
    ```
    py super.py create_mock_data -ubdnr 3
    ```
    - nr_of_days_to_calculate_upper_boundary_day: 3 weeks
    - upper boundary day of time interval in which to create data is 3 days in the future

<br />
<br/>


```
    py super.py show_profit -ed 2023-10-05
```
-   start_date: start of financial  year of system_date. e.g. if system_date 23-06-08, then: 23-01-01
-   end_date: 2023-10-05
-   result in terminal:  
    'profit from start_date: 2023-01-01 to end_date: 2023-10-05 inclusive: Euro 18.6'


- ex3: 
```
    py super.py show_profit -sd 2023-07-01
```
-   start_date: 2023-07-01
-   end_date: end_date is by default system_date (here, e.g. 2023-09-17) 
-   result in terminal:  
    'Profit from start_date: 2023-07-01 to end_date: 2023-09-17 inclusive: Euro 9.9'  


- arg1: optional argument start_date in format 'YYYY-MM-DD'. ex: -sd 2023-09-01, or: -start_date 2023-09-01  
    default value is january 1st of year from system_date: e.g. if system_date is 23-06-28, then default value is 23-01-01.  
    reason: often you want to know the cost of the current financial year until today inclusive.  

- arg2: optional argument end_date in format 'YYYY-MM-DD'. ex: -ed 2023-10-15, or: -end_date 2023-10-15  
    default value is system_date, because often you want to know the cost of the current financial year until today  inclusive.


 
<br /> 
<br /> 
<br /> 

## Delete

quick links: 
-  [Table of contents](#table-of-contents)
-  [Argparse commands and arguments](#argparse-commands-and-arguments)
<br/><br/>
Goal: delete all data in bought.csv and sold.csv

- ex1: 

```
    py super.py delete 
```

- result: all transaction records in bought.csv and sold.csv have been deleted


<br /> 
<br /> 
<br /> 

## Reset system date
quick links: 
-  [Table of contents](#table-of-contents)
-  [Argparse commands and arguments](#argparse-commands-and-arguments)
<br/><br/>
Goal: reset system_date in system_date.txt (...\superpy\data_used_in_superpy\system_date.txt) to   
    current date on the device Superpy is running on.

- ex1: 

```
    py super.py reset_system_date 
```

- result: system_date.txt now contains current system_date from the  device Superpy is running on.


<br /> 
<br /> 
<br /> 

## Sell product
quick links: 
-  [Table of contents](#table-of-contents)
-  [Argparse commands and arguments](#argparse-commands-and-arguments)
<br/><br/>

Goal: sell product and add to file sold.csv 

- ex1: 

```
    py super.py b_15 3.75 -s 2023-11-15 
```

-   product: row with id b_15 in bought.csv is sold, price: &euro; 3.75, sell_date: 23-11-15

- ex2: 
```
    py super.py b_16 5.15
```
-   product: row with id b_15 in bought.csv is sold, price: &euro; 5.15, sell_date: system_date as default     

- ex3: 
```
    py super.py b_128 2.42 
```
-   product: row with id b_128 in bought.csv is sold, price: &euro; 2.42, sell_date: system_date as default
<br/>
- arg1: positional argument buy_id: e.g. b_7, b_18, etc. See bought.csv for buy_ids
- arg2: positional argument price, in euros: e.g. 1.24, 0.3, 0.35  
- arg3: optional argument -sell_date, -s (ex: -sd 2023-09-15) with default value system_date 
<br/>
- arg with date value can be entered in format YYYY-MM-DD: e.g. 2029-02-03 , or as a word (exhaustive list):  
    today, tomorrow, overmorrow, yesterday, next_monday (...) next_sunday.
<br /> 
<br /> 
<br /> 

## Set system date
quick links: 
-  [Table of contents](#table-of-contents)
-  [Argparse commands and arguments](#argparse-commands-and-arguments)
<br/><br/>
Goal: set_system_date_to a specific date in the file system_date.txt 

- ex1: 

```
    py super.py set_system_date 2025-01-01
```

- system_date: 2025-01-01   
- result: 'Superpy system_date is set to date: 2025-01-01'

- ex2: 

```
    py super.py set_system_date 2023-09-20 
```

- system_date: 2023-09-20
- result: 'Superpy system_date is set to date: 2023-09-20'
</br>
- arg1: positional argument system_date, e.g. 2023-10-11 --> string representation in format 'yyy-mm-dd'<br/>
</br>
- arg with date value can be entered in format YYYY-MM-DD: e.g. 2029-02-03 , or as a word (exhaustive list):  
    today, tomorrow, overmorrow, yesterday, next_monday (...) next_sunday.

<br /> 
<br /> 
<br /> 

## Show bought.csv
quick links: 
-  [Table of contents](#table-of-contents)
-  [Argparse commands and arguments](#argparse-commands-and-arguments)
<br/><br/>

Goal: show all data from bought.csv in a table in the terminal

- ex1: 

```
    py super.py show_bought_csv
```

- result: bought.csv is shown in the terminal as a table 


<br /> 
<br /> 
<br /> 

## Show cost
quick links: 
-  [Table of contents](#table-of-contents)
-  [Argparse commands and arguments](#argparse-commands-and-arguments)
<br/><br/>
Goal: show cost in time range between start_date and end_date inclusive

- ex1: 

```
    py super.py show_cost -sd 2023-09-01 -ed 2023-10-10 
```
-   start_date: 2023-09-01, 
-   end_date: 2023-10-10
-   result in terminal:  
    'Cost from start_date: 2023-09-01 to end_date: 2023-10-10 inclusive: Euro 27.9'   

- ex2: 
```
    py super.py show_cost -ed 2023-10-05
```
-   start_date is by default start of financial  year of system_date. e.g. if system_date 23-06-08, then: 23-01-01.  
-   end_date: 2023-10-05
-   result in terminal:  
    'Cost from start_date: 2023-01-01 to end_date: 2023-10-05 inclusive: Euro 18.6'  


- ex3: 
```
    py super.py show_cost -sd 2023-07-01
```
-   start_date: 2023-07-01 
-   end_date is by default system_date (here, e.g. 2023-09-17) 
-   result in terminal:  
    'Cost from start_date: 2023-07-01 to end_date: 2023-09-17 inclusive: Euro 9.9'  


- arg1: optional argument start_date in format 'YYYY-MM-DD'. ex: -sd 2023-09-01, or: -start_date 2023-09-01  
    default value is january 1st of year from system_date: e.g. if system_date is 23-06-28, then default value is 23-01-01.  
    reason: often you want to know the cost of the current financial year until today inclusive.  

- arg2: optional argument end_date in format 'YYYY-MM-DD'. ex: -ed 2023-10-15, or: -end_date 2023-10-15  
    default value is system_date, because often you want to know the cost of the current financial year until today  inclusive.
    
 
<br /> 
<br /> 
<br /> 

## SHOW_EXPIRED_PRODUCTS
quick links: 
-  [Table of contents](#table-of-contents)
-  [Argparse commands and arguments](#argparse-commands-and-arguments)
<br/><br/>
Goal: calculate expired products on a day in format 'YYYY-MM-DD' (e.g. 2023-09-18)

- ex1: 

```
    py super.py show_expired_products -d 23-09-28
```
-   date: 2023-09-28, 
-   result is displayed in table in the terminal:  
 

- ex2: 
```
    py super.py show_expired_products -ed 2023-10-05
```
-   date: by default system_date
-   end_date: 2023-10-05
-   result is displayed in table in the terminal:    


- arg1: optional argument date in following format: 'YYYY-MM-DD'. ex: -d 2026-10-21, or: -date 2026-10-21 
    default value is system_date
    reason: often you want to know which products expire today. 

 
<br /> 
<br /> 
<br /> 

## Show inventory
quick links: 
-  [Table of contents](#table-of-contents)
-  [Argparse commands and arguments](#argparse-commands-and-arguments)
<br/><br/>
Goal: calculate inventory on a day in format 'YYYY-MM-DD' (e.g. 2023-09-18)

- ex1: 

```
    py super.py show_inventory -d 23-09-28
```
-   date: 2023-09-28, 
-   result is displayed in table in the terminal:  
 

- ex2: 
```
    py super.py show_inventory -ed 2023-10-05
```
-   date: by default system_date
-   end_date: 2023-10-05
-   result is displayed in table in the terminal:    


- arg1: optional argument date in following format: 'YYYY-MM-DD'. ex: -d 2026-10-21, or: -date 2026-10-21 
    default value is system_date
    reason: often you want to know which products expire today. 


<br /> 
<br /> 
<br /> 

## Show profit
quick links: 
-  [Table of contents](#table-of-contents)
-  [Argparse commands and arguments](#argparse-commands-and-arguments)
<br/><br/>
Goal: show profit in time range between start_date and end_date inclusive

- ex1: 

```
    py super.py show_profit -sd 2023-09-01 -ed 2023-10-10
```
-   start_date: 2023-09-01, 
-   end_date: 2023-10-10
-   result in terminal:  
    'Profit from start_date: 2023-09-01 to end_date: 2023-10-10 inclusive: Euro 27.9'   

- ex2: 
```
    py super.py show_profit -ed 2023-10-05
```
-   start_date: start of financial  year of system_date. e.g. if system_date 23-06-08, then: 23-01-01
-   end_date: 2023-10-05
-   result in terminal:  
    'profit from start_date: 2023-01-01 to end_date: 2023-10-05 inclusive: Euro 18.6'


- ex3: 
```
    py super.py show_profit -sd 2023-07-01
```
-   start_date: 2023-07-01
-   end_date: end_date is by default system_date (here, e.g. 2023-09-17) 
-   result in terminal:  
    'Profit from start_date: 2023-07-01 to end_date: 2023-09-17 inclusive: Euro 9.9'  


- arg1: optional argument start_date in format 'YYYY-MM-DD'. ex: -sd 2023-09-01, or: -start_date 2023-09-01  
    default value is january 1st of year from system_date: e.g. if system_date is 23-06-28, then default value is 23-01-01.  
    reason: often you want to know the cost of the current financial year until today inclusive.  

- arg2: optional argument end_date in format 'YYYY-MM-DD'. ex: -ed 2023-10-15, or: -end_date 2023-10-15  
    default value is system_date, because often you want to know the cost of the current financial year until today  inclusive.


<br /> 
<br /> 
- -----------------------------------------------------------------------------------------------
<br /> 
<br /> 

## Show revenue
quick links: 
-  [Table of contents](#table-of-contents)
-  [Argparse commands and arguments](#argparse-commands-and-arguments)
<br/><br/>
Goal: show revenue in time range between start_date and end_date inclusive

- ex1: 

```
    py super.py show_revenue -sd 2023-09-01 -ed 2023-10-10
```
-   start_date: 2023-09-01, 
-   end_date: 2023-10-10
-   result in terminal:  
    'Cost from start_date: 2023-09-01 to end_date: 2023-10-10 inclusive: Euro 27.9'   

- ex2: 
```
    py super.py show_revenue -ed 2023-10-05
```
-   start_date: start of financial  year of system_date. e.g. if system_date 23-06-08, then: 23-01-01
-   end_date: 2023-10-05
-   result in terminal:  
    'Revenue from start_date: 2023-01-01 to end_date: 2023-10-05 inclusive: Euro 18.6'


- ex3: 
```
    py super.py show_revenue -sd 2023-07-01
```
-   start_date: 2023-07-01
-   end_date: end_date is by default system_date (here, e.g. 2023-09-17) 
-   result in terminal:  
    'Cost from start_date: 2023-07-01 to end_date: 2023-09-17 inclusive: Euro 9.9'  


- arg1: optional argument start_date in format 'YYYY-MM-DD'. ex: -sd 2023-09-01, or: -start_date 2023-09-01  
    default value is january 1st of year from system_date: e.g. if system_date is 23-06-28, then default value is 23-01-01.  
    reason: often you want to know the cost of the current financial year until today inclusive.  

- arg2: optional argument end_date in format 'YYYY-MM-DD'. ex: -ed 2023-10-15, or: -end_date 2023-10-15  
    default value is system_date, because often you want to know the cost of the current financial year until today  inclusive.


<br /> 
<br /> 
- -----------------------------------------------------------------------------------------------
<br /> 
<br /> 

## Show sales volume
quick links: 
-  [Table of contents](#table-of-contents)
-  [Argparse commands and arguments](#argparse-commands-and-arguments)
<br/><br/>
Goal: show sales_volume in time range between start_date and end_date inclusive

- ex1: 

```
    py super.py show_sales_volume -sd 2023-09-01 -ed 2023-10-10
```
-   start_date: 2023-09-01, 
-   end_date: 2023-10-10
-   result in terminal:  
    'Profit from start_date: 2023-09-01 to end_date: 2023-10-10 inclusive: Euro 27.9'   

- ex2: 
```
    py super.py show_sales_volume -ed 2023-10-05
```
-   start_date: start of financial  year of system_date. e.g. if system_date 23-06-08, then: 23-01-01
-   end_date: 2023-10-05
-   result in terminal:  
    'Sales volume from start_date: 2023-01-01 to end_date: 2023-10-05 inclusive: Euro 18.6'


- ex3: 
```
    py super.py show_sales_volume -sd 2023-07-01
```
-   start_date: 2023-07-01
-   end_date: end_date is by default system_date (here, e.g. 2023-09-17) 
-   result in terminal:  
    'Profit from start_date: 2023-07-01 to end_date: 2023-09-17 inclusive: Euro 9.9'  


- arg1: optional argument start_date in format 'YYYY-MM-DD'. ex: -sd 2023-09-01, or: -start_date 2023-09-01  
    default value is january 1st of year from system_date: e.g. if system_date is 23-06-28, then default value is 23-01-01.  
    reason: often you want to know the cost of the current financial year until today inclusive.  

- arg2: optional argument end_date in format 'YYYY-MM-DD'. ex: -ed 2023-10-15, or: -end_date 2023-10-15  
    default value is system_date, because often you want to know the cost of the current financial year until today  inclusive.


<br /> 
<br /> 
- -----------------------------------------------------------------------------------------------
<br /> 
<br /> 

## Show sold.csv
quick links: 
-  [Table of contents](#table-of-contents)
-  [Argparse commands and arguments](#argparse-commands-and-arguments)
<br/><br/>

Goal: show all data from sold.csv in a table in the terminal.

- ex1: 

```
    py super.py show_sold_csv
```

- result: sold.csv is shown in the terminal as a table  




<br /> 
<br /> 
- -----------------------------------------------------------------------------------------------
<br /> 
<br /> 

## Time travel 
quick links: 
-  [Table of contents](#table-of-contents)
-  [Argparse commands and arguments](#argparse-commands-and-arguments)
<br/><br/>

- goal: change system_date by adding or subtracting nr of day(s)

- ex1: 

```
    py super.py time_travel 3
```
-  nr_of_days: 3
- result: you travel with 3 days to the future. So if system_date is 2020-03-10, then  
  new date becomes 2020-03-13 in the future.

- ex2: 
```
    py super.py time_travel -3
```
-  nr_of_days: -3
- result: you travel with 3 days to the past. So if system_date is 2020-03-10, then  
  new date becomes 2020-03-07 in the past.  

- arg1: positional argument days to add or subtract from system_date: e.g. 9, -8, etc.





<br /> 
<br /> 

# USE CASES
quick links: 
-  [Table of contents](#table-of-contents)
-  [Argparse commands and arguments](#argparse-commands-and-arguments)
<br/><br/>


## intro 
[Table of contents](#table-of-contents)

-   The commands and arguments from the previous chapter, a.k.a. building blocks that each provide  
    a certain functionality a.k.a. lego blocks are put together in this chapter to create
    use cases (ucs).

    A use case is a description of how Superpy will be used by its user to achieve a  
    specific goal. The use cases (ucs) below describe the interaction between the user and  
    the Superpy, and the steps that Superpy will take to complete the user's goal.  


    The  following ucs are examples. Feel free to combine the commands and arguments  
    into your own  ucs.  

    The example ucs start easy using default optional values, and gradually become more  
    difficult using custom optional arguments.  
    The intro of  this document contains 2 examples of this:

        ```python
        py super.py buy newspaper 0.29 

        ```
        explanation: buy_date (== -bd) has default value system_date (can be e.g. 2025-11-23).
        explanation: expiry_date (== -e) has default value 'no expiry date'
        and then try this:
        ```python
        py super.py buy apple 0.29 -b tomorrow -expd next_tuesday

        ```  
        explanation: buy_date (== -b) is tomorrow. Tomorrow == system_date "plus 1 day" (can be e.g. 2025-11-24).
        explanation: expiry_date (== -expd) is next_tuesday. If system_date is e.g. 2025-11-23 on a Friday,  
            then next_tuesday is  2025-11-27. 
        <br/>
        another ex: first try:
        ```python
        py super.py create_mock_data  
        ```
        <br/>
        explanation: create_mock_data with default values.  
        <br/>

        and  then try e.g. this:
        ```python
            py super.py create_mock_data  -product_range 24 -delete_every_nth_row 3 -shelf_life 100  
                                            -turnover_time 100 -markup 100 -lower_boundary_year 2023 
                                            -lower_boundary_month 9 -lower_boundary_day 18 
                                            -upper_boundary_month 3 -upper_boundary_week 3 
                                            -upper_boundary_day 3
        ```
        explanation: see next chapter argparse-commands-and-arguments. 

    If you have  any questions about the commands and arguments in the following workflows, then either go to  
    chapter superpy-commands-and-arguments or:  

    ```python
    py super.py -h
    ```
    <br/>

    Before diving into the workflows, plz read the following.  
    An argparse argument with date value can be entered in format YYYY-MM-DD: e.g.  
    2029-02-14, or as a word (exhaustive list): today, tomorrow, overmorrow, yesterday,  
    next_monday (...) next_sunday.  

    Reference point: today == system_date (see definition of system_date)  
    compare the dates in the following two cli commands:

        ```python
        py super.py buy apple 0.29 -b 2023-09-27 -e 2023-10-04
        py super.py buy apple 0.29 -b tomorrow -e next_tuesday
        py super.py buy apple 0.29 -b yesterday -e next_sunday
        py super.py buy apple 0.29 -b 2023-09-15 -e today

        ```  
        <br/>
        Another example
        ```python
        py super.py set_system_date 2023-09-27
        py super.py set_system_date 2022-10-15
        py super.py set_system_date yesterday
        py super.py set_system_date tomorrow
        py super.py set_system_date next_thursday
        ```
        <br/>
    1. all optional arguments in Superpy have a long and a short form. Only the short form is used in the examples.

        |  short            |  long                                                                                         |
        |-------------------|-----------------------------------------------------------------------------------------------|
        | -b                | -buy_date                                                                                     |          
        | -denr             | -delete_every_nth_row                                                                         |   
        | -e                | -expiry-date
        | -lbd              | -'lower_boundary_day_of_time_interval_in_which_to_create_random_testdata'                     |
        | -lbm              | -lower_boundary_month_of_time_interval_in_which_to_create_random_testdatareset_system_date    |
        | -lby              | -lower_boundary_year_of_time_interval_in_which_to_create_random_testdata                      |
        | -mu               | -markup                                                                                       |
        | -pr               | -product_range                                                                                |
        | -s                | -sell_date                                                                                    |
        | -sl               | -shelf_life                                                                                   | 
        | -tt               | -turnover_time                                                                                |
        | -ubd              | -upper_boundary_nr_of_days_to_add_to_calculate                                                |
        | -ubm              | -upper_boundary_nr_of_months_to_add_to_calculate                                              |
        | -ubw              | -upper_boundary_nr_of_weeks_to_add_to_calculate                                               |


    <br/>
    Tip: copy-paste the code snippets into your cli.  
    Ready to Superpy rumble.
    <br/>






## UC: get familiar with the data
quick links: 
-  [Table of contents](#table-of-contents)
-  [Use cases](#use-cases)
<br/><br/>
    
    - step 1: 
    ```python
        py super.py create_mock_data
    ```
    - step 2: 
    ```python
        py super.py show_bought_csv
    ```
    - step 3: 
    ```python
        py super.py show_sold_csv
    ```
    - step 4:  
    ```python
        py super.py set_system_date next_tuesday
    ```
    
    - step 5:  
    ```python
        py super.py show_system_date
    ```
    - step 6: 
    ```python
        py super.py reset_system_date
    ```
    - step 7:  
    ```python
        py super.py show_system_date
    ```
    Superpy system_date is now equal to that of the host machine,  
    on which you are running Superpy. 

## UC: buy and sell a few products
quick links: 
-  [Table of contents](#table-of-contents)
-  [Use cases](#use-cases)
<br/><br/>
    - step 1: let's  start with a clean slate: so let's  
        delete all data (if any) in bought.csv and sold.csv:
    ```python
        py super.py delete
    ```       
    - step 2: observe that bought.csv and sold.csv do not  
            contain any transaction records:

    ```python
        py super.py show_bought_csv
        py super.py show_sold_csv
    ```  
    - step 3: reset the system_date to the system_date of your  
        host machine:
    ```python
        py super.py reset_system_date
    ```

    - step 4: buy the following products: 
    ```python
        py super.py buy apple 0.29 -b 2023-09-27 -e 2023-10-04
        py super.py buy banana 0.29 -b tomorrow -e next_tuesday
        py super.py buy mandarin 0.29 -b yesterday -e next_sunday
        py super.py buy pineapple 0.29 -b 2023-09-15 -e today
    
    ```
    - step 5: show transactions in bought.csv:
    ```python
        py super.py show_bought_csv
    ```  
    - step 4: sell_product
    - step 5: show_sold_csv



        py super.py set_system_date 2023-09-27
        py super.py set_system_date 2022-10-15
        py super.py set_system_date yesterday
        py super.py set_system_date tomorrow
        py super.py set_system_date next_thursday


## UC: show all management reports
quick links: 
-  [Table of contents](#table-of-contents)
-  [Use cases](#use-cases)
<br/><br/>

    - step 1: create_mock_data
        by default: if data is created in time interval between e.g. 2024-02-01 and 2024-04-01, then  
                    the system_date is automatically set to the middle of the interval. 
    - step 2: show_cost
    - step 3: show_expired_products
    - step 4: show_inventory
    - step 5: show_profit
    - step 6: show_revenue
    - step 7: show_cost
    - step 8: show_sales_volume


## UC: create_mock_date and add buy and sell transactions
quick links: 
-  [Table of contents](#table-of-contents)
-  [Use cases](#use-cases)
<br/><br/>
    - step 1: let's  start with a clean slate: so let's  
        delete all data in bought.csv and sold.csv
    - step 2: buy the following products:
    - 
    - step 1: create_mock_data
    - step 2: buy_product
    - step 3: show_bought_csv
    - step 4: sell_product
    - step 5: show_sold_csv



## UC: buy products in all syntax-variations 
-  [Table of contents](#table-of-contents)
-  [Use cases](#use-cases)
<br/><br/>


## UC: sell products in all syntax-variations 
quick links: 
-  [Table of contents](#table-of-contents)
-  [Use cases](#use-cases)
<br/><br/>


## UC: time travel to the future and past
quick links: 
-  [Table of contents](#table-of-contents)
-  [Use cases](#use-cases)
<br/><br/>

    - step 1: create_mock_data --> use custom optional arguments. 
        by default: if data is created in time interval between e.g. 2024-02-01 and 2024-04-01, then  
                    the system_date is automatically set to the middle of the interval. 
    - step 2: show_cost
    - step 3: show_expired_products
    - step 4: show_inventory
    - step 5: show_profit
    - step 6: show_revenue
    - step 7: show_cost
    - step 8: show_sales_volume
    - step 9: time_travel to the past and future and  check the differences in the reports. 

## UC: make profit
quick links: 
-  [Table of contents](#table-of-contents)
-  [Use cases](#use-cases)
<br/><br/>

## UC: make loss
quick links: 
-  [Table of contents](#table-of-contents)
-  [Use cases](#use-cases)
<br/><br/>

## UC: inventory "versus" expired products...let's time_travel
quick links: 
-  [Table of contents](#table-of-contents)
-  [Use cases](#use-cases)
<br/><br/>

## UC: show reports from start of financial year
quick links: 
-  [Table of contents](#table-of-contents)
-  [Use cases](#use-cases)
<br/><br/>


<br/><br/><br/>

# INSTALLATION
[Table of contents](#table-of-contents)
<br/>
1. The latest version of Superpy is in Github: https://github.com/davidjfk/David_Sneek_Superpy . Check if there is a newer version.
2. In Powershell navigate into folder Superpy 
3. create a virtual environment:
```python
    py -m venv env
```
<br/>
    remark: you can use 'py' or 'python' to run a scrip in the  cli. The differences do not matter  
    for Superpy.
4. activate virtual environment: 


    in Powersell:
```python
    .\env\Scripts\activate
``` 
    or in Git Bash:
```python
    source ./env/Scripts/activate
``` 
    To verify that the virtual environment is active, you should see  the name of the   
    virtual environment in parentheses at the beginning of your command prompt.

5. install all dependencies:
```python
   pip install -r requirements.txt
``` 

6. Ready to use Superpy. See next chapter Usage

7. To deactivate virtual environment (in Powershell or Git Bash), enter 'deactivate'  
    in cli and press enter.


# DEFINITIONS
[Table of contents](#table-of-contents)
<br/>
    
    argument (in argparse) == value that is passed to a command.
    ex: py super.py buy apple 0.39 -bd today -expd 2023-10-12  
        --> arguments: 0.39 , today , 2023-10-12
    ex: py super.py sell b_11 0.79 -sd tomorrow  
        --> arguments: 0.79 , tomorrow
    
    2 types of arguments: positional arguments and optional  
    arguments, see definitions below. 

    business task = activity that is carried out in Superpy, e.g. buy a product, show 
       an overview of profit in a certain time interval.
       A business task is in pyton argparse technically a subparser. 


    command (in argparse) == specific action that the program can perform.  
    ex: py super.py buy apple 0.39 -bd today -expd 2023-10-12  
        --> command is buy
    ex: py super.py sell b_11 0.79 -sd tomorrow  
        --> command is sell   

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

    optional argument (in argparse) == flag == values that modify the behavior of a program.  
    They are usually preceded by a hyphen (-) or two hyphens (--). Options can be used to  
    enable or disable certain features, set configuration values, or provide additional  
    information to the program.  
    ex: py super.py buy apple 0.39 -bd today -expd 2023-10-12  
        --> optional argument: -bd today , expd 2023-10-12
    ex: py super.py sell b_11 0.79 -sd tomorrow  
        --> arguments: -sd tomorrow

    positional argument (in argparse) == flag == are specified by their position on the  
    command line and do not have any flags. They are required and must be provided in the  
    order in which they are defined in the program.  
    ex: py super.py buy apple 0.39 -bd today -expd 2023-10-12  
        --> positional argument: 0.39 
    ex: py super.py sell b_11 0.79 -sd tomorrow  
        --> positional arguments: 0.79 

    product_range == product_assortment == the amount of different products in a shop .
        e.g. ['apple', 'cabbage', 'beetroot'], or e.g. ['coffee', 'potato', 'orange']
        product_range is an operand in fn product from module itertools.
        So more products in product_range lead to more rows in bought.csv and sold.csv.
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


    sales_volume == (Dutch: afzet) == the quantity of items a business sells during a given period, such as a year or fiscal quarter. 
        It is a measure of the total number of units sold, regardless of the type or category of the product.


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


    turnover time == inventory turnover == the number of days between buying and selling a product  
        ex: sell an apple:
        buy_date    sell_date     turnover_time
        23-09-12     23-09-14         2
        23-09-12     23-09-15         3
        (used in fn create_data_for_csv_files_bought_and_sold() )

# LOCATION OF IMPORTANT DIRECTORIES AND FILES
[goto Table of Contents at start of this markdown file: ](#LOCATION-OF-IMPORTANT-DIRECTORIES-AND-FILES)
<br/>

- bought.csv      :  ...\superpy\date_used_in_superpy\bought.csv
- create_testdata_for_csv_files_bought_and_sold   :  ...\superpy\data_pytest_create_boughtcsv_and_soldcsv_for_pytestcases_here\
                                                   create_testdata_for_csv_files_bought_and_sold
- erd             :  ...\superpy\erd  (entity relationship diagram)
- readme_files    :  ...\superpy\readme_files
- sold.csv        :  ...\superpy\date_used_in_superpy\sold.csv
- super.py        :  ...\superpy\super.py 
- system_date     :  ...\superpy\date_used_in_superpy\system_date.txt
- test_utils      :  ...\superpy\test_utils   (regression testcases, run in pytest)
- utils.py        :  ...\superpy\test_utils   (functions)


# DATA-MODEL
[Table of contents](#table-of-contents)
<br/>

Before moving on, please have a look at the data model. This provides some context to  
better understand the business tasks of Superpy in next chapter Usage.


<img src="../erd/erd_superpy.png" alt="Image Name" width="400" height="600">





# Testing the application in pytest
[Table of contents](#table-of-contents)
<br/>

## 1of2: run regression testcases:

There are 2 options to run the regression testcases in pytest:

Option 1of2: run them all (this is usually what you want):
1. navigate into (...\superpy) or (...\superpy\test_utils)
2. enter following command:
```python
    pytest
```
3. all 27 testcases should pass. If not then investigate the failing testcase(s).
<br/>
<br/>

Option 2of2: run only the testcase(s) that test a specific function:
1. navigate into (...\superpy) or (...\superpy\test_utils)
2. navigate into the folder that contains the testcases of the fn that you want to test.
    - ex: to test fn buy_product, navigate into directory 'fn_buy_product_testcases'.
    - or: 
    - ex: to test fn calculate_profit_in_time_range_between_start_date_and_end_date_inclusive,  
        navigate into directory 'fn_calculate_profit_in_time_range_between_start_date_and_end_date_inclusive'  
    etc.
3. now enter following command:
```python
    pytest
```
4. all testcases of this fn (e.g. fn buy_product) should pass.  
    If not then investigate the failing testcase(s).
<br/>
<br/>

## 2of2: create testdata for additional testcases:
[Table of contents](#table-of-contents)

Creating testdata involves creating testdata for bought.csv and sold.csv.

1. navigate into (...\superpy\data_pytest_create_boughtcsv_and_soldcsv_for_pytestcases_here)
2. run the following script:
```python
    py create_testdata_for_csv_files_bought_and_sold.py
```
3. bought.csv and sold.csv have now been created. You can find them in the same location
    as the script: (...\superpy\data_pytest_create_boughtcsv_and_soldcsv_for_pytestcases_here)

- Inside this script at the beginning of main() in section 'CONFIGURATION', the following variables  
    (actually fn-arguments) can be assigned another value to your liking:
    - product_range
    - delete_every_nth_row_in_soldcsv_so_every_nth_row_in_boughtcsv_can_expire_when_time_travelling
    - shelf_life
    - turnover_time
    - markup
    - lower_boundary_year_of_time_interval_in_which_to_create_random_testdata
    - lower_boundary_month_of_time_interval_in_which_to_create_random_testdata
    - lower_boundary_week_of_time_interval_in_which_to_create_random_testdata
    - upper_boundary_nr_of_months_to_add_to_calculate
    - upper_boundary_nr_of_weeks_to_add_to_calculate
    - upper_boundary_nr_of_days_to_add_to_calculate 

     - Chapter USAGE --> paragraph create_mock_data explains exactly what these variables mean and  
        how they can be used to create testdata.
     - Chapter EXAMPLES shows them "in action".  
        ex: if you create 10 rows in bought.csv (these are automatically copied into 10 rows in sold.csv) and then  
        delete every 2nd row in sold.csv AND THEN time travel to the future, then more products will expire, compared  
        to when you only let every tenth row in sold.csv expire.  
        Setting the shelf_life (e.g. 4 days or 25 days) also make a difference in how many products will expire, or
        or still  be part of the inventory, etc.


<br/>
<br/>



# Trouble shooting
[Table of contents](#table-of-contents)
<br/>

If you encounter a problem, first run the pytest regression testcases.
1. navigate into (...\superpy) or (...\superpy\test_utils)
2. enter following command:
```python
    pytest
```
1. all 23 testcases should pass. If not then investigate the failing testcase(s).


# FAQ
[Table of contents](#table-of-contents)
</br>

1. Can I export data from bought.csv or sold.csv as a pdf?
    - no

2. Do I need a licence to use this application?
    - Unlicence applies to Superpy. Unlicense is a public domain dedication that allows anyone to  
    use your code for any purpose without restriction. 


# Support
[Table of contents](#table-of-contents)
<br/>

For support please send an email to noreply@really.com or call  
0011-2233-4455 during business hours GMT+2. 
