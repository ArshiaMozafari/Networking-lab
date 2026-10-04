import json
import ipaddress


routing_table = [
    ('192.168.1.0/24', 'direct'),
    ('10.0.0.0/16',    '192.168.1.254'),
    ('0.0.0.0/0',      '192.168.1.1'),
]

def save_table(table, path):
    with open(path, "w") as f:
        json.dump(table, f, indent=4)


if __name__ == "__main__":
    file_name = "routing-table.json"
    save_table(routing_table, file_name)
    print(f'Routing table saved as {file_name}')