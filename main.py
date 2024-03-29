import numpy as np
import time
from datetime import datetime
from time import sleep
from pySerialTransfer import pySerialTransfer as txfer
import struct
import threading
from enum import IntEnum
import subprocess
from picamera2 import Picamera2
import sys


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

    except:
        print(f"Error in sending message")




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
    except:
        print(f"Error in getting service status")
    

def UARTLinkThread():
    try:
        # Initialize UART link
        link.open()
        print("Serial port opened")


        # All good, start the main loop
        systemStatus = SystemState.SYS_OK

        while True:
            # Get the status of the rtl_record service
            rtlStatus = get_service_status()

            # Send the status message
            sendMessage()

            # Wait for a while before checking again
            time.sleep(1)
    except Exception as e:
        #Close the serial port and start again
        link.close()
        print(f"Error: {e}")
        print("Restarting the UART link thread in 2 seconds")
        time.sleep(2)
        UARTLinkThread()
        
#Camera thread
def CameraThread():
    try:
        # Initialize the camera
        picam2 = Picamera2()

        # Configure the camera
        config = picam2.create_still_configuration()
        config["main"]["size"] = (2592, 1944)
        picam2.configure(config)
        picam2.start()

        parentDirectory = "/home/eclipse/Pictures/"
        #Create unique directory for the current date and time
        currentDateTime = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        directory = parentDirectory + currentDateTime
        


        count = 0
        while True:
            # Generate the filename based on the count
            filename = f"{directory}/image_{count:06d}.jpg"

            # Capture the image
            try:
                picam2.capture_file(filename)
                cameraStatus = CameraState.PHOTO_SUCCESS
            except:
                cameraStatus = CameraState.PHOTO_ERROR


            # Wait for the specified interval before taking the next picture
            time.sleep(rate_between_pictures)

            # Increment the count
    except Exception as e:
        #Start the camera thread again in two seconds
        print(f"Error: {e}")
        print("Restarting the camera thread in 2 seconds")
        time.sleep(2)
        CameraThread()







# Main function
if __name__ == "__main__":

    print("Starting the system")
    # Start the UART link thread
    uart_thread = threading.Thread(target=UARTLinkThread)
    uart_thread.start()
    print("UART link thread started")

    # Start the camera thread
    camera_thread = threading.Thread(target=CameraThread)
    camera_thread.start()
    print("Camera thread started")

    try:
        uart_thread.join()
        camera_thread.join()
        
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

