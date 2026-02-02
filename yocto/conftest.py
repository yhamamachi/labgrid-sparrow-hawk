import pytest

@pytest.fixture(scope="session")
def command(target):
    shell = target.get_driver("ShellDriver")
    target.activate(shell)
    return shell

@pytest.fixture(scope="session")
def uboot_command(target):
    shell = target.get_driver("UBootDriver")
    target.activate(shell)
    return shell

