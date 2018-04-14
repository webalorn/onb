#!/bin/bash

echo "Tests executed inside pipenv virtual environment"
pipenv run python3 -m unittest "$@"