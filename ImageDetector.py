# -*- coding: utf-8 -*-
"""
Created on Thu Mar  1 18:05:07 2018
@author: Kathy
"""
import cv2
import math
import numpy as np
from scipy.spatial import distance as dist
from collections import OrderedDict
from skimage.measure import structural_similarity as ssim

class ImageDetector:
    def __init__(self):
        # initialize the colors dictionary, containing the color
		# name as the key and the RGB tuple as the value
        colors = OrderedDict({
			"black": (0, 0, 0),
			"white": (255, 255, 255)})

		# allocate memory for the L*a*b* image, then initialize
		# the color names list
        self.lab = np.zeros((len(colors), 1, 3), dtype="uint8")
        self.colorNames = []

		# loop over the colors dictionary
        for (i, (name, rgb)) in enumerate(colors.items()):
			# update the L*a*b* array and the color names list
            self.lab[i] = rgb
            self.colorNames.append(name)

		# convert the L*a*b* array from the RGB color space
		# to L*a*b*
        self.lab = cv2.cvtColor(self.lab, cv2.COLOR_RGB2LAB)

    def detectShape(self, contour):
        shape = "unknown"
        perimeter = cv2.arcLength(contour, True)
        vertices = cv2.approxPolyDP(contour, 0.04*perimeter, True)
        #print("vertices = " + str(len(vertices)))
        # if the shape is a triangle, it will have 3 vertices
        if len(vertices) == 3:
            shape = "triangle"

		# if the shape has 4 vertices, it is either a square or a rectangle
        elif len(vertices) == 4:
			# compute the bounding box of the contour and use the bounding box to compute the aspect ratio
            (x, y, w, h) = cv2.boundingRect(vertices)
            ar = w / float(h)

			# a square will have an aspect ratio that is approximately equal to one, otherwise, the shape is a rectangle
            shape = "square" if ar >= 0.95 and ar <= 1.05 else "rectangle"

		# if the shape is a pentagon, it will have 5 vertices
#        elif len(vertices) == 5:
#            shape = "half-arrow"
#            
#        elif len(vertices) == 7:
#            shape = "arrow"
		# otherwise, we assume the shape is a circle
        else:
            shape = "circle"

		# return the name of the shape
        return shape

    def detectFill(self, image, contour):
        
        # construct a mask for the contour, then compute the
		# average L*a*b* value for the masked region
        mask = np.zeros(image.shape[:2], dtype="uint8")
        cv2.drawContours(mask, [contour], -1, 255, -1)
        mask = cv2.erode(mask, None, iterations=2)
        mean = cv2.mean(image, mask=mask)[:3]
        #print("mean = " + str(mean))

		# initialize the minimum distance found thus far
        minDist = (np.inf, None)
        allDist=[]
		# loop over the known L*a*b* color values
        for (i, row) in enumerate(self.lab):
			# compute the distance between the current L*a*b*
			# color value and the mean of the image
            d = dist.euclidean(row[0], mean)
            #print("distance = " + str(d))
            allDist.append(d)

			# if the distance is smaller than the current distance,
			# then update the bookkeeping variable
            if d < minDist[0]:
                minDist = (d, i)

		# return the name of the color with the smallest distance
        difference = abs(allDist[1] - allDist[0])
        #print("difference" + str(difference))
        if(difference < 20):
            return "half-half"
        else:
            return self.colorNames[minDist[1]]
    
    def detectSize(self, contour, image):
        #perimeter = cv2.arcLength(contour, True)
        #poly = cv2.fillPoly(contour, pts =[contour], color=(255,255,255))
        #area = cv2.contourArea(contour)
        #print("area = "  + str(area))
        rotrect = cv2.minAreaRect(contour)
        #print("rot rect = " + str(rotrect))
        width,height = rotrect[1]
        #print("Wdith = " + str(width))
#        angle = rotrect[2]
#        if(width < height):
#            new_angle = angle + 180
#        else:
#            new_angle = angle + 90
#        print("angle = " + str(new_angle))
        x,y,w,h = cv2.boundingRect(contour)
        #box = cv2.boxPoints(rotrect)
        #print("rectangle = " + str(rotrect))
        #width_dist = math.sqrt(( - x1)**2 + (y2 - y1)**2)
        #length_dist = math.sqrt((x2 - x1)**2 + (y2 - y1)**2)
        #print("width x height = " + str(int(w*h)))
        area = int(w*h)
        if(area > 43500):
            size="large"
        elif(area <= 43500 and area > 12000):
            size="medium"
        else:
            size="small"
#        elif(area <= 12000 and area >= 8000 ):
#            size="small"
#        else:
#            size="x-small"
#        if(area < 1000):
#            size="small"
#        elif(area > 1000 and area < 2000):
#            size="medium"
#        else:
#            size="large"
        #ratio = area / float(image_size)
        #print("ratio " + str(ratio))
#        if(perimeter > 650):
#            size="large"
##        elif(perimeter > 650 and perimeter < 700):
##            size="medium"
#        else:
#            size="small"
        return size
    
    def detectRotation(self, contour):
        #(x,y),(MA,ma),angle = cv2.fitEllipse(contour)
        #print("angle = " + str(angle))
        #print("contour = " + str(contour))
        # grab the (x, y) coordinates of all pixel values that
        #coords = np.column_stack(np.where(contour > 0))
        #angle = cv2.minAreaRect(contour)[-1]
        rotrect = cv2.minAreaRect(contour)
        print("rot rect = " + str(rotrect))
        width,height = rotrect[1]
        #print("Wdith = " + str(width))
        angle = rotrect[2]
        if(width < height):
            new_angle = angle + 180
        else:
            new_angle = angle + 90
        print("angle = " + str(new_angle))
        return int(new_angle)
        #print("angle " + str(angle))

# the `cv2.minAreaRect` function returns values in the
# range [-90, 0); as the rectangle rotates clockwise the
# returned angle trends to 0 -- in this special case we
# need to add 90 degrees to the angle
#        if angle < -45:
#            angle = -(90 + angle)
#
## otherwise, just take the inverse of the angle to make
## it positive
#        else:
#            angle = -angle
#        #print("angle " + str(angle))
#        return int(angle)
        #print("final angle = " + str(angle))
        
    def mse(self, imageA, imageB):
    # the 'Mean Squared Error' between the two images is the
	# sum of the squared difference between the two images;
	# NOTE: the two images must have the same dimension
        err = np.sum((imageA.astype("float") - imageB.astype("float")) ** 2)
        err /= float(imageA.shape[0] * imageA.shape[1])
	
	# return the MSE, the lower the error, the more "similar"
	# the two images are
        return err
            