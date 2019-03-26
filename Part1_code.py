import numpy as np
import cv2
import os
from os import path, getcwd, chdir
import glob

num_cuts = []

disp_status = np.repeat(0,8)

# The order in the modified_num_cuts is not labbeled respectively "name of file" with "image/file content"
# So to match up the files loaded with their respective content i have made this "mod_cut_seq"
mod_cut_seq = np.array([0,3,7,6,4,5,2,1])

# reading the input video file
cap = cv2.VideoCapture('input2a_small.mp4')

# Here we are setting up the file paths and files contains the file path for all the .jpg files in "modified_num_cuts"
script_dir = os.path.dirname(__file__)
rel_path = "modified_num_cuts/*.jpg"
abs_file_path = os.path.join(script_dir, rel_path)

files = glob.glob (abs_file_path)

total_cuts = 0

# Here we have the seven segment display coordinates, so that we can black those regions once we haveread the info from that area
disp_Lcol = np.array([33,62,131,163,248,283,315,344])
disp_Ucol = np.array([61,95,161,200,282,314,345,384])
disp_Lrow = np.repeat(60,8)
disp_Urow = np.repeat(115,8)

disp_Lrow[7] = 56
disp_Urow[7] = 119

 
# Here we are loading all the .jpg images from "modified_num_cuts" temporarily to image and then to do some operation and hten save into "num_cuts"
for myFile in files:
    image = cv2.imread(myFile,0)
    if  total_cuts == 1:
        kernel = np.ones((4,4),np.uint8)
    else:
        kernel = np.ones((3,3),np.uint8)
    eroded_frame = cv2.erode(image,kernel)
    ret,thresh2 = cv2.threshold(eroded_frame,185,230,cv2.THRESH_BINARY)
    # cv2.imshow("Edoded 7", eroded_frame)
    num_cuts.append (thresh2)
    total_cuts+=1

# Few settings for writing the the output video
fourcc = cv2.VideoWriter_fourcc(*'X264')
out = cv2.VideoWriter('NEW_p2a_output.mp4',fourcc, 10.0, (int(cap.get(3)),int(cap.get(4))),isColor=1)


while(cap.isOpened()):
    ret, frame = cap.read()
    
    frame1 = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    # print(frame1.shape)
    # cv2.imshow("Just checking",frame1)
    ret,thresh1 = cv2.threshold(frame1,185,230,cv2.THRESH_BINARY)
    temp_frame = thresh1

    disp_status = np.repeat(0,8)
    # print(thresh1.shape)

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
                    # print(disp_status[h],"  ",h)

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
                            cv2.putText(frame,num_name, (int(centroids[j,0]-17),int(centroids[j,1]-36)), cv2.FONT_HERSHEY_SIMPLEX, 1.3, (0,255,0),4)
                        thresh1[disp_Lrow[h]:disp_Urow[h] , disp_Lcol[h]:disp_Ucol[h]]=0

    cv2.imshow('frame',frame)
    

    out.write(frame)

    if cv2.waitKey(10) & 0xFF == ord('q'):
        break
 



cap.release()
out.release()
cv2.destroyAllWindows()