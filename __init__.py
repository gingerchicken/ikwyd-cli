import ikwyd
import argparse
from tabulate import tabulate

# Argparser stuff
parser = argparse.ArgumentParser(description='query iknowwhatyoudownload (ikwyd) while in a command line interface')
parser.add_argument('ip_addr', nargs="?", type=str, help='the ip which you would like to query', default=str())

args = parser.parse_args()

# Get the IP Address
raw_addr = args.ip_addr.strip()
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
    title = "N/A" if len(t.title) == 0 else t.title
    raw_torrents.append([
        t.first_seen, t.last_seen, t.category, title, t.size
    ])
raw_torrents.reverse()

# Show the list
print(tabulate(
    raw_torrents, headers=["First Seen", "Last Seen", "Category", "Title", "Size"]
))