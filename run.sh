#!/usr/bin/env bash

# This script configure & start this account

# specify the account
export FLASK_APP=advclick

# configure
export FLASK_ENT=development
export FLASK_DEBUG=True

# start account
flask run --host=0.0.0.0
#python -m flask run