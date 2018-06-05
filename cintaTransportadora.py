# import the necessary packages
from collections import deque
import serial
import numpy as np
import time
import argparse
import imutils
import cv2
import math
from arduino import Arduino

#Contador
countV = 0
countA = 0
firstV = False
flagV = False
firstA = False
flagA = False
mandaV=0
contadorRadio= 0
contadorLecturas=0
ard = Arduino()

# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-v", "--video",
	help="path to the (optional) video file")
ap.add_argument("-b", "--buffer", type=int, default=64,
	help="max buffer size")
args = vars(ap.parse_args())
# define the lower and upper boundaries of the "green"
# ball in the HSV color space, then initialize the
# list of tracked points
greenLower = (29, 86, 6)
greenUpper = (64, 255, 255)
yellowLower = (15, 100, 100)
yellowUpper = (25, 255, 255)
pts = deque(maxlen=args["buffer"])
 
# if a video path was not supplied, grab the reference
# to the webcam
if not args.get("video", False):
	camera = cv2.VideoCapture(0)
 
# otherwise, grab a reference to the video file
else:
	camera = cv2.VideoCapture(args["video"])

def cintaOff():
	#envio un caracter al arduino
	print("Apagando Cinta ...")

def cintaOn():
	#envio un caracter al arduino
	print("Encendiendo Cinta ...")
	

def tratarVerde():
	#envio un caracter al arduino
	print("Despachando Verde ...")
	ard.sendArduino(b'v')

def tratarAmarillo():
	#envio un caracter al arduino
	print("Despachando Amarillo ...")
	ard.sendArduino(b'a')

def volumen_esfera(radio):
    volumen=(4/3)*math.pi*radio**3
    return volumen

 #keep looping
while True:
	# grab the current frame
	(grabbed, frame) = camera.read()
 
	# if we are viewing a video and we did not grab a frame,
	# then we have reached the end of the video
	if args.get("video") and not grabbed:
		break

	# resize the frame, blur it, and convert it to the HSV
	# color space
	frame = imutils.resize(frame, width=1000)
	# blurred = cv2.GaussianBlur(frame, (11, 11), 0)
	hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
 
	# construct a mask for the color "green", then perform
	# a series of dilations and erosions to remove any small
	# blobs left in the mask
	mask = cv2.inRange(hsv, greenLower, greenUpper)
	mask = cv2.erode(mask, None, iterations=2)
	mask = cv2.dilate(mask, None, iterations=2)
	mask2 = cv2.inRange(hsv, yellowLower, yellowUpper)
	mask2 = cv2.erode(mask2, None, iterations=2)
	mask2 = cv2.dilate(mask2, None, iterations=2)
	# find contours in the mask and initialize the current
	# (x, y) center of the ball
	cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL,
		cv2.CHAIN_APPROX_SIMPLE)[-2]
	cnts2 = cv2.findContours(mask2.copy(), cv2.RETR_EXTERNAL,
		cv2.CHAIN_APPROX_SIMPLE)[-2]	
	center = None
	# print("Verde : ", len(cnts))
	# print("Amarillo : ", len(cnts2))
	# only proceed if at least one contour was found
	if len(cnts) > 0:
		# find the largest contour in the mask, then use
		# it to compute the minimum enclosing circle and
		# centroid
		c = max(cnts, key=cv2.contourArea)
		((x, y), radius) = cv2.minEnclosingCircle(c)
		M = cv2.moments(c)
		center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))
		# only proceed if the radius meets a minimum size
		if radius > 100:
			#print(str(radius))
			contadorRadio += radius
			contadorLecturas +=1
			flagV = True
			mandaV +=1
			if(mandaV == 1):
				tratarVerde()
			# draw the circle and centroid on the frame,
			# then update the list of tracked points
			cv2.circle(frame, (int(x), int(y)), int(radius),
			(113, 202, 0), 2)
			cv2.circle(frame, center, 5, (0, 0, 255), -1)
		elif (flagV == True):
			flagV = False
			firstV = True
	
	if len(cnts2) > 0:
		# find the largest contour in the mask, then use
		# it to compute the minimum enclosing circle and
		# centroid
		c = max(cnts2, key=cv2.contourArea)
		((x, y), radius) = cv2.minEnclosingCircle(c)
		M = cv2.moments(c)
		center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))
		# only proceed if the radius meets a minimum size
		if radius > 100:
			contadorRadio += radius
			contadorLecturas +=1
			flagA = True
			# draw the circle and centroid on the frame,
			# then update the list of tracked points
			cv2.circle(frame, (int(x), int(y)), int(radius),
				(0, 255, 255), 2)
			cv2.circle(frame, center, 5, (0, 0, 255), -1)
		elif (flagA == True):
			flagA = False
			firstA = True
	# update the points queue
	pts.appendleft(center)
	# loop over the set of tracked points
	for i in range(1, len(pts)):
		# if either of the tracked points are None, ignore
		# them
		if pts[i - 1] is None or pts[i] is None:
			continue
 
		# otherwise, compute the thickness of the line and
		# draw the connecting lines
		thickness = int(np.sqrt(args["buffer"] / float(i + 1)) * 2.5)
		#cv2.line(frame, pts[i - 1], pts[i], (0, 0, 255), thickness)
 
	# show the frame to our screen
	cv2.imshow("Frame", frame)
	key = cv2.waitKey(1) & 0xFF
 
	if( flagV == False and firstV == True):
		if(contadorLecturas>0):	
			firstV = False
			flagV = False
			countV =countV + 1
			radioP = (contadorRadio / contadorLecturas * 3)/132.8068571895002
			print("radio > " + str("%.2f" % radioP) + 'cm')
			print("volumen > " + str("%.2f" % volumen_esfera(radioP))+ 'cm^3')
			print("Verdes:",countV)
			contadorRadio =0
			contadorLecturas =0
			mandaV =0
			#tratarVerde()

	if( flagA == False and firstA == True):	
		if(contadorLecturas>0):	
			flagA = False
			firstA = False
			countA = countA + 1
			radioP = contadorRadio / contadorLecturas
			radioP = (radioP * 3)/132.8068571895002
			print("radio > " + str("%.2f" % radioP) + 'cm')
			print("volumen > " + str("%.2f" % volumen_esfera(radioP)) + 'cm^3')
			contadorRadio =0
			contadorLecturas =0
			print("Amarillo: ",countA)
			tratarAmarillo()
		
	# if the 'q' key is pressed, stop the loop
	if key == ord("q"):
		break
	if key == ord("s"):
		cintaOff()
	if key == ord("a"):
		cintaOn()

# cleanup the camera and close any open windows
camera.release()
cv2.destroyAllWindows()