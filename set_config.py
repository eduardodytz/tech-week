# Importing the Nornir functions.
from nornir import InitNornir
from nornir_utils.plugins.functions import print_result

# Importing the "F" function, which provides us with an advanced filter.
from nornir.core.filter import F


# Importing functions from resource folder
# 
# Example: We have the "foo.py" and inside it we have the function "bar"
# 
# The import command of the "bar" function would look like this:
# from resource.foo import bar
from utils.nx_os import generate_nxos_config_file, multitask_config

# # Starting the nornir and passing which configuration file it should use.
nr = InitNornir(config_file="nornir/config.yaml")

# List of vlan dictionary by device
vlans = [
    {
        "device": "dist-sw01",
        "vlan_id": 108,
        "description": "teste",
        "ip": "172.16.108.2",
        "mask": 24,
        "hsrp": "172.16.108.1"
    },
        {
        "device": "dist-sw02",
        "vlan_id": 108,
        "description": "teste",
        "ip": "172.16.108.3",
        "mask": 24,
        "hsrp": "172.16.108.1"
    }
]

# Filter host
nrf = nr.filter(F(type="switch"))

# Function to generate the configuration files for each device.
generate_nxos_config_file(vlans)

# Associating the output of the function that will configure and save the changes in the device.
result = nrf.run(task=multitask_config)

# Print the result
print_result(result)