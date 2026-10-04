from scapy.all import *

# ARP: map IP to MAC
# Searching within a LAN networking, assuming the network address is 192.168.0.0/24.
arp = ARP(pdst="192.168.0.0/24")

# Ethernet broadcast
ether = Ether(dst="ff:ff:ff:ff:ff:ff")

# create the packet
packet = ether / arp

# Send and collect responses
result = srp(packet, timeout=2, verbose=0)[0]

print("Devices found:")
# output: IPs of devices within the same LAN network + their MAC.
for sent, received in result:
    print(f"IP: {received.psrc}    MAC: {received.hwsrc}")