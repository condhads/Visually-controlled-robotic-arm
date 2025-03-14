import cv2
import numpy as np
from vision_module import VisionSystem
from arm_control import RoboticArm

class MainApp:
    def __init__(self):
        self.vision = VisionSystem()
        self.arm = RoboticArm()

    def run(self):
        try:
            while True:
                # Get visual input
                frame = self.vision.capture_frame()
                
                # Process visual data
                target_position = self.vision.detect_target(frame)
                
                # Control robotic arm
                if target_position is not None:
                    self.arm.move_to(target_position)
                
                # Display results
                self.vision.display_output(frame)
                
                # Check for exit condition
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
        finally:
            self.vision.cleanup()
            self.arm.cleanup()

if __name__ == '__main__':
    app = MainApp()
    app.run()