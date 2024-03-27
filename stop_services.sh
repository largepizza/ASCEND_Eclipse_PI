#!/bin/bash

# Stop the services
echo "Stopping ascend.service and rtl_record.service..."
sudo systemctl stop ascend.service
sudo systemctl stop rtl_record.service
echo "Services stopped successfully."
