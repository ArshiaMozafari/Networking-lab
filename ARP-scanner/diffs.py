import json
import sys


def load_devices(path):
    with open(path) as f:
        data = json.load(f)
    return {d["mac"].lower(): d for d in data["devices"]}


def main():
    if len(sys.argv) != 3:
        print("Usage: python3 diff_scans.py old.json new.json")
        sys.exit(1)

    old = load_devices(sys.argv[1])
    new = load_devices(sys.argv[2])

    appeared = [new[m] for m in new if m not in old]
    disappeared = [old[m] for m in old if m not in new]

    print(f"NEW ({len(appeared)}):")
    for d in appeared:
        print(f"  + {d['ip']:<16} {d['mac']:<18} {d.get('hostname','?')}")

    print(f"\nGONE ({len(disappeared)}):")
    for d in disappeared:
        print(f"  - {d['ip']:<16} {d['mac']:<18} {d.get('hostname','?')}")


if __name__ == "__main__":
    main()