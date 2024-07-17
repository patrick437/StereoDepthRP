#!/usr/bin/python3q

import cv2
from  picamera2 import Picamera2
import time


def createCamera(cam_number):
	picam = Picamera2(cam_number)
	picam.start()
	time.sleep(2) #Allow camera time to warm up
	return picam

def captureGreyImage(picam):
	im = picam.capture_array()
	grey = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
	return grey


	
def main():
	cv2.startWindowThread()#start threading in the main loop rather then the function

	picam1 = createCamera(0)
	picam2 = createCamera(1)

	while True:
		grey1 = captureGreyImage(picam1)
		grey2 = captureGreyImage(picam2)

		cv2.imshow("Camera 1", grey1)
		cv2.imshow("Camera 2", grey2)	

		if cv2.waitKey(1) & 0xFF == ord('q'):
			break

	picam1.stop()
	picam2.stop()	
	cv2.destroyAllWindows()

if __name__ == "__main__":
	main()
	
	
