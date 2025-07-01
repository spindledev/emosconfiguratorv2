#!/bin/bash
set -e

echo "[INFO] Starting EMOS Configurator installation..."

# Update en dependencies
sudo apt update
sudo apt install -y dnsmasq hostapd python3-pip

# Disable NetworkManager and dhcpcd which conflict with systemd-networkd on Bookworm
sudo systemctl disable --now NetworkManager || true
sudo systemctl disable --now dhcpcd || true

# Maak directories indien nodig
sudo mkdir -p /etc/emos
sudo cp config/dnsmasq.conf /etc/dnsmasq.conf
sudo cp config/hostapd.conf /etc/hostapd/hostapd.conf
# Configure static IP via systemd-networkd
sudo mkdir -p /etc/systemd/network
sudo cp config/wlan0.network /etc/systemd/network/wlan0.network
sudo systemctl enable systemd-networkd
sudo systemctl restart systemd-networkd

# Schakel services in
sudo systemctl unmask hostapd
sudo systemctl enable hostapd
sudo systemctl enable dnsmasq

# Zet netwerkconfiguratie
sudo rfkill unblock wlan

# Python requirements
pip3 install --break-system-packages -r requirements.txt

# Webapp & services
REPO_DIR=$(pwd)
CURRENT_USER=$(whoami)
sed "s|/home/spindle/emosconfiguratorv2|$REPO_DIR|; s|User=spindle|User=$CURRENT_USER|" emos-configurator.service \
  | sudo tee /etc/systemd/system/emos-configurator.service >/dev/null
sed "s|/home/spindle/emosconfiguratorv2|$REPO_DIR|; s|User=spindle|User=$CURRENT_USER|" emos-boot-manager.service \
  | sudo tee /etc/systemd/system/emos-boot-manager.service >/dev/null
sudo cp unblock-wifi.service /etc/systemd/system/
sudo chmod +x emos_boot_manager.sh
sudo systemctl daemon-reload
sudo systemctl enable emos-configurator.service
sudo systemctl enable emos-boot-manager.service
sudo systemctl enable unblock-wifi.service

# Mark installation as complete so next boot starts in business mode
echo "business" | sudo tee /etc/emos/boot_mode > /dev/null

echo "[INFO] Installation completed. Rebooting in 5 seconds..."
sleep 5
sudo reboot
