"""
Module for creating, adding rows and printing tables
In this example, tables will be created according to the features defined previously.

Author: Eduardo Dytz
"""

# Importing the PrettyTable function from the prettytable library
from prettytable import PrettyTable


# Function to create the table the first time the script is invoked. 
def create_table():

    # Defining that the variables with the tables will be global variables.
    global version,interface,ospf

    # Verifying that the variable of the table already exists in the global scope. 
    # If it does not exist, then it is created and also inserted the header.
    if 'version' not in globals():
        version = PrettyTable()
        version.field_names = ["Device","OS","Version","Uptime","Image","Device Family","Last Reason"]

    if 'interface' not in globals():
        interface = PrettyTable()
        interface.field_names = ["Device", "Interface", "IP", "Protocol", "Status"]

    if 'ospf' not in globals():
        ospf = PrettyTable()
        ospf.field_names = ["Device","OSPF Interface","Neighbor Router ID","Address","State"]


# Function to add row by row to the table
def add_row_table(table_name, row):
    """Function to add rows to the tables.

    Args:
        table_name (str): Table name
        row (list): list with data for each column
    """

    # Calling the function that manages the creation of the tables.
    create_table()

    # Based on the table name, the data will be added
    if table_name == 'version':

        # Adding a row according to the data of the variable "row".
        version.add_row(row)


    if table_name == 'interface':

        interface.add_row(row)


    if table_name == 'ospf':

        ospf.add_row(row)


def print_table(tables):
    """Function to print the list(s)

    Args:
        tables (list): Table(s) name
    """

    # For each table in the list of tables, print the table.
    for table in tables:
        print(globals()[table])