import numpy as np
import imutils
import math
import time
import cProfile
import cv2 
import board
import busio
import adafruit_vcnl4040



class Vision: 
    def __init__(self):
        # parameters that change 
        self.random = 1
        self.changingVariable = 1
        
        self.i2c = busio.I2C(board.SCL, board.SDA)
        self.sensor = adafruit_vcnl4040.VCNL4040(i2c)
        self.cap = cv2.VideoCapture(0)  		# Connect to camera 0 (or the only camera)
        self.cap.set(3, 320)                     	# Set the width to 320
        self.cap.set(4, 240)                      	# Set the height to 240
        self.Center=np.array([])
        self.f=3.04/(1.12*10**-3)
        #img=cv2.imread("MultipleCovers.jpg")
        self.sample_parameters={"hue":[0,5],"sat":[100,255],"value":[100,255],"Height":40,"OR_MASK":True,
         "Kernel":True,"Circle":True,"BBoxColour":[204,0,204]}
        self.lander_parameters={"hue":[15,30],"sat":[100,255],"value":[100,255],"Height":570,"OR_MASK":False,
         "Kernel":False,"Circle":False,"BBoxColour":[0,0,255]}
        self.obstacle_parameters={"hue":[40,70],"sat":[50,255],"value":[40,255],"Height":150,"OR_MASK":False,
         "Kernel":False,"Circle":False,"BBoxColour":[204,204,0]}
        self.cover_parameters={"hue":[95,107],"sat":[60,255],"value":[0,255],"Height":70,"OR_MASK":False,
         "Kernel":False,"Circle":False,"BBoxColour":[255,255,255]} 

    def Detection(self, image,parameters_dict):
            #image=cv2.resize(image,(640,480))
            #cv2.imshow("normal",image)
            ogimg=image#store the image given as a parameter for later bitwise and operation
            image=cv2.cvtColor(cv2.UMat(image), cv2.COLOR_BGR2HSV)

            #image=cv2.GaussianBlur(image, (17, 17), 2) 
            lower=np.array([parameters_dict["hue"][0],parameters_dict["sat"][0],parameters_dict["value"][0]])
            higher=np.array([parameters_dict["hue"][1],parameters_dict["sat"][1],parameters_dict["value"][1]])
            mask=cv2.inRange(image,lower,higher)
            if parameters_dict["OR_MASK"]==True:
                lower_oran=np.array([175,100,100],dtype="uint8") 
                higher_oran=np.array([179,255,255],dtype="uint8")
                mask1=cv2.inRange(image,lower_oran,higher_oran)
                mask=cv2.bitwise_or(mask,mask1)
            if parameters_dict["Kernel"]==True:
                Kernel=cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(15,15))
            else:
                Kernel=cv2.getStructuringElement(cv2.MORPH_RECT,(5,5))
            Thresholded_img=cv2.bitwise_and(ogimg,ogimg,mask=mask)
            filtered_img=cv2.morphologyEx(mask,cv2.MORPH_OPEN,Kernel)
            return filtered_img,Thresholded_img

    def Range(self,img,parameters_dict,finalimage):
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
                    cv2.rectangle(finalimage,(int(x-radius),int(y+radius)),(int(x+radius),int(y-radius)),
                    parameters_dict["BBoxColour"],2)
                    Distance=(parameters_dict["Height"]*(self.f/(2*radius))/8)*math.cos(0.2967)
                    Distance=(-0.0005*Distance**2)+(1.4897*Distance)-66.919
                    Distance=Distance/1000
                    ZDistance=np.append(ZDistance,Distance)
                    Bearing=np.append(Bearing,math.radians((x-160)*(31.1/160)))
                    Range=np.vstack((ZDistance,Bearing)).T#Put Bearing and ZDistance into one array and arrange
                    #columnwise
                    Range=Range[Range[:,0].argsort()] 
                else:
                    Lx=int(Moment["m10"]/Moment["m00"])
                    Ly=int(Moment["m01"]/Moment["m00"])
                    Centroid=np.array([Lx,Ly])
                    Center=np.append(Center,Centroid)
                    Lx1,Ly1,LWidth,LHeight=cv2.boundingRect(a)
                    cv2.rectangle(finalimage,(Lx-int(LWidth/2),Ly+int(LHeight/2)),(Lx+int(LWidth/2),Ly-int(LHeight/2)),
                    parameters_dict["BBoxColour"],2)
                    Distance=parameters_dict["Height"]*(self.f/LHeight)/4
                    ZDistance=np.append(ZDistance,Distance)
                    Bearing=np.append(Bearing,(Lx-160)*(31.1/160))
                    Range=np.vstack((ZDistance,Bearing)).T#Put Bearing and ZDistance into one array and arrange
                    #columnwise
                    Range=Range[Range[:,0].argsort()] 
                    #if positive then it's to the right if negative then to left of center 
        return Range,finalimage

    def visMain(self, i):
        ret, img = self.cap.read()	     		# Get a frame from the camera
        if ret == True:	
            cv2.waitKey(1)	
            #initiate some variables

        sample_img,SFin=self.Detection(img,self.sample_parameters)
        cover_img,CFin=self.Detection(img,self.cover_parameters)
        obstacle_img,OFin=self.Detection(img,self.obstacle_parameters)
        lander_img,LFin=self.Detection(img,self.lander_parameters)
        FinalImage=cv2.bitwise_or(SFin,CFin)
        FinalImage=cv2.bitwise_or(FinalImage,OFin)
        FinalImage=cv2.bitwise_or(FinalImage,LFin)
        sample_Z,S_Bound_Image=self.Range(sample_img,self.sample_parameters,FinalImage)
        cover_Z,C_Bound_Image=self.Range(cover_img,self.cover_parameters,FinalImage)
        obstacle_Z,O_Bound_Image=self.Range(obstacle_img,self.obstacle_parameters,FinalImage)
        lander_Z,L_Bound_Image=self.Range(lander_img,self.lander_parameters,FinalImage)
        print(sample_Z)
        if (i%5)==0:
             cv2.imshow("Binary Thresholded Frame",FinalImage)# Display thresholded frame

        #print(Bearing1)
        return sample_Z,lander_Z,cover_Z,obstacle_Z
    
    def GetDetectedObjects(self):
        sampleRB, landerRB, obstaclesRB, rocksRB = None, None, None, None
        i=0
        now=time.time()
        #i+=1
        sampleRB,landerRB,rocksRB,obstaclesRB=self.visMain(i)
        elapsed=time.time()-now
        #time.sleep(Interval-elapsed)
        elapsed2=time.time()-now
        rate2=1/elapsed2
        print(rate2)

            # sample [[R, B], [R,B]]
            # lander [R, B]
        # if nothing sampleRB = None
        return sampleRB/1000, landerRB/1000, obstaclesRB/1000, rocksRB/1000

# 
    def sampleCollected(self):
        a=self.sensor.proximity
        if a>=13:
            SamplePresent=True
        else:
            SamplePresent=False
        return SamplePresent 
        pass
    
    def UpdateObjectPositions(self):
        pass
