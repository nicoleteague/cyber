import threading
import socket
from scapy.all import ARP, Ether, srp


def scan_network(ip_range):
    try:
        # Create ARP request packet
        arp = ARP(pdst=ip_range)

        # Create Ethernet frame
        ether = Ether(dst='ff:ff:ff:ff:ff:ff')

        # Combine Ethernet frame and ARP request packet
        packet = ether / arp

        # Send packet and receive response
        result = srp(packet, timeout=2, verbose=0)[0]

        devices = []
        for sent, received in result:
            devices.append({'ip': received.psrc, 'mac': received.hwsrc})

        return devices

    except Exception as e:
        print(f"Error in scan_network: {e}")
        return []


def scan_ports(ip, ports):
    open_ports = []
    for port in ports:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(1)
        result = sock.connect_ex((ip, port))
        if result == 0:
            open_ports.append(port)
        sock.close()
    return open_ports


class PortScannerThread(threading.Thread):
    def __init__(self, ip, ports):
        threading.Thread.__init__(self)
        self.ip = ip
        self.ports = ports
        self.open_ports = []

    def run(self):
        self.open_ports = scan_ports(self.ip, self.ports)


def main():
    ip_range = input("Enter IP Range: ")
    devices = scan_network(ip_range)

    if not devices:
        print("No Devices Found")
        return

    print("Devices found on this network:")
    for device in devices:
        print(f"IP: {device['ip']} MAC: {device['mac']}")

    ports = list(range(1, 1025))
    threads = []

    print("\nScanning for open ports on devices...")
    for device in devices:
        thread = PortScannerThread(device['ip'], ports)
        thread.start()
        threads.append(thread)

    for thread in threads:
        thread.join()
        if thread.open_ports:
            print(f"\nOpen ports for {thread.ip}: {thread.open_ports}")


if __name__ == '__main__':
    main()
