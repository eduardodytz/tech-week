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

# Filter host
nrf = nr.filter(F(role="dist"))

# Executing commands "show"
output = nrf.run(task=netmiko_send_command, command_string="show ip interface brief")

# Executing commands "show" with JSON parsing
# output = nrf.run(task=netmiko_send_command, command_string="show ip interface brief", use_genie=True)

# Print results
print_result(output)