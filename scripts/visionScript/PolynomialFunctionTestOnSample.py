import numpy as np
import imutils
import math
import time
import cv2 
cap = cv2.VideoCapture(0)  		# Connect to camera 0 (or the only camera)
cap.set(3, 320)                     	# Set the width to 320
cap.set(4, 240)                      	# Set the height to 240
Center=np.array([])
f=3.04/(1.12*10**-3) 
sample_parameters={"hue":[0,5],"sat":[100,255],"value":[100,255],"Height":40,"OR_MASK":True,
"Kernel":True,"Circle":True,"BBoxColour":[204,0,204],"Obstacle":False}
lander_parameters={"hue":[15,30],"sat":[30,255],"value":[30,255],"Height":65,"OR_MASK":False,
"Kernel":False,"Circle":False,"BBoxColour":[0,0,255],"Obstacle":False}
obstacle_parameters={"hue":[40,70],"sat":[100,255],"value":[40,255],"Height":113,"OR_MASK":False,
"Kernel":False,"Circle":False,"BBoxColour":[204,204,0],"Obstacle":True}
cover_parameters={"hue":[100,107],"sat":[0,255],"value":[0,255],"Height":70,"OR_MASK":False,
"Kernel":False,"Circle":False,"BBoxColour":[255,255,255],"Obstacle":False}
def Detection(image,parameters_dict):
    ogimg=image#store the image given as a parameter for later bitwise and operation
    image=cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    #image=cv2.GaussianBlur(image, (17, 17), 2) 
    lower=np.array([parameters_dict["hue"][0],parameters_dict["sat"][0],parameters_dict["value"][0]])
    higher=np.array([parameters_dict["hue"][1],parameters_dict["sat"][1],parameters_dict["value"][1]])
    mask=cv2.inRange(image,lower,higher)
    if parameters_dict["OR_MASK"]==True:
        lower_oran=np.array([170,100,100],dtype="uint8") 
        higher_oran=np.array([179,255,255],dtype="uint8")
        mask1=cv2.inRange(image,lower_oran,higher_oran)
        mask=cv2.bitwise_or(mask,mask1)
    if parameters_dict["Kernel"]==True:
        Kernel=cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(5,5))
    else:
        Kernel=cv2.getStructuringElement(cv2.MORPH_RECT,(5,5))
    Thresholded_img=cv2.bitwise_and(ogimg,ogimg,mask=mask)
    filtered_img=cv2.morphologyEx(mask,cv2.MORPH_OPEN,Kernel)
    return filtered_img,Thresholded_img
def Range(img,parameters_dict,finalimage):
    Range=np.array([])
    ZDistance=np.array([])
    Bearing=np.array([])
    Center=np.array([])
    #LWidth=np.array([])
    #LHeight=np.array([])
    #GrayFiltimg=cv2.cvtColor(img,cv2.COLOR_HSV2BGR)
    #GrayFiltimg=cv2.cvtColor(GrayFiltimg,cv2.COLOR_RGB2GRAY)
    Contour=cv2.findContours(img,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
    if Contour == []:
        print("there is nothing here")
    else:
        Contour=imutils.grab_contours(Contour)
        for a in Contour:
            #find the center of the contour
            Moment=cv2.moments(a)
            #Area=cv2.contourArea(a)
            if parameters_dict["Circle"]==True:
                (x,y),radius=cv2.minEnclosingCircle(a)
                LWidth=2*radius #Lwidth=Lheight
                LHeight=2*radius
                cv2.rectangle(finalimage,(int(x-radius),int(y+radius)),(int(x+radius),int(y-radius)),
                 parameters_dict["BBoxColour"],2)
                Distance=(parameters_dict["Height"]*(f/(2*radius))/8)*math.cos(0.2967)
                Distance=(-0.0005*Distance**2)+(1.4897*Distance)-66.919
                ZDistance=np.append(ZDistance,Distance)
                Bearing=np.append(Bearing,(x-160)*(31.1/160))
                Range=np.vstack((ZDistance,Bearing)).T#Put Bearing and ZDistance into one array and arrange
                #columnwise
                Range=Range[Range[:,0].argsort()] 
            else:
                Lx=int(Moment["m10"]/Moment["m00"])
                Ly=int(Moment["m01"]/Moment["m00"])
                Centroid=np.array([Lx,Ly])
                Center=np.append(Center,Centroid)
                Lx1,Ly1,LWidth,LHeight=cv2.boundingRect(a)
                Area=LWidth*LHeight
                if Area>1250:
                    if parameters_dict["Obstacle"]==True:
                        cv2.rectangle(finalimage,(Lx-int(LWidth/2),Ly+int(LHeight/2)),(Lx+int(LWidth/2),Ly-int(LHeight/2)),
                         parameters_dict["BBoxColour"],2)
                        Distance=(parameters_dict["Height"]*(f/LWidth)/8)
                        Distance=(1.04*Distance)-8.7164
                        ZDistance=np.append(ZDistance,Distance)
                        Bearing=np.append(Bearing,(Lx-160)*(31.1/160))
                        Range=np.vstack((ZDistance,Bearing)).T#Put Bearing and ZDistance into one array and arrange
                        Range=Range[Range[:,0].argsort()] 
                    
                    else:
                        cv2.rectangle(finalimage,(Lx-int(LWidth/2),Ly+int(LHeight/2)),(Lx+int(LWidth/2),Ly-int(LHeight/2)),
                         parameters_dict["BBoxColour"],2)
                        Distance=(parameters_dict["Height"]*(f/LHeight)/8)*math.cos(0.2967)
                        ZDistance=np.append(ZDistance,Distance)
                        Bearing=np.append(Bearing,(Lx-160)*(31.1/160))
                        Range=np.vstack((ZDistance,Bearing)).T#Put Bearing and ZDistance into one array and arrange
                        Range=Range[Range[:,0].argsort()] 
                        #columnwise
                        
                else:
                    continue
                    
                
                #if positive then it's to the right if negative then to left of center 
    return Range,finalimage

def main(i):
    ret, img = cap.read()	     		# Get a frame from the camera 
    if ret == True:	
        cv2.waitKey(1)	
        #initiate some variables 
    """ img=cv2.imread("MultipleCovers.jpg")
    img=cv2.resize(img,(320,240)) """
    if __name__=="__main__":
        sample_img,SFin=Detection(np.copy(img),sample_parameters)
        cover_img,CFin=Detection(np.copy(img),cover_parameters)
        obstacle_img,OFin=Detection(np.copy(img),obstacle_parameters)
        lander_img,LFin=Detection(np.copy(img),lander_parameters)
        FinalImage=cv2.bitwise_or(SFin,CFin)
        FinalImage=cv2.bitwise_or(FinalImage,OFin)
        FinalImage=cv2.bitwise_or(FinalImage,LFin)#get a final image with all 
        #objects of interest in the image
        sample_Z,S_Bound_Image=Range(sample_img,sample_parameters,FinalImage)
        cover_Z,C_Bound_Image=Range(cover_img,cover_parameters,FinalImage)
        obstacle_Z,O_Bound_Image=Range(obstacle_img,obstacle_parameters,FinalImage)
        Lander_Z,L_Bound_Image=Range(lander_img,lander_parameters,FinalImage)
        print("Sample",sample_Z)
        print("Obstacle",obstacle_Z)
        print("Cover",cover_Z)
        print("Lander",Lander_Z)
        #print("Cover",cover_Z)
        if (i%5)==0:
            cv2.imshow("Binary Thresholded Frame",FinalImage)# Display thresholded frame
            cv2.waitKey(1)
            pass
    

if __name__=="__main__":
    i=0
    frequency=10
    Interval=1/frequency
    while True:
        try:
            now=time.time()
            i+=1
            main(i)
            #if i>30:
            #    break
            
            elapsed2=time.time()-now
            rate2=1/elapsed2
            print(rate2)
        except KeyboardInterrupt:
            break
                
    
