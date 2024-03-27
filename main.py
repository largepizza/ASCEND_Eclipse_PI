import numpy as np
import threading
import time
from datetime import datetime
from time import sleep
from pySerialTransfer import pySerialTransfer as txfer
import struct
from enum import IntEnum
import subprocess
from picamera2 import Picamera2


# Define the system state as per your existing code
class SystemState(IntEnum):
    IDLE = 0  # The system is idle
    OK = 1  # The system is working correctly, heartbeat
    ERROR = 2  # The system has encountered an error
    PHOTO_SUCCESS = 3  # The system has taken a photo
    PHOTO_ERROR = 4  # The system has failed to take a photo
    RTL_ACTIVE = 5  # The rtl_record service is active
    RTL_INACTIVE = 6  # The rtl_record service is inactive
    RTL_FAIL = 7  # The rtl_record service has failed
    REBOOT = 8  # The system is rebooting
    

# Globals
link = txfer.SerialTransfer('/dev/serial0')

def sendMessage(status):
    try:
        # get the current time
        now = datetime.now()

        

        # Get time as integers
        hour = now.hour()
        minute = now.minute()
        second = now.second()

        # Send the status and message over 
        send_size = 0
        send_size = link.tx_obj(int(status), start_pos=send_size)
        send_size = link.tx_obj(int(hour), start_pos=send_size)
        send_size = link.tx_obj(int(minute), start_pos=send_size)
        send_size = link.tx_obj(int(second), start_pos=send_size)
        link.send(send_size)

    except Exception as e:
        print(f"Error in sending message: {e}")




def check_service_status():
    try:
        # Check the status of the rtl_record service
        result = subprocess.run(['systemctl', 'is-active', 'rtl_record.service'], capture_output=True, text=True)
        return result.stdout.strip()  # Returns 'active', 'inactive', or 'failed'
    except Exception as e:
        return str(e)
    

# Function for sending heartbeat over UART
def send_heartbeat():
    try:
        while True:
            # Send a heartbeat message
            sendMessage(SystemState.OK )
            sleep(1)  # Delay between heartbeats
    except Exception as e:
        print(f"Error in heartbeat thread: {e}")

#Function to send the status of the rtl_record service
def send_rtl_status():
    try:
        while True:
            status = check_service_status()
            if status == 'active':
                sendMessage(SystemState.RTL_ACTIVE)
            elif status == 'inactive':
                sendMessage(SystemState.RTL_INACTIVE)
            elif status == 'failed':
                sendMessage(SystemState.RTL_FAIL)
            sleep(500)  # Delay between status checks
    except Exception as e:
        print(f"Error in rtl status thread: {e}")


# Main function
if __name__ == "__main__":

    # Initialize UART link
    link.open()
    print("Serial port opened")

    # Start the heartbeat thread
    heartbeat_thread = threading.Thread(target=send_heartbeat, args=())
    heartbeat_thread.start()

    # Start the rtl_record status thread
    rtl_status_thread = threading.Thread(target=send_rtl_status, args=())
    rtl_status_thread.start()

  

    try:
        # Wait for the threads to complete (they won't, so this waits forever until interrupted)
        heartbeat_thread.join()
        rtl_status_thread.join()

    except KeyboardInterrupt:
        print("Stopping threads and cleaning up...")
        link.close()
