#!/bin/bash
# Benchmark runner script

cd "$(dirname "$0")/.."
PYTHONPATH="$PWD/src" ./venv/bin/python src/benchmark.py "$@"
