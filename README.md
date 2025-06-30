# EMOS Configurator

This project provides a minimal web interface for configuring EMOS cameras on a Raspberry Pi. The service can run in hotspot mode or over an existing wired connection.

## Installation

Run the installer on the target device:

```bash
sudo ./scripts/install.sh
```

The script installs required packages, sets up `hostapd` and `dnsmasq`, and registers the system services for the configurator. After completion the device reboots and exposes a WiFi network `Spindle_EMOS_Config`.

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
