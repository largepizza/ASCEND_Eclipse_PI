#!/bin/bash

# Define the source and destination paths
SOURCE_FILE="rtl_record.service"
DESTINATION_PATH="/etc/systemd/system/"

# Check if the source file exists
if [ ! -f "$SOURCE_FILE" ]; then
    echo "Error: $SOURCE_FILE does not exist."
    exit 1
fi

# Copy the service file to the systemd directory
echo "Copying $SOURCE_FILE to $DESTINATION_PATH"
sudo cp "$SOURCE_FILE" "${DESTINATION_PATH}${SOURCE_FILE}"

# Reload systemd to recognize the new service
echo "Reloading systemd daemon..."
sudo systemctl daemon-reload

# Enable the service to start on boot
echo "Enabling the $SOURCE_FILE service..."
sudo systemctl enable "$SOURCE_FILE"

# Provide instructions to start the service now, if desired
echo "The service has been installed. To start the service, run:"
echo "    sudo systemctl start $SOURCE_FILE"
