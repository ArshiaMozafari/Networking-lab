import json
import sys
from pathlib import Path


def load_scan(path: str) -> dict:
    """Load and validate a scan file."""
    p = Path(path)
    if not p.exists():
        raise FileNotFoundError(f"No scan file: {path}")

    with p.open(encoding="utf-8") as f:
        data = json.load(f)

    if "devices" not in data or not isinstance(data["devices"], list):
        raise ValueError(f"Malformed scan file: {path}")

    return data


def print_scan(data: dict) -> None:
    print(f"Scan target : {data.get('target', '?')}")
    print(f"Scan time   : {data.get('scan_time', '?')}")
    print(f"Duration    : {data.get('duration_seconds', '?')}s")
    print(f"Devices     : {data.get('device_count', len(data['devices']))}")
    print("-" * 56)
    print(f"{'IP':<16}{'MAC':<20}{'Hostname'}")
    print("-" * 56)
    for d in data["devices"]:
        print(f"{d['ip']:<16}{d['mac']:<20}{d.get('hostname', '?')}")


def find_by_mac(data: dict, mac: str) -> list[dict]:
    mac = mac.lower()
    return [d for d in data["devices"] if d["mac"].lower() == mac]


def main():
    if len(sys.argv) < 2:
        print("Usage: python3 read_scan.py <scan.json> [mac-to-find]")
        sys.exit(1)

    data = load_scan(sys.argv[1])
    print_scan(data)

    if len(sys.argv) > 2:
        mac = sys.argv[2]
        matches = find_by_mac(data, mac)
        print(f"\nLookup {mac}:")
        if matches:
            for m in matches:
                print(f"  found: {m['ip']} ({m.get('hostname', '?')})")
        else:
            print("  not found")


if __name__ == "__main__":
    main()