
import mysql.connector 
from mysql.connector import Error

from dbproductmenu import *
from dbcouriers import *
from dborders import *

# CONNECTING TO DATABASE PAPIS_HAIR_PRODUCTS
try:
    connection = mysql.connector.connect(host='localhost',
                                        database='papis_hair_products',
                                        user='root',
                                        password='password')

except Error as e:
    print("Error while connecting to MySQL", e)


def main_menu_opts():
    while True:
        print("----- Welcome to Papi's Deli -----\n")
        print("""
            ---------------------
            Main Menu Options: 
            
            0. Exit app 
            1. Product Menu
            2. Couriers Menu
            3. Orders Menu
            
            ---------------------\n""")
        user_command = input("Enter a number from the menu options: ")
        print(user_command)
        if user_command == "0":
            cursor = connection.cursor()   # opens connection with DB
            cursor.close()   # closes cursor  
            connection.close()   # closes connection with DB completely on exit
            exit()
        elif user_command == "1":
            check_for_db_table()   # connects with product table in DB or creates if doesn't exist
            product_menu()   # takes you to product menu 
        elif user_command == "2":
            check_for_c_db_table()   # connects with courier table in DB or creates if doesn't exist
            couriers_menu()   # takes you to courier menu
        elif user_command == "3":
            check_for_o_db_table()   # connects with orders table in DB or creates if doesn't exist
            check_for_os_db_table()   # # connects with order status table in DB or creates if doesn't exist
            order_menu()   # takes you to orders menu 
        else:
            # if user inputs number other than one of above, it will show this statement instead of crashing
            print("Invalid entry. Try again")   
            
            
main_menu_opts()         