#!/bin/bash

echo "Tests executed inside pipenv virtual environment"
rm -rf db_testing
pipenv run python3 -m unittest "$@"
rm -rf db_testing