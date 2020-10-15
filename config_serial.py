from netmiko import ConnectHandler
from prettytable import PrettyTable
from getpass import getpass


#Function to send commands to the device
def showCommand(command, delay=False):
    if delay:
        output = net_connect.send_command_timing(command,delay_factor=50)
    else:
        output = net_connect.send_command(command, use_genie=True)
    return output

#Function to create a table with parsing data
def createTable(table_name, field_names=False, add_row=False, add_column=False):
    table_name = PrettyTable()
    if (field_names or add_row):
        table_name.field_names
        table_name.add_row
    elif add_column:
        table_name.add_column
    else:
        table_name = 'no table'

    return table_name


#Function to parsing output from "show clock"
def shClock(show_clock):
    day = show_clock['day']
    month = show_clock['month']
    year = show_clock['year']
    time = show_clock['time']
    output = ("{} - {}/{}/{}".format(time, day, month, year))
    return output


def get_info():
    show_version = showCommand('show version')
    show_clock = showCommand('show clock')
    show_ip_interface_brief = show('show ip interface brief')
    show_interfaces = show('show interfaces')
    show_arp = show("show arp summary")


#Dictionary of device
device = {
        'device_type': 'cisco_xe',
        'ip': '10.10.10.1',
        'username': 'admin',
        'password': getpass(),
        'fast_cli': True
    }


#Trying to connect on device
try:
    net_connect = ConnectHandler(**device)
    net_connect.enable()
    get_info()
except Exception as error:
    print(error)

