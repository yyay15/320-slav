import numpy as np
import imutils
import math
import time
import cv2 
""" cap = cv2.VideoCapture(0)  		# Connect to camera 0 (or the only camera)
cap.set(3, 320)                     	# Set the width to 320
cap.set(4, 240)      """               	# Set the height to 240
Center=np.array([])

f=3.04/(1.12*10**-3)

sample_parameters={"hue":[0,5],"sat":[125,255],"value":[125,255],"Height":40,"OR_MASK":True,
    "Kernel":True,"Circle":True,"BBoxColour":[204,0,204],"type":0}
lander_parameters={"hue":[15,30],"sat":[0,255],"value":[30,255],"Height":80,"OR_MASK":False,
    "Kernel":False,"Circle":False,"BBoxColour":[0,0,255],"type":1}
obstacle_parameters={"hue":[40,70],"sat":[50,255],"value":[40,255],"Height":80,"OR_MASK":False,
    "Kernel":False,"Circle":False,"BBoxColour":[204,204,0],"type":2}
cover_parameters={"hue":[100,120],"sat":[40,200],"value":[40,200],"Height":70,"OR_MASK":False,
    "Kernel":False,"Circle":False,"BBoxColour":[255,255,255],"type":3} 
hole_parameters={"hue":[0,255],"sat":[0,100],"value":[0,80],"Height":50,"OR_MASK":False,
    "Kernel":False,"Circle":False,"BBoxColour":[180,0,180],"type":4} 


""" if self.state == 8:
        use other threshold
"""
def MaxMinLocations(c,img):
    maxleft=tuple(c[c[:,:,0].argmin()][0])
    maxright=tuple(c[c[:,:,0].argmax()][0])
    maxtop=tuple(c[c[:,:,1].argmin()][0])
    maxbot=tuple(c[c[:,:,1].argmax()][0])
    cv2.line(img,maxbot,maxright,(0,255,0),2)
    cv2.line(img,maxbot,maxleft,(0,255,0),2)
    right_diff=maxright[0]-maxbot[0]
    left_diff=maxbot[0]-maxleft[0]
    #if left_diff>10:

    #elif right_diff>10:
        

    

def Detection(image,parameters_dict):
    #cv2.imshow("normal",image)
    #ogimg=image#store the image given as a parameter for later bitwise and operation
    image=cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

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
            Area=cv2.contourArea(a)
            if parameters_dict["Circle"]==True:
                Lx1,Ly1,LWidth,LHeight=cv2.boundingRect(a)
                if Area>30:
                    if LWidth/LHeight<1.1:
                        (x,y),radius=cv2.minEnclosingCircle(a)
                        cv2.rectangle(finalimage,(int(x-radius),int(y+radius)),(int(x+radius),int(y-radius)),
                        parameters_dict["BBoxColour"],2)
                        Distance=(parameters_dict["Height"]*(f/(2*radius))/8)*math.cos(0.2967)
                        Distance=(-0.0005*Distance**2)+(1.4897*Distance)-66.919
                        Distance=Distance/1000
                        ZDistance=np.append(ZDistance,Distance)
                        Bearing=np.append(Bearing,math.radians((x-160)*(31.1/160)))
                        Range=np.vstack((ZDistance,-Bearing)).T#Put Bearing and ZDistance into one array and arrange
                        #columnwise
                        Range=Range[Range[:,0].argsort()]
                    elif LHeight/LWidth<1.1:
                        (x,y),radius=cv2.minEnclosingCircle(a)
                        cv2.rectangle(finalimage,(int(x-radius),int(y+radius)),(int(x+radius),int(y-radius)),
                        parameters_dict["BBoxColour"],2)
                        Distance=(parameters_dict["Height"]*(f/(2*radius))/8)*math.cos(0.2967)
                        Distance=(-0.0005*Distance**2)+(1.4897*Distance)-66.919
                        Distance=Distance/1000
                        ZDistance=np.append(ZDistance,Distance)
                        Bearing=np.append(Bearing,math.radians((x-160)*(31.1/160)))
                        Range=np.vstack((ZDistance,-Bearing)).T#Put Bearing and ZDistance into one array and arrange
                        #columnwise
                        Range=Range[Range[:,0].argsort()]
                    else:
                        continue
                else:
                    continue 
            elif parameters_dict["type"]==3:
                Lx1,Ly1,LWidth,LHeight=cv2.boundingRect(a)
                if Area>150 and Area<5000:
                    if LWidth/LHeight<1.2:
                        Lx=int(Moment["m10"]/Moment["m00"])
                        Ly=int(Moment["m01"]/Moment["m00"])
                        Centroid=np.array([Lx,Ly])
                        Center=np.append(Center,Centroid)
                        cv2.rectangle(finalimage,(Lx-int(LWidth/2),Ly+int(LHeight/2)),(Lx+int(LWidth/2),Ly-int(LHeight/2)),
                        parameters_dict["BBoxColour"],2)
                        Distance=(parameters_dict["Height"]*(f/LHeight)/8)*math.cos(0.2967)
                        Distance=((-0.0002*Distance**2)+(0.8492*Distance)+51)/1000
                        ZDistance=np.append(ZDistance,Distance)
                        MaxMinLocations(a,finalimage)
                        Bearing=np.append(Bearing,math.radians((Lx-160)*(31.1/160)))
                        Range=np.vstack((ZDistance,-Bearing)).T#Put Bearing and ZDistance into one array and arrange
                        #columnwise
                        Range=Range[Range[:,0].argsort()] 
                        #if positive then it's to the right if negative then to left of center 
                    elif LHeight/LWidth<1.2:
                        Lx=int(Moment["m10"]/Moment["m00"])
                        Ly=int(Moment["m01"]/Moment["m00"])
                        Centroid=np.array([Lx,Ly])
                        Center=np.append(Center,Centroid)
                        cv2.rectangle(finalimage,(Lx-int(LWidth/2),Ly+int(LHeight/2)),(Lx+int(LWidth/2),Ly-int(LHeight/2)),
                        parameters_dict["BBoxColour"],2)
                        Distance=(parameters_dict["Height"]*(f/LHeight)/8)*math.cos(0.2967)
                        Distance=((-0.0002*Distance**2)+(0.8492*Distance)+51)/1000
                        ZDistance=np.append(ZDistance,Distance)
                        
                        MaxMinLocations(a,finalimage)
                        Bearing=np.append(Bearing,math.radians((Lx-160)*(31.1/160)))
                        Range=np.vstack((ZDistance,-Bearing)).T#Put Bearing and ZDistance into one array and arrange
                        #columnwise
                        Range=Range[Range[:,0].argsort()] 
                    else:
                        continue
                else: 
                    continue
            elif parameters_dict["type"]==2:
                Lx1,Ly1,LWidth,LHeight=cv2.boundingRect(a)
                if Area>150:
                    if LWidth/LHeight<1.2:
                        Lx=int(Moment["m10"]/Moment["m00"])
                        Ly=int(Moment["m01"]/Moment["m00"])
                        Centroid=np.array([Lx,Ly])
                        Center=np.append(Center,Centroid)
                        cv2.rectangle(finalimage,(Lx-int(LWidth/2),Ly+int(LHeight/2)),(Lx+int(LWidth/2),Ly-int(LHeight/2)),
                        parameters_dict["BBoxColour"],2)
                        Distance=(parameters_dict["Height"]*(f/LHeight)/8)*math.cos(0.2967)
                        Distance=(262.22*np.log(Distance)-1222.1)/1000
                        ZDistance=np.append(ZDistance,Distance)
                        MaxMinLocations(a,finalimage)
                        Bearing=np.append(Bearing,math.radians((Lx-160)*(31.1/160)))
                        Range=np.vstack((ZDistance,-Bearing)).T#Put Bearing and ZDistance into one array and arrange
                        #columnwise
                        Range=Range[Range[:,0].argsort()] 
                        #if positive then it's to the right if negative then to left of center 
                    elif LHeight/LWidth<1.2:
                        Lx=int(Moment["m10"]/Moment["m00"])
                        Ly=int(Moment["m01"]/Moment["m00"])
                        Centroid=np.array([Lx,Ly])
                        Center=np.append(Center,Centroid)
                        cv2.rectangle(finalimage,(Lx-int(LWidth/2),Ly+int(LHeight/2)),(Lx+int(LWidth/2),Ly-int(LHeight/2)),
                        parameters_dict["BBoxColour"],2)
                        Distance=(parameters_dict["Height"]*(f/LHeight)/8)*math.cos(0.2967)
                        Distance=(262.22*np.log(Distance)-1222.1)/1000
                        ZDistance=np.append(ZDistance,Distance)
                        MaxMinLocations(a,finalimage)
                        Bearing=np.append(Bearing,math.radians((Lx-160)*(31.1/160)))
                        Range=np.vstack((ZDistance,-Bearing)).T#Put Bearing and ZDistance into one array and arrange
                        #columnwise
                        Range=Range[Range[:,0].argsort()] 
                    else:
                        continue
                else: 
                    continue
            elif parameters_dict["type"]==1:
                    Lx1,Ly1,LWidth,LHeight=cv2.boundingRect(a)
                    if Area>5000:
                        Lx=int(Moment["m10"]/Moment["m00"])
                        Ly=int(Moment["m01"]/Moment["m00"])
                        Centroid=np.array([Lx,Ly])
                        Center=np.append(Center,Centroid)
                        cv2.rectangle(finalimage,(Lx-int(LWidth/2),Ly+int(LHeight/2)),(Lx+int(LWidth/2),Ly-int(LHeight/2)),
                        parameters_dict["BBoxColour"],2)
                        Distance=(parameters_dict["Height"]*(f/LHeight)/8)*math.cos(0.2967)
                        Distance=((1.2*Distance)-8.7164)/1000
                        ZDistance=np.append(ZDistance,Distance)
                        #self.MaxMinLocations(a,finalimage)
                        Bearing=np.append(Bearing,math.radians((Lx-160)*(31.1/160)))
                        Range=np.vstack((ZDistance,-Bearing)).T#Put Bearing and ZDistance into one array and arrange
                        #columnwise
                        Range=Range[Range[:,0].argsort()] 
                    else:
                        continue
            elif parameters_dict["type"]==4:
                Lx1,Ly1,LWidth,LHeight=cv2.boundingRect(a)
                if Area>30 and Area<3000:
                    if LWidth/LHeight<1.1:
                        (x,y),radius=cv2.minEnclosingCircle(a)
                        cv2.rectangle(finalimage,(int(x-radius),int(y+radius)),(int(x+radius),int(y-radius)),
                        parameters_dict["BBoxColour"],2)
                        Distance=(parameters_dict["Height"]*(f/(2*radius))/8)*math.cos(0.2967)
                        Distance=(-0.0005*Distance**2)+(1.4897*Distance)-66.919
                        Distance=Distance/1000
                        ZDistance=np.append(ZDistance,Distance)
                        Bearing=np.append(Bearing,math.radians((x-160)*(31.1/160)))
                        Range=np.vstack((ZDistance,-Bearing)).T#Put Bearing and ZDistance into one array and arrange
                        #columnwise
                        Range=Range[Range[:,0].argsort()]
                    elif LHeight/LWidth<1.1:
                        (x,y),radius=cv2.minEnclosingCircle(a)
                        cv2.rectangle(finalimage,(int(x-radius),int(y+radius)),(int(x+radius),int(y-radius)),
                        parameters_dict["BBoxColour"],2)
                        Distance=(parameters_dict["Height"]*(f/(2*radius))/8)*math.cos(0.2967)
                        Distance=(-0.0005*Distance**2)+(1.4897*Distance)-66.919
                        Distance=Distance/1000
                        ZDistance=np.append(ZDistance,Distance)
                        Bearing=np.append(Bearing,math.radians((x-160)*(31.1/160)))
                        Range=np.vstack((ZDistance,-Bearing)).T#Put Bearing and ZDistance into one array and arrange
                        #columnwise
                        Range=Range[Range[:,0].argsort()]
                    else:
                        continue
                else:
                    continue 

    return Range
def DetectandRange(img,sample_parameters,cover_parameters,obstacle_parameters,lander_parameters,finalImage):
    sample_img=Detection(img,sample_parameters)
    cover_img=Detection(img,cover_parameters)
    obstacle_img=Detection(img,obstacle_parameters)
    lander_img=Detection(img,lander_parameters)
    hole_img=Detection(img,hole_parameters)
    sample_Z=Range(sample_img,sample_parameters,finalImage)#sample_img is the filtered img finalImage is just 
    #the plain image
    cover_Z=Range(cover_img,cover_parameters,finalImage)
    obstacle_Z=Range(obstacle_img,obstacle_parameters,finalImage)
    lander_Z=Range(lander_img,lander_parameters,finalImage)
    hole_Z=Range(hole_img,hole_parameters,finalImage)
    print(sample_Z)
    print(cover_Z)
    print(obstacle_Z)
    print(lander_Z)
    print(hole_Z)
    return sample_Z,cover_Z,obstacle_Z,lander_Z
def visMain(i):
    """ ret, img = cap.read()	     		# Get a frame from the camera
    if ret == True:	
        cv2.waitKey(1)	 """
        #initiate some variables
    img=cv2.imread("visionScript\manCap9.jpg")
    img=cv2.resize(img,(320,240))
    sample_Z,cover_Z,obstacle_Z,lander_Z=DetectandRange(img,sample_parameters,
        cover_parameters,obstacle_parameters,lander_parameters,img)
    if (i%5)==0:
            cv2.imshow("Binary Thresholded Frame",img)# Display thresholded frame
            cv2.waitKey(1)
    #print(Bearing1)
    

if __name__=="__main__":
    i=0
    frequency=10
    Interval=1/frequency
    while True:
        try:
            now=time.time()
            i+=1
            visMain(i)
            elapsed2=time.time()-now
            rate2=1/elapsed2
            print(rate2)
        except KeyboardInterrupt:
            #cap.release()
            cv2.destroyAllWindows()
            break
                
    
