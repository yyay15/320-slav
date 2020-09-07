import numpy as np
import imutils
from cv2 import cv2 
#cap = cv2.VideoCapture(0)  		# Connect to camera 0 (or the only camera)
#cap.set(3, 320)                     	# Set the width to 320
#cap.set(4, 240)                     	# Set the height to 240
#ret, img = cap.read()	     		# Get a frame from the camera 
#if ret == True:	
#       cv2.waitKey(500)	
img=cv2.imread("lunar_field.jpg")
imgblur=cv2.GaussianBlur(img, (17, 17), 2)
img2=np.copy(img)
img2blur=cv2.GaussianBlur(img2, (15, 15), 2)
img3=np.copy(img)
img3blur=cv2.GaussianBlur(img3, (15, 15), 2)#copy and blur image for green obstacle
cv2.imshow("normal",img)
filtered_img=cv2.fastNlMeansDenoising(img,10,10,7,21)
hsv_frame = cv2.cvtColor(imgblur, cv2.COLOR_BGR2HSV) 		# Convert from BGR to HSV colourspace
hsv_cover_frame=cv2.cvtColor(img2blur,cv2.COLOR_BGR2HSV)
hsv_obstacle=cv2.cvtColor(img3blur,cv2.COLOR_BGR2HSV)
hue_frame = hsv_frame						# Extract hue channel
hue_frame_cover=hsv_cover_frame
lower_green=np.array([40,50,40],dtype="uint8")
upper_green=np.array([70,255,255],dtype="uint8")
lower_blue = np.array([95,60,0],dtype="uint8") 
upper_blue = np.array([107,255,255],dtype="uint8")
lower_orang=np.array([0,100,100],dtype="uint8") 
higher_orang=np.array([5,255,255],dtype="uint8")
lower_oran=np.array([175,100,100],dtype="uint8") 
higher_oran=np.array([179,255,255],dtype="uint8")
mask=cv2.inRange(hue_frame,lower_orang,higher_orang)
mask1=cv2.inRange(hue_frame,lower_oran,higher_oran)
mask=cv2.bitwise_or(mask,mask1)#or the two masks together to allow a threshold
#between 175 to 5
kernel_sample=cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(2,2))
kernel_cover=cv2.getStructuringElement(cv2.MORPH_RECT,(15,15))
kernel_obstacle=cv2.getStructuringElement(cv2.MORPH_RECT,(30,30))
mask_obstacle=cv2.inRange(hsv_obstacle,lower_green,upper_green)
#if I get a multitude of circlevalues from HoughCircles maybe I can just average them?
mask_cover=cv2.inRange(hue_frame_cover,lower_blue,upper_blue)
#thresholded_img=cv2.adaptiveThreshold(hue_frame,179,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
        #    cv2.THRESH_BINARY,573,2)
#Threshold the following images
thresholded_img = cv2.bitwise_and(img, img, mask= mask)
thresholded_cover=cv2.bitwise_and(img2,img2,mask=mask_cover)
thresholded_obstacle=cv2.bitwise_and(img3,img3,mask=mask_obstacle)
#Filter the imags 
filtered_img=cv2.morphologyEx(thresholded_img,cv2.MORPH_OPEN,kernel_sample)
filtered_mask=cv2.morphologyEx(mask,cv2.MORPH_OPEN,kernel_sample)
filtered_maskcover=cv2.morphologyEx(thresholded_cover,cv2.MORPH_OPEN,kernel_cover)
filtered_obstacle=cv2.morphologyEx(thresholded_obstacle,cv2.MORPH_OPEN,kernel_obstacle)
GrayFiltObstacle=cv2.cvtColor(filtered_obstacle,cv2.COLOR_HSV2BGR)
GrayFiltObstacle=cv2.cvtColor(GrayFiltObstacle,cv2.COLOR_RGB2GRAY)
obstacleContour,hierarchy=cv2.findContours(GrayFiltObstacle,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)


detector_sample=cv2.SimpleBlobDetector_create()#setup BlobDetector for sample
detector_cover=cv2.SimpleBlobDetector_create()#setup BlobDetector for cover
parameters_cover=cv2.SimpleBlobDetector_Params()
#Filter by Area
parameters_cover.filterByArea=True
parameters_cover.minArea=10
parameters_cover.maxArea=5000

#Filter by Circularitry 
parameters_cover.filterByCircularity=True
parameters_cover.maxCircularity=0.9
parameters_cover.minCircularity=0.7
#filter by convexity
parameters_cover.filterByConvexity=False

#Filter by Inertia
parameters_cover.filterByInertia=True
parameters_cover.minInertiaRatio=0.5

#Distance between blobs
parameters_cover.minDistBetweenBlobs=100

parameters=cv2.SimpleBlobDetector_Params()#setup parameters for sample detection
#Filter by Area
parameters.filterByArea=True
parameters.minArea=2
parameters.maxArea=500

#Filter by Circularitry 
parameters.filterByCircularity=True
parameters.minCircularity=0.8
#filter by convexity
parameters.filterByConvexity=False

#Filter by Inertia
parameters.filterByInertia=True
parameters.minInertiaRatio=0.5

#Distance between blobs
parameters.minDistBetweenBlobs=100

detector_sample=cv2.SimpleBlobDetector_create(parameters)
#detector_cover=cv2.SimpleBlobDetector_create(parameters_cover)
blobs=detector_sample.detect(filtered_img)
#blobs_cover=detector_cover.detect(filtered_obstacle)
circlenum=cv2.HoughCircles(filtered_mask,cv2.HOUGH_GRADIENT,1,20,param1=50,
        param2=10,minRadius=50,maxRadius=0)
sample_coordinates=cv2.KeyPoint_convert(blobs)
sample_coordinates=np.array(sample_coordinates)
sample_coordinates=sample_coordinates.astype('int')
#Covercoord=cv2.KeyPoint_convert(blobs_cover)
#Covercoord=np.array(Covercoord)
#Covercoord=Covercoord.astype('int')
#ret, thresholded_frame = cv2.threshold(hue_frame,,179,cv2.THRESH_BINARY)	# Threshold blue channel
#print(circlenum)
print(sample_coordinates)
if  np.size(sample_coordinates)>0:
   ab=sample_coordinates[0,1]
   ba=sample_coordinates[0,0]
   filtered_img=cv2.circle(filtered_img,(ba,ab),20,(255,0,0),3)
cv2.imshow("Binary Thresholded Frame",filtered_img)# Display thresholded frame
cv2.imshow("Binary Thresholded Frame for rock cover",filtered_maskcover)
cv2.imshow("Binary Thresholded Frame for Obstacle",filtered_obstacle)
cv2.waitKey(0)									# Exit on keypress

cv2.destroyAllWindows()
