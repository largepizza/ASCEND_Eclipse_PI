from time import sleep
from pySerialTransfer import pySerialTransfer as txfer
import struct
import enum

class SystemState (enum.IntEnum):
    IDLE = 0 # The system is idle
    OK = 1 # The system is working correctly, heartbeat
    STAUS_ERROR = 2 # The system has encountered an error
    PHOTO_SUCCESS = 3 # The system has taken a photo
    PHOTO_ERROR = 4 # The system has failed to take a 
    
# Create a TX message class, containing SystemState
    

link = txfer.SerialTransfer('/dev/serial0')


if __name__ == "__main__":
    #Attempt to open the serial port

    state = SystemState.OK

    try:
        # Open the serial port
        link.open()
        print("Serial port opened")

        while True:
          
            
            # If SystemState is not IDLE, send heartbeat
            if state != SystemState.IDLE:

                heartbeat = 1
                
                send_size = link.tx_obj(heartbeat)
                link.send(send_size)
                print("Heartbeat sent")

            #delay for 0.5 seconds
            sleep(0.5)



    except KeyboardInterrupt:
        # Stop the preview and close the camera if the user interrupts the process (e.g., by pressing Ctrl+C)
        print("Experiment stopped")


