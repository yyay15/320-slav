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
        self.state = 1
        self.random = 1
        self.changingVariable = 1
        
        i2c = busio.I2C(board.SCL, board.SDA)
        self.sensor = adafruit_vcnl4040.VCNL4040(i2c)
        self.cap = cv2.VideoCapture(0)  		# Connect to camera 0 (or the only camera)
        self.cap.set(3, 320)                     	# Set the width to 320
        self.cap.set(4, 240)                      	# Set the height to 240
        self.Center=np.array([])
        self.f=3.04/(1.12*10**-3)
        #img=cv2.imread("MultipleCovers.jpg")
        self.sample_parameters={"hue":[0,5],"sat":[125,255],"value":[125,255],"Height":40,"OR_MASK":True,
            "Kernel":True,"Circle":True,"BBoxColour":[204,0,204],"type":0}
        self.lander_parameters={"hue":[15,30],"sat":[100,255],"value":[100,255],"Height":80,"OR_MASK":False,
            "Kernel":False,"Circle":False,"BBoxColour":[0,0,255],"type":1}
        self.obstacle_parameters={"hue":[40,70],"sat":[30,255],"value":[40,255],"Height":80,"OR_MASK":False,
            "Kernel":False,"Circle":False,"BBoxColour":[204,204,0],"type":2}
        self.cover_parameters={"hue":[95,107],"sat":[100,255],"value":[0,200],"Height":70,"OR_MASK":False,
            "Kernel":False,"Circle":False,"BBoxColour":[255,255,255],"type":3} 
        self.hole_parameters={"hue":[0,255],"sat":[0,255],"value":[50,60],"Height":50,"OR_MASK":False,
            "Kernel":False,"Circle":False,"BBoxColour":[255,0,0],"type":4} 
        self.wall_parameters={"hue":[0,255],"sat":[0,255],"value":[0,30],"Height":80,"OR_MASK":False,
            "Kernel":False,"Circle":False,"BBoxColour":[255,0,0],"type":4} 


    """ if self.state == 8:
            use other threshold
    """#Lx is obtained in Range function below
    def MaxMinLocations(self,c,img,Lx):
        total_diff=0
        diff=0
        maxleft=tuple(c[c[:,:,0].argmin()][0])
        maxright=tuple(c[c[:,:,0].argmax()][0])
        maxtop=tuple(c[c[:,:,1].argmin()][0])
        maxbot=tuple(c[c[:,:,1].argmax()][0])
        left_diff=maxright[0]-maxbot[0]
        right_diff=maxleft[0]-maxbot[0]
        cv2.line(img,maxbot,maxright,(0,255,0),2)
        cv2.line(img,maxbot,maxleft,(0,255,0),2)
        if left_diff>5 and right_diff>5:
            if right_diff>left_diff:
                diff=right_diff/2
            elif right_diff<left_diff:
                diff=left_diff/2
            total_diff=Lx+diff #so total diff will be less than Lx if left difference is greater than 
            #otherwise then we have to angle left if total diff is greater than Lx that 
            # means that we have to angle right:
        else:
            total_diff=0
       
        return total_diff,right_diff,left_diff


        #cv2.line(img,maxbot,maxright,(0,255,0),2)
    def Detection(self, image,parameters_dict):
        #image=cv2.resize(image,(640,480))
        #cv2.imshow("normal",image)
        #ogimg=image#store the image given as a parameter for later bitwise and operation
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
            Kernel=cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(5,5))
        else:
            Kernel=cv2.getStructuringElement(cv2.MORPH_RECT,(5,5))
        #Thresholded_img=cv2.bitwise_and(ogimg,ogimg,mask=mask)
        filtered_img=cv2.morphologyEx(mask,cv2.MORPH_OPEN,Kernel)
        return filtered_img

    
    def Range(self,img,parameters_dict,finalimage):
        Range=np.array([])
        RangeRBC=np.array([])
        ZDistance=np.array([])
        Bearing=np.array([])
        NewBearing=np.array([])
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
                Area=cv2.contourArea(a)
                if parameters_dict["Circle"]==True:
                    Lx1,Ly1,LWidth,LHeight=cv2.boundingRect(a)
                    if Area>30:
                        if (LWidth/LHeight)<1.3 and (LHeight/LWidth)<1.3:
                            (x,y),radius=cv2.minEnclosingCircle(a)
                            cv2.rectangle(finalimage,(int(x-radius),int(y+radius)),(int(x+radius),int(y-radius)),
                            parameters_dict["BBoxColour"],2)
                            Distance=(parameters_dict["Height"]*(self.f/(2*radius))/8)*math.cos(0.2967)
                            Distance=(-0.0005*Distance**2)+(1.4897*Distance)-66.919
                            Distance=Distance/1000
                            ZDistance=np.append(ZDistance,Distance)
                            Bearing=np.append(Bearing,math.radians((x-160)*(31.1/160)))
                            #print range bearing on image
                            textOrigin = (int(x-radius),int(y-radius)+ 5)
                            rangeText = "R: {:.4f}".format(Distance)
                            bearingText = " B: {:.4f}".format((math.radians((x-160)*(31.1/160))))
                            cv2.putText(finalimage, rangeText + bearingText, textOrigin, cv2.FONT_HERSHEY_SIMPLEX, 0.4,  parameters_dict["BBoxColour"] )

                            Range=np.vstack((ZDistance,-Bearing)).T#Put Bearing and ZDistance into one array and arrange
                            #columnwise
                            Range=Range[Range[:,0].argsort()]
                        else:
                            continue
                    else:
                        continue 
                elif parameters_dict["type"]==3:
                    Lx1,Ly1,LWidth,LHeight=cv2.boundingRect(a)
                    if (LWidth*LHeight)>300:
                        #if (LWidth/LHeight)<=2 and (LHeight/LWidth)<=2:
                        Lx=int(Moment["m10"]/Moment["m00"])
                        Ly=int(Moment["m01"]/Moment["m00"])
                        Centroid=np.array([Lx,Ly])
                        Center=np.append(Center,Centroid)
                        cv2.rectangle(finalimage,(Lx-int(LWidth/2),Ly+int(LHeight/2)),(Lx+int(LWidth/2),Ly-int(LHeight/2)),
                        parameters_dict["BBoxColour"],2)
                        Distance=(parameters_dict["Height"]*(self.f/LHeight)/8)*math.cos(0.2967)
                        Distance=((-0.0002*Distance**2)+(0.8492*Distance)+51)/1000
                        ZDistance=np.append(ZDistance,Distance)
                        New_Lx,left_diff,right_diff=self.MaxMinLocations(a,finalimage,Lx)
                        NewBearing=np.append(NewBearing,math.radians((New_Lx-160)*(31.1/160)))
                        textOrigin = (Lx-int(LWidth/2),Ly-int(LHeight/2)+ 5)
                        #rangeText = "R: {:.4f}".format(Distance)
                        rangeText = "left diff: {:.4f} ".format(left_diff)
                        bearingText = "right diff: {:.4f}".format(right_diff)
                        #bearingText = " B: {:.4f}".format((math.radians((Lx-160)*(31.1/160))))
                        cv2.putText(finalimage, rangeText + bearingText, (Lx1-5,Ly1), cv2.FONT_HERSHEY_SIMPLEX, 0.4,  parameters_dict["BBoxColour"] )
                        RangeRBC=np.vstack((ZDistance,NewBearing)).T
                        RangeRBC=RangeRBC[RangeRBC[:,0].argsort()] 
                        Bearing=np.append(Bearing,math.radians((Lx-160)*(31.1/160)))
                        Range=np.vstack((ZDistance,-Bearing)).T#Put Bearing and ZDistance into one array and arrange
                        #columnwise
                        Range=Range[Range[:,0].argsort()] 
                        #if positive then it's to the right if negative then to left of center 
                        #else:
                        #    continue
                    else: 
                        continue
                elif parameters_dict["type"]==2:#for obstacle
                    Lx1,Ly1,LWidth,LHeight=cv2.boundingRect(a)
                    if Area>150:
                        #f LWidth/LHeight<1.5 and LHeight/LWidth<1.5:
                        Lx=int(Moment["m10"]/Moment["m00"])#centroids of shapes identified
                        Ly=int(Moment["m01"]/Moment["m00"])
                        Centroid=np.array([Lx,Ly])
                        Center=np.append(Center,Centroid)
                        cv2.rectangle(finalimage,(Lx-int(LWidth/2),Ly+int(LHeight/2)),(Lx+int(LWidth/2),Ly-int(LHeight/2)),
                        parameters_dict["BBoxColour"],2)
                        Distance=(parameters_dict["Height"]*(self.f/LHeight)/8)*math.cos(0.2967)
                        Distance=(262.22*np.log(Distance)-1222.1)/1000
                        ZDistance=np.append(ZDistance,Distance)
                        Bearing=np.append(Bearing,math.radians((Lx-160)*(31.1/160)))
                        #Print range bearing
                        textOrigin = (Lx-int(LWidth/2),Ly-int(LHeight/2)+ 5)
                        rangeText = "R: {:.4f}".format(Distance)
                        bearingText = " B: {:.4f}".format((math.radians((Lx-160)*(31.1/160))))
                        cv2.putText(finalimage, rangeText + bearingText, textOrigin, cv2.FONT_HERSHEY_SIMPLEX, 0.4,  parameters_dict["BBoxColour"] )
                        ##
                        Range=np.vstack((ZDistance,-Bearing)).T#Put Bearing and ZDistance into one array and arrange
                        #columnwise
                        Range=Range[Range[:,0].argsort()] 
                        #if positive then it's to the right if negative then to left of center 
                    #else:
                    #    continue
                    else: 
                        continue
                elif parameters_dict["type"]==1: #for lander
                        Lx1,Ly1,LWidth,LHeight=cv2.boundingRect(a)
                        if Area>3000 and Area<60000:
                            Lx=int(Moment["m10"]/Moment["m00"])
                            Ly=int(Moment["m01"]/Moment["m00"])
                            Centroid=np.array([Lx,Ly])
                            Center=np.append(Center,Centroid)
                            cv2.rectangle(finalimage,(Lx-int(LWidth/2),Ly+int(LHeight/2)),(Lx+int(LWidth/2),Ly-int(LHeight/2)),
                            parameters_dict["BBoxColour"],2)
                            Distance=(parameters_dict["Height"]*(self.f/LHeight)/8)*math.cos(0.2967)
                            Distance=(0.8667*Distance-3)/1000
                            ZDistance=np.append(ZDistance,Distance)
                            
                            Bearing=np.append(Bearing,math.radians((Lx-160)*(31.1/160)))
                            #print range bearing
                            textOrigin = (Lx-int(LWidth/2),Ly-int(LHeight/2)+ 5)
                            rangeText = "R: {:.4f}".format(Distance)
                            bearingText = " B: {:.4f}".format((math.radians((Lx-160)*(31.1/160))))
                            cv2.putText(finalimage, rangeText + bearingText, textOrigin, cv2.FONT_HERSHEY_SIMPLEX, 0.4,  parameters_dict["BBoxColour"] )
                            Range=np.vstack((ZDistance,-Bearing)).T#Put Bearing and ZDistance into one array and arrange
                            #columnwise
                            Range=Range[Range[:,0].argsort()] 
                        else:
                            continue
                elif parameters_dict["type"]==4: #for hole on lander
                    Range=0
                else:
                    continue 
        return Range,RangeRBC
    def DetectandRange(self,img,sample_parameters,cover_parameters,obstacle_parameters,lander_parameters,finalImage):
        sample_img=self.Detection(img,self.sample_parameters)
        cover_img=self.Detection(img,self.cover_parameters)
        obstacle_img=self.Detection(img,self.obstacle_parameters)
        lander_img=self.Detection(img,self.lander_parameters)

        sample_Z, abc=self.Range(sample_img,self.sample_parameters,finalImage)
        cover_Z,holeCover_Z=self.Range(cover_img,self.cover_parameters,finalImage)
        obstacle_Z, abc=self.Range(obstacle_img,self.obstacle_parameters,finalImage)
        lander_Z, abc=self.Range(lander_img,self.lander_parameters,finalImage)
        # print(sample_Z)
        # print(cover_Z)
        # print(obstacle_Z)
        print("Lander", lander_Z)
        return sample_Z,cover_Z,obstacle_Z,lander_Z,holeCover_Z
    def visMain(self, i):
        ret, img = self.cap.read()	     		# Get a frame from the camera
        #imcopy=np.copy(img)
        if ret == True:	
            cv2.waitKey(1)	
            #initiate some variables
        sample_Z,cover_Z,obstacle_Z,lander_Z,holeCover_Z=self.DetectandRange(img,self.sample_parameters,
            self.cover_parameters,self.obstacle_parameters,self.lander_parameters,img)
        self.holefinder()
        
        if (i%5)==0:
             cv2.imshow("Binary Thresholded Frame",img)# Display thresholded frame
        #print(Bearing1)holes_RB,
        return sample_Z,lander_Z,cover_Z,obstacle_Z,holeCover_Z
    
    def GetDetectedObjects(self,state):
        sampleRB, landerRB, obstaclesRB, rocksRB, holesRB, rotHoleRB = None, None, None, None, None, None
        i=0
        now=time.time()
        #i+=1   holesRB,
        sampleRB,landerRB,rocksRB,obstaclesRB,rotHoleRB=self.visMain(i)
        #self.updateVisionState(state)
        
        elapsed=time.time()-now
        #time.sleep(Interval-elapsed)
        elapsed2=time.time()-now
        rate2=1/elapsed2
        print(rate2)

            # sample [[R, B], [R,B]]
            # lander [R, B]
        # if nothing sampleRB = None,holesRB,
        return sampleRB, landerRB, obstaclesRB, rocksRB,  holesRB, rotHoleRB


    def sampleCollected(self):
        a=self.sensor.proximity
        if a>=13:
            SamplePresent=True
        else:
            SamplePresent=False
        return SamplePresent 
        pass
    def holefinder(self):
        hole_Z=None
        #imcopy=np.copy(img)
        if self.state==8:
            Lander_parameter_update={"hue":[15,30],"sat":[0,255],"value":[30,255]}
            self.lander_parameters.update(Lander_parameter_update)#update dictionary for lander
            #to change values to adjust for dodge lighting when going up lander
            #hole_img=self.Detection(img,self.hole_parameters)
            #hole_Z=self.Range(hole_img,self.hole_parameters,img)
            #LanderMasklow=np.array([15,0,0],dtype="uint8")
            #LanderMaskhigh=np.array([30,255,255],dtype="uint8")
        #elif self.state==10:
        #   hole_img=self.Detection(img,self.hole_parameters)
        #    hole_Z=self.Range(hole_img,self.hole_parameters,img)

        else:
            Lander_parameter_update={"hue":[15,30],"sat":[100,255],"value":[100,255]}
            self.lander_parameters.update(Lander_parameter_update)
            #revert the changes listed above.
    def updateVisionState(self,state):
        self.state = state
        
       




    # Alan Testing for Commandcentre integration
    def commandCentreVideoFeed(self,img):
        frame = cv2.imencode('.jpg', img)[1].tobytes()
        yield (b'--frame\r\n'b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')