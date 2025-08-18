#!/bin/bash

> successful_pins.txt  # Clear/create output file

# Function to test a single PIN
test_pin() {
    local pin=$1
    local output=$(echo -e "$pin\n" | python3 /Users/testing/Downloads/HackTheVault-main/__pycache__/CyberGate1.cpython-312.pyc)
    
    # Check if the output contains success indicators
    if echo "$output" | grep -q "ACCESS GRANTED\|SUCCESS\|WELCOME" && ! echo "$output" | grep -q "DENIED"; then
        echo "Success with PIN: $pin"
        echo "PIN: $pin" >> successful_pins.txt
        echo "$output" >> successful_pins.txt
        return 0
    fi
    return 1
}

# Use GNU Parallel if available (much faster)
if command -v parallel > /dev/null; then
    echo "Using parallel processing..."
    # Generate all PINs and process them in parallel
    seq -f "%04g" 0 9999 | parallel -j $(nproc || sysctl -n hw.ncpu) "pin={}; output=\$(echo -e \"\$pin\n\" | python3 /Users/testing/Downloads/HackTheVault-main/__pycache__/CyberGate1.cpython-312.pyc); if echo \"\$output\" | grep -q \"ACCESS GRANTED\|SUCCESS\|WELCOME\" && ! echo \"\$output\" | grep -q \"DENIED\"; then echo \"Success with PIN: \$pin\"; echo \"PIN: \$pin\" >> successful_pins.txt; echo \"\$output\" >> successful_pins.txt; fi"
else
    # Try a smarter approach - check common PINs first
    echo "Trying common PINs first..."
    common_pins=("1234" "0000" "1111" "9999" "1212" "7777" "1004" "2000" "4321" "2222" "6969" "1122" "1313" "2001" "1010" "2580" "1998" "2468" "0420" "1337")
    
    for pin in "${common_pins[@]}"; do
        echo "Trying common PIN: $pin"
        if test_pin "$pin"; then
            exit 0  # Exit if we find a match
        fi
    done
    
    echo "Trying birth year PINs..."
    # Try years (popular birth years as PINs)
    for year in {1950..2023}; do
        pin="${year:2:4}"  # Last two digits of year
        echo "Trying year PIN: $pin"
        if test_pin "$pin"; then
            exit 0
        fi
    done
    
    echo "Trying sequential brute force..."
    # If we haven't found anything, try a sequential approach but with visual feedback
    for i in {0..9}; do
        echo "Progress: ${i}0% complete"
        for j in {0..9}; do
            for k in {0..9}; do
                for l in {0..9}; do
                    pin="${i}${j}${k}${l}"
                    # Print progress every 100 attempts
                    if (( ($j*$k*$l) % 100 == 0 )); then
                        echo -ne "Trying PIN: $pin\r"
                    fi
                    if test_pin "$pin"; then
                        exit 0
                    fi
                done
            done
        done
    done
fi

echo "No successful PIN found"
