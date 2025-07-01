#!/bin/bash

MODE_FILE="/etc/emos/boot_mode"
MODE="install"

if [ -f "$MODE_FILE" ]; then
    MODE=$(cat "$MODE_FILE")
fi

case "$MODE" in
    install)
        echo "[BOOT] Installation mode - ethernet required for internet"
        systemctl stop hostapd >/dev/null 2>&1 || true
        systemctl stop dnsmasq >/dev/null 2>&1 || true
        ;;
    business)
        echo "[BOOT] Business mode - starting hotspot"
        systemctl start hostapd >/dev/null 2>&1 || true
        systemctl start dnsmasq >/dev/null 2>&1 || true
        ;;
    *)
        echo "[BOOT] Unknown mode '$MODE'"
        ;;
fi
