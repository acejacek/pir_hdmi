# PIR controlled HDMI

This daemon allows to control HDMI output in Raspberry Pi. It can put monitor to sleep when no nearby movement detected. It can be useful in kiosk applications. Works beautifully with [MagicMirror](https://magicmirror.builders). Requires [Passive Infrared Sensor](https://en.wikipedia.org/wiki/Passive_infrared_sensor) connected to Raspbrerry Pi. Look here for inspirations:

- [Raspberry Pi GPIO Sensing: Motion Detection](https://www.modmypi.com/blog/raspberry-pi-gpio-sensing-motion-detection)
- [How to Interface a PIR Motion Sensor With Raspberry Pi GPIO](https://maker.pro/education/bluetooth-basics-how-to-control-an-led-using-a-smartphone-and-arduino-1)
- [Raspberry Pi Motion Sensor using a PIR Sensor](https://pimylifeup.com/raspberry-pi-motion-sensor/)

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

3. Test if program works correctly. Check all options:
```
sudo python pirhdmi.py --help
```

4. Real check. Specify where your PIR is conencted (pin 11 in this example):
```
sudo python pirhdmi.py --debug --pir-pin 11
```
If all behaves as expected, interrupt program with `Ctrl-C`, and follow next step to install service.

5. In `pirhdmi.service` adjust your setting, specifically `--pir-pin` to be the same as used in your connection.

6. Configure `systemd` daemon to run script. Copy service definition to `/lib/systemd/system` folder:
```
sudo cp pirhdmi.service /lib/systemd/system
```

7. Now, activate the service:
```
sudo chmod 644 /lib/systemd/system/pirhdmi.service
sudo systemctl daemon-reload
sudo systemctl enable pirhdmi.service
sudo systemctl start pirhdmi.service
```

8. Check the status:
```
sudo systemctl status pirhdmi.service
```

## Update
1. In `pir_hdmi` folder execute:
```
git pull
```

2. All your customizations can be overwritten. Check again, if `--pir-pin` in `pirhdmi.service` points to correct one.

3. If you copy updated service definition `pirhdmi.service` to `/lib/systemd/system` folder, remember to inform `systemd` about the changes:
```
sudo systemctl daemon-reload
```
4. Restart service:
```
sudo systemctl restart pirhdmi.service
```

