import os
from Agent import Agent
from Problem import Problem
from Matrix import Matrix
from Object import Object
import numpy as np
import cv2
import imutils
from ImageDetector import ImageDetector
from skimage.measure import compare_ssim as ssim

def parseFile(self):
   matrices=[]
   for i, line in enumerate(self):
       line = line.rstrip()
       if i == 0:
           problemTitle = line
       elif i == 1:
           problemType = line
       elif i == 2:
           correctAnswer = line
   problem = Problem(problemTitle, problemType, correctAnswer, matrices)
   return problem

def processImage(self, filename):
    print("file = " + str(filename))
    matrix = Matrix(filename)
    image = cv2.imread(self)
    # load the image and resize it to a smaller factor so that
    # the shapes can be approximated better
    resized = imutils.resize(image, width=300)
    # convert the resized image to grayscale, blur it slightly,
    # and threshold it
    gray = cv2.cvtColor(resized, cv2.COLOR_BGR2GRAY)   

    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    thresh = cv2.threshold(blurred, 60, 255, cv2.THRESH_BINARY_INV)[1]
    external_contours = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
    #print("hierarchy= " + str(hierarchy[0]))
    #print("contours first time =" + str(contours))
    external_contours = external_contours[0] if imutils.is_cv2() else external_contours[1]
    #print("contours first time =" + str(contours))
    _,contours,hierarchy=cv2.findContours(thresh.copy(), cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
    #print("hierarchy= " + str(hierarchy[0]))
    hierarchy = hierarchy[0]
    contour_list=[]
    object_index=0
    for index, c in enumerate(external_contours):
        obj = Object(object_index)
        matrix.objects[object_index]= obj
        contour_list.append(c)
        for c_index, ct in enumerate(contours):
            ret = cv2.matchShapes(ct,c,1,0.0)
            if(ret == 0):
                child = hierarchy[c_index][2]
                parent = hierarchy[child][3]
                while True:
                    if(child != -1):
                        grand_child=hierarchy[child][2]
                        child_parent = hierarchy[child][3]
                        if(hierarchy[child][2] != -1 or parent == -1):
                            if(object_index in matrix.objects.keys()):
                                object_index+=1
                            obj = Object(object_index)
                            matrix.objects[object_index]= obj
                            contour_list.append(contours[grand_child])
                            matrix.objects[object_index].attributes.update({"inside" : str(child_parent)})
                            if(object_index in matrix.objects.keys()):
                                object_index+=1
                            child=hierarchy[grand_child][2]
                        else:
                            if(object_index in matrix.objects.keys()):
                                object_index+=1
                            break
                    else:
                        if(object_index in matrix.objects.keys()):
                            object_index+=1
                        break

            
    detector = ImageDetector()
    object_index=0
    for index, c in enumerate(contour_list):
        shape= detector.detectShape(c)
        print("shape = " + str(shape))

        if ("inside" in matrix.objects[index].attributes):
            existing = matrix.objects[index].attributes.get("inside")
            matrix.objects[index].attributes.clear()
        else:
            existing = None
        
        matrix.objects[index].attributes.update({"shape" : shape})
        fill_color = detector.detectFill(gray, c)
        if(fill_color == "black"):
            fill="yes"
        elif(fill_color =="half-half"):
            fill="half-and-half"
        else:
            fill="no"
        matrix.objects[index].attributes.update({"fill" : fill})
        size = detector.detectSize(c, image)
        matrix.objects[index].attributes.update({"size" : size})
        
        if(existing):
            matrix.objects[index].attributes.update({"inside": existing})
        
        angle = detector.detectRotation(c)
        #matrix.objects[index].attributes.update({"angle" : str(angle)})
        #do  rotation  and position
    return matrix

def interImageTransformations(matrices, A_image, B_image):
    image_A = cv2.imread(A_image)
    image_B = cv2.imread(B_image)
    A_name = os.path.basename(A_image)
    B_name = os.path.basename(B_image)
    A_filename, A_extension = os.path.splitext(A_name)
    B_filename, B_extension = os.path.splitext(B_name)
    
    matrix_A=[x for x in matrices if x.getName() == A_filename][0]
    matrix_B=[x for x in matrices if x.getName() == B_filename][0]

    resized_A = imutils.resize(image_A, width=300)
    resized_B = imutils.resize(image_B, width=300)
    gray_A = cv2.cvtColor(resized_A, cv2.COLOR_BGR2GRAY)
    gray_B = cv2.cvtColor(resized_B, cv2.COLOR_BGR2GRAY)
    
    horizontal_img = cv2.flip( gray_A, 0 )
    vertical_img = cv2.flip( gray_A, 1 )
    detector = ImageDetector()
    horizontal_mse = detector.mse(horizontal_img, gray_B)
    #print("horizontal mse = " + str(B_filename) + " : " + str(horizontal_mse))
    if(horizontal_mse < 2000):
        for obj in matrix_B.objects.keys():
            matrix_B.objects[obj].attributes.update({"horizontal-flip" : "yes"})
        
    vertical_mse = detector.mse(vertical_img, gray_B)
    #print("vertical mse = "+ str(B_filename) + " : " + str(vertical_mse))
    if(vertical_mse < 2000):
        for obj in matrix_B.objects.keys():
            matrix_B.objects[obj].attributes.update({"vertical-flip" : "yes"})
    
#    for angle in np.arange(0, 360, 15):
#        rotated = imutils.rotate(gray_A, angle)
#        rotate_mse = detector.mse(rotated, gray_B)
#        if(angle == 45):
            #print("rotate mse = " + str(rotate_mse))
        
    return matrices

def main():
    sets=[]     

    for file in os.listdir("2x1 Basic Problem Images"): 
        matrices=[]
        print("******FILE******* = " + str(file))
        image_directory = "2x1 Basic Problem Images" + os.sep 
        for f in os.listdir(image_directory + file):
             file_directory = image_directory + file + os.sep
             name, extension = os.path.splitext(f)
             if(extension == ".png"):
                 matrix = processImage(file_directory + f, name)
                 matrices.append(matrix)
             else:
                f = open(file_directory + f) 
                problem = parseFile(f)
        matrices = interImageTransformations(matrices, file_directory + "A.png", file_directory + "B.png")
        matrices = interImageTransformations(matrices, file_directory + "C.png", file_directory + "1.png")
        matrices = interImageTransformations(matrices, file_directory + "C.png", file_directory + "2.png")
        matrices = interImageTransformations(matrices, file_directory + "C.png", file_directory + "3.png")
        matrices = interImageTransformations(matrices, file_directory + "C.png", file_directory + "4.png")
        matrices = interImageTransformations(matrices, file_directory + "C.png", file_directory + "5.png")
        matrices = interImageTransformations(matrices, file_directory + "C.png", file_directory + "6.png")
        problem.setMatrices(matrices)
        sets.append(problem)
#        
#    #initialize agent
    agent=Agent() 

    for problem in sets:
        print("%s" % "--------------------")   
        problem.setAgentAnswer(agent.solveProblem(problem))                                                  
        print("Agent's Answer : " + str(problem.getAgentAnswer()) + " \nCorrect Answer : " + str(problem.getCorrectAnswer()) +" \nResult : " + problem.checkAnswer())


if __name__ == "__main__":
    main()