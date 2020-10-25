################################################################################################################################
#
# Script for creating, adding rows and printing tables
# In this example, tables will be created according to the features defined previously.
#
# Author: Eduardo Dytz
#
################################################################################################################################

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
    """
    table_name = Table name (str)
    row = Row data (list)
    """
    create_table()

    if table_name == 'version':

        version.add_row(row)


    if table_name == 'interface':

        interface.add_row(row)


    if table_name == 'ospf':

        ospf.add_row(row)


def print_table(tables):

    for table in tables:
        print(globals()[table])