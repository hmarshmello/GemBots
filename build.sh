#!/bin/bash

# Exit on error
set -e

# Print commands
set -x

# Install Python
curl -L https://raw.githubusercontent.com/pyenv/pyenv-installer/master/bin/pyenv-installer | bash
export PATH="$HOME/.pyenv/bin:$PATH"
eval "$(pyenv init -)"
eval "$(pyenv virtualenv-init -)"

# Install Python 3.11
pyenv install 3.11
pyenv global 3.11

# Upgrade pip and install dependencies
python -m pip install --upgrade pip
pip install -r requirements.txt

# Install Node.js dependencies
npm install
