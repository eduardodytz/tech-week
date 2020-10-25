"""
Module to perform tasks and data parsing for the IOS-XE platform.

Author: Eduardo Dytz
"""

# Importing the "netmiko_send_commad" function
# 
# I am using the "send_command" function of netmiko because it's already well spread and with big documentation. 
# Nornir can also use other connection libraries such as NAPALM, Paramiko and NETCONF.
from nornir_netmiko import netmiko_send_command

# Importing the function to add rows to the tables.
from utils.get_table import add_row_table


def multitask_ios_xe(task,features):
    """Function to perform tasks on devices with IOS-XE according to the list of features.

    Args:
        task (Nornir): Nornir task
        features (list): List of features
    """

    # For each feature in the feature list.
    for feature in features:

        # According to the character name, set the variable the task output.
        if feature == 'version':
            output_version = task.run(
                            task=netmiko_send_command,          # Defining the function that the task will execute, in this case "netmiko_send_command".
                            name=feature,                       # Passing the task name, in this case the name of the feature.
                            command_string="show version",      # Passing the command to be executed via CLI.
                            use_genie=True                      # Genieparser is a library to format the output of the command in JSON.
                            )
            
            # Calling function to extract the data from the task output.
            parsing_ios_xe_version(output_version)

        if feature == 'interface':
            output_interface = task.run(
                            task=netmiko_send_command,
                            name=feature,
                            command_string="show ip interface brief", 
                            use_genie=True
                            )
            parsing_ios_xe_interface(output_interface)

        if feature == 'ospf':
            output_ospf = task.run(
                            task=netmiko_send_command,
                            name=feature,
                            command_string="show ip ospf neighbor", 
                            use_genie=True
                            )
            parsing_ios_xe_ospf(output_ospf)


def parsing_ios_xe_version(output):
    """Function to extract the data of AggregatedResult from the "show version" command.

    Args:
        output (AggregatedResult): Task output
    """

    # For each device in output task 
    for device in output.keys():

        # Associating the dictionary to a variable for better manipulation of it.
        command_output = output[device][0].result['version']

        # Associating the variables to each item that we want to be displayed in the table.
        operating_system = command_output['os']
        software_version = command_output['version']
        uptime = command_output['uptime']
        image = command_output['image_id']
        device_family = command_output['rtr_type']
        reason = command_output['last_reload_reason']
        
        # Calling the function to add the items to the table columns.
        add_row_table(table_name="version",row=[device, operating_system, software_version, uptime, image, device_family, reason])


def parsing_ios_xe_interface(output):
    """Function to extract the data of AggregatedResult from the "show ip interface brief" command.

    Args:
        output (AggregatedResult): Task output
    """

    # For each device in output task 
    for device in output.keys():

        # Associating the dictionary to a variable for better manipulation of it.
        list_interface = output[device][0].result['interface']

        # If you do not want to include any interface in the table, 
        # it's in this variable that we insert them. 
        # It's format must be list.
        interface_bypass = ['Loopback0']

        # For each interface in the interface list
        for interface in list_interface:

            # for each interface that is not on the interface_bypass
            if interface not in interface_bypass:

                # Associating the variables to each item that we want to be displayed in the table.
                ip_address = list_interface[interface]['ip_address']
                line_protocol = list_interface[interface]['protocol']
                oper_status = list_interface[interface]['status']

                # Calling the function to add the items to the table columns.
                add_row_table(table_name="interface",row=[device, interface, ip_address, line_protocol, oper_status])


def parsing_ios_xe_ospf(output):
    """Function to extract the data of AggregatedResult from the "show ip ospf neighbor" command.

    Args:
        output (AggregatedResult): Task output
    """

    # For each device in output task 
    for device in output.keys():

        # Associating the dictionary to a variable for better manipulation of it.
        ospf_interfaces = output[device][0].result['interfaces']

        # For each neighbor OSPF
        for ospf_neighbor in ospf_interfaces.keys():

            # Associating router id
            router_id = ospf_interfaces[ospf_neighbor]['neighbors']

            # For each neighbor OSPF in router_id
            for each_neighbor in router_id.keys():

                # Associating the variables to each item that we want to be displayed in the table.
                neighbor_router_id = each_neighbor
                address = router_id[each_neighbor]['address']
                state = router_id[each_neighbor]['state']

                # Calling the function to add the items to the table columns.
                add_row_table(table_name="ospf",row=[device, ospf_neighbor, neighbor_router_id, address, state])