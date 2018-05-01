#!/bin/bash

sqldb/cleanDb.py testing
echo "Tests executed inside pipenv virtual environment"
pipenv run python3 -m unittest "$@"