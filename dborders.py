
import mysql.connector 
from mysql.connector import Error
from dbproductmenu import *
from dbcouriers import *


# CONNECTING TO DATABASE PAPIS_HAIR_PRODUCTS
try:
    connection = mysql.connector.connect(host='localhost',
                                        database='papis_hair_products',
                                        user='root',
                                        password='password')

except Error as e:
    print("Error while connecting to MySQL", e)


# *ORDER TABLE*:

# CHECKS FOR ORDERS TABLE, IF IT DOESN'T EXIST, CREATE IT
def check_for_o_db_table():
    try:
        # connecting to cursor and checking if orders exists
        cursor = connection.cursor()
        cursor.execute("SHOW TABLES LIKE 'orders'")
        result = cursor.fetchone()
        
        # if it does, print this statement
        if result:
            print("'orders' table found")
        else:
            # if it doesn't exist, create it
            mySql_Create_Table_Query = """CREATE TABLE orders ( 
                                    Id int(11) NOT NULL AUTO_INCREMENT,
                                    Customer_Name varchar(250) NOT NULL,
                                    Customer_Address varchar(250) NOT NULL,
                                    Customer_Phone varchar(250) NOT NULL,
                                    Courier INT(100) NOT NULL,
                                    Status INT(100) NOT NULL,
                                    Items varchar(250) NOT NULL,
                                    PRIMARY KEY (Id)) """
            cursor.execute(mySql_Create_Table_Query)
            print("Table 'orders' created successfully")
        
        # closing connection to cursor    
        cursor.close()
    
    # print statement if there's an error completing above        
    except Error as e:
        print("Error while creating table", e)


# INSERTS NEW ROW INTO ORDERS TABLE
def insert_order_row():
    try:
        # connecting to cursor
        cursor = connection.cursor()
        
        # asks for user input first for order details line by line
        customer_name = input("Enter customer firstname and surname: ")
        customer_address = input("Enter customer address: ")
        customer_phone = input("Enter cutomer phone number: ")
        display_courier_rows()
        courier = input("Enter courier Id (see options above): ")
        display_order_status_rows()
        status = input("Enter order status Id (see options above): ")
        display_product_rows()
        items = input("Enter order items using product Id (see options above): ")
        
        # instructions to insert above details into new row assigned to variable
        mysql_insert_query = """INSERT INTO orders (Customer_Name, Customer_Address, 
                                Customer_Phone, Courier, Status, Items)
                                VALUES (%s, %s, %s, %s, %s, %s)"""

        # checks if above order name exists already using 'select'                         
        cursor.execute("SELECT * FROM orders WHERE Customer_Name = %s", (customer_name,))
        existing_order = cursor.fetchone()
        
        # if it exists print that message, if not, execute variable above with the inputted values
        if existing_order:
            print(f"Product '{customer_name}' already exists")
        else:
            cursor.execute(mysql_insert_query, (customer_name, customer_address, customer_phone, courier, status, items))
            connection.commit()
            print("Data inserted into 'orders' table successfully")
        
        # close connection to cursor    
        cursor.close()
    
    # print statement if there's an error completing above        
    except mysql.connector.Error as error:
        print("Failed to insert data in MySql: {}".format(error))


# DISPLAY ROWS FROM ORDERS TABLE
def display_order_rows():
    try:
        # connecting to cursor
        cursor = connection.cursor()
        
        # selecting all data from orders then executing variable
        sql_select_query = "SELECT * FROM orders"
        cursor.execute(sql_select_query)
        
        # get all records and print
        records = cursor.fetchall()
        print("Total number of rows in table: ", cursor.rowcount)

        # printing data in correct format
        print("\nListing all order details", "\n")
        for row in records:
            print("Id = ", row[0], )
            print("Full Name = ", row[1])
            print("Address = ", row[2])
            print("Phone Number  = ", row[3])
            print("Courier  = ", row[4]) 
            print("Status = ", row[5])
            print("Items = ", row[6], "\n")
            
        # close connection to cursor
        cursor.close()

    # printing statement if there's an error completing above
    except mysql.connector.Error as e:
        print("Error reading data from MySQL table", e) 


# UPDATE ROWS FROM ORDERS TABLE
def update_order_row():
    try:
        # connecting to cursor
        cursor = connection.cursor()
        
        # after displaying list of all orders below in menu 
        
        # ask for user input of order Id you want to update 
        select_order_update = int(input("Enter order ID of the order details you want to update: "))
        
        # selecting above order Id details then checking if exists     
        cursor.execute("SELECT * FROM orders WHERE Id = %s", (select_order_update,))
        existing_order = cursor.fetchone()
        
        if existing_order:
            # if it's a valid Id, allow for user input for details
            customer_fullname = input("Enter updated customer firstname and surname: ")
            if not customer_fullname.strip():
                customer_fullname = existing_order[1]
            
            customer_address = input("Enter updated customer address: ")
            if not customer_address.strip():
                customer_address = existing_order[2]
            
            customer_phone = input("Enter updated cutomer phone number: ")
            if not customer_phone.strip():
                customer_phone = existing_order[3]                    
            
            display_courier_rows()    
            courier = input("Enter updated courier Id (see above): ")
            if not courier.strip():
                courier = existing_order[4]
            
            display_order_status_rows()
            status = input("Enter updated order status Id (see above): ")
            if not status.strip():
                status = existing_order[5]
            
            display_product_rows()
            items = input("Enter updated order items using product Id (see above): ")
            if not items.strip():
                items = existing_order[6]
            
            # instructions to update details using above input for chosen Id, assigned to variable
            mysql_update_query = """UPDATE  orders 
                                    SET Customer_Name = %s, Customer_Address = %s, 
                                        Customer_Phone = %s, Courier = %s, Status = %s, Items = %s
                                    WHERE Id = %s"""
            
            # executing variable along with all parameters
            cursor.execute(mysql_update_query, (customer_fullname, customer_address, customer_phone, courier, status, items, select_order_update))
            
            connection.commit()
            print("Order details successfully updated") 
            
        # if input of Id isn't within parameters, print this statement    
        else:
            print("Invalid order Id. Try again")
        
        # closing connection to cursor
        cursor.close()
 
    # print statement if there's an error completing above       
    except mysql.connector.Error as error:
        print("Failed to update data in MySql: {}".format(error))


# UPDATE ORDER STATUS ONLY FROM ORDERS TABLE
def update_order_status():
    try:
        # connecting to cursor
        cursor = connection.cursor()
        
        # after displaying list of all orders below in menu 
        
        # ask for user input of order Id you want to update 
        select_order_update = int(input("Enter order ID of the order status you want to update: "))
        
        display_order_status_rows()
        
        # selecting above order Id details then checking if exists     
        cursor.execute("SELECT * FROM orders WHERE Id = %s", (select_order_update,))
        existing_order = cursor.fetchone()
        
        if existing_order:
            
            # instructions to update details using above input for chosen Id, assigned to variable
            new_status = int(input("Enter updated order status Id): "))
            mysql_update_query = """UPDATE  orders 
                                    SET Status = %s
                                    WHERE Id = %s"""
            
            # executing variable along with all parameters
            cursor.execute(mysql_update_query, (new_status, select_order_update))
            
            connection.commit()
            print("Order details successfully updated") 
            
        # if input of Id isn't within parameters, print this statement    
        else:
            print("Invalid order Id. Try again")
        
        # closing connection to cursor
        cursor.close()
 
    # print statement if there's an error completing above       
    except mysql.connector.Error as error:
        print("Failed to update data in MySql: {}".format(error))


# DELETE ORDER ROW
def delete_order_row():
    try: 
        # connecting to cursor
        cursor = connection.cursor()
        
        # after displaying list of all order below in menu
        
        # allowing for user input to select which order Id details you want to delete
        deleted_order = int(input("Enter the order ID of the order you want to delete: "))
        
        # selecting above order Id details then checking if exists      
        cursor.execute(f"SELECT * FROM orders WHERE Id = {deleted_order}")
        existing_order = cursor.fetchone()
        
        # if it does then delete inputted order, otherwise print invalid statement if out of parameters
        if existing_order:
            mysql_delete_query = f"""DELETE FROM orders WHERE Id = {deleted_order}"""
            cursor.execute(mysql_delete_query)
            print("Order successfully deleted")
        else:
            print("Invalid order Id. Try again")        

        # close connection to cursor
        cursor.close()
    
    # print statement if there's an error completing above
    except mysql.connector.Error as error:
        print("Failed to delete data in MySql: {}".format(error))
        
        
# *ORDER STATUS TABLE*:       

# CHECKS FOR ORDER STATUS TABLE, IF IT DOESN'T EXIST, CREATE IT
def check_for_os_db_table():
    try:
        # connecting to cursor and checking if order status exists
        cursor = connection.cursor()
        cursor.execute("SHOW TABLES LIKE 'order_status'")
        result = cursor.fetchone()
        
        # if it does, print this statement
        if result:
            print("'order_status' table found")
        else:
            # if it doesn't exist, create it
            mySql_Create_Table_Query = """CREATE TABLE order_status ( 
                                    Id int(11) NOT NULL AUTO_INCREMENT,
                                    Order_Status varchar(250) NOT NULL,
                                    PRIMARY KEY (Id)) """
            cursor.execute(mySql_Create_Table_Query)
            print("Table 'order_status' created successfully")
        
        # closing connection to cursor    
        cursor.close()
    
    # print statement if there's an error completing above        
    except Error as e:
        print("Error while creating table", e)


# INSERTS NEW ROW INTO ORDER STATUS TABLE
def insert_order_status_row():
    try:
        # connecting to cursor
        cursor = connection.cursor()
        
        # asks for user input first for order status 
        order_status = input("Enter order status: ")
        
        # instructions to insert above details into new row assigned to variable
        mysql_insert_query = """INSERT INTO order_status (Order_Status)
                                VALUE (%s)"""

        # executes inserting new order status in row, auto-incrementing ID
        cursor.execute(mysql_insert_query, (order_status,))
        connection.commit()
        print("Data inserted into 'order status' table successfully")

        # close connection to cursor    
        cursor.close()
    
    # print statement if there's an error completing above        
    except mysql.connector.Error as error:
        print("Failed to insert data in MySql: {}".format(error))


# UPDATE ROW FROM ORDER STATUS TABLE
def update_order_status_row():
    try:
        # connecting to cursor
        cursor = connection.cursor()
        
        # after displaying list of all order status' below in menu 
        
        # ask for user input of order status Id you want to update 
        select_order_status_update = input("Enter order status ID of the order status you want to update: ")
        
        # selecting above order status Id then checking if exists     
        cursor.execute(f"SELECT * FROM order_status WHERE Id = {select_order_status_update}")
        existing_order_status_id = cursor.fetchone()
        if existing_order_status_id:
            # if it's a valid order status Id, allow for user input for new order status
            order_status = input("Enter updated order status: ")
            
            # instructions to update status using above input for chosen Id, assigned to variable
            mysql_update_query = """UPDATE order_status
                                    SET Order_Status = %s
                                    WHERE Id = %s"""
            
            # executing variable along with all parameters
            cursor.execute(mysql_update_query, (order_status, select_order_status_update))
            connection.commit()
            print("Order status successfully updated") 
            
        # if input of Id isn't within parameters, print this statement    
        else:
            print("Invalid order status Id. Try again")
        
        # closing connection to cursor
        cursor.close()
 
    # print statement if there's an error completing above       
    except mysql.connector.Error as error:
        print("Failed to update data in MySql: {}".format(error))


# DISPLAY ROWS FROM ORDER STATUS TABLE
def display_order_status_rows():
    try:
        # connecting to cursor
        cursor = connection.cursor()
        
        # selecting all data from order status then executing variable
        sql_select_query = "SELECT * FROM order_status"
        cursor.execute(sql_select_query)
        
        # get all records and print
        records = cursor.fetchall()
        print("Total number of rows in table: ", cursor.rowcount)

        # printing data in correct format
        print("\nListing all order status options", "\n")
        for row in records:
            print("Id = ", row[0], )
            print("Order Status = ", row[1], "\n")
            
        # close connection to cursor
        cursor.close()

    # printing statement if there's an error completing above
    except mysql.connector.Error as e:
        print("Error reading data from MySQL table", e) 
                
        
# MAIN ORDER MENU CONTROLS
def order_menu():
    while True:
        print("""
            
            *** ORDER MENU ***
            
            0. Return to main menu
            1. Show List of Orders
            2. Add new order
            3. Update/Show order status
            4. Update existing order
            5. Delete order\n""")
        user_input = input("Enter a number from the menu options: ")
        print(user_input)
        if user_input == "0":
            return   # returns you to main menu
        elif user_input == "1":
            display_order_rows()   # displays full list of orders
        elif user_input == "2":
            display_order_rows()   # shows full list first
            insert_order_row()   # then inserts new order row
        elif user_input == "3":
            user_command = input("Enter 1 to update existing status, or 2 to list order status options: ")
            if user_command == "1":
                display_order_rows()   # shows full list first
                update_order_status()   # updates order status only 
            elif user_command == "2":
                display_order_status_rows()   # shows list of order status options
            else:
                print("Invalid entry. Try again")
        elif user_input == "4":    
            display_order_rows()   # shows full list first
            update_order_row()   # then updates existing order
        elif user_input == "5":
            display_order_rows()   # shows full list first
            delete_order_row()   # then deletes existing order
        else:
            ("Invalid entry. Try again")
            
            