#!/usr/bin/python

import ikwyd
import argparse
import sys

from tabulate import tabulate
from ipaddress import IPv4Address, ip_address

# Argparser stuff
parser = argparse.ArgumentParser(description='Query iknowwhatyoudownload (ikwyd) while in a command line interface')
parser.add_argument('ip_addr', nargs="?", type=str, help='The ip which you would like to query, leave blank for your own IP', default=str())

args = parser.parse_args()

# Get the IP Address
raw_addr = args.ip_addr.strip()

# Check it is an actual IPv4 Address
try:
    if len(raw_addr) > 0 and type(ip_address(raw_addr)) is not IPv4Address:
        raise ValueError()
except ValueError:
    sys.stderr.write("ERROR: Expected IPv4 address, received something else.\n")
    exit(1)

ip = ikwyd.IP(raw_addr)

# Give a more descriptive message
if len(raw_addr) == 0:
    print(f"Acquiring Torrent downloads and distributions for your IP...")
else:
    print(f"Acquiring Torrent downloads and distributions for IP: {raw_addr}...")

torrents = ip.get_torrents()

# Undo the parse kinda...
# TODO Optimise this
raw_torrents = list()
for t in torrents:
    raw_torrents.append([
        t.first_seen, t.last_seen, t.category, t.title, t.size
    ])
raw_torrents.reverse()

# Show the list
print(tabulate(
    raw_torrents, headers=["First Seen", "Last Seen", "Category", "Title", "Size"]
))