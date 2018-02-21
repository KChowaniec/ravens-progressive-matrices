# -*- coding: utf-8 -*-
"""
Created on Sun Feb 11 11:17:40 2018

@author: Kathy
"""

#represents entire Raven's problem to solve
class Problem:

    def __init__(self,title, size, correctAnswer, matrices):
        self.title=title
        self.size=size
        self.correctAnswer=correctAnswer
        self.matrices=matrices
        self.problems=[]
        self.agentAnswer=None

    def getTitle(self):
        return self.title

    def getProblems(self):
        return self.problems
    
    def getSize(self):
        return self.size
    
    def getCorrectAnswer(self):
        return self.correctAnswer
    
    def getMatrices(self):
        return self.matrices

    def setAgentAnswer(self, agentAnswer):
        self.agentAnswer=agentAnswer

    def getAgentAnswer(self):
        return self.agentAnswer

    def checkAnswer(self):
        if self.agentAnswer==self.correctAnswer:
             return "CORRECT"
        else:
             return "INCORRECT"
#