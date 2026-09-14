#!/bin/bash

# openssl req -x509 -newkey rsa:4096 -keyout key.pem -out cert.pem -sha256 -days 365 -nodes -subj "/CN=localhost"

python -m pip install --upgrade pip
python -m pip install -r requirements.txt
python -m main
