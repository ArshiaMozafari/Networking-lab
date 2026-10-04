import json
import ipaddress


def load_table(path):
    with open(path) as f:
        raw = json.load(f)
    return [(ipaddress.ip_network(dest), hop) for dest, hop in raw]


def lookup(ip_str, table):
    """Longest-prefix match."""
    ip = ipaddress.ip_address(ip_str)
    matches = [(net, hop) for net, hop in table if ip in net]
    if not matches:
        return None
    # most specific prefix wins
    return max(matches, key=lambda item: item[0].prefixlen)


if __name__ == "__main__":
    table = load_table("routing-table.json")

    for test_ip in ["192.168.1.55", "10.5.0.1", "8.8.8.8"]:
        net, hop = lookup(test_ip, table)
        print(f"{test_ip:<16} -> {net} via {hop}")
