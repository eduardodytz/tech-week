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
nr = InitNornir(config_file="nornir/config.yaml", dry_run=True)


vlans = [
    {
        "device": "dist-sw01",
        "vlan_id": 107,
        "description": "atm",
        "ip": "172.16.107.2",
        "mask": 24,
        "hsrp": "172.16.107.1"
    },
        {
        "device": "dist-sw02",
        "vlan_id": 107,
        "description": "atm",
        "ip": "172.16.107.3",
        "mask": 24,
        "hsrp": "172.16.107.1"
    }
]

nrf = nr.filter(F(type="switch"))

generate_nxos_config_file(vlans)

result = nrf.run(task=multitask_config)

print_result(result)