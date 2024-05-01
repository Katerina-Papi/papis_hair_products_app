
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


# CHECKS FOR COURIERS TABLE, IF IT DOESN'T EXIST, CREATE IT
def check_for_c_db_table():
    try:
        # connecting to cursor and checking if couriers exists
        cursor = connection.cursor()
        cursor.execute("SHOW TABLES LIKE 'couriers'")
        result = cursor.fetchone()
        
        # if it does, print this statement
        if result:
            print("'couriers' table found")
        else:
            # if it doesn't exist, create it
            mySql_Create_Table_Query = """CREATE TABLE couriers ( 
                                    Id int(11) NOT NULL AUTO_INCREMENT,
                                    Courier_Fullname varchar(250) NOT NULL,
                                    Courier_Number varchar(20),
                                    Hire_Date Date NOT NULL,
                                    PRIMARY KEY (Id)) """
            cursor.execute(mySql_Create_Table_Query)
            print("Table 'couriers' created successfully")
        
        # closing connection to cursor    
        cursor.close()
    
    # print statement if there's an error completing above        
    except Error as e:
        print("Error while creating table", e)


# INSERTS NEW ROW INTO COURIER TABLE
def insert_courier_row():
    try:
        # connecting to cursor
        cursor = connection.cursor()
        
        # asks for user input first for courier details line by line
        courier_fullname = input("Enter courier firstname and surname: ")
        courier_number = input("Enter courier phone number: ")
        hire_date = input("Enter hire date (YYYY-MM-DD): ")
        
        # instructions to insert above details into new row assigned to variable
        mysql_insert_query = """INSERT INTO couriers (Courier_Fullname, Courier_Number, Hire_Date)
                                VALUES (%s, %s, %s)"""

        # checks if above courier full name exists already using 'select'                         
        cursor.execute("SELECT * FROM couriers WHERE Courier_Fullname = %s", (courier_fullname,))
        existing_product = cursor.fetchone()
        
        # if it exists print that message, if not, execute variable above with the inputted values
        if existing_product:
            print(f"Product '{courier_fullname}' already exists")
        else:
            cursor.execute(mysql_insert_query, (courier_fullname, courier_number, hire_date))
            connection.commit()
            print("Data inserted into 'couriers' table successfully")
        
        # close connection to cursor    
        cursor.close()
    
    # print statement if there's an error completing above        
    except mysql.connector.Error as error:
        print("Failed to insert data in MySql: {}".format(error))


# DISPLAY ROWS FROM COURIERS TABLE
def display_courier_rows():
    try:
        # connecting to cursor
        cursor = connection.cursor()
        
        # selecting all data from couriers then executing variable
        sql_select_query = "SELECT * FROM couriers"
        cursor.execute(sql_select_query)
        
        # get all records and print
        records = cursor.fetchall()
        print("Total number of rows in table: ", cursor.rowcount)

        # printing data in correct format
        print("\nListing all courier details", "\n")
        for row in records:
            print("Id = ", row[0], )
            print("Full Name = ", row[1])
            print("Phone Number  = ", row[2])
            print("Hire date  = ", row[3], "\n") 
            
        # close connection to cursor
        cursor.close()

    # printing statement if there's an error completing above
    except mysql.connector.Error as e:
        print("Error reading data from MySQL table", e) 


# UPDATE ROWS FROM COURIERS TABLE
def update_courier_row():
    try:
        # connecting to cursor
        cursor = connection.cursor()
        
        # after displaying list of all couriers below in menu 
        
        # ask for user input of courier Id you want to update 
        select_courier_update = input("Enter courier ID of the courier details you want to update: ")
        
        # selecting above courier Id details then checking if exists     
        cursor.execute("SELECT * FROM couriers WHERE Id = %s", (select_courier_update,))
        existing_courier = cursor.fetchone()
        if existing_courier:
            # if it's a valid courier Id, allow for user input for courier details
            courier_fullname = input("Enter updated courier name: ")
            if not courier_fullname.strip():
                courier_fullname = existing_courier[1]
                
            courier_number = input("Enter updated courier phone number: ")
            if not courier_number.strip():
                courier_number = existing_courier[2]
                
            hire_date = input("Enter updated hire date (YYYY-MM-DD): ")
            if not hire_date.strip():
                hire_date = existing_courier[3]
            
            # instructions to update details using above input for chosen Id, assigned to variable
            mysql_update_query = """UPDATE  couriers 
                                    SET Courier_Fullname = %s, Courier_Number = %s, Hire_Date = %s
                                    WHERE Id = %s"""

            # executing variable along with all parameters
            cursor.execute(mysql_update_query, (courier_fullname, courier_number, hire_date, select_courier_update))
            connection.commit()
            print("Courier details successfully updated") 
            
        # if input of Id isn't within parameters, print this statement    
        else:
            print("Invalid order Id. Try again")
        
        # closing connection to cursor
        cursor.close()
 
    # print statement if there's an error completing above       
    except mysql.connector.Error as error:
        print("Failed to update data in MySql: {}".format(error))


# DELETE COURIER ROW
def delete_courier_row():
    try: 
        # connecting to cursor
        cursor = connection.cursor()
        
        # after displaying list of all couriers below in menu
        
        # allowing for user input to select which courier Id details you want to delete
        deleted_courier = int(input("Enter the courier ID of the courier you want to delete: "))
        
        # selecting above courier Id details then checking if exists      
        cursor.execute(f"SELECT * FROM couriers WHERE Id = {deleted_courier}")
        existing_courier = cursor.fetchone()
        
        # if it does then delete inputted courier, otherwise print invalid statement if out of parameters
        if existing_courier:
            mysql_delete_query = f"""DELETE FROM couriers WHERE Id = {deleted_courier}"""
            cursor.execute(mysql_delete_query)
            print("Courier successfully deleted")
        else:
            print("Invalid courier Id. Try again")        

        # close connection to cursor
        cursor.close()
    
    # print statement if there's an error completing above
    except mysql.connector.Error as error:
        print("Failed to delete data in MySql: {}".format(error))
        

# MAIN COURIERS MENU CONTROLS
def couriers_menu():
    while True:
        print("""
            *** COURIERS ***
            
            0. Return to main menu
            1. Show list of couriers
            2. Add new courier
            3. Update existing courier
            4. Delete courier
            \n""")
        user_input = input("Enter a number from couriers menu: ")
        if user_input == "0":
            return   # returns you to the main menu
        elif user_input == "1":
            display_courier_rows()   # shows full list of couriers
        elif user_input == "2":
            display_courier_rows()   # shows full list first
            insert_courier_row()   # then inserts new courier row
        elif user_input == "3":
            display_courier_rows() # shows full list first
            update_courier_row() # then updates existing courier row
        elif user_input == "4":
            display_courier_rows()   # shows full list first
            delete_courier_row()   # then deletes courier
        else:
            print("Invalid entry. Try again")
