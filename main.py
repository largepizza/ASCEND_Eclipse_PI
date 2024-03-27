import numpy as np
import threading
import time
from datetime import datetime
from time import sleep
from pySerialTransfer import pySerialTransfer as txfer
import struct
from enum import IntEnum
import subprocess



# Define the system state as per your existing code
class SystemState(IntEnum):
    IDLE = 0  # The system is idle
    OK = 1  # The system is working correctly, heartbeat
    STATUS_ERROR = 2  # The system has encountered an error
    PHOTO_SUCCESS = 3  # The system has taken a photo
    PHOTO_ERROR = 4  # The system has failed to take a photo
    RTL_SUCCESS = 5  # The system has successfully received data from the RTL-SDR
    RTL_ERROR = 6  # The system has failed to receive data from the RTL-SDR
    RTL_RESET = 7  # The system has reset the RTL-SDR

# Globals
link = txfer.SerialTransfer('/dev/serial0')

def sendMessage(status, message = ' '):
    try:
        # get the current time
        now = datetime.now()
        current_time = now.strftime("%H,%M,%S,")

        #combine the timestamp and message
        buffer = current_time + message
        # Send the status and message over 
        send_size = 0
        send_size = link.tx_obj(int(status), start_pos=send_size)
        send_size = link.tx_obj(buffer, start_pos=send_size)
        link.send(send_size)
        print("Message sent")
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
    state = SystemState.OK  # Or update based on your system's status dynamically
    try:
        while True:
            if state != SystemState.IDLE:
                sendMessage(state, check_service_status())
                #print("Heartbeat sent")
            sleep(0.5)  # Delay between heartbeats
    except Exception as e:
        print(f"Error in heartbeat thread: {e}")



# Main function
if __name__ == "__main__":

    # Initialize UART link
    link.open()
    print("Serial port opened")

    # Start the heartbeat thread
    heartbeat_thread = threading.Thread(target=send_heartbeat, args=())
    heartbeat_thread.start()

  

    try:
        # Wait for the threads to complete (they won't, so this waits forever until interrupted)
        heartbeat_thread.join()

    except KeyboardInterrupt:
        print("Stopping threads and cleaning up...")
        link.close()
