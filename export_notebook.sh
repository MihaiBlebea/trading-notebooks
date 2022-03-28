#!/bin/bash

export PYTHONDONTWRITEBYTECODE=1
export PYTHONPATH="${PYTHONPATH}:${PWD}"
# eval "./env/bin/python3 -u ${1} ${@:2}"
./env/bin/jupyter nbconvert --execute --to html --template full --output-dir=./output ${1}