import subprocess
from ipaddress import ip_network, ip_address
from typing import List, Set

from scapy.all import sniff, Ether, IP


def find_emos_cameras(
    interface: str = "eth0", prefix: str = "DC:36:43"
) -> List[str]:
    """Return a list of IPs on *interface* whose MAC starts with *prefix*.

    Parameters
    ----------
    interface: str
        Network interface to query, e.g. ``"eth0"``.
    prefix: str
        MAC address prefix to match (case-insensitive).
    """
    try:
        output = subprocess.check_output(
            ["ip", "neigh", "show", "dev", interface],
            text=True,
        )
    except subprocess.CalledProcessError:
        return []

    cameras = []
    for line in output.splitlines():
        parts = line.split()
        if len(parts) >= 5 and parts[4].upper().startswith(prefix.upper()):
            cameras.append(parts[0])
    return cameras


def sniff_emos_cameras(
    interface: str = "eth0",
    prefix: str = "DC:36:43",
    timeout: int = 5,
    subnet: str | None = None,
) -> List[str]:
    """Sniff *interface* for packets from EMOS cameras.

    Parameters
    ----------
    interface: str
        Interface to listen on.
    prefix: str
        MAC address prefix identifying EMOS cameras.
    timeout: int
        Capture duration in seconds.
    subnet: str | None
        Optional subnet filter in CIDR notation.
    """

    net = ip_network(subnet, strict=False) if subnet else None
    ips: Set[str] = set()

    def handler(pkt):
        if pkt.haslayer(Ether):
            mac = pkt[Ether].src.upper()
            if mac.startswith(prefix.upper()) and pkt.haslayer(IP):
                ip_addr = pkt[IP].src
                if net is None or ip_address(ip_addr) in net:
                    ips.add(ip_addr)

    sniff(iface=interface, prn=handler, timeout=timeout, store=False)
    return list(ips)


def get_subnet(interface: str = "eth0") -> str:
    """Return the IPv4 subnet of *interface* in CIDR notation."""
    try:
        output = subprocess.check_output(
            ["ip", "-4", "addr", "show", "dev", interface], text=True
        )
    except subprocess.CalledProcessError:
        return ""
    for line in output.splitlines():
        line = line.strip()
        if line.startswith("inet "):
            parts = line.split()
            if len(parts) >= 2:
                return parts[1]
    return ""


def set_eth0_static(ip: str = "192.168.40.240/24") -> None:
    """Configure ``eth0`` with a static IP address."""
    subprocess.run(["sudo", "ip", "addr", "flush", "dev", "eth0"], check=False)
    subprocess.run(["sudo", "ip", "addr", "add", ip, "dev", "eth0"], check=False)
    subprocess.run(["sudo", "ip", "link", "set", "eth0", "up"], check=False)


def set_eth0_dhcp() -> None:
    """Bring ``eth0`` up and obtain an address via DHCP."""
    subprocess.run(["sudo", "ip", "addr", "flush", "dev", "eth0"], check=False)
    subprocess.run(["sudo", "ip", "link", "set", "eth0", "up"], check=False)
    subprocess.run(["sudo", "dhclient", "-1", "eth0"], check=False)


def eth0_is_static(ip: str = "192.168.40.240/24") -> bool:
    """Return ``True`` if ``eth0`` has the specified static address."""
    try:
        output = subprocess.check_output(
            ["ip", "-4", "addr", "show", "dev", "eth0"], text=True
        )
    except subprocess.CalledProcessError:
        return False
    return ip in output
