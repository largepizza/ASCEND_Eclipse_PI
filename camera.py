import time
from picamera2 import Picamera2

def take_time_lapse(interval, resolution=(2592, 1944)):
    # Initialize the camera
    picam2 = Picamera2()

    # Configure the camera
    config = picam2.create_still_configuration()
    config["main"]["size"] = resolution
    picam2.configure(config)
    picam2.start()
    # Start the preview (optional, comment out if not needed)
    # picam2.start_preview()

    try:
        count = 0
        while True:
            # Generate the filename based on the count
            filename = f"image_{count:04d}.jpg"
            
            # Capture the image
            picam2.capture_file(filename)
            print(f"Captured {filename}")
            
            # Wait for the specified interval before taking the next picture
            time.sleep(interval)
            
            # Increment the count
            count += 1
    except KeyboardInterrupt:
        # Stop the preview and close the camera if the user interrupts the process (e.g., by pressing Ctrl+C)
        print("Time-lapse stopped")
        #picam2.stop_preview()
        # No need to close in most recent Picamera2 versions, but if you need to release resources, do it here.

if __name__ == "__main__":
    # Define the rate between pictures in seconds
    rate_between_pictures = 0.05  # Change this to your desired interval
    
    # Start the time-lapse
    take_time_lapse(rate_between_pictures)
