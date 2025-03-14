import cv2
import numpy as np

class VisionSystem:
    def __init__(self):
        self.cap = cv2.VideoCapture(0)
        if not self.cap.isOpened():
            raise Exception('Could not open video device')

    def capture_frame(self):
        ret, frame = self.cap.read()
        if not ret:
            raise Exception('Failed to capture frame')
        return frame

    def detect_target(self, frame):
        # Convert to HSV color space
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        
        # Define color range for target detection
        lower_bound = np.array([30, 150, 50])
        upper_bound = np.array([255, 255, 180])
        
        # Create mask and find contours
        mask = cv2.inRange(hsv, lower_bound, upper_bound)
        contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        
        # Find largest contour
        if len(contours) > 0:
            largest_contour = max(contours, key=cv2.contourArea)
            M = cv2.moments(largest_contour)
            if M['m00'] != 0:
                cx = int(M['m10']/M['m00'])
                cy = int(M['m01']/M['m00'])
                return (cx, cy)
        return None

    def display_output(self, frame):
        cv2.imshow('Frame', frame)

    def cleanup(self):
        self.cap.release()
        cv2.destroyAllWindows()