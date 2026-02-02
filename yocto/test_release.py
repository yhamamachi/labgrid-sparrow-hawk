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
