from nornir import InitNornir
from nornir.core.filter import F
from nornir_utils.plugins.functions import print_result
from nornir_netmiko import netmiko_send_command
from prettytable import PrettyTable

nr = InitNornir(config_file="config.yaml")

nrf = nr.filter(F(role="core"))


def multitask_ios_xr(task):
    
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
            name='arp',
            command_string="show arp detail", 
            use_genie=True
            )

    task.run(
            task=netmiko_send_command,
            name='ospf',
            command_string="show ospf vrf all-inclusive neighbor detail", 
            use_genie=True
            )

# if 'ospf' in feature:
#             if 'nxos' in nrf.inventory.hosts[device].platform:
#                 ospf_command = "show ip ospf neighbors detail"
#             elif 'xr' in nrf.inventory.hosts[device].platform:
#                 ospf_command = "show ospf vrf all-inclusive neighbor detail"
#             elif 'xe' in nrf.inventory.hosts[device].platform:
#                 ospf_command = "show ip ospf neighbor"

output = nrf.run(
            task=multitask_ios_xr,
            )




def ios_xr(output):
    
    version_table = PrettyTable()
    version_table.field_names = ["Hostname","OS","Version","Uptime","Image","Device Family","Config Register"]

    interface_table = PrettyTable()
    interface_table.field_names = ["Hostname","Interface","IP","Protocol","Status","Description","MTU","Port Speed","Last Flapped", "Input","Output","ARP"]

    ospf_table = PrettyTable()
    ospf_table.field_names = ["Hostname","OSPF Interface","Neighbor Router ID","Address","State","bdr_ip_addr","Neighbor Uptime"]

    for device in output.keys():
        
        hostname = output[device][1].host.name

        show_version_command_output = output[device][1].result
        
        operating_system = show_version_command_output['operating_system']
        software_version = show_version_command_output['software_version']
        uptime = show_version_command_output['uptime']
        image = show_version_command_output['image']
        device_family = show_version_command_output['device_family']
        config_register = show_version_command_output['config_register']

        version_table.add_row([hostname, operating_system, software_version, uptime, image, device_family, config_register])

        list_interface = output[device][2].result
        
        interface_bypass = ['Loopback0','Null0','MgmtEth0/0/CPU0/0']
        for interface in list_interface:
            interface_data = list_interface[interface]
            if interface not in interface_bypass:

                show_arp_command_output = output[device][3].result
                count_arp = len(show_arp_command_output['interfaces'][interface]['ipv4']['neighbors'])

                interface_name = interface
                ip_address = [key for key in interface_data['ipv4'].keys()][0]
                line_protocol = interface_data['line_protocol']
                oper_status = interface_data['oper_status']
                description = interface_data['description']
                mtu = interface_data['mtu']
                port_speed = interface_data['port_speed']
                last_link_flapped = interface_data['last_link_flapped']
                in_octets = interface_data['counters']['in_octets']
                out_octets = interface_data['counters']['out_octets']

                interface_table.add_row([hostname, interface_name, ip_address, line_protocol, oper_status, description, mtu, port_speed, last_link_flapped, in_octets, out_octets, count_arp])

        ospf_interfaces = output[device][4].result['vrf']['default']['address_family']['ipv4']['instance']['1']['areas']['0.0.0.0']['interfaces']
    
        for ospf_neighbor in ospf_interfaces.keys():

                router_id = ospf_interfaces[ospf_neighbor]['neighbors']

                for each_neighbor in router_id.keys():
                    neighbor_router_id = router_id[each_neighbor]['neighbor_router_id']
                    address = router_id[each_neighbor]['address']
                    state = router_id[each_neighbor]['state']
                    bdr_ip_addr = router_id[each_neighbor]['bdr_ip_addr']
                    neighbor_uptime = router_id[each_neighbor]['neighbor_uptime']

                    ospf_table.add_row([hostname, ospf_neighbor, neighbor_router_id, address, state, bdr_ip_addr, neighbor_uptime])
    
    print(version_table)

    print(interface_table)

    print(ospf_table)


ios_xr(output)

#IOS-XR
#show ip route ospf
#show ip ospf neighbor

#NX-OS
#show ip route ospf
#show ip ospf neighbors detail
