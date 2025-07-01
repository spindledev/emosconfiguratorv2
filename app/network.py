import subprocess
import re
from typing import List


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
    timeout: int = 60,
) -> List[dict]:
    """Return MAC and IP addresses of EMOS cameras seen in a tcpdump.

    This function invokes ``tcpdump`` on ``interface`` for ``timeout`` seconds
    and parses the output for packets originating from devices whose MAC address
    starts with ``prefix``. The detection works independently of the subnet the
    camera is on.
    """

    cameras = {}
    prefix = prefix.upper()

    try:
        proc = subprocess.Popen(
            ["timeout", str(timeout), "tcpdump", "-eni", interface, "-n", "ip"],
            stdout=subprocess.PIPE,
            stderr=subprocess.DEVNULL,
            text=True,
        )
    except FileNotFoundError:
        return []

    if proc.stdout is None:
        return []

    mac_re = r"([0-9A-Fa-f]{2}(?::[0-9A-Fa-f]{2}){5})"
    ip_re = r"(\d{1,3}(?:\.\d{1,3}){3})(?:\.\d+)?"

    for line in proc.stdout:
        line = line.strip()
        mac_match = re.search(mac_re, line)
        ip_match = re.search(ip_re, line)
        if not mac_match or not ip_match:
            continue
        mac = mac_match.group(1).upper()
        if not mac.startswith(prefix):
            continue
        ip_addr = ip_match.group(1)
        cameras[mac] = ip_addr

    proc.wait()

    return [{"mac": mac, "ip": ip} for mac, ip in cameras.items()]


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


def subnet_from_ip(ip: str) -> str:
    """Return a /24 subnet in CIDR notation derived from *ip*."""
    parts = ip.split(".")
    if len(parts) != 4:
        return ""
    return ".".join(parts[:3] + ["0"]) + "/24"


def set_eth0_subnet(subnet: str) -> None:
    """Configure ``eth0`` for the supplied ``subnet``."""
    try:
        network, prefix = subnet.split("/")
    except ValueError:
        return
    parts = network.split(".")
    if len(parts) != 4:
        return
    ip = ".".join(parts[:3] + ["240"]) + f"/{prefix}"
    set_eth0_static(ip)
