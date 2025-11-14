#!/bin/bash
# Benchmark analysis script

cd "$(dirname "$0")/.."
PYTHONPATH="$PWD/src" ./venv/bin/python src/analyze_benchmark.py "$@"
