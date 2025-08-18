#!/bin/bash

for inpu in inputs.txt; do
    (cat $inpu; echo "") | python3 /Users/testing/Downloads/HackTheVault-main/__pycache__/CyberGate1.cpython-312.pyc >> outputs.txt
done
