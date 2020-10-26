################################################################################################################################
#
#
# Script with outputs without any processing.
# To manage the connections, the Nornir framework will be used. I choose it because of its high scalability.
# 
# Nornir documentation: https://nornir.readthedocs.io/en/3.0.0/index.html
#
# Author: Eduardo Dytz
# 
# 
################################################################################################################################

# Importing the Nornir functions.
from nornir import InitNornir
from nornir_utils.plugins.functions import print_result
from nornir_netmiko import netmiko_send_command

# Importing the "F" function, which provides us with an advanced filter.
from nornir.core.filter import F

# Starting the nornir and passing which configuration file it should use.
nr = InitNornir(config_file="nornir/config.yaml")


##############################################
# hosts.yaml configuration example:
#
#   dist-rtr01:
#    hostname: 10.10.20.175
#    port: 22
#    platform: cisco_xe
#    groups:
#        - cisco
#    data:
#        role: dist
#        type: router
#
#   dist-sw01:
#    hostname: 10.10.20.177
#    port: 22
#    platform: cisco_nxos
#    groups:
#        - cisco
#    data:
#        role: dist
#        type: switch

# Filter host
nrf = nr.filter(F(name="dist-rtr01") | F(name="dist-sw01"))

# Executing commands "show"
#output = nrf.run(task=netmiko_send_command, command_string="show ip interface brief")

# Executing commands "show" with JSON parsing
output = nrf.run(task=netmiko_send_command, command_string="show ip interface brief", use_genie=True)

# Print results
print_result(output)