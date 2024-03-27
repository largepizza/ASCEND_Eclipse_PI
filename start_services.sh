#!/bin/bash

# Start the services
echo "Starting ascend.service and rtl_record.service..."
sudo systemctl start ascend.service
sudo systemctl start rtl_record.service
echo "Services started successfully."
