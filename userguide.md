# EMOS Configurator – User Guide

1. Power on the Raspberry Pi
2. Connect to WiFi network: `Spindle_EMOS_Config`
   - Password: `emosconfig`
3. Open a browser and go to: [http://192.168.10.1:8000](http://192.168.10.1:8000)
4. Configure EMOS cameras:
   - Choose codec (MJPEG / H264)
   - Set multicast port
   - Save per camera
5. Use the **Discover** form to find connected cameras. Toggle the slider to
   switch between scanning and sniffing. In sniff mode ``tcpdump`` runs for one
   minute and lists the MAC and IP address of each EMOS camera.
6. Klik op "Switch to Business Mode" om het apparaat naar bedrijfsmodus te zetten.
   Het ethernetinterface krijgt dan het statische adres `192.168.40.240/24`.
   Druk daarna op "DHCP Mode" om weer een adres via DHCP op te halen.
