import cv2
import numpy as np
from picamera2 import Picamera2

def setup_cameras():
    # Set up the two cameras
    camera1 = Picamera2(0)
    camera2 = Picamera2(1)
    
    config1 = camera1.create_still_configuration(main={"size": (640, 480)})
    config2 = camera2.create_still_configuration(main={"size": (640, 480)})
    
    camera1.configure(config1)
    camera2.configure(config2)
    
    camera1.start()
    camera2.start()
    
    return camera1, camera2

def capture_images(camera1, camera2):
    # Capture images from both cameras
    img1 = camera1.capture_array()
    img2 = camera2.capture_array()
    
    return cv2.cvtColor(img1, cv2.COLOR_RGB2GRAY), cv2.cvtColor(img2, cv2.COLOR_RGB2GRAY)

def compute_disparity(img1, img2):
    # Compute disparity map
    stereo = cv2.StereoBM_create(numDisparities=16, blockSize=15)
    disparity = stereo.compute(img1, img2)
    return disparity

def estimate_depth(disparity, baseline, focal_length):
    # Estimate depth from disparity
    depth = np.zeros(disparity.shape)
    depth[disparity > 0] = (focal_length * baseline) / disparity[disparity > 0]
    return depth

def main():
    # Camera parameters (you may need to adjust these)
    baseline = 0.1  # Distance between cameras in meters
    focal_length = 500  # Focal length of the cameras in pixels

    camera1, camera2 = setup_cameras()

    while True:
        img1, img2 = capture_images(camera1, camera2)
        
        disparity = compute_disparity(img1, img2)
        depth = estimate_depth(disparity, baseline, focal_length)
        
        # Normalize depth for display
        depth_normalized = cv2.normalize(depth, None, 0, 255, cv2.NORM_MINMAX)
        depth_display = cv2.applyColorMap(depth_normalized.astype(np.uint8), cv2.COLORMAP_JET)
        
        cv2.imshow('Depth Map', depth_display)
        
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    
    camera1.stop()
    camera2.stop()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()