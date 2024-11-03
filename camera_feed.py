from picamera2 import Picamera2
import cv2
import numpy as np

class CameraFeed:
    def __init__(self):
        # Initialize the camera
        self.picam2 = Picamera2()
        self.config = self.picam2.create_video_configuration(main={"size": (480, 480)})
        self.picam2.configure(self.config)
        self.picam2.start()
        
        # Define HSV range for fluorescent pink
        self.lower_pink = np.array([140, 150, 50])
        self.upper_pink = np.array([180, 255, 255])

    def capture_and_find_ball(self):
            # Capture image
            image = self.picam2.capture_array()
            # Convert to HSV color space
            hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
            # Create mask for pink color
            mask = cv2.inRange(hsv_image, self.lower_pink, self.upper_pink)
            # Find contours in the mask
            contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
            
            if contours:
                largest_contour = max(contours, key=cv2.contourArea)
                (x, y), radius = cv2.minEnclosingCircle(largest_contour)
                if cv2.contourArea(largest_contour) > 200:
                    # Draw circle around detected pink object
                    cv2.circle(image, (int(x), int(y)), int(radius), (0, 255, 0), 2)
            
            cv2.imshow("Detected Object", image)
            cv2.waitKey(1)

    def shut_down(self):
        self.picam2.stop()
        cv2.destroyAllWindows()


