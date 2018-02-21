import os
from Agent import Agent
from Problem import Problem
from Matrix import Matrix
from Object import Object

#parse text files to store matrices, objects and object attributes
def parseFile(self):
   matrices=[]
   for i, line in enumerate(self):
       line = line.rstrip()
       if i == 0:
           problemTitle = line
       elif i == 1:
           problemSize = line
       elif i == 2:
           correctAnswer = line
       else:
           if not line.startswith("\t"):
                #this is a matrix
                newMatrix = Matrix(line) 
                matrices.append(newMatrix)
           elif not line.startswith("\t\t"):
                #this is an object
                line = line.strip()
                newObject=Object(line)
                newMatrix.objects.append(newObject)
           else:
                #this is an attribute (key-value pair)
                line = line.strip()
                keyValue=line.split(":")
                newObject.attributes.update({keyValue[0]: keyValue[1]})
            
   problem = Problem(problemTitle, problemSize, correctAnswer, matrices)
   return problem

def main():
    sets=[] 
    

    for file in os.listdir("2x1 Basic Problems"): 
        f = open("2x1 Basic Problems" + os.sep + file) 
        problem = parseFile(f)
        sets.append(problem)
        
    #initialize agent
    agent=Agent() 

    for problem in sets:
        print("%s" % "--------------------")   
        problem.setAgentAnswer(agent.solveProblem(problem))                                                  
        print("Agent's Answer : " + str(problem.getAgentAnswer()) + " \nCorrect Answer : " + str(problem.getCorrectAnswer()) +" \nResult : " + problem.checkAnswer())


if __name__ == "__main__":
    main()