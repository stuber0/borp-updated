from camera_feed import CameraFeed
import time

camera = CameraFeed()

try:
    while True:
        camera.capture_and_find_pink()
        time.sleep(0.1)  # Adjust the delay as needed
except KeyboardInterrupt:
    camera.clean_up()
