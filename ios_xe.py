from nornir_netmiko import netmiko_send_command
from create_table import make_table

def multitask_ios_xe(task):
    
    task.run(
            task=netmiko_send_command,
            name='version',
            command_string="show version", 
            use_genie=True
            )

    task.run(
            task=netmiko_send_command,
            name='interface',
            command_string="show interfaces", 
            use_genie=True
            )

    task.run(
            task=netmiko_send_command,
            name='ospf',
            command_string="show ip ospf neighbor", 
            use_genie=True
            )


def ios_xe(nrf):

    output = nrf.run(task=multitask_ios_xe)

    for device in output.keys():
        
        hostname = output[device][1].host.name

        show_version_command_output = output[device][1].result['version']

        operating_system = show_version_command_output['os']                          ##
        software_version = show_version_command_output['version']                     ## Set 
        uptime = show_version_command_output['uptime']                                ##          
        image = show_version_command_output['image_id']                               ##           
        device_family = show_version_command_output['rtr_type']                       ##                   
        config_register = show_version_command_output['curr_config_register']         ##            
        
        make_table(table_name="version",data=[hostname, operating_system, software_version, uptime, image, device_family, config_register])

        list_interface = output[device][2].result
        
        interface_bypass = ['Loopback0']
        for interface in list_interface:
            interface_data = list_interface[interface]
            if interface not in interface_bypass:

                interface_name = interface
                ip_address = [key for key in interface_data['ipv4'].keys()][0]
                line_protocol = interface_data['line_protocol']
                oper_status = interface_data['oper_status']
                description = interface_data['description']
                mtu = interface_data['mtu']
                port_speed = interface_data['port_speed']
                in_octets = interface_data['counters']['in_octets']
                out_octets = interface_data['counters']['out_octets']
                
                make_table(table_name="interface",data=[hostname, interface_name, ip_address, line_protocol, oper_status, description, mtu, port_speed, in_octets, out_octets])


        ospf_interfaces = output[device][3].result['interfaces']
        for ospf_neighbor in ospf_interfaces.keys():

                router_id = ospf_interfaces[ospf_neighbor]['neighbors']

                for each_neighbor in router_id.keys():
                    neighbor_router_id = each_neighbor
                    address = router_id[each_neighbor]['address']
                    state = router_id[each_neighbor]['state']
                    
                    make_table(table_name="ospf",data=[hostname, ospf_neighbor, neighbor_router_id, address, state])
