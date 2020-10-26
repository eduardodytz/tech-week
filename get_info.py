################################################################################################################################
#
#
# Main script, through it the tasks will be executed.
# To manage the connections, the Nornir framework will be used. I choose it because of its high scalability.
# 
# Nornir documentation: https://nornir.readthedocs.io/en/3.0.0/index.html
#
# Author: Eduardo Dytz
# 
# 
################################################################################################################################


# Importing the Nornir initialization function.
from nornir import InitNornir

# Importing the "F" function, which provides us with an advanced filter.
from nornir.core.filter import F

# Importing functions from resource folder
# 
# Example: We have the "foo.py" and inside it we have the function "bar"
# 
# The import command of the "bar" function would look like this:
# from resource.foo import bar
from utils.ios_xe import multitask_ios_xe
from utils.nx_os import multitask_nx_os
from utils.get_table import print_table


def exec_connection(nrf,features):
    """ Function that segments the hosts by platform and at the end prints the tables, according to the list of features.

    Args:
        nrf (Nornir.filter): Host filter
        features (list): List of features
    """

    # Segmenting the hosts according to their platform.
    filter_ios_xe = nrf.filter(F(platform="cisco_xe"))

    # Checking for cisco_xe (IOS-XE) hosts.
    if filter_ios_xe.inventory.hosts:

        # If there are hosts in the filter, the function that will perform the tasks in this host group will be called.
        multitask_ios_xe(filter_ios_xe,features)

     # Segmenting the hosts according to their platform.
    filter_nx_os = nrf.filter(F(platform="cisco_nxos"))

    # Checking for cisco_nxos (NX-OS) hosts.
    if filter_nx_os.inventory.hosts:

        # If there are hosts in the filter, the function that will perform the tasks in this host group will be called.
        multitask_nx_os(filter_nx_os,features)

    # At the end will be printed the table(s) of the features.
    print_table(tables=features)


if __name__ == "__main__":

    # Starting the nornir and passing which configuration file it should use.
    nr = InitNornir(config_file="nornir/config.yaml")

    # Host filter. Using the "F" function, we can filter hosts by any parameter defined in the nornir/inventory/hosts.yaml.
    #
    # For example:
    #
    #   Filter by platform (OS):
    #       nrf = nr.filter(F(platform="cisco_nxos"))
    #       or platforms:
    #       nrf = nr.filter(F(platform="cisco_xe") | F(platform="cisco_nxos"))
    #
    #   Filter by device:
    #       nrf = nr.filter(F(name="dist-rtr01"))
    #       or devices:
    #       nrf = nr.filter(F(name="dist-rtr01") | F(name="dist-rtr02"))
    #
    #   Filter by role:
    #       nrf = nr.filter(F(role="dist"))
    #
    #   Filter by group:
    #       nrf = nr.filter(F(groups__contains="devnet"))
    #
    #   Filter by type:
    #       nrf = nr.filter(F(type="router"))
    nrf = nr.filter(F(type="switch"))

    # List with the features we wish to obtain information. These features are already defined in the files of each platform, in the resource folder.
    # In this script are already written parser for the commands:
    #
    # ['version'] for "show version" 
    # ['interface'] for "show ip interface brief" 
    # ['ospf'] for "show ip ospf neighbor"
    #
    # Why use CLI commands to obtain this data? 
    # Becacuse CLI commands do not require additional configuration on devices, such as NETCONF/RESCONF,
    # which in addition to additional configuration, has newer IOS versions and firewall rules as prerequisites.
    #
    # So the use of this network script with equipment with older IOS versions is perfectly possible.
    #
    # Where as prerequisites:
    #   - username
    #   - password
    #   - access via ssh
    #
    #
    # The characters can be used all together or separately.
    #
    # For example:
    #   features = ['version','interface','ospf']
    #   or
    #   features = ['version','interface']
    #   or
    #   features = ['ospf']
    features = ['interface']

    # Calling the connection function to the devices, passing the hosts according to the filter previously done and also passing the list of features.
    exec_connection(nrf,features=features)