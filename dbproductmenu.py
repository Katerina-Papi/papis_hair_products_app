import mysql.connector 
from mysql.connector import Error


# CONNECTING TO DATABASE PAPIS_HAIR_PRODUCTS
try:
    connection = mysql.connector.connect(host='localhost',
                                        database='papis_hair_products',
                                        user='root',
                                        password='password')

except Error as e:
    print("Error while connecting to MySQL", e)
    

# CHECK IF THE PRODUCTS TABLE EXISTS SO IT DOESN'T TRY TO DUPLICATE
def check_for_db_table():
    try:
        cursor = connection.cursor()
        cursor.execute("SHOW TABLES LIKE 'products'")
        result = cursor.fetchone()
        if result:
            print("'products' table found")
        else:
            # if it doesn't exist, create it
            mySql_Create_Table_Query = """CREATE TABLE products ( 
                                    Id int(11) NOT NULL AUTO_INCREMENT,
                                    Product_Name varchar(250) NOT NULL,
                                    Product_Price float NOT NULL,
                                    Purchase_Date Date NOT NULL,
                                    PRIMARY KEY (Id)) """
            cursor.execute(mySql_Create_Table_Query)
            print("Table 'products' created successfully")
            
        cursor.close()
            
    except Error as e:
        print("Error while creating table", e)
        
# INSERT NEW PRODUCT ROW
def insert_product_row():
    try:
        cursor = connection.cursor()
        # asks for user input first for product details line by line
        product_name = input("Enter product name: ")
        product_price = float(input("Enter product price: "))
        purchase_date = input("Enter purchase date (YYYY-MM-DD): ")
        
        # instructions to insert above details into new row assigned to variable
        mysql_insert_query = """INSERT INTO products (Product_Name, Product_Price, Purchase_Date)
                                VALUES (%s, %s, %s)"""

        # checks if above product name exists already using 'select'                         
        cursor.execute("SELECT * FROM products WHERE Product_Name = %s", (product_name,))
        existing_product = cursor.fetchone()
        # if it exists print that message, if not, execute variable above with the inputted values
        if existing_product:
            print(f"Product '{product_name}' already exists")
        else:
            cursor.execute(mysql_insert_query, (product_name, product_price, purchase_date))
            connection.commit()
            print("Data inserted into 'products' table successfully")
            
        cursor.close()
            
    except mysql.connector.Error as error:
        print("Failed to insert data in MySql: {}".format(error))
        
                       
# DISPLAY ROWS FROM PRODUCT TABLE
def display_product_rows():
    try:
        # connecting to cursor
        cursor = connection.cursor()
        
        # selecting all data from products then executing variable 
        sql_select_query = "SELECT * FROM products"
        cursor.execute(sql_select_query)
        
        # get all records and print
        records = cursor.fetchall()
        print("Total number of rows in table: ", cursor.rowcount)

        # printing data in correct format
        print("\nListing all product details", "\n")
        for row in records:
            print("Id = ", row[0], )
            print("Name = ", row[1])
            print("Price  = ", row[2])
            print("Purchase date  = ", row[3], "\n") 
        
        # closing cursor to prepare for next funtion    
        cursor.close()

    # print statement if there's an error completing above
    except mysql.connector.Error as e:
        print("Error reading data from MySQL table", e)
    

# UPDATE ROWS FROM PRODUCT TABLE
def update_product_row():
    try:
        cursor = connection.cursor()
        # after displaying list of all products below in menu 
        
        # ask for user input of product id you want to update 
        select_product_update = input("Enter product ID of the product details you want to update: ")
        
        # selecting above product Id details then checking if exists     
        cursor.execute("SELECT * FROM products WHERE Id = %s", (select_product_update,))
        existing_product = cursor.fetchone()
        if existing_product:
            
            # if it's a valid product Id, allow for user input for product details
            product_name = input("Enter updated product name (press Enter to skip): ")
            if not product_name.strip():  # Check if input is empty
                product_name = existing_product[1]   # if empty keep existing product, name takes position 1 of list
            
            product_price_input = input("Enter updated product price (press Enter to skip): ")
            if product_price_input.strip(): 
                  product_price = float(product_price_input)   # converts input into float
            else:  
                product_price = existing_product[2]
                
            purchase_date = input("Enter updated purchase date (YYYY-MM-DD) (press Enter to skip): ")
            if not purchase_date.strip():  # Check if input is empty
                purchase_date = existing_product[3]
            
            # instructions to update details using above input for chosen Id, assigned to variable
            mysql_update_query = """UPDATE  products 
                                    SET Product_Name = %s, Product_Price = %s, Purchase_Date = %s
                                    WHERE Id = %s"""

            # executing variable along with all 4 parameters: name, price, date & Id
            cursor.execute(mysql_update_query, (product_name, product_price, purchase_date, select_product_update))
            connection.commit()
            print("Product details successfully updated") 
            
        # if input of Id isn't within parameters, print this statement    
        else:
            print("Invalid product Id. Try again")
        
        cursor.close()
            
    except mysql.connector.Error as error:
        print("Failed to update data in MySql: {}".format(error)) 


# DELETE PRODUCT ROW
def delete_product_row():
    try: 
        # connecting to cursor
        cursor = connection.cursor()
        
        # after displaying list of all products below in menu
        
        # allowing for user input to select which product Id details you want to delete
        deleted_product = int(input("Enter the product ID of the product you want to delete: "))
        
        # selecting above product Id details then checking if exists      
        cursor.execute(f"SELECT * FROM products WHERE Id = {deleted_product}")
        existing_product = cursor.fetchone()
        
        # if it does then delete inputted product, otherwise print invalid statement if out of parameters
        if existing_product:
            mysql_delete_query = f"""DELETE FROM products WHERE Id = {deleted_product}""" 
            cursor.execute(mysql_delete_query)
            print("Product successfully deleted")
        else:
            print("Invalid product Id. Try again")        

        # close connection to cursor
        cursor.close()
    
    # print statement if there's an error completing above
    except mysql.connector.Error as error:
        print("Failed to delete data in MySql: {}".format(error))
        

# MAIN PRODUCT MENU FUNCTION
def product_menu(): 
    while True: 
        print(""" \n
        *** PRODUCT MENU ***
         
        0. Return to main menu
        1. Show products list
        2. Create new product
        3. Update exisiting product
        4. Delete product\n""")  
        user_input = input("Please select number from the product menu: ")     
        if user_input == "0":
            return   # Returns you to the main menu   
        elif user_input == "1":     # Shows list
            display_product_rows()
        elif user_input == "2":     # Adds a new product row
            insert_product_row()
        elif user_input == "3":     
            display_product_rows()  # Views the full list first
            update_product_row()    # Updates existing product row
        elif user_input == "4":     
            display_product_rows()  # Views the full list first
            delete_product_row()    # Deletes existing product row
        else:
            print("Invalid entry. Try again")
