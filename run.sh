#!/bin/bash

echo "Command runned inside pipenv virtual environment"
pipenv run python3 run_script.py "$@"