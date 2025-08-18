#!/bin/bash

> output_all_pins.txt  # Clear/create output file

for pin in {0000..9999}; do
    echo "Trying PIN: $pin"
    (echo $pin; echo "") | python3 /Users/testing/Downloads/HackTheVault-main/__pycache__/CyberGate1.cpython-312.pyc > temp_output.txt
    
    # Check if the output contains "ACCESS GRANTED" or similar success message
    if grep -q "ACCESS GRANTED\|SUCCESS\|WELCOME" temp_output.txt; then
        echo "Success with PIN: $pin"
        cat temp_output.txt
        echo "PIN: $pin" >> successful_pins.txt
        cat temp_output.txt >> successful_pins.txt
    fi
done
