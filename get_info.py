from nornir import InitNornir
from nornir.core.filter import F
from resource.ios_xe import ios_xe
from resource.ios_xr import ios_xr
from resource.nx_os import nx_os
from resource.create_table import make_table


def filter_platform(nrf):

    filter_ios_xe = nrf.filter(F(platform="cisco_xe"))

    if filter_ios_xe.inventory.hosts:
        ios_xe(filter_ios_xe)

    filter_ios_xr = nrf.filter(F(platform="cisco_xr"))

    if filter_ios_xr.inventory.hosts:
        ios_xr(filter_ios_xr)

    filter_nx_os = nrf.filter(F(platform="cisco_nxos"))

    if filter_nx_os.inventory.hosts:
        nx_os(filter_nx_os)


if __name__ == "__main__":

    nr = InitNornir(config_file="nornir/config.yaml")

    nrf = nr.filter(F(platform="cisco_xe") | F(platform="cisco_xr"))

    filter_platform(nrf)

    make_table(table_name='version',print_table=True)
    make_table(table_name='interface',print_table=True)
    make_table(table_name='ospf',print_table=True)