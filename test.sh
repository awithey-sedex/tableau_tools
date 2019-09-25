#! /bin/bash

set -e

python -m venv .venv

. .venv/bin/activate

python -m unittest discover
