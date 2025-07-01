# EMOS Configurator – User Guide

1. Power on the Raspberry Pi
2. Connect to WiFi network: `Spindle_EMOS_Config`
   - Password: `emosconfig`
3. Open a browser and go to: [http://192.168.10.1:8000](http://192.168.10.1:8000)
4. Configure EMOS cameras:
   - Choose codec (MJPEG / H264)
   - Set multicast port
   - Save per camera
5. Open the **Discover** page to sniff for EMOS cameras. ``tcpdump`` runs for
   one minute and lists the MAC and IP address of each camera. Apply the detected
   subnet to ``eth0`` and return to the configuration page to adjust settings.
6. Klik op "Switch to Business Mode" om het apparaat naar bedrijfsmodus te zetten.
   Het ethernetinterface krijgt dan het statische adres `192.168.40.240/24`.
   Druk daarna op "DHCP Mode" om weer een adres via DHCP op te halen.
