#!/bin/bash

SSID="Your_SSID_Here"
PASSWORD="Your_WiFi_Password"

echo "[*] Starting Wi-Fi force connect loop to '$SSID'..."

while true; do
    # Check if already connected
    CURRENT_SSID=$(nmcli -t -f active,ssid dev wifi | grep '^yes' | cut -d: -f2)
    if [ "$CURRENT_SSID" == "$SSID" ]; then
        echo "[+] Connected to $SSID."
        break
    fi

    echo "[!] Not connected to $SSID. Attempting to connect..."
    nmcli dev wifi connect "$SSID" password "$PASSWORD"

    # Wait before retrying
    sleep 5
done

