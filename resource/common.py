def get_item(interface_data,item):

    if item in interface_data:
        if item == 'ipv4':
            output = [key for key in interface_data['ipv4'].keys()][0]
        else:
            output = interface_data[item]
    else:
        output = ''
    
    return output