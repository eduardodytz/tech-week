from nornir_netmiko import netmiko_send_command
from resource.get_table import add_row_table


def multitask_ios_xe(task,features):
    """[summary]

    Args:
        task (Nornir): [description]
        features (list): [description]
    """
    for feature in features:

        if feature == 'version':
            output_version = task.run(
                            task=netmiko_send_command,
                            name=feature,
                            command_string="show version", 
                            use_genie=True
                            )
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

    for device in output.keys():

        show_version_command_output = output[device][0].result['version']

        operating_system = show_version_command_output['os']
        software_version = show_version_command_output['version']
        uptime = show_version_command_output['uptime']
        image = show_version_command_output['image_id']
        device_family = show_version_command_output['rtr_type']
        reason = show_version_command_output['last_reload_reason']
        
        add_row_table(table_name="version",row=[device, operating_system, software_version, uptime, image, device_family, reason])



def parsing_ios_xe_interface(output):

    for device in output.keys():

        list_interface = output[device][0].result['interface']

        interface_bypass = ['Loopback0']

        for interface in list_interface:
            interface_data = list_interface[interface]
            if interface not in interface_bypass:

                ip_address = interface_data['ip_address']
                line_protocol = interface_data['protocol']
                oper_status = interface_data['status']

                add_row_table(table_name="interface",row=[device, interface, ip_address, line_protocol, oper_status])


def parsing_ios_xe_ospf(output):

    for device in output.keys():

        ospf_interfaces = output[device][0].result['interfaces']

        for ospf_neighbor in ospf_interfaces.keys():

            router_id = ospf_interfaces[ospf_neighbor]['neighbors']

            for each_neighbor in router_id.keys():
                neighbor_router_id = each_neighbor
                address = router_id[each_neighbor]['address']
                state = router_id[each_neighbor]['state']
                
                add_row_table(table_name="ospf",row=[device, ospf_neighbor, neighbor_router_id, address, state])