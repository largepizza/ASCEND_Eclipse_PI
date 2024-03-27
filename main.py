import numpy as np
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
    SYS_IDLE = 0  # The system is idle
    SYS_OK = 1  # The system is working correctly, heartbeat
    SYS_ERROR = 2  # The system has encountered an error
    SYS_REBOOT = 3  # The system is rebooting

class CameraState(IntEnum):
    PHOTO_OFF = 0  # The system is idle
    PHOTO_SUCCESS = 1  # The system has taken a photo
    PHOTO_ERROR = 2  # The system has failed to take a photo

class RtlState(IntEnum):
    RTL_INACTIVE = 0  # The rtl_record service is inactive
    RTL_ACTIVE = 1  # The rtl_record service is active
    RTL_FAIL = 2  # The rtl_record service has failed
    
    




# Objects
link = txfer.SerialTransfer('/dev/serial0')
picam2 = Picamera2()

# Globals
rate_between_pictures = 0.05  # Seconds

systemStatus = SystemState.SYS_IDLE
cameraStatus = CameraState.PHOTO_OFF
rtlStatus = RtlState.RTL_INACTIVE



def sendMessage():
    try:
        # get the current time
        now = datetime.now()

        

        # Get time as integers
        hour = now.hour
        minute = now.minute
        second = now.second

        # Send the status and message over 
        send_size = 0
        send_size = link.tx_obj(int(systemStatus), start_pos=send_size)
        send_size = link.tx_obj(int(cameraStatus), start_pos=send_size)
        send_size = link.tx_obj(int(rtlStatus), start_pos=send_size)
        send_size = link.tx_obj(int(hour), start_pos=send_size)
        send_size = link.tx_obj(int(minute), start_pos=send_size)
        send_size = link.tx_obj(int(second), start_pos=send_size)
        link.send(send_size)

    except Exception as e:
        print(f"Error in sending message: {e}")




def get_service_status():
    try:
        # Check the status of the rtl_record service
        result = subprocess.run(['systemctl', 'is-active', 'rtl_record.service'], capture_output=True, text=True)
        status = result.stdout.strip()  # Returns 'active', 'inactive', or 'failed'
        if status == 'active':
            rtlStatus = RtlState.RTL_ACTIVE
        elif status == 'inactive':
            rtlStatus = RtlState.RTL_INACTIVE
        elif status == 'failed':
            rtlStatus = RtlState.RTL_FAIL
        return rtlStatus
    except Exception as e:
        return str(e)
    




# Main function
if __name__ == "__main__":

    # Initialize UART link
    link.open()
    print("Serial port opened")

    #Initialize the camera



    # All good, start the main loop
    systemStatus = SystemState.SYS_OK

    try:
        while True:
            # Get the status of the rtl_record service
            rtlStatus = get_service_status()

            # Send the status message
            sendMessage()

            # Wait for a while before checking again
            time.sleep(1)
        

    except KeyboardInterrupt:
        print("Stopping")
        link.close()
