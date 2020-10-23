from prettytable import PrettyTable


def make_table(table_name, data=False, print_table=False):

    global version, interface, ospf

    if table_name == 'version' and data:
        if 'version' not in globals():
            version = PrettyTable()
            version.field_names = ["Hostname","OS","Version","Uptime","Image","Device Family","Config Register"]

        version.add_row(data)

    elif table_name == 'version' and print_table:
        print(version)   


    if table_name == 'interface' and data:
        if 'interface' not in globals():
            interface = PrettyTable()
            interface.field_names = ["Hostname", "Interface", "IP", "Protocol", "Status", "Description", "MTU", "Port Speed", "Input", "Output"]

        interface.add_row(data)

    elif table_name == 'interface' and print_table:
        print(interface)


    if table_name == 'ospf' and data:
        if 'ospf' not in globals():
            ospf = PrettyTable()
            ospf.field_names = ["Hostname","OSPF Interface","Neighbor Router ID","Address","State"]

        ospf.add_row(data)

    elif table_name == 'ospf' and print_table:
        print(ospf)