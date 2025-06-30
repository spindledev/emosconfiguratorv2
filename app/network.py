import subprocess
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
