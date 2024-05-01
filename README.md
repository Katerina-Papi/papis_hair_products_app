# Papis Hair Products App 


My menu is a command line application, aimed at restaurant staff that allows users to navigate through a menu, and as per the client's requirements, perform various tasks to help in the running of the restaurant such as managing delivery orders, couriers and inventory. In doing so, this enables the restaurant to handle higher volumes of orders efficiently, ultimately leading to increased turnover and profitability. 


# Features

Main Menu: Once the application has been launched, users are presented with a main menu that provides options to access sub-menus containing different features.

Product Menu: Users can view inventory, create new products, and update & delete existing products. Within the database menu, each product also includes details of an Id number, price, and purchase date.

Order Menu: Within the order menu, users can view a list of their current orders. Each order contains an order number, customer name, customer address, customer phone number, courier, order status & items. In this menu you can also add an order, update an order status alone (preparing, out for delivery, delivered or cancelled), or the whole order, and delete an order if necessary. When the user adds an order, they will be asked to use the appropriate IDs to refer to the order status, courier, and items. These Ids can be viewed in the list or products, couriers, and orders.

Option 3 in this menu will present the user with the option to either, 1- update an existing order status only (this will connect you with the orders table in the database and single out the status in the order to update), or 2- show the list of status' (this will connect with the order status table. I haven't allowed for updating or inserting into this table as there shouldn't be a need). 


Courier Menu: Once opening the courier menu, users will be able to view a list of couriers, along with their phone number, and the date they were hired, as well as add a new courier, update existing courier details, and delete an existing courier.  


# Navigation

Users can navigate through the menu using numbers for ease of use, time constraints and to minimise chance of errors such as spelling mistakes. 
The number options are presented to the user throughout each stage of the menu for a clear and concise application.     


# Technicals

Data Persistance: I have created 2 menus, one connects to csv files, and the other to a database in order to save any changes the user makes, and manage the data more efficiently.

Dependencies: I have chosen to separate each menu into their own file, and imported these into my main entry page in order to run the whole app from one file. This was my personal preference in terms of readability. 

Troubleshooting: Throughout the application, I have allowed for inevitable human error, such as inputting a number that isn't within reach of the programme, an error message will show as opposed to crashing.


You will find this project uploaded to github, along with different versions showing updates made along the way. 


# Project Reflections

Throughout the process of building this application, I maintained a 'problems' text file in order to track any problems I faced along the way, along with their solutions and date the problem was encountered. 

In order to meet the client's requirements, I made sure to firstly carefully review the pseudocode to understand what functions and features were needed. I then planned the menu layout and connections within them, through a mixture of pen to paper planning, and creating extra files on vscode to experiment and note take. I then went on to build a block of code at a time, making sure to test its functionailty every step of the way, ensuring the client's requirements were met. 

If I had more time I would have liked to implement unit testing into my app. Ideally I would've started with some tests before writing the code. I'd also want to implement a method to recognise and print an error statement, if the user has inputted a number that isn't in the list of IDs shown. 

Overall, I enjoyed implementing 'imports' and functions into my app, as I feel like it helps with readability and feel as though I found my personal style of programming. I also learnt lots about these aspects whilst intially trying to implement these, since I had a lot of errors at the start. And of course I mostly enjoyed seeing everything work together without any crashes!