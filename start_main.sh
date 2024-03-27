#!/bin/bash


# Get the current date and time for the unique file name
timestamp=$(date '+%Y-%m-%d_%H-%M-%S')

# Full path to where you want to store your log files
log_path="/home/eclipse/vlf/logs/"

# Create the log file with the current timestamp
log_file="${log_path}log_${timestamp}.txt"

# Activate the virtual environment
source /home/eclipse/vlf/ASCEND_Eclipse_PI/.venv/bin/activate

# Run Python script
nohup python /home/eclipse/vlf/ASCEND_Eclipse_PI/main.py > $log_file &