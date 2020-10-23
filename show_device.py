from nornir import InitNornir
from nornir.core.filter import F
from nornir_utils.plugins.functions import print_result
from ios_xe import ios_xe
from ios_xr import ios_xr
from create_table import make_table


def filter_platform(nrf):

    filter_ios_xe = nrf.filter(F(platform="cisco_xe"))

    if filter_ios_xe.inventory.hosts:
        ios_xe(filter_ios_xe)

    filter_ios_xr = nrf.filter(F(platform="cisco_xr"))

    if filter_ios_xr.inventory.hosts:
        ios_xr(filter_ios_xr)


nr = InitNornir(config_file="config.yaml")

nrf = nr.filter(F(name="dist-rtr01"))

filter_platform(nrf)

make_table(table_name='version',print_table=True)
make_table(table_name='interface',print_table=True)
make_table(table_name='ospf',print_table=True)