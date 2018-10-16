#!/usr/bin/env bash

# ATTENTION: This script would drop all tables, no calling if necessary !!!
# It's your responsibility for data loss when calling this script.

# specify the account
export FLASK_APP=advclick
flask init_db