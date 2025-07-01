# EMOS Configurator

Tool for configuring EMOS cameras via hotspot or wired setup.

## Setup

1. Clone this repository.
2. (Optional) Create and activate a Python virtual environment.
3. Install the dependencies:

```bash
pip install -r requirements.txt
```

## Running the FastAPI App

Launch the server with `uvicorn`:

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Visit `http://localhost:8000` in your browser to open the configurator.

Visit `http://192.168.10.1:8000` to access the web interface. Each camera can be
assigned a codec and multicast port via the form and the settings are saved
through the FastAPI backend.

Use the **Discover** form on the web page to find connected cameras. A slider
allows switching between active ARP scanning and a passive sniffer mode. When
sniffing, you can copy the subnet of `eth0` with a single click.

An alternative is to passively sniff the ethernet interface for broadcast or
multicast traffic. The cameras regularly send out packets such as mDNS, SSDP or
DHCP requests. You can capture these without sending any traffic yourself:

```bash
sudo tcpdump -i eth0 -n -e
```

Look for frames with the Orlaco vendor prefix `DC:36:43:C` to identify the
camera's MAC address.

This project provides a minimal web interface for configuring EMOS cameras on a Raspberry Pi. The service can run in hotspot mode or over an existing wired connection.

## Installation

Follow these steps to set up the configurator:

1. **Installation mode** – connect the device to the internet via `eth0` and run:

   ```bash
   sudo ./scripts/install.sh
   ```

   The script installs required packages, disables `NetworkManager` and
   `dhcpcd` (both enabled by default on Raspberry Pi OS Bookworm), configures
   `systemd-networkd` so that `wlan0` uses the static address `192.168.10.1`,
   and sets up `hostapd` and `dnsmasq` so that the hotspot works right after
   reboot. It also builds the [OCC](https://github.com/Codemonkey1973/OCC)
   utility and installs it to `/usr/bin/occ`. The system is marked for business
   mode on the next reboot.

2. **Business mode** – after the reboot, connect to Wi‑Fi network `Spindle_EMOS_Config` and open [http://192.168.10.1:8000](http://192.168.10.1:8000). The ethernet interface is now used only to configure EMOS cameras and for ARP scans.

## Example API usage

The FastAPI app exposes a small REST API. The root endpoint is useful for a quick health check:

```bash
curl http://192.168.10.1:8000/
```

Response:

```json
{"msg": "ok"}
```

## Hotspot and camera configuration

Power on the Raspberry Pi and connect to the hotspot mentioned above, then browse to [http://192.168.10.1:8000](http://192.168.10.1:8000). Follow the steps in the [user guide](userguide.md) to configure each camera.

### Bookworm notes

On Raspberry Pi OS Bookworm, `NetworkManager` manages wireless interfaces by default. The installer disables `NetworkManager` and `dhcpcd` for you so that `systemd-networkd` can assign the static address `192.168.10.1` to `wlan0`. DHCP leases are served by `dnsmasq` as configured in `config/dnsmasq.conf`.

## Version updates

A `VERSION` file keeps track of the installed version. The utilities in `app/version.py` compare this to the latest release on GitHub. Set the `GITHUB_REPO` environment variable (for example `user/repo`) to enable the update check.



## License

This project is licensed under the [MIT License](LICENSE).



