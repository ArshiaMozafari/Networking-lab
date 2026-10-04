import json
import socket
import sys
import time
from datetime import datetime

from scapy.layers.l2 import ARP, Ether
from scapy.sendrecv import srp


def resolve_hostname(ip: str) -> str:
    """Best-effort reverse DNS. Returns '?' on failure."""
    try:
        return socket.gethostbyaddr(ip)[0]
    except (socket.herror, socket.gaierror, OSError):
        return "?"


def arp_scan(target: str, iface: str | None = None,
             timeout: float = 2.0, retry: int = 2,
             resolve_names: bool = True) -> list[dict]:
    """Scan a single IP or CIDR. Returns list of device dicts."""
    arp = ARP(pdst=target)
    ether = Ether(dst="ff:ff:ff:ff:ff:ff")
    packet = ether / arp

    kwargs = {"timeout": timeout, "retry": retry, "verbose": 0}
    if iface:
        kwargs["iface"] = iface

    answered, _ = srp(packet, **kwargs)

    devices = []
    for _, rcv in answered:
        devices.append({
            "ip": rcv.psrc,
            "mac": rcv.hwsrc,
            "hostname": resolve_hostname(rcv.psrc) if resolve_names else "?",
        })

    # stable output: sort by IP numerically
    devices.sort(key=lambda d: tuple(int(o) for o in d["ip"].split(".")))
    return devices


def main():
    if len(sys.argv) < 2:
        print("Usage: sudo python3 arp_scan.py <target> [output.json]")
        print("  e.g. sudo python3 arp_scan.py 192.168.0.0/24 scan.json")
        sys.exit(1)

    target = sys.argv[1]
    output = sys.argv[2] if len(sys.argv) > 2 else "arp_scan.json"

    started = time.time()
    print(f"Scanning {target} ...")

    devices = arp_scan(target)

    duration = round(time.time() - started, 2)

    payload = {
        "scan_time": datetime.now().isoformat(timespec="seconds"),
        "target": target,
        "duration_seconds": duration,
        "device_count": len(devices),
        "devices": devices,
    }

    with open(output, "w", encoding="utf-8") as f:
        json.dump(payload, f, indent=4)

    print(f"Found {len(devices)} device(s) in {duration}s")
    for d in devices:
        print(f"  {d['ip']:<16} {d['mac']:<18} {d['hostname']}")
    print(f"\nSaved -> {output}")


if __name__ == "__main__":
    main()