import numpy as np
import cv2
import os
from os import path, getcwd, chdir
import glob
import matplotlib.pyplot as plt

num_cuts = []
leds = []

disp_status = np.repeat(0,8)

mod_cut_seq = np.array([0,3,7,6,4,5,2,1])
led_status = np.repeat(0,25)

cap = cv2.VideoCapture('input2c_small.mp4')

script_dir = os.path.dirname(__file__)
rel_path = "modified_num_cuts/*.jpg"
abs_file_path = os.path.join(script_dir, rel_path)

files = glob.glob (abs_file_path)

total_cuts = 0

for myFile in files:
    image = cv2.imread(myFile,0)
    kernel = np.ones((3,3),np.uint8)
    eroded_frame = cv2.erode(image,kernel)
    ret,thresh2 = cv2.threshold(eroded_frame,185,230,cv2.THRESH_BINARY)
    # cv2.imshow("Edoded 7", eroded_frame)
    num_cuts.append (thresh2)
    total_cuts+=1

# Here we have the LED coordinates,fro example: we know that LED in this region is on so  this led is the fourth LED
Lcol = np.array([37,66,100,125,155,190,220,246,275,303,338,368,396,425,460,481,517,542,571,600,634,657,715,746,775])
Ucol = np.array([57,92,125,150,180,204,240,271,300,325,357,389,421,444,480,500,536,566,595,625,654,683,743,771,800])
Lrow = np.repeat(130,25)
Urow = np.repeat(157,25)



# Here we have the seven segment display coordinates, so that we can black those regions once we haveread the info from that area
disp_Lcol = np.array([33,62,131,163,248,283,315,344])
disp_Ucol = np.array([61,95,161,200,282,314,345,384])
disp_Lrow = np.repeat(60,8)
disp_Urow = np.repeat(115,8)

disp_Lrow[7] = 56
disp_Urow[7] = 119

# Few settings for writing the the output video
fourcc = cv2.VideoWriter_fourcc(*'X264')
out = cv2.VideoWriter('2c_output.mp4',fourcc, 20.0, (int(cap.get(3)),int(cap.get(4))),isColor=1)
frame_num=0

while(cap.isOpened()):
    ret, frame = cap.read()
    # temp_frame = frame
    temp_frame = frame
    led_status = np.repeat(0,25)
    
    frame1 = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    # print(frame1.shape)
    # cv2.imshow("Just checking",frame1)
    ret,thresh1 = cv2.threshold(frame1,185,230,cv2.THRESH_BINARY)
    kernel_c = np.ones((4,4),np.uint8)
    eroded_frame_c = cv2.erode(thresh1,kernel_c)
    disp_status = np.repeat(0,8)
    # temp_frame = thresh1


    # Below we are checking the LED regions if that location has a ON LED or not
    for p in range(25):
        # name = "led%d"%p
        kame = "LED%d"%p
        name_c = eroded_frame_c[Lrow[p]:Urow[p] , Lcol[p]:Ucol[p]]
        # cv2.waitKey()
        # cv2.imshow(kame,name)
        whiteOnes = cv2.countNonZero(name_c)
        # print(kame," ",whiteOnes)

        # So here we are confirming that an LED is "ON" by checking if the number of pixels glowing are greater than 38
        # Then if we find, we are going to place text above them
        if whiteOnes >=38:
            # led_status[p,frame_num]=1
            led_status[p]=1
            if p<19:
                cv2.putText(temp_frame,"1", (int((Lcol[p]+Ucol[p])/2)-15,Urow[p]+30), cv2.FONT_HERSHEY_SIMPLEX, 1.3, (0,0,255),3)
            else:
                cv2.putText(temp_frame,"1", (int((Lcol[p]+Ucol[p])/2)-15,Urow[p]+30), cv2.FONT_HERSHEY_SIMPLEX, 1.3, (0,255,0),3)
        else:
            # if p in range(6) or range(11,18,1) or range(21,22,1) or range(24,25,1):
            #     print("Hello i am 0 at ",p)
            if p<19:
                cv2.putText(temp_frame,"0", (int((Lcol[p]+Ucol[p])/2)-15,Urow[p]+30), cv2.FONT_HERSHEY_SIMPLEX, 1.3, (0,0,255),3)
            else:
                cv2.putText(temp_frame,"0", (int((Lcol[p]+Ucol[p])/2)-15,Urow[p]+30), cv2.FONT_HERSHEY_SIMPLEX, 1.3, (0,255,0),3)

    # Here we are going to "WRITE" the led values that we have read into a .txt file, here "p2c_output.txt"
    for d in range(25):
        if d in range(0,6,1):
            with open('./p2c_output.txt', 'a') as f1:
                if d==5:
                    content = "%d\t"%led_status[d]
                else:
                    content = "%d"%led_status[d]
                f1.write(content)
        elif d in range(10,18,1):
            with open('./p2c_output.txt', 'a') as f1:
                if d==17:
                    content = "%d\t"%led_status[d]
                else:
                    content = "%d"%led_status[d]
                f1.write(content)
        elif d in range(20,22,1):
            with open('./p2c_output.txt', 'a') as f1:
                if d==21:
                    content = "%d\t"%led_status[d]
                else:
                    content = "%d"%led_status[d]
                f1.write(content)
        elif d in range(23,25,1):
            with open('./p2c_output.txt', 'a') as f1:
                if d==24:
                    content = "%d\t"%led_status[d]
                    f1.write(content)
                else:
                    content = "%d"%led_status[d]
                    f1.write(content)





    for i in range(total_cuts):

        # Here we are eroding the Binary frame with the cutouts of numbers we have
        eroded_fullimg = cv2.erode(thresh1,num_cuts[i],iterations = 1)

        # Checking if the the result of eroding a image resulted in any white left over (Which implies that we have found that number cutout in that region)
        if np.any(eroded_fullimg != 0):
            # print("Hello I have found white dots on the eroded image")

            # From here we are checking at which region we have found the number_cutout "i" , to do this we ar eusing disp_Lcol, disp_Ucol, disp_Lrow and disp_Urow that we have defined above
            for h in range(8):
                tame = eroded_fullimg[disp_Lrow[h]:disp_Urow[h] , disp_Lcol[h]:disp_Ucol[h]]
                # cv2.waitKey()
                # cv2.imshow(kame,name)
                whiteOnes_1 = cv2.countNonZero(tame)
                if whiteOnes_1 !=0:

                    disp_status[h] = mod_cut_seq[i]

                    # Below we are trying to get the connected components of the blobs from the eroded image
                    cc_output = cv2.connectedComponentsWithStats(eroded_fullimg)

                    # Here we are trying to find the centroids of the blobs so that we can place our text above them
                    centroids = cc_output[3]
                    rows,cols = centroids.shape

                    # Here we are writing the number that we found above certain distance from centroid
                    for j in range(rows):
                        if centroids[j,0]<392:
                            num_name = "%d"%mod_cut_seq[i]
                            # frame[int(centroids[j,1]-35):int(centroids[j,1])-25,int(centroids[j,0]):int(centroids[j,0])+20] = 255
                            cv2.putText(temp_frame,num_name, (int(centroids[j,0]-17),int(centroids[j,1]-36)), cv2.FONT_HERSHEY_SIMPLEX, 1.3, (0,255,0),4)
                        thresh1[disp_Lrow[h]:disp_Urow[h] , disp_Lcol[h]:disp_Ucol[h]]=0

    # for b in range(8):
    #     print(disp_status[b])

    # Here I am storing the Seven segment display values into .txt file ("p2c_output.txt")
    for v in range(8):
        if v in range(0,4,1):
            with open('./p2c_output.txt', 'a') as f1:
                if v==3:
                    content = "%d\t"%disp_status[v]
                else:
                    content = "%d"%disp_status[v]
                f1.write(content)
        elif v in range(4,8,1):
            with open('./p2c_output.txt', 'a') as f1:
                if v==7:
                    content = "%d"%disp_status[v]
                    f1.write(content + os.linesep)
                else:
                    content = "%d"%disp_status[v]
                    f1.write(content)
    
    
    # frame_num+=1
    # cv2.waitKey()
# plt.show()
    
    
    
    cv2.imshow('frame',temp_frame)
    

    out.write(temp_frame)

    if cv2.waitKey(10) & 0xFF == ord('q'):
        break
 



cap.release()
out.release()
cv2.destroyAllWindows()