import numpy as np
import imutils
import math
import time
import cv2 

cap = cv2.VideoCapture(0)  		# Connect to camera 0 (or the only camera)
cap.set(3, 640)                     	# Set the width to 320
cap.set(4, 480)                     	# Set the height to 240
Center=np.array([])
f=3.04/(1.12*10**-3)
#img=cv2.imread("MultipleCovers.jpg")
sample_parameters={"hue":[0,4],"sat":[100,255],"value":[100,255],"Height":40,"OR_MASK":True,
"Kernel":True}
lander_parameters={"hue":[15,30],"sat":[100,255],"value":[100,255],"Height":570,"OR_MASK":False,
"Kernel":False}
obstacle_parameters={"hue":[40,70],"sat":[50,255],"value":[40,255],"Height":150,"OR_MASK":False,
"Kernel":False}
cover_parameters={"hue":[95,107],"sat":[60,255],"value":[0,255],"Height":70,"OR_MASK":False,
"Kernel":False}
def Detection(image,parameters_dict):
    #image=cv2.resize(image,(640,480))
    #cv2.imshow("normal",image)
    ogimg=image#store the image given as a parameter for later bitwise and operation
    image=cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    image=cv2.GaussianBlur(image, (17, 17), 2) 
    lower=np.array([parameters_dict["hue"][0],parameters_dict["sat"][0],parameters_dict["value"][0]])
    higher=np.array([parameters_dict["hue"][1],parameters_dict["sat"][1],parameters_dict["value"][1]])
    mask=cv2.inRange(image,lower,higher)
    if parameters_dict["OR_MASK"]==True:
        lower_oran=np.array([175,100,100],dtype="uint8") 
        higher_oran=np.array([179,255,255],dtype="uint8")
        mask1=cv2.inRange(image,lower_oran,higher_oran)
        mask=cv2.bitwise_or(mask,mask1)
    if parameters_dict["Kernel"]==True:
        Kernel=cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(3,3))
    else:
        Kernel=cv2.getStructuringElement(cv2.MORPH_RECT,(5,5))
    Thresholded_img=cv2.bitwise_and(ogimg,ogimg,mask=mask)
    filtered_img=cv2.morphologyEx(Thresholded_img,cv2.MORPH_OPEN,Kernel)
    return filtered_img
def Range(img,parameters_dict):
    Range=np.array([])
    ZDistance=np.array([])
    Bearing=np.array([])
    Center=np.array([])
    GrayFiltimg=cv2.cvtColor(img,cv2.COLOR_HSV2BGR)
    GrayFiltimg=cv2.cvtColor(GrayFiltimg,cv2.COLOR_RGB2GRAY)
    Contour=cv2.findContours(GrayFiltimg,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
    if Contour == []:
        print("there is no lander here")
    else:
        Contour=imutils.grab_contours(Contour)
        for a in Contour:
            #find the center of the contour
            Moment=cv2.moments(a)
            Area=cv2.contourArea(a)
            Lx=int(Moment["m10"]/Moment["m00"])
            Ly=int(Moment["m01"]/Moment["m00"])
            cv2.circle(img, (Lx, Ly), 7, (255, 255, 255), -1)
            Centroid=np.array([Lx,Ly])
            Center=np.append(Center,Centroid)
            Lx1,Ly1,LWidth,LHeight=cv2.boundingRect(a)
            Distance=parameters_dict["Height"]*(f/LHeight)/4
            ZDistance=np.append(ZDistance,Distance)
            Bearing=np.append(Bearing,(Lx-320)*(31.1/320))
            Range=np.vstack((ZDistance,Bearing)).T#Put Bearing and ZDistance into one array and arrange
            #columnwise
            Range=Range[Range[:,0].argsort()] 
            #if positive then it's to the right if negative then to left of center 
    #ZDistance=np.sort(ZDistance)   
    return Range
i=0
while True:
    try:
        t=time.time()
        ret, img = cap.read()	     		# Get a frame from the camera 
        if ret == True:	
               cv2.waitKey(1)	
        #initiate some variables
        if __name__=="__main__":
            sample_img=Detection(np.copy(img),sample_parameters)
            cover_img=Detection(np.copy(img),cover_parameters)
            obstacle_img=Detection(np.copy(img),obstacle_parameters)
            FinalImage=cv2.bitwise_or(sample_img,cover_img)
            FinalImage=cv2.bitwise_or(FinalImage,obstacle_img)
            sample_Z=Range(sample_img,sample_parameters)
            cover_Z=Range(cover_img,cover_parameters)
            #Bearing1=np.degrees(Bearing1)
            print(sample_Z)
            #print(Bearing1)
            i+=1
            if (i%5)==0:
                cv2.imshow("Binary Thresholded Frame",FinalImage)# Display thresholded frame
                cv2.waitKey(250)
                time.sleep(2)									# Exit on keypress
                cv2.destroyAllWindows()
            elapsed=time.time()-t
            if i>30:
                break
            print(elapsed)
    except KeyboardInterrupt:
        break
