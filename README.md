# PIR controlled HDMI

This daemon allows to control HDMI output in Raspberry Pi. It can put monitor to sleep when no movement detected. It can be useful in kiosk applications. Works beautifully with [MagicMirror](https://magicmirror.builders). Requires [Passive Infrared Sensor](https://en.wikipedia.org/wiki/Passive_infrared_sensor) connected to Raspbrerry Pi. Look here for inspirations:

- [https://www.modmypi.com](https://www.modmypi.com/blog/raspberry-pi-gpio-sensing-motion-detection)

## Installation

1. Make sure you have all needed components:
```
sudo apt-get install git
```

2. Clone repository. From `pi` home execute:
```
git clone https://github.com/acejacek/pir_hdmi.git
```
New folder will appear: `pir_hdmi`. Navigate into it.

3. In `pirhdmi.py` code adjust your setting, specifically `PIR_PIN` needs to be the same as used in your connection.

4. Test if all works correctly:
```
sudo python pirhdmi.py —debug
```

5. Configure `systemd` daemon to run script. Copy service definition to `/lib/systemd/system` folder:
```
sudo cp pirhdmi.service /lib/systemd/system
```

6. Now, activate the service:
```
sudo chmod 644 /lib/systemd/system/pirhdmi.service
sudo systemctl daemon-reload
sudo systemctl enable pirhdmi.service
sudo systemctl start pirhdmi.service
```

7. Check the status:
```
sudo systemctl status pirhdmi.service
```

## Update
1. In `pir_hdmi` folder execute:
```
git pull
```
2. If you copy updated service definition `pirhdmi.service` to `/lib/systemd/system` folder, remember to inform `systemd` about the changes:
```
sudo systemctl daemon-reload
```
3. Restart service:
```
sudo systemctl restart pirhdmi.service
```

