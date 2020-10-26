"""
Module to perform tasks and data parsing for the NX-OS platform.
"""

# Importing the "netmiko_send_commad" function
# 
# I am using the "send_command" function of netmiko because it's already well spread and with big documentation. 
# Nornir can also use other connection libraries such as NAPALM, Paramiko and NETCONF.
from nornir_netmiko import netmiko_send_command
from nornir_netmiko import netmiko_send_config

# Importing the function to add rows to the tables.
from utils.get_table import add_row_table

# Importing the functions by jinja2
from jinja2 import Environment, FileSystemLoader
import os, glob


def multitask_nx_os(task,features):
    """Function to perform tasks on devices with NX-OS according to the list of features.

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
                            name='version',                     # Passing the task name, in this case the name of the feature.
                            command_string="show version",      # Passing the command to be executed via CLI.
                            use_genie=True                      # Genieparser is a library to format the output of the command in JSON.
                            )

            # Calling function to extract the data from the task output.
            parsing_nx_os_version(output_version)

        if feature == 'interface':
            output_interface = task.run(
                            task=netmiko_send_command,
                            name='interface',
                            command_string="show ip interface brief", 
                            use_genie=True
                            )
            parsing_nx_os_interface(output_interface)

        if feature == 'ospf':
            output_ospf = task.run(
                            task=netmiko_send_command,
                            name='ospf',
                            command_string="show ip ospf neighbors detail", 
                            use_genie=True
                            )
            parsing_nx_os_ospf(output_ospf)


def parsing_uptime(clock):
    """Function to format clock dictionary

    Args:
        clock (dict): Clock dictionary.

    Returns:
        str: string clock
    """
    clock_parse = {}

    for key, value in clock.items():
        if value >= 1:
            clock_parse[key] = value
    clock_parse = str(clock_parse)[1:-1].replace("'", "")

    return clock_parse


def parsing_nx_os_version(output):
    """Function to extract the data of AggregatedResult from the "show version" command.

    Args:
        output (AggregatedResult): Task output
    """

    # For each device in output task 
    for device in output.keys():

        # Associating the dictionary to a variable for better manipulation of it.
        command_output = output[device][0].result['platform']

        # Associating the variables to each item that we want to be displayed in the table.
        operating_system = command_output['os']
        software_version = command_output['software']['system_version']
        uptime = parsing_uptime(command_output['kernel_uptime'])
        image = command_output['software']['system_image_file']
        device_family = command_output['hardware']['model']
        reason = command_output['reason']
        
        # Calling the function to add the items to the table columns.
        add_row_table(table_name="version",row=[device, operating_system, software_version, uptime, image, device_family, reason])


def parsing_nx_os_interface(output):
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
        interface_bypass = ['loopback0','mgmt0','Vlan1']

        # For each interface in the interface list
        for interface in list_interface:
            
            # for each interface that is not on the interface_bypass
            if interface not in interface_bypass:

                # Checking if the interface is a vlan
                if 'Vlan' in interface:

                    # Associating the vlan number
                    vlan_number = interface.split('Vlan')[1]

                    # For vlan interfaces, the dictionary is different from non vlan interfaces. 
                    # Due to this, we need to collect the vlan number to use as key.
                    # Associating the variables to each item that we want to be displayed in the table.
                    ip_address = list_interface[interface]['vlan_id'][vlan_number]['ip_address']
                    interface_status = list_interface[interface]['vlan_id'][vlan_number]['interface_status']

                # If not vlan
                else:
                    # Associating the variables to each item that we want to be displayed in the table.
                    ip_address = list_interface[interface]['ip_address']
                    interface_status = list_interface[interface]['interface_status']

                # Associating the variables to each item that we want to be displayed in the table.
                line_protocol = interface_status.split('/')[0].split('-')[1]
                oper_status = interface_status.split('/')[1].split('-')[1]

                # Calling the function to add the items to the table columns.
                add_row_table(table_name="interface",row=[device, interface, ip_address, line_protocol, oper_status])


def parsing_nx_os_ospf(output):
    """Function to extract the data of AggregatedResult from the "show ip ospf neighbors detail" command.

    Args:
        output (AggregatedResult): Task output
    """

    # For each device in output task 
    for device in output.keys():

        # Associating the dictionary to a variable for better manipulation of it.
        ospf_interfaces = output[device][0].result['vrf']['default']['address_family']['ipv4']['instance']['1']['areas']['0.0.0.0']['interfaces']

        # For each neighbor OSPF
        for ospf_neighbor in ospf_interfaces.keys():

            # Associating router id
            router_id = ospf_interfaces[ospf_neighbor]['neighbors']

            # For each neighbor OSPF in router_id
            for each_neighbor in router_id.keys():

                # Associating the variables to each item that we want to be displayed in the table.
                neighbor_router_id = router_id[each_neighbor]['neighbor_router_id']
                address = router_id[each_neighbor]['address']
                state = router_id[each_neighbor]['state']

                # Calling the function to add the items to the table columns.
                add_row_table(table_name="ospf",row=[device, ospf_neighbor, neighbor_router_id, address, state])


def generate_nxos_config_file(vlans):
    """Function to generate the configuration files for each device.

    Args:
        vlans (list): List with vlan dict
    """

    # If there are configuration files in the folder, they will be deleted.
    config_files = glob.glob("templates/*.ios")
    for config_file in config_files:
        os.remove(config_file)

    file_loader = FileSystemLoader('templates')
    env = Environment(loader=file_loader)
    template = env.get_template('vlan_nxos.j2')
    for host in vlans:

        device = host['device']
        vlan_id = host['vlan_id']
        description = host['description']
        ip = host['ip']
        mask = host['mask']
        hsrp = host['hsrp']

        output_config = template.render(
            vlan_id=vlan_id,
            description=description,
            ip=ip,
            mask=mask,
            hsrp=hsrp
        )

        file = open("templates/{}.ios".format(device),"w")
        file.write(str(output_config))
        file.close()


def multitask_config(task):

    task.run(
        task=netmiko_send_config,
        config_file="templates/{}.ios".format(task.host.name)
    )