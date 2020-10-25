from nornir_netmiko import netmiko_send_command
from resource.get_table import add_row_table


def multitask_nx_os(task,features):
    
    for feature in features:

        if feature == 'version':
            output_version = task.run(
                            task=netmiko_send_command,
                            name='version',
                            command_string="show version", 
                            use_genie=True
                            )
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

    clock_parse = {}

    for key, value in clock.items():
        if value >= 1:
            clock_parse[key] = value
    clock_parse = str(clock_parse)[1:-1].replace("'", "")

    return clock_parse


def parsing_nx_os_version(output):

    for device in output.keys():

        show_version_command_output = output[device][0].result['platform']
        operating_system = show_version_command_output['os']
        software_version = show_version_command_output['software']['system_version']
        uptime = parsing_uptime(show_version_command_output['kernel_uptime'])
        image = show_version_command_output['software']['system_image_file']
        device_family = show_version_command_output['hardware']['model']
        reason = show_version_command_output['reason']
        
        add_row_table(table_name="version",row=[device, operating_system, software_version, uptime, image, device_family, reason])


def parsing_nx_os_interface(output):

    for device in output.keys():

        list_interface = output[device][0].result['interface']

        interface_bypass = ['loopback0','mgmt0','Vlan1']

        for interface in list_interface:
            
            if interface not in interface_bypass:
                if 'Vlan' in interface:
                    vlan_number = interface.split('Vlan')[1]
                    ip_address = list_interface[interface]['vlan_id'][vlan_number]['ip_address']
                    interface_status = list_interface[interface]['vlan_id'][vlan_number]['interface_status']

                else:
                    ip_address = list_interface[interface]['ip_address']
                    interface_status = list_interface[interface]['interface_status']

                line_protocol = interface_status.split('/')[0].split('-')[1]
                oper_status = interface_status.split('/')[1].split('-')[1]

                add_row_table(table_name="interface",row=[device, interface, ip_address, line_protocol, oper_status])


def parsing_nx_os_ospf(output):

    for device in output.keys():
    
        ospf_interfaces = output[device][0].result['vrf']['default']['address_family']['ipv4']['instance']['1']['areas']['0.0.0.0']['interfaces']
            
        for ospf_neighbor in ospf_interfaces.keys():

            router_id = ospf_interfaces[ospf_neighbor]['neighbors']

            for each_neighbor in router_id.keys():
                neighbor_router_id = router_id[each_neighbor]['neighbor_router_id']
                address = router_id[each_neighbor]['address']
                state = router_id[each_neighbor]['state']

                add_row_table(table_name="ospf",row=[device, ospf_neighbor, neighbor_router_id, address, state])