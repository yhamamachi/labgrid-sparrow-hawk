# labgrid-sparrow-hawk
labgrid envrionment for sparrow hawk board with my lab

![SH](./SHv3.gif)

## Setup

### Install labgrid

See also: https://labgrid.readthedocs.io/en/latest/getting_started.html

```
python3 -m venv labgrid-venv
source labgrid-venv/bin/activate
pip install --upgrade pip
pip install labgrid pytest-html
```

### udev rules

Create udev rule to fix serial device name.
```
-> % cat /etc/udev/rules.d/99-fixedSerial.rules
SUBSYSTEM=="tty",  ATTRS{idVendor}=="0403", ATTRS{idProduct}=="6010", ENV{ID_USB_INTERFACE_NUM}=="00",SYMLINK+="ttyUSB-sh-main"
SUBSYSTEM=="tty",  ATTRS{idVendor}=="0403", ATTRS{idProduct}=="6010", ENV{ID_USB_INTERFACE_NUM}=="01",SYMLINK+="ttyUSB-sh-sub"
```

## test

```
./run.sh
```

