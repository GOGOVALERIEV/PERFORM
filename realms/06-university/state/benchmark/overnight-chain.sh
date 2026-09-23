#!/bin/bash
# wait for batch1 driver to finish, then run batch2
cd "C:/Users/User/Desktop/PERFORM/realms/06-university"
while tasklist | grep -q "python.exe"; do sleep 60; done
python -u scripts/run_benchmark.py --batch state/benchmark/batch2/papers.json > state/benchmark/batch2.log 2>&1
