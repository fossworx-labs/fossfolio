#!/bin/sh
chmod 755 *
apt-get update
sudo yum update
apt-get install python3
dnf install python3
pacman -S python3 
dnf install python3-pip
apt-get install python3-pip
pacman -Syu python-pip
pip install virtualenv
virtualenv venv 
source venv/bin/activate
pip install poetry 
poetry init
poetry install
cd fossfolio
python3 build.py
poetry init
poetry install
cd fossfolio
python build.py
