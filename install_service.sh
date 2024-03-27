#!/bin/bash

# Define the source and destination paths
RTL_SOURCE_FILE="rtl_record.service"
ASCEND_SOURCE_FILE="ascend.service"

DESTINATION_PATH="/etc/systemd/system/"

# Check if the rtl source file exists
if [ ! -f "$RTL_SOURCE_FILE" ]; then
    echo "Error: $RTL_SOURCE_FILE does not exist."
    exit 1
fi

# Check if the ascend source file exists
if [ ! -f "$ASCEND_SOURCE_FILE" ]; then
    echo "Error: $ASCEND_SOURCE_FILE does not exist."
    exit 1
fi


# Copy the rtl service file to the systemd directory
echo "Copying $RTL_SOURCE_FILE to $DESTINATION_PATH"
sudo cp "$RTL_SOURCE_FILE" "${DESTINATION_PATH}${RTL_SOURCE_FILE}"

# Copy the ascend service file to the systemd directory
echo "Copying $ASCEND_SOURCE_FILE to $DESTINATION_PATH"
sudo cp "$ASCEND_SOURCE_FILE" "${DESTINATION_PATH}${ASCEND_SOURCE_FILE}"


# Reload systemd to recognize the new service
echo "Reloading systemd daemon..."
sudo systemctl daemon-reload

# Enable the rtl service to start on boot
echo "Enabling the $RTL_SOURCE_FILE service..."
sudo systemctl enable "$RTL_SOURCE_FILE"

# Enable the ascend service to start on boot
echo "Enabling the $ASCEND_SOURCE_FILE service..."
sudo systemctl enable "$ASCEND_SOURCE_FILE"

# Provide instructions to start the service now, if desired
echo "The service has been installed. To start the rtl service, run:"
echo "    sudo systemctl start $RTL_SOURCE_FILE"
echo "To start the ascend service, run:"
echo "    sudo systemctl start $ASCEND_SOURCE_FILE"
