from nornir_netmiko import netmiko_send_command
from resource.create_table import make_table


def multitask_nx_os(task):
    
    task.run(
            task=netmiko_send_command,
            name='version',
            command_string="show version", 
            use_genie=True
            )

    task.run(
            task=netmiko_send_command,
            name='interface',
            command_string="show interface", 
            use_genie=True
            )

    task.run(
            task=netmiko_send_command,
            name='ospf',
            command_string="show ip ospf neighbors detail", 
            use_genie=True
            )


def parsing_uptime(clock):

    clock_parse = {}

    for key, value in clock.items():
        if value >= 1:
            clock_parse[key] = value
    clock_parse = str(clock_parse)[1:-1].replace("'", "")

    return clock_parse


def nx_os(nrf):

    output = nrf.run(task=multitask_nx_os)

    for device in output.keys():
        
        hostname = output[device][1].host.name

        show_version_command_output = output[device][1].result['platform']
        operating_system = show_version_command_output['os']
        software_version = show_version_command_output['software']['system_version']
        uptime = parsing_uptime(show_version_command_output['kernel_uptime'])
        image = show_version_command_output['software']['system_image_file']
        device_family = show_version_command_output['hardware']['model']
        config_register = "N/A"
        
        make_table(table_name="version",data=[hostname, operating_system, software_version, uptime, image, device_family, config_register])

        list_interface = output[device][2].result
        
        interface_bypass = ['Loopback0']
        for interface in list_interface:
            interface_data = list_interface[interface]
            if interface not in interface_bypass:

                interface_name = interface

                if 'ipv4' in interface_data:
                    ip_address = [key for key in interface_data['ipv4'].keys()][0]
                else:
                    ip_address = "no ip address"

                line_protocol = interface_data['admin_state']
                oper_status = interface_data['oper_status']
                description = interface_data['description']
                mtu = interface_data['mtu']

                if interface_data['admin_state'] == 'up':
                    port_speed = interface_data['port_speed']
                else:
                    port_speed = "N/A"

                in_octets = interface_data['counters']['rate']['in_rate']
                out_octets = interface_data['counters']['rate']['out_rate']
                
                make_table(table_name="interface",data=[hostname, interface_name, ip_address, line_protocol, oper_status, description, mtu, port_speed, in_octets, out_octets])


        ospf_interfaces = output[device][3].result['vrf']['default']['address_family']['ipv4']['instance']['1']['areas']['0.0.0.0']['interfaces']
        
        for ospf_neighbor in ospf_interfaces.keys():

                router_id = ospf_interfaces[ospf_neighbor]['neighbors']

                for each_neighbor in router_id.keys():
                    neighbor_router_id = router_id[each_neighbor]['neighbor_router_id']
                    address = router_id[each_neighbor]['address']
                    state = router_id[each_neighbor]['state']

                    make_table(table_name="ospf",data=[hostname, ospf_neighbor, neighbor_router_id, address, state])
