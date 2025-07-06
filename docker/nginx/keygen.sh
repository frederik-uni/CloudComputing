#!/usr/bin/bash

mkdir nginx/keys
openssl req -x509 -nodes -days 365 \
  -newkey rsa:2048 \
  -keyout nginx/keys/privkey.pem \
  -out nginx/keys/fullchain.pem \
  -subj "/CN=localhost"