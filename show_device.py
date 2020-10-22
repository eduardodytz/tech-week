from nornir import InitNornir
from nornir.core.filter import F
from nornir_utils.plugins.functions import print_result
from nornir_netmiko import netmiko_send_command

nr = InitNornir(config_file="config.yaml")

nrf = nr.filter(F(name="dist-rtr01"))


def multitask(task,feature):
    for device in nrf.inventory.hosts.keys():
        if 'ospf' in feature:
            if 'nxos' in nrf.inventory.hosts[device].platform:
                ospf_command = "show ip ospf neighbors detail"
            elif 'xr' in nrf.inventory.hosts[device].platform:
                ospf_command = "show ospf vrf all-inclusive neighbor detail"
            elif 'xe' in nrf.inventory.hosts[device].platform:
                ospf_command = "show ip ospf neighbor"
    
    task.run(
            task=netmiko_send_command,
            command_string=ospf_command, 
            use_genie=True
            )


output = nrf.run(
            task=multitask,
            feature='ospf',
            )

print_result(output)

#dist-rtr01
#show ip route ospf
#show ip ospf neighbor

#dist-sw01
#show ip route ospf
#show ip ospf neighbors detail
