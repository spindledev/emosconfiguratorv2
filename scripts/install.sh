#!/bin/bash
set -e

echo "[INFO] Starting EMOS Configurator installation..."

# Update en dependencies
sudo apt update
sudo apt install -y dnsmasq hostapd python3-pip

# Maak directories indien nodig
sudo mkdir -p /etc/emos
sudo mkdir -p /etc/network/interfaces.d
sudo cp config/dnsmasq.conf /etc/dnsmasq.conf
sudo cp config/hostapd.conf /etc/hostapd/hostapd.conf
sudo cp config/wlan0_static.conf /etc/network/interfaces.d/wlan0_static.conf

# Schakel services in
sudo systemctl unmask hostapd
sudo systemctl enable hostapd
sudo systemctl enable dnsmasq

# Zet netwerkconfiguratie
sudo rfkill unblock wlan

# Python requirements
pip3 install --break-system-packages -r requirements.txt

# Webapp & services
sudo cp emos-configurator.service /etc/systemd/system/
sudo cp emos-boot-manager.service /etc/systemd/system/
sudo chmod +x emos_boot_manager.sh
sudo systemctl daemon-reload
sudo systemctl enable emos-configurator.service
sudo systemctl enable emos-boot-manager.service

echo "[INFO] Installation completed. Rebooting in 5 seconds..."
sleep 5
sudo reboot
