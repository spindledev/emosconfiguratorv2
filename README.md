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


## License

This project is licensed under the [MIT License](LICENSE).



