#!/bin/bash

# Exit in case of error
set -e

# Check OS
if [[ "$(uname -s)" == "Linux" ]]; then
        python3 -m venv .venv
        source .venv/bin/activate

elif [[ "$(uname -s)" == "Darwin" ]]; then
        python3 -m pip install virtualenv
        python3 -m virtualenv .venv
        source ./venv/bin/activate

elif [[ "$(uname -s)" == "CYGWIN"  || "$(uname -s)" == "MINGW"* ]]; then
        python -m venv .venv
        venv\Scripts\actuvate

else
        echo "Unknown OS"
fi

pip3 install --upgrade pip
pip3 install uv 

uv pip install .
