import numpy as np
from rtlsdr import RtlSdr
import threading
import time
from datetime import datetime
from time import sleep
from pySerialTransfer import pySerialTransfer as txfer
import struct
from enum import IntEnum




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
sdr = RtlSdr()

# Function for sending heartbeat over UART
def send_heartbeat():
    state = SystemState.OK  # Or update based on your system's status dynamically
    try:
        while True:
            if state != SystemState.IDLE:
                heartbeat = int(SystemState.OK)
                send_size = link.tx_obj(heartbeat)
                link.send(send_size)
                print("Heartbeat sent")
            sleep(0.5)  # Delay between heartbeats
    except Exception as e:
        print(f"Error in heartbeat thread: {e}")

# Function for capturing RTL-SDR samples
def capture_samples(sample_rate, duration_sec, interval_sec):
    try:
        while True:
            start_time = time.time()
            filename = datetime.now().strftime('sample_%Y-%m-%d_%H-%M-%S.npy')
            # Place captured samples in directory on SSD /media/eclipse/eclipse_data
            filename = "/media/eclipse/eclipse_data/" + filename
            num_samples = int(sample_rate * duration_sec)
            samples = sdr.read_samples(num_samples)
            np.save(filename, samples)
            print(f"RTL-SDR capture complete, saved as {filename}")
            elapsed_time = time.time() - start_time
            wait_time = max(interval_sec - elapsed_time, 0)

            # Send status over UART
            state = SystemState.RTL_SUCCESS
            send_size = link.tx_obj(state)
            link.send(send_size)
            
            
            time.sleep(wait_time)
    except Exception as e:
        print(f"Error in RTL-SDR capture thread: {e}")

# Main function
if __name__ == "__main__":
    # Configuration for RTL-SDR
    SAMPLE_RATE = 2.048e6
    CENTER_FREQ = 125e6
    DURATION_SEC = 60
    INTERVAL_SEC = 60

    # Initialize and configure the SDR
    sdr.sample_rate = SAMPLE_RATE
    sdr.center_freq = CENTER_FREQ
    sdr.freq_correction = 60
    sdr.gain = 'auto'

    # Initialize UART link
    link.open()
    print("Serial port opened")

    # Start the heartbeat thread
    heartbeat_thread = threading.Thread(target=send_heartbeat, args=())
    heartbeat_thread.start()

    # Start the RTL-SDR capture thread
    rtl_thread = threading.Thread(target=capture_samples, args=(SAMPLE_RATE, DURATION_SEC, INTERVAL_SEC))
    rtl_thread.start()

    try:
        # Wait for the threads to complete (they won't, so this waits forever until interrupted)
        heartbeat_thread.join()
        rtl_thread.join()
    except KeyboardInterrupt:
        print("Stopping threads and cleaning up...")
        sdr.close()
        link.close()
