
from Matrix import Matrix
import random
import copy

#represents knowledge-based agent
class Agent:
    def __init__(self):
        pass

    def solveProblem(self,problem):
        print("Problem : ", problem.getTitle())
        
        answer_choices = []
       
        #Get matrices and create frames for each object
        A = [x for x in problem.getMatrices() if x.getName() == "A"][0]
        AFrame = self.createFrame(A)
        
        B = [x for x in problem.getMatrices() if x.getName() == "B"][0]
        BFrame = self.createFrame(B)
        
        C = [x for x in problem.getMatrices() if x.getName() == "C"][0]
        CFrame = self.createFrame(C)
       
        DFrame= copy.deepcopy(CFrame)
        
        #get answer choices
        choice_1 = [x for x in problem.getMatrices() if x.getName() == "1"][0]
        answer_choices.append(choice_1)
        choice_2 = [x for x in problem.getMatrices() if x.getName() == "2"][0]
        answer_choices.append(choice_2)
        choice_3 = [x for x in problem.getMatrices() if x.getName() == "3"][0]
        answer_choices.append(choice_3)
        choice_4 = [x for x in problem.getMatrices() if x.getName() == "4"][0]
        answer_choices.append(choice_4)
        choice_5 = [x for x in problem.getMatrices() if x.getName() == "5"][0]
        answer_choices.append(choice_5)
        choice_6 = [x for x in problem.getMatrices() if x.getName() == "6"][0]
        answer_choices.append(choice_6)

        #get differences between A and B
        AtoB = self.getDelta(AFrame, BFrame)

        #generate object D using differences determined from A to B
        C_obj = C.getObjects()
        D= Matrix("D")
        custom_keys={"vertical-flip"}
        for obj in C_obj:
            newValues = AtoB.get(obj)
            #object in C doesn't exist in A
            if not(obj in AFrame.keys()):
                objAtt = C_obj[obj].getAttributes()
                for val in AtoB.items():
                    common_keys = set(objAtt).intersection(val[1])
                    for key in common_keys:
                        objAtt.update({key:val[1].get(key)})
            if not(newValues):
                newValues=[]
            if("deleted" not in newValues ):
                    #get attributes added during delta that don't exist in C
                    added_attributes= list(set(newValues) - set(C_obj[obj].getAttributes().keys()) - set(custom_keys))
                    if(added_attributes):
                        for add in added_attributes:
                            DFrame[obj].update({add: newValues.get(add)})
                    #for each attribute of C, see if there was a change based on delta results of A to B
                    for keyValue in CFrame[obj].items():
                        if(keyValue[0] in newValues):
                            #special logic to handle angles
                                if(keyValue[0] == "angle"):
                                    A_angle = AFrame[obj].get("angle")
                                    B_angle = BFrame[obj].get("angle")
                                    C_shape = CFrame[obj].get("shape")
                                    vertical_flip = newValues.get("vertical-flip")
                                    newAtt=self.determineAngle(keyValue[1], C_shape, A_angle, B_angle, vertical_flip)
                                elif(keyValue[0] == "shape"):
                                    DFrame = self.changeShape(AFrame, BFrame, CFrame, AtoB, DFrame)
                                    newAtt=None
                                else:
                                    newAtt=newValues.get(keyValue[0])
                                #ignore deleted attribute values
                                if not(newAtt == "deleted" or newAtt == None):
                                    multipleVal=keyValue[1].split(",")
                                    if(len(multipleVal) > 1):
                                        attList = newAtt.split(",")
                                        for val in attList:
                                            if not(val in multipleVal):
                                                multipleVal.append(val)
                                        newAtt = ','.join(multipleVal)
                                    DFrame[obj].update({keyValue[0]: newAtt})
                                elif (newAtt == "deleted"):
                                    #remove attribute from DFrame
                                    DFrame[obj].pop(keyValue[0]) 
                        else:
                            DFrame[obj].update({keyValue[0]: keyValue[1]})
            else:
                #remove object from DFrame
                DFrame.pop(obj)
        #print("Dframe = " + str(DFrame))
        return self.chooseAnswer(answer_choices, DFrame, CFrame)


    #generate and test method of determining correct answer choice
    def chooseAnswer(self, answer_choices, DFrame, CFrame):
        matches=set()
        for i in range(len(answer_choices)):
            match=True
            choiceObj = answer_choices[i].getObjects()
            for obj in choiceObj.keys():
                if (obj in DFrame.keys()):
                    #compare attributes of answer choice to generated object D
                    choiceAttr = choiceObj[obj].getAttributes()
                    DAttr = DFrame[obj]
                    if(choiceAttr != DAttr):
                        match=False
                else:
                    match=False
            if(match):
                matches.add(answer_choices[i].getName())
        if(len(matches) == 1):
            return matches.pop()
        else: #agent knows it made a mistake since generated object doesn't match any answer choice
            matches = self.eliminateAnswers(answer_choices, DFrame, CFrame)
            if(len(matches) == 1):
                return matches.pop()
            else:
                #stil no match, randomly pick answer choice from list of matches (or if no matches, pick random from answer choices)
                return self.guessRandomAnswer(matches)
    
    def guessRandomAnswer(self, matches):
        #guess random from list of matches
        if(len(matches) > 0):
            return str(random.choice(tuple(matches)))
        else:
            #guess random from all answer choices
            return str(random.randint(1,7))
    
    def eliminateAnswers(self, answer_choices, DFrame, CFrame):
        matches=set()
        for i in range(len(answer_choices)):
            match=True
            choiceObj = answer_choices[i].getObjects()
            numChoiceObj=len(choiceObj.keys())
            numDObj = len(DFrame.keys())
            #compare number of objects in answer choice to generated object
            if(numChoiceObj != numDObj):
                match=False
            else:
                for obj in choiceObj.keys():
                    choice_shape = choiceObj[obj].attributes.get("shape")
                    C_shapes = []
                    if (obj in CFrame.keys()):
                        for key in CFrame.keys():
                            C_shapes.append(CFrame[key].get("shape"))
                            #compare shapes of answer choices to C objects
                        if not(choice_shape in C_shapes):
                            match=False
                    else:
                        match=False
            #check negative angles
            for obj in DFrame.keys():
                if ("angle" in DFrame[obj]):
                    choice_angle = choiceObj[obj].attributes.get("angle")
                    D_angle = DFrame[obj].get("angle")
                    if not(choice_angle == D_angle):
                        negative_angle = str(360 - int(D_angle))
                        if not(negative_angle == choice_angle):
                            match=False            
            if(match):
                matches.add(answer_choices[i].getName()) 
        #print("matches = " + str(matches))
        return matches

    def getDelta(self, AFrame, BFrame):
        A_Objs = AFrame.keys()
        B_Objs = BFrame.keys()
        
        A_names = [A_Obj for A_Obj in A_Objs]
        B_names = [B_Obj for B_Obj in B_Objs]
        A_differences = list(set(A_names) - set(B_names))
        B_differences = list(set(B_names) - set(A_names))
        delta = {}
        
        #find object differences between A and B to determine which objects were deleted/added
        for difference in A_differences:
            delta[difference]="deleted"
        for difference in B_differences:
            delta[difference]="added"
        
        #iterate through objects of A and B
        for A_name,B_name in zip(A_names,B_names):
            for obj in A_Objs:
                if obj == A_name:
                    A_Obj = obj
            for obj in B_Objs:
                if obj == B_name:
                    B_Obj = obj
            
            #A attributes that B doesn't have
            A_attr_differences = list(set(AFrame[A_Obj].keys()) - set(BFrame[B_Obj].keys()))
            if(A_attr_differences):
                for diff in A_attr_differences:
                    self.updateDelta(delta, B_name, diff, "deleted")
            
            #B attributes that A doesn't have
            B_attr_differences = list(set(BFrame[B_Obj].keys()) - set(AFrame[A_Obj].keys()))
            if(B_attr_differences):
                for diff in B_attr_differences:
                    self.updateDelta(delta, B_name, diff, BFrame[B_Obj].get(diff))
            
            #iterate through attributes of A and B
            for A_att,B_att in zip(AFrame[A_Obj].items(),BFrame[B_Obj].items()):                        
                #same attribute for both A and B
                if(A_att[0] == B_att[0]):
                    if(A_att[1] != B_att[1]):
                        if(B_att[0] == "angle"):
                            if(abs(int(A_att[1]) - int(B_att[1])) == 180):
                                if(int(A_att[1]) in [0,180] and int(B_att[1]) in [0,180]):
                                    #vertical flip
                                    self.updateDelta(delta, B_name, "vertical-flip", "yes")
                                else:
                                    #horizontal flip
                                    self.updateDelta(delta, B_name, "vertical-flip", "no")
                        self.updateDelta(delta, B_name, B_att[0], B_att[1])               
                    
        #print("Delta = " + str(delta))
        return delta

    #method to update delta dictionary object
    def updateDelta(self, delta, key, newAttr, newValue):
        if key in delta:
            existing = delta.get(key)
            existing.update({newAttr:newValue})
        else:
            newEntry = { newAttr: newValue}
            delta.update({key: newEntry })

    def createFrame(self, matrix):
        frame = {}
        for obj in list(matrix.objects):
            frame[matrix.objects[obj].name] = matrix.objects[obj].attributes
        return frame
    
    def changeShape(self, AFrame, BFrame, CFrame, delta, DFrame):
        for change in delta.keys():
            if("shape" in delta[change].keys()):
                A_shape = AFrame[change].get("shape")
                B_shape = BFrame[change].get("shape")
                for obj in CFrame.keys():
                    C_shape = CFrame[obj].get("shape")
                    if(C_shape == A_shape):
                        DFrame[obj].update({"shape" : B_shape})
        return DFrame

    def determineAngle(self, C_angle, C_shape, A_angle, B_angle, vertical_flip):
        if(abs(int(A_angle) - int(B_angle)) == 180):
            if(vertical_flip == "yes"):
                newAngle = int(C_angle) + 180
                 #vertical flip add 180 to C angle (if > 360, subtract 360 from it)
                if(newAngle > 360):
                    newAngle = newAngle - 360
                return str(newAngle)
            else:
                #horizontal flip, if start angle of C is 0, copy angle otherwise add 180 to it
                if(int(C_angle) == 0):
                    return str(C_angle)
                else:
                    newAngle = int(C_angle) + 180
                    if(newAngle > 360):
                        newAngle = newAngle - 360
                    return str(newAngle)
        else:
            if(C_shape == "circle"):
                #circles can't rotate
                return C_angle
            else:
                return str(B_angle)