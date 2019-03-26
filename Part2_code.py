import numpy as np
import cv2
import os
from os import path, getcwd, chdir
import glob
import matplotlib.pyplot as plt

# reading the input video file
cap = cv2.VideoCapture('input2b_small.mp4')

leds = []

script_dir = os.path.dirname(__file__)

# Here we have the LED coordinates,fro example: we know that LED in this region is on so  this led is the fourth LED
Lcol = np.array([37,66,100,125,155,190,220,246,275,303,338,368,396,425,460,481,517,542,571,600,634,657,715,746,775])
Ucol = np.array([57,92,125,150,180,204,240,271,300,325,357,389,421,444,480,500,536,566,595,625,654,683,743,771,800])
Lrow = np.repeat(130,25)
Urow = np.repeat(157,25)

# Few settings for writing the the output video
fourcc = cv2.VideoWriter_fourcc(*'X264')
out = cv2.VideoWriter('NEW_2b_output.mp4',fourcc, 10.0, (int(cap.get(3)),int(cap.get(4))),isColor=1)


while(cap.isOpened()):
    ret, frame = cap.read()
    temp_frame = frame
    frame1 = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    # print(frame1.shape)
    # cv2.imshow("Just checking",frame1)
    ret,thresh1 = cv2.threshold(frame1,185,230,cv2.THRESH_BINARY)
    kernel = np.ones((4,4),np.uint8)
    eroded_frame = cv2.erode(thresh1,kernel)
    # cv2.imshow("eroded_frame",eroded_frame)

    # height, width = thresh1.shape[:2]

    # Below we are checking the LED regions if that location has a ON LED or not
    for p in range(25):
        # name = "led%d"%p
        kame = "LED%d"%p
        name = eroded_frame[Lrow[p]:Urow[p] , Lcol[p]:Ucol[p]]
        # cv2.waitKey()
        # cv2.imshow(kame,name)
        whiteOnes = cv2.countNonZero(name)
        # print(kame," ",whiteOnes)

        # So here we are confirming that an LED is "ON" by checking if the number of pixels glowing are greater than 38
        # Then if we find, we are going to place text above them
        if whiteOnes >=38:
            if p<19:
                cv2.putText(temp_frame,"1", (int((Lcol[p]+Ucol[p])/2)-15,Urow[p]+30), cv2.FONT_HERSHEY_SIMPLEX, 1.3, (0,0,255),3)
            else:
                cv2.putText(temp_frame,"1", (int((Lcol[p]+Ucol[p])/2)-15,Urow[p]+30), cv2.FONT_HERSHEY_SIMPLEX, 1.3, (0,255,0),3)
        else:
            if p<19:
                cv2.putText(temp_frame,"0", (int((Lcol[p]+Ucol[p])/2)-15,Urow[p]+30), cv2.FONT_HERSHEY_SIMPLEX, 1.3, (0,0,255),3)
            else:
                cv2.putText(temp_frame,"0", (int((Lcol[p]+Ucol[p])/2)-15,Urow[p]+30), cv2.FONT_HERSHEY_SIMPLEX, 1.3, (0,255,0),3)
    cv2.imshow("Final_Output",temp_frame)
    out.write(temp_frame)
    if cv2.waitKey(10) & 0xFF == ord('q'):
        break

# cv2.waitKey()

cap.release()
out.release()
cv2.destroyAllWindows()