#!/bin/bash
set -e

# install python
sudo apt install python3 python3-dev python3-pip python3-venv

python3 -m venv venv
source venv/bin/activate
pip install scikit-learn==1.7.1 pandas flask


# move files to right directory
mkdir models
mv *.pkl models
mkdir serving
mv flask-server_model.py serving
