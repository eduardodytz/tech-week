from netmiko import ConnectHandler

def sshSession(**device):
    try:
        net_connect = ConnectHandler(**device)
        net_connect.enable()
    except Exception as error:
        print(error)
