from nornir import InitNornir
from nornir.core.filter import F
from nornir_utils.plugins.functions import print_result
from nornir_netmiko import netmiko_send_command

nr = InitNornir(config_file="config.yaml")

nrf = nr.filter(F(name="dist-sw02"))

output = nrf.run(
            task=netmiko_send_command,
            name="command output",
            command_string="show version", 
            use_genie=True
            )

print_result(output)


