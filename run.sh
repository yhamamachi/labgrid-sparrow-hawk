#!/bin/bash

SCRIPT_DIR=$(cd `dirname $` && pwd)

# Setup python virtual environment
cd ${SCRIPT_DIR}
if [[ ! -e "${SCRIPT_DIR}/labgrid-venv" ]]; then
    python3 -m venv ${SCRIPT_DIR}/labgrid-venv
    source ${SCRIPT_DIR}/labgrid-venv/bin/activate
    pip install --upgrade pip
    pip install --upgrade labgrid
else
    source ${SCRIPT_DIR}/labgrid-venv/bin/activate
fi

# Run testsuite
cd ${SCRIPT_DIR}/yocto
#pytest --lg-env local.yaml --capture=no test_shell.py
pytest --lg-env local.yaml --capture=no test_release.py

