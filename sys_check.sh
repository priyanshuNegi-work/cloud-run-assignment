#!/bin/bash

# --- PART 1: GATHER SYSTEM INFO ---
# We use '>' to create the file (or overwrite if it exists).
echo "--- System Report ---" > log.txt

# We use '>>' to APPEND (add to the bottom) of the file.
echo "Date and Time:" >> log.txt
date >> log.txt

echo "Disk Usage:" >> log.txt
df -h >> log.txt

echo "Current User:" >> log.txt
whoami >> log.txt

# --- PART 2: DIRECTORY CHECK ---
# 'if [ ! -d ... ]' translates to: "If the directory does NOT exist..."
if [ ! -d "deploy_app" ]; then
    echo "Creating deploy_app directory..."
    mkdir deploy_app
fi

# --- PART 3: MOVE THE FILE ---
echo "Moving log.txt to deploy_app..."
mv log.txt deploy_app/

echo "Script finished successfully."
