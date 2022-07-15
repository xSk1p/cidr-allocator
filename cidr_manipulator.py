"""
Contains functions used to manipulate the CIDR block in order to get next available range
"""

import logging
import ipaddress

from matplotlib.style import available
from postgres_handler import get_cidr_list, push_cidr_to_db

logging.basicConfig(
        filename = 'logs/cidr_manipulator.log',
        level = logging.INFO,
        format = '%(levelname)s:%(asctime)s:%(message)s')

def sub_cidr(cidr, cidr_blocks):
    """Returns substraction of 2 CIDR blocks."""
    nets = []
    if len(cidr_blocks) == 0:
        nets.append([cidr])
    for cidr_block in cidr_blocks:
        if len(nets) > 0:
            if cidr_block in nets[0]:
                nets[0].remove(cidr_block)
        a = ipaddress.ip_network(cidr)
        b = ipaddress.ip_network(cidr_block)
        if (b.subnet_of(a)):
            raw_new_nets = list((ipaddress.ip_network(cidr)).address_exclude(ipaddress.ip_network(cidr_block)))
            clean_new_nets = []
            for raw_new_net in raw_new_nets:
                clean_new_nets.append(str(raw_new_net))
            if len(nets) == 0:
                nets.append(clean_new_nets)
            if len(clean_new_nets) <= len(nets):
             nets = clean_new_nets
        else:
            nets.append([cidr])
    if len(nets) > 0:
        return nets[0]
    else:
        return "None"

def cidr_to_range(cidr_list):
    """Converts CIDR block to range"""
    if cidr_list == "None":
        return "None"
    else:
        for cidr in cidr_list:
            return (
                str(ipaddress.ip_network(cidr)[0]) + "-" + str(ipaddress.ip_network(cidr)[-1])
            )

def next_available_range(cidr):
    """Starts the execution of all the functions in order to get next available range"""
    available_cidr = sub_cidr(cidr, get_cidr_list())
    push_cidr_to_db(cidr)
    return cidr_to_range(available_cidr)



if __name__ == '__main__':
    master = "10.0.0.0/16"
    print(next_available_range(master))
