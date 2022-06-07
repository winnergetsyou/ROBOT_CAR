# STEP: 1
# import all the header files required

import cv2
import os
import mediapipe 
import serial
import time
from handDetector import HandDetector

# STEP: 2
# Getting the video from webcam

cap = cv2.VideoCapture(0)

"""\
Use this below commands, if you want to receive video from IP_CAMERA via RSTP Protocol


RTSP_URL = 'rtsp://user_name:password@ip_address/channal'

RTSP_URL = 'rtsp://Tapo_cam1:958@192.168.180.150/stream1'
 
os.environ['OPENCV_FFMPEG_CAPTURE_OPTIONS'] = 'rtsp_transport;udp'
 
cap = cv2.VideoCapture(RTSP_URL, cv2.CAP_FFMPEG)

"""


# STEP: 3
# Calling mediapipe functions
# The mediapipe.solutions.hands is responsible for detecting your hand

Palm = mediapipe.solutions.hands
Real_Palm = Palm.Hands()

# Drawing_utils function will draw your hand on the screen, whenever hand appears
Draw_your_hand = mediapipe.solutions.drawing_utils




# STEP: 4
# CREATING A INFINITE LOOP, And adding the function that has to be performed repetively.


#while True:
#   success, img = cap.read()
#   What cap.read() returns is a boolean (True/False) and image content
#   cv2.imshow("Video", img)
#   if (cv2.waitKey(1) & 0xFF ==ord('q')):
#     break
# references:https://stackoverflow.com/questions/65535939/python-understanding-read-in-opencv#:~:text=What%20cap.read%20%28%29%20returns%20is%20a%20boolean%20%28True%2FFalse%29,tuple.%20This%20is%20why%20you%20get%20an%20error.

handDetector = HandDetector(min_detection_confidence=0.7)

while 1:
# Image Processing 
    sucess, image = cap.read()
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    results = Real_Palm.process(image)
   
#sucess, image = cap.read()
#Reference for Mediapipe
# MediaPipe References:https://google.github.io/mediapipe/solutions/hands.html



# This below part of work is taken from "https://medium.com/analytics-vidhya/mediapipe-fingers-counting-in-python-w-o-gpu-f9494439090c"
    handLandmarks = handDetector.findHandLandMarks(image=image, draw=True)
    count=0

    if(len(handLandmarks) != 0):
        #we will get y coordinate of finger-tip and check if it lies above middle landmark of that finger
        #details: https://google.github.io/mediapipe/solutions/hands

        if handLandmarks[4][3] == "Right" and handLandmarks[4][1] > handLandmarks[3][1]:       #Right Thumb
            count = count+1
        elif handLandmarks[4][3] == "Left" and handLandmarks[4][1] < handLandmarks[3][1]:       #Left Thumb
            count = count+1
        if handLandmarks[8][2] < handLandmarks[6][2]:       #Index finger
            count = count+1
        if handLandmarks[12][2] < handLandmarks[10][2]:     #Middle finger
            count = count+1
        if handLandmarks[16][2] < handLandmarks[14][2]:     #Ring finger
            count = count+1
        if handLandmarks[20][2] < handLandmarks[18][2]:     #Little finger
            count = count+1
    cv2.putText(image, str(count), (45, 375), cv2.FONT_HERSHEY_SIMPLEX, 5, (255, 0, 0), 25)
    print(count)
    cv2.imshow("Volume", image)
    cv2.waitKey(1)

    
'''
# Assiging finger and thumb co-ordinates according to Mediapipe
# These are the default co-ordinates for finger and thumb provided by mediapipe Library
finger_Coord = [(8, 6), (12, 10), (16, 14), (20, 18)]
thumb_Coord = (4,2)
if multiLandMarks:
        handList = []
        for handLms in multiLandMarks:
            mpDraw.draw_landmarks(image, handLms, mp_Hands.HAND_CONNECTIONS)
            for idx, lm in enumerate(handLms.landmark):
              h, w, c = image.shape
              cx, cy = int(lm.x * w), int(lm.y * h)
              handList.append((cx, cy))
            for point in handList:
              cv2.circle(image, point, 10, (255, 255, 0), cv2.FILLED)
            upCount = 0
            for coordinate in finger_Coord:
             if handList[coordinate[0]][1] < handList[coordinate[1]][1]:
                upCount += 1
            if handList[thumb_Coord[0]][0] > handList[thumb_Coord[1]][0]:
              upCount += 1
            cv2.putText(image, str(upCount), (150,150), cv2.FONT_HERSHEY_PLAIN, 12, (0,255,0), 12)
            print(upCount)
            
    cv2.imshow("lets print!", image)
    cv2.waitKey(1)
'''



