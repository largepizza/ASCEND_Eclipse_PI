#!/bin/bash
# Define the base path for your IQ files and ensure the directory exists
BASE_PATH="/media/eclipse/eclipse_data/IQ"
mkdir -p "$BASE_PATH"

# Create a unique filename using the date and time
# Format: YYYYMMDD_HHMMSS (Year, Month, Day, Hours, Minutes, Seconds)
FILENAME="$(date +%Y%m%d_%H%M%S).bin"
IQ_FILE="${BASE_PATH}/${FILENAME}"

# Record IQ data using rtl_sdr
FREQUENCY=126020000  # 125Mhz + half of the bandwidth
SAMPLE_RATE=2048000  # Set to 2048000 for 2.048 MHz
rtl_sdr -d 0 -f $FREQUENCY -s $SAMPLE_RATE -g 0 - > $IQ_FILE
