import time

def test_power_on_board(target):
    power = target.get_driver('PowerProtocol', name="NanoKVM-1")
    # Force reset
    power.off()
    time.sleep(1)
    power.on()


def test_can(command):
    cmd = """
    ip link set can0 up type can restart-ms 100 bitrate 1000000 dbitrate 5000000 fd on
    ip link set can1 up type can restart-ms 100 bitrate 1000000 dbitrate 5000000 fd on
    timeout 10 candump can0 -n 16 &
    PID=$!
    sleep 0.2
    cangen can1 -I i -L i -D i -f -n 16
    wait $PID

    timeout 10 candump can1 -n 16 &
    PID=$!
    sleep 0.2
    cangen can0 -I i -L i -D i -f -n 16
    wait $PID
    """
    stdout, stderr, returncode = command.run(cmd)
    assert returncode == 0
    assert "  can0  00A  [16]  0A 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00" in stdout
    assert "  can1  00A  [16]  0A 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00" in stdout


def test_ethernet(command):
    cmd = """
    ping 1.1.1.1 -c 4
    """
    stdout, stderr, returncode = command.run(cmd)
    assert returncode == 0


def test_audio(command):
    cmd = """
    amixer set "Headphone" 40%
    amixer set "Headphone" on
    amixer set "Mixout Left DAC Left" on
    amixer set "Mixout Right DAC Right" on
    amixer set "Aux" on
    amixer set "Aux" 80%
    amixer set "Mixin PGA" on
    amixer set "Mixin PGA" 50%
    amixer set "ADC" on
    amixer set "ADC" 80%
    amixer set "Mixin Left Aux Left" on
    amixer set "Mixin Right Aux Right" on
    amixer set "Mic 1" on
    amixer set "Mic 1" 80%
    amixer set "Mixin Left Mic 1" on
    amixer set "Mixin Right Mic 1" on

    arecord -D hw:0,0 -t wav -c 2 -d 5 -r 48000 -f S16_LE | aplay
    """
    stdout, stderr, returncode = command.run(cmd)
    assert returncode == 0


def test_displayport(command):
    cmd = """
    ls /sys/class/drm/card0-DP-1 >/dev/null
    cat /sys/class/drm/card0-DP-1/connector_id
    """
    stdout, stderr, returncode = command.run(cmd)
    assert returncode == 0


def test_i2c(command):
    cmd = """
    i2cdetect -r -y 0
    i2cdetect -r -y 1
    i2cdetect -r -y 2
    i2cdetect -r -y 3
    i2cdetect -r -y 4
    """
    stdout, stderr, returncode = command.run(cmd)
    assert returncode == 0


def test_i2c(command):
    cmd = """
    stty -F /dev/ttySC2 -echo
    cat /dev/ttySC2 &
    sleep 0.2
    echo Hello > /dev/ttySC2
    sleep 2
    killall cat
    """
    stdout, stderr, returncode = command.run(cmd)
    assert returncode == 0
    assert "Hello" in stdout


def test_thermal(command):
    cmd = """
    for i in `seq 10`; do \
        cat /sys/class/thermal/thermal_zone*/temp; \
        sleep 1s; \
    done
    """
    stdout, stderr, returncode = command.run(cmd)
    assert returncode == 0


def test_picamera(command):
    cmd = """
    cam -l
    timeout 10 cam -c 1 --capture=30 --file=/dev/null
    timeout 10 cam -c 2 --capture=30 --file=/dev/null
    """
    stdout, stderr, returncode = command.run(cmd)
    assert returncode == 0
    assert "1: External camera 'imx219' (/base/soc/i2c@e6508000/cam@10)" in stdout
    assert "2: External camera 'imx708' (/base/soc/i2c@e6510000/sensor@1a)" in stdout


def test_pidisplay(command):
    cmd = """
    ls /sys/class/drm/card0-DSI-1 >/dev/null
    cat /sys/class/drm/card0-DSI-1/connector_id
    """
    stdout, stderr, returncode = command.run(cmd)
    assert returncode == 0


def test_pwm(command):
    cmd = """
    echo 2 > /sys/class/hwmon/hwmon4/pwm1_enable
    echo 150 > /sys/class/hwmon/hwmon4/pwm1
    sleep 10
    echo 255 > /sys/class/hwmon/hwmon4/pwm1
    """
    stdout, stderr, returncode = command.run(cmd)
    assert returncode == 0


def test_pcie(command):
    cmd = """
    lspci
    """
    stdout, stderr, returncode = command.run(cmd)
    assert returncode == 0
    assert "0000:00:00.0 PCI bridge: Renesas Technology Corp. Device 0030" in stdout
    assert "0000:01:00.0 USB controller: Renesas Technology Corp. uPD720201 USB 3.0 Host Controller (rev 03)" in stdout
    assert "0001:00:00.0 PCI bridge: Renesas Technology Corp. Device 0030" in stdout


def test_usb(command):
    cmd = """
    lsusb
    """
    stdout, stderr, returncode = command.run(cmd)
    assert returncode == 0
    assert "Bus 001 Device 001: ID 1d6b:0002 Linux Foundation 2.0 root hub" in stdout
    assert "Bus 002 Device 001: ID 1d6b:0003 Linux Foundation 3.0 root hub" in stdout


def test_shell(command):
    stdout, stderr, returncode = command.run("cat /proc/version")
    assert returncode == 0
    assert stdout
    assert not stderr
    assert "Linux" in stdout[0]

    stdout, stderr, returncode = command.run("false")
    assert returncode != 0
    assert not stdout
    assert not stderr
